#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  connect 
    CreateTime     ：  2026-07-20 20:44:52 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from logger import logger
from typing import Optional
import pymysql
from agents import OpenAIChatCompletionsModel
from dbutils.pooled_db import PooledDB
from openai import AsyncOpenAI
from pymysql import Connect, Error
from pymysql.cursors import DictCursor
from config import ModelConfig, MysqlConfig


# Mysql 连接
class MysqlConnection:
    # 初始化数据
    def __init__(self, conf: MysqlConfig) -> None:
        self.host = conf.HOST
        self.port = conf.PORT
        self.user = conf.USER
        self.password = conf.PASSWORD
        self.database = conf.DATABASE
        self.charset = conf.CHARSET
        self.timeout = conf.TIME_OUT
        self.max_connections = conf.MAX_CONNECTIONS
        self.print_sql = conf.PRINT_SQL
        self.uri = f"{conf.USER}@{conf.HOST}:{conf.PORT}/{conf.DATABASE}?charset={conf.CHARSET}"
        self.mysql_connect = None
        
    def __enter__(self):
        if self.mysql_connect is None:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        
        if exc_type:
            logger.info(f"=============== mysql 退出异常: ===============")
            logger.info(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
        
    def connect(self) -> None:
        try:
            self.mysql_connect = Connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                         database=self.database, charset=self.charset, connect_timeout=self.timeout)
            logger.info(f"=============== 连接到 {self.uri} ===============")
        except Error as e:
            logger.error(f"=============== mysql 连接异常 ===============")
            logger.error(f"error = {e}")
    
    # 查询数据
    def query_data(self, query: str, args: tuple = None, print_query: bool = False) -> Optional[list[dict]]:
        if self.mysql_connect is None:
            self.connect()
        
        if print_query or self.print_sql:
            logger.info(f"\n========================= sql =========================")
            logger.info(query)
            logger.info(f"=======================================================\n")
        
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            with self.mysql_connect.cursor(cursor=DictCursor) as mysql_cursor:
                mysql_cursor.execute(query=query, args=args)         # 执行 SQL 查询
                dict_tuple = mysql_cursor.fetchall()                 # 获取数据
                mysql_cursor.close()                                 # 关闭游标
            
            return list(dict_tuple)
        except Exception as e:
            logger.error(f"=============== {query} 查询异常: ===============")
            logger.error(e)
    
    # 关闭数据库连接
    def close(self) -> None:
        try:
            self.mysql_connect.close()
            logger.info(f"=============== {self.uri} 的连接已关闭 ===============")
        except Error:
            logger.error(f"=============== mysql 关闭异常 ===============")
    

# Mysql 连接池
class MysqlPool:
    def __init__(self, conf: MysqlConfig) -> None:
        self.host = conf.HOST
        self.port = conf.PORT
        self.user = conf.USER
        self.password = conf.PASSWORD
        self.database = conf.DATABASE
        self.charset = conf.CHARSET
        self.timeout = conf.TIME_OUT
        self.max_connection = conf.MAX_CONNECTIONS
        self.print_sql = conf.PRINT_SQL
        
        self.uri = f"{conf.USER}@{conf.HOST}:{conf.PORT}/{conf.DATABASE}?{conf.CHARSET}"
        self.mysql_pool = None
        self.connection = None
    
    # 获取数据库连接
    def __enter__(self):
        if self.mysql_pool is None:
            self.connect()
        return self
    
    # 释放数据库连接
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        
        if exc_type:
            logger.info(f"=============== mysql 退出异常: ===============")
            logger.info(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 连接数据库
    def connect(self) -> None:
        try:
            self.mysql_pool = PooledDB(creator=pymysql, host=self.host, port=self.port, user=self.user,
                                       password=self.password, database=self.database, charset=self.charset,
                                       connect_timeout=self.timeout, maxconnections=self.max_connection)
            
            self.connection = self.mysql_pool.connection()
            logger.info(f"=============== 连接到 {self.uri} ===============")
        except Error as e:
            logger.error(f"=============== mysql 池连接异常 ===============")
            logger.error(e)
    
    # 查询数据
    def query_data(self, query: str, args: tuple = None, print_query: bool = False) -> Optional[list[dict]]:
        if self.connection is None:
            self.connect()
        
        if print_query or self.print_sql:
            logger.info(f"\n========================= sql =========================")
            logger.info(query)
            logger.info(f"=======================================================\n")
        
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            with self.connection.cursor(cursor=DictCursor) as mysql_cursor:
                mysql_cursor.execute(query=query, args=args)         # 执行 SQL 查询
                dict_tuple = mysql_cursor.fetchall()                 # 获取数据
                mysql_cursor.close()                                 # 关闭游标
            
            return list(dict_tuple)
        except Exception as e:
            logger.error(f"=============== {query} 查询异常: ===============")
            logger.error(e)
            
    # 关闭数据库连接
    def close(self) -> None:
        try:
            self.connection.close()
            logger.info(f"=============== {self.uri} 的连接已关闭 ===============")
        except Error:
            logger.error(f"=============== mysql 池关闭异常 ===============")
          

class CloudModel:
    def __init__(self, conf: ModelConfig) -> None:
        self.url = conf.URL
        self.api_key = conf.API_KEY
        self.model_name = conf.MODEL_NAME
        self.timeout = conf.TIMEOUT
        self.max_retries = conf.MAX_RETRIE
        self.temperature = conf.TEMPERATURE
        self.max_token = conf.MAX_TOKEN
        
    def create_model(self):
        model = None
        
        try:
            client = AsyncOpenAI(base_url=self.url, api_key=self.api_key,
                                 timeout=self.timeout, max_retries=self.max_retries)
            
            model = OpenAIChatCompletionsModel(model=self.model_name, openai_client=client)
            logger.info(f"构建模型成功：{self.model_name} ==> {self.url}")
        except Exception as e:
            logger.error(f"模型构建失败：{e}")
        finally:
            return model
    
        
if __name__ == '__main__':
    from json import dumps
    from config import MysqlConfig
    
    with MysqlConnection(conf=MysqlConfig()) as mysql:
        results = mysql.query_data(query="select * from test")
    for result in results:
        data = dumps(obj=result, indent=4, ensure_ascii=False)
        print(data)
        
    with MysqlPool(conf=MysqlConfig()) as pool:
        results = pool.query_data(query="select * from repair_shops")
    for result in results:
        # data = dumps(obj=result, indent=4, ensure_ascii=False)
        print(str(result))
    
    # from config import MainModelConfig, SubModelConfig
    # mc = CloudModel(conf=MainModelConfig()).create_model()
    #
    # mc.get_response(system_instructions="", input="请写一个关于机器学习的程序", model_settings=None,
    #                 tools=[], output_schema=None, handoffs=[], tracing=None)
    #
    # sc = CloudModel(conf=SubModelConfig()).create_model()

