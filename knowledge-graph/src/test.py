#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph 
    FileName       ：  teat 
    CreateTime     ：  2026-07-04 13:13:23 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6 
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from unittest import TestCase
from commerce import GraphModel
from process import DataProcessor
from connnect import Neo4jConnection, GraphConnection
from config import Neo4jConfig
from web import IndexUtil, ChatService


class EnvTest(TestCase):
    def test_env(self):
        from dotenv import load_dotenv
        load_dotenv()
        print(os.environ.get("HF_ENDPOINT"))


class ProcessTest(TestCase):
    process = DataProcessor()
    
    def test_process(self):
        self.process.process_data()


class ModelTest(TestCase):
    model = GraphModel()
    
    def test_train(self):
        self.model.train()
    
    def test_predict(self):
        text_list = ["麦德龙德国进口双心多维叶黄素护眼营养软胶囊30粒x3盒眼干涩",
                     "韩国耳环现货nuance品牌正品耳坠耳钉耳饰品不对称木片耳环",
                     ["曼妮芬性感轻透舒适提托文胸女士性感蕾丝单层围薄款调整型内衣",
                      "bothyoung蕾丝前扣美背文胸套装女士聚拢厚小胸胸罩性感内衣套装",
                      "高跟鞋子女一字扣女猫跟鞋2017春季新款露脚背尖头细跟百搭单鞋",
                      "hipanda你好熊猫设计潮牌男款跨版条纹尼龙风衣防晒"]
                     ]
        
        for text in text_list:
            result = self.model.predict(text=text)
            print(f"result = {result}")
        
        while 1:
            # text = input("请输入文本：")
            text = "exit"
            
            if text == "exit":
                break
            else:
                result = self.model.predict(text=text)
                print(f"result = {result}")


class ConnectTest(TestCase):
    connect = Neo4jConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                              password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
    
    def test_query_all(self):
        query = "MATCH (n) RETURN n"
        result = self.connect.query_data(query=query)
        print(f"result = {result}")
        self.connect.close()
    
    def test_clear_all(self):
        query = "MATCH (n) DETACH DELETE n"
        result = self.connect.query_data(query=query)
        print(f"result = {result}")
        self.connect.close()


class GraphTest(TestCase):
    graph = GraphConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                            password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
    
    def test_query(self):
        query = "MATCH (n:Trademark) RETURN n"
        result = self.graph.query_data(query=query)
        print(f"result = {result}")
        self.graph.close()
        

class IndexTest(TestCase):
    index = IndexUtil()

    def test_create_index(self):
        self.index.create_full_text_index("trademark_fulltext_index", "Trademark", "name")
        self.index.create_vector_index("trademark_vector_index", "Trademark", "name", "embedding")
    
    def test_index(self):
        self.index.create_index()
    
    # 查询所有索引
    def test_query_index(self):
        query = "SHOW INDEXES"
        results = self.index.graph.query_data(query=query)
        for result in results:
            print(f"result = {result}")


class ChatTest(TestCase):
    chat = ChatService()
    
    def test_vector(self):
        print(f"result = {self.chat.vector_dict}")
