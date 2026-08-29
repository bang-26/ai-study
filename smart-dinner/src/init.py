#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  init 
    CreateTime     ：  2026-07-19 16:50:20 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from fastapi import FastAPI
from config import PathConfig, MysqlConfig, AmapConfig, CloudModelConfig, PineConeConfig, DataDict
from connect import MysqlConnection, AmapMap, CloudModelConnect, PineConeConnection
from utils import SqlParser, PromptParser

mysql_connect = MysqlConnection(conf=MysqlConfig())
mysql_connect.connect()

pinecone_connect = PineConeConnection(conf=PineConeConfig())
pinecone_connect.connect()

amap_map = AmapMap(conf=AmapConfig())
cloud_model = CloudModelConnect(conf=CloudModelConfig())

app = FastAPI(title="智能点餐助手的API接口", description="智能点餐应用主要暴露三个接口分别为智能对话接口、配送查询接口、菜品列表接口")

sql_parser = SqlParser(path=PathConfig.SQL_PATH)
prompt_parser = PromptParser(path=PathConfig.PROMPT_PATH)
data_dict = DataDict()
