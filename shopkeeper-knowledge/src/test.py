#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  test 
    CreateTime     ：  2026-08-12 20:29:31 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import environ

from config import app_config
from query_node import node_rerank

environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from unittest import TestCase
from json import dumps
from graph import file_import_graph
from transformers import AutoTokenizer, AutoModel
from modelscope.hub.snapshot_download import snapshot_download

from logger import logger
from state import create_default_state


class GraphTest(TestCase):
    
    def test_graph(self):
        initial_state = create_default_state(local_file_path="万用表RS-12的使用.pdf")
        final_state = None
        
        # 只输出更最终的状态值（字典形式），不包含节点名称、执行日志、元数据等额外信息
        for event in file_import_graph.process_stream(initial_state):
            for key, value in event.items():
                logger.info(f"节点: {key}")
                final_state = value
        
        # 格式化输出最终状态
        logger.info(f"最终状态: \n{dumps(final_state, indent=4, ensure_ascii=False, default=str)}")
        
        logger.info("图结构:")
        # uv add grandalf
        file_import_graph.get_graph().print_ascii()
        
class DownloadTest(TestCase):
    def test_download(self):
        model_name = app_config.embed_config.model_path
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        # logger.info(f"模型下载完成: {model_name}")
        
        # snapshot_download(model_id="BAAI/bge-m3")


class NodeRerankTest(TestCase):
    def test_node_rerank(self):
        mock_rrf_chunks = [
            {"entity": {"chunk_id": "local_1", "content": "RRF是一种倒数排名融合算法", "title": "算法介绍", "score" : 0.9}},
            {"entity": {"chunk_id": "local_2", "content": "BGE是一个强大的重排序模型", "title": "模型介绍", "score" : 0.8}},
            {"entity": {"chunk_id": "local_3", "content": "无关的测试文档内容", "title": "测试文档", "score": 0.1}}
        ]
        
        # 1.2 MCP 联网搜索数据
        mock_web_docs = [
            {"title": "Rerank技术详解", "url": "http://web.com/1", "snippet": "Rerank即重排序，常用于RAG系统的第二阶段"},
            {"title": "无关网页", "url": "http://web.com/2", "snippet": "今天天气不错，适合出去游玩"}  # 预期低分
        ]
        
        mock_state = {
            "session_id"     : "test_rerank_session",
            "rewritten_query": "什么是RRF和Rerank？",  # 查询意图：想了解这两个算法
            "rrf_chunks"     : mock_rrf_chunks,
            "web_search_docs": mock_web_docs,
            "is_stream"      : False
        }
    
        result = node_rerank(mock_state)
        reranked = result.get("reranked_docs", [])
        print(reranked)
