#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  crawler 
    CreateTime     ：  2026-07-20 21:37:10 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Any
from config import KnowledgeConfig
from http.client import HTTPException
from requests import get


# 知识库接口客户端：提供一个方法 获取网络知识
class KnowledgeCrawler:
    def __init__(self, conf: KnowledgeConfig):
        self.knowledge_domain = conf.KNOWLEDGE_DOMAIN
        self.knowledge_uri = conf.KNOWLEDGE_URI
        self.headers = conf.HEADERS
        self.timeout = conf.TIME_OUT
    
    # 根据知识库编号 获取联想知识库内容(data部分)
    def fetch_content(self, knowledge_no: int = 1) -> dict[str, Any]:
        # 1. 定义 URL
        knowledge_url = f"{self.knowledge_domain}/{self.knowledge_uri}"
        
        # 2.定义参数
        params = {"knowledgeNo": knowledge_no}
        
        result = ""
        try:
            # 3.发送请求
            response = get(url=knowledge_url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # 4.得到结果(知识库内容)
            response_dict = response.json()
            
            # 5. 获取data
            result = response_dict.get("data", "")
        except HTTPException as e:
            raise HTTPException(f"发送知识库请求失败:{e}")
        finally:
            return result
        

if __name__ == '__main__':
    knowledge_crawler = KnowledgeCrawler(conf=KnowledgeConfig())
    knowledge = knowledge_crawler.fetch_content(knowledge_no=1)
    print(f"knowledge = {knowledge}")
