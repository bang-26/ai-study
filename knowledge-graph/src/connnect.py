#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph  
    FileName       ：  connect
    CreateTime     ：  2026-07-05 16:59:40 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import LiteralString, Optional, Union
from pymysql import Connect
from pymysql.cursors import DictCursor
from neo4j import GraphDatabase, Driver
from langchain_neo4j import Neo4jGraph
from tqdm import tqdm
from config import Neo4jConfig


# Mysql 连接
class MysqlConnection:
    # 初始化数据
    def __init__(self, host: str, port: int, user: str, password: str, database: str,
                 charset: str = "utf8mb4", connect_timeout: int = 10) -> None:
        self.uri = f"{host}:{port}/{database}"
        
        try:
            self.mysql_connect = Connect(host=host, port=port, user=user, password=password, database=database,
                                         charset=charset, connect_timeout=connect_timeout)
            print(f"=============== 连接到 {self.uri} ===============")
        except Exception as e:
            print(f"=============== mysql 连接异常 ===============")
            print(e)
            exit(1)
    
    # 查询数据
    def query_data(self, query: str, args: Union[tuple, list, dict, None] = None, print_query: bool = False) -> list[dict]:
        if print_query:
            print(f"query ===> {query} ")
            
        result_list = []
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            with self.mysql_connect.cursor(cursor=DictCursor) as mysql_cursor:
                mysql_cursor.execute(query=query, args=args)         # 使用 execute() 方法执行 SQL 查询
                dict_tuple = mysql_cursor.fetchall()                 # 使用 fetchone() 方法获取数据
                result_list = list(dict_tuple)
        except Exception as e:
            print(f"=============== {query} 查询异常: ===============")
            print(e)
        finally:
            return result_list
    
    # 关闭数据库连接
    def close(self) -> None:
        try:
            self.mysql_connect.close()
            print(f"=============== {self.uri} 的连接已关闭 ===============")
        except Exception as e:
            print(f"=============== mysql 关闭异常 ===============")
            print(e)


# Neo4j 链接
class Neo4jConnection:
    # 创建数据库连接
    def __init__(self, host: str, port: int, user: str, password: str, database: str="neo4j", protocol: str = "bolt"):
        self.uri = f"{protocol}://{host}:{port}/{database}"          # 数据库地址
        self.auth = (user, password)                                 # 数据库认证
        
        self.connect: Optional[Driver] = None                        # 数据库连接
        self.__connection()                                          # 创建数据库连接
    
    # 创建数据库连接
    def __connection(self) -> None:
        if self.connect:
            print(f"=============== {self.uri} 已经连接 ===============")
        else:
            try:
                self.connect = GraphDatabase.driver(uri=self.uri, auth=self.auth)
                print(f"=============== 连接到 {self.uri} ===============")
            except Exception as e:
                print(f"=============== neo4j 连接异常 ===============")
                print(e)
                
    # 查询数据
    def query_data(self, query: str, params: Optional[dict[str, list[dict]]] = None, print_query: bool = False) -> list[dict]:
        if print_query:
            print(f"query ===> {query} ")
            
        result_list = []
        try:
            with self.connect.session() as session:
                runner = session.run(query=query, parameters=params or {})
                result_list = runner.data()
        except Exception as e:
            print(f"=============== {query} 查询异常 ===============")
            print(e)
        finally:
            return result_list
            
    # 处理数据
    def write_data(self, cypher: str, data_list: list[dict[str, int]], batch_size: int = 20) -> None:
        bar = tqdm(iterable=range(0, len(data_list), batch_size), desc="正在写入数据")
        for i in bar:
            batch_data = data_list[i: i + batch_size]
            properties = { "batch": batch_data }
            try:
                self.query_data(query=cypher, params=properties)
            except Exception as e:
                print(f"=============== {cypher} 写入异常 ===============")
                print(e)
            
    # 添加节点
    def write_nodes(self, node_list: list[dict], node_label: str) -> None:
        cypher = f" UNWIND $batch AS row MERGE (n:{node_label} {{id: row.id, name: row.name}}) "
        self.write_data(cypher=cypher, data_list=node_list, batch_size=Neo4jConfig.BATCH_SIZE)
        
    # 添加关系
    def write_relations(self, start, end, relation_list, relation_type) -> None:
        cypher = f"""
              UNWIND $batch AS row
              MATCH (start:{start} {{id: row.start_id}}),
                 (end:{end} {{id: row.end_id}})
              MERGE (start)-[:{relation_type}]->(end)
              """
        self.write_data(cypher=cypher, data_list=relation_list, batch_size=Neo4jConfig.BATCH_SIZE)
        
    # 清空数据库
    def __clear_database(self) -> None:
        try:
            cycler_clear = "MATCH (n) DETACH DELETE n"
            self.query_data(query=cycler_clear)
            print(f"=============== {self.uri} 数据库已清空 ===============")
        except Exception as e:
            print(f"=============== 数据库清空异常 ===============")
            print(e)
            
    # 关闭数据库连接
    def close(self) -> None:
        try:
            self.connect.close()
            print(f"=============== {self.uri} 连接已关闭 ===============")
        except Exception as e:
            print(f"=============== neo4j 关闭异常 ===============")
            print(e)
            
# Graph 连接
class GraphConnection:
    def __init__(self, host: str, port: int, user: str, password: str, database: str="neo4j", protocol: str = "neo4j"):
        self.url = f"{protocol}://{host}:{port}/{database}"
        self.user = user                                             # 数据库用户
        self.password = password                                     # 数据库密码
        
        self.connect: Optional[Neo4jGraph] = None                    # 数据库连接
        self.__connection()                                          # 创建数据库连接
    
    # 创建数据库连接
    def __connection(self) -> None:
        if self.connect:
            print(f"=============== {self.url} 已经连接 ===============")
        else:
            try:
                self.connect = Neo4jGraph(url=self.url, username=self.user, password=self.password)
                self.schema = self.connect.schema
                print(f"=============== 连接到 {self.url} ===============")
            except Exception as e:
                print(f"=============== neo4j 连接异常 ===============")
                print(e)
    
    # 查询数据
    def query_data(self, query: str, params: Optional[dict[str, str]] = None, print_query: bool = False) -> list[dict]:
        if params is None:
            params = {}
            
        if print_query:
            print(f"query ===> {query} ")
            
        result_list = []
        try:
            result_list = self.connect.query(query=query, params=params)
        except Exception as e:
            print(f"=============== {query} 查询异常: ===============")
            print(e)
        finally:
            return result_list
            
    # 关闭数据库连接
    def close(self) -> None:
        try:
            self.connect.close()
            print(f"=============== {self.url} 的连接已关闭 ===============")
        except:
            print(f"=============== neo4j 关闭异常 ===============")
