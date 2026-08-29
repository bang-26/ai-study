#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  agents 
    CreateTime     ：  2026-07-29 23:18:45 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import TypedDict
from clients import CloudModelClient, EmbeddingModel
from repositories import ColumnRepository, ValueRepository, MetricRepository, MetaRepository
from configs import app_config


# 数据代理上下文
class DataAgentContext(TypedDict):
    embedding_client: EmbeddingModel
    column_qdrant_repository: ColumnRepository
    value_es_repository: ValueRepository
    metric_qdrant_repository: MetricRepository
    meta_mysql_repository: MetaRepository


llm_client = CloudModelClient(conf=app_config.model_config)
llm_client.connect()
# 暴露底层 LangChain BaseChatModel，支持 | 管道操作符
llm = llm_client.llm


if __name__ == '__main__':
    response = llm_client.invoke("hello, who are you")
    print(response)
