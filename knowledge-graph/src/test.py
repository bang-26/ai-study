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

from os import environ
environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from unittest import TestCase
from dotenv import load_dotenv
from requests import get, post
from config import MysqlConfig, Neo4jConfig
from process import DataProcessor
from commerce import GraphModel
from connnect import MysqlConnection, Neo4jConnection, GraphConnection
from web import IndexUtil, ChatService


class EnvTest(TestCase):
    load_dotenv()
    
    def test_env(self):
        hf = environ.get("HF_ENDPOINT")
        print(f"hf = {hf}")


class ProcessTest(TestCase):
    process = DataProcessor()
    
    def test_load(self):
        dataset = self.process.load_data()
        print(f"dataset = {dataset}")
        
    def test_process(self):
        self.process.process_data()
        

class ModelTest(TestCase):
    model = GraphModel()
    
    def test_train(self):
        from config import TrainConfig
        TrainConfig.EPOCHS = 10
        
        results = self.model.train()
        print(f"results = {results}")
    
    def test_eval(self):
        result = self.model.eval()
        for metric, value in result.items():
            print(f"{metric} ==> {value}")
        
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


class MysqlTest(TestCase):
    mysql = MysqlConnection(host=MysqlConfig.HOST, port=MysqlConfig.PORT, user=MysqlConfig.USER,
                            password=MysqlConfig.PASSWORD, database=MysqlConfig.DATABASE)
    
    def test_query(self):
        query = "show tables"
        result = self.mysql.query_data(query=query, print_query=True)
        for row in result:
            print(f"row = {row}")
        self.mysql.close()
        
        
class GraphTest(TestCase):
    graph = GraphConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                            password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
    
    def test_query(self):
        query = "MATCH (n) RETURN DISTINCT labels(n), count(*) LIMIT 25;"
        result = self.graph.query_data(query=query)
        print(f"result = {result}")
        self.graph.close()


class Neo4jTest(TestCase):
    connect = Neo4jConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                              password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
    
    def test_query(self):
        query = "MATCH (n) RETURN DISTINCT labels(n), count(*) LIMIT 25;"
        result = self.connect.query_data(query=query)
        print(f"result = {result}")
        self.connect.close()
        

class IndexTest(TestCase):
    index = IndexUtil()
    
    def test_create_index(self):
        self.index.create_full_text_index(name="trademark_fulltext_index", label="Trademark", properties="name")
        self.index.create_vector_index(name="trademark_vector_index", label="Trademark",
                                       source_property="name", embedding_property="embedding")
                
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

    def test_chat(self):
        result = self.chat.chat("你叫什么名字")
        print(f"result = {result}")
        
        
class WebTest(TestCase):
    base_url = "http://10.0.0.136:8000"

    def test_index(self):
        url = f"{self.base_url}/"
        response = get(url)
        print(f"response = {response.text}")

    def test_chat(self):
        url = f"{self.base_url}/api/chat"
        json = {"message": "介绍下小米手机"}
        response = post(url=url, json=json).json()
        
        print(f"message = {response.get('message')}")
