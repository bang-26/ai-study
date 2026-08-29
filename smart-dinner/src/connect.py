#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  connect 
    CreateTime     ：  2026-07-17 16:37:41 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Optional, Union
from http import HTTPStatus

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.utils import Output
from pymysql import Connect, Error
from pymysql.cursors import DictCursor
from pinecone import Pinecone, ServerlessSpec, ScoredVector
from dashscope import TextEmbedding
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError
from urllib3 import Retry
from langchain_openai import ChatOpenAI
from config import MysqlConfig, PineConeConfig, BaiLianConfig, CloudModelConfig, AmapConfig


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
            print(f"=============== mysql 退出异常: ===============")
            print(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
        
    def connect(self) -> bool:
        try:
            self.mysql_connect = Connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                         database=self.database, charset=self.charset, connect_timeout=self.timeout)
            print(f"=============== 连接到 {self.uri} ===============")
        except Error as e:
            print(f"=============== mysql 连接异常 ===============")
            print(f"error = {e}")
    
    # 查询数据
    def query_data(self, query: str, args: tuple = None, print_query: bool = False) -> Optional[list[dict]]:
        if print_query or self.print_sql:
            print(f"\n========================= sql =========================")
            print(query)
            print(f"=======================================================\n")
        
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            with self.mysql_connect.cursor(cursor=DictCursor) as mysql_cursor:
                mysql_cursor.execute(query=query, args=args)         # 执行 SQL 查询
                dict_tuple = mysql_cursor.fetchall()                 # 获取数据
                mysql_cursor.close()                                 # 关闭游标
            
            return list(dict_tuple)
        except Exception as e:
            print(f"=============== {query} 查询异常: ===============")
            print(e)
    
    # 关闭数据库连接
    def close(self) -> None:
        try:
            self.mysql_connect.close()
            print(f"=============== {self.uri} 的连接已关闭 ===============")
        except Error:
            print(f"=============== mysql 关闭异常 ===============")


# PineCone 连接
class PineConeConnection:
    def __init__(self, conf: PineConeConfig) -> None:
        self.api_key = conf.API_KEY
        self.index_name = conf.INDEX_NAME
        self.cloud_name = conf.CLOUD_NAME
        self.region = conf.REGION
        self.model_name = conf.MODEL_NAME
        self.field_map = conf.FILD_MAP
        self.index_type = conf.INDEX_TYPE
        self.dimension = conf.DIMENSION
        self.metric = conf.METRIC
        self.pinecone_connect = None
        self.index = None
    
    def __enter__(self):
        if self.pinecone_connect is None:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        
        if exc_type:
            print(f"=============== pinecone 退出异常: ===============")
            print(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 连接向量数据库
    def connect(self) -> None:
        try:
            self.pinecone_connect = Pinecone(api_key=self.api_key)
            
            if self.has_index() is False:
                self.create_database()
            else:
                self.index = self.pinecone_connect.Index(name=self.index_name)
            print(f"=============== 连接到 Pinecone ===============")
        except Error as e:
            print(f"=============== Pinecone 连接异常 ===============")
            print(f"error = {e}")
    
    # 判断索引是否存在
    def has_index(self) -> bool:
        is_exist = False
        if self.pinecone_connect is not None:
            is_exist = self.pinecone_connect.indexes.exists(name=self.index_name)
        return is_exist
    
    # 创建索引
    def create_database(self):
        spec = ServerlessSpec(cloud=self.cloud_name, region=self.region)
        
        try:
            self.pinecone_connect.create_index(name=self.index_name, vector_type=self.index_type,
                                               dimension=self.dimension, metric=self.metric, spec=spec)
            
            self.index = self.pinecone_connect.Index(name=self.index_name)
        except Exception as e:
            print(f"=============== 创建索引异常: ===============")
            print(f"error = {e}")
    
    # 插入向量数据
    def upsert_data(self, vector_list: list[tuple]):
        try:
            self.index.upsert(vectors=vector_list)
            # self.index.flush()
            print(f"=============== 索引 {self.index_name} 添加数据成功 ===============")
        except Exception as e:
            print(f"=============== 索引 {self.index_name} 添加数据异常: ===============")
            print(f"error = {e}")
    
    # 清空索引数据
    def clear_data(self):
        try:
            index_stats = self.index.describe_index_stats()
            vector_count = index_stats.total_vector_count = 0
            
            if vector_count != 0:
                self.index.delete(delete_all=True)
                print(f"=============== 清空索引 {self.index_name} 成功 ===============")
        except Exception as e:
            print(f"=============== 清空索引异常: ===============")
            print(f"error = {e}")
    
    # 相似性检索
    def similarity_search(self, vector: list[float], top_k: int = 5) -> list[ScoredVector]:
        result_list = []
        
        try:
            print(f"=============== 索引 {self.index_name} 相似性检索 ===============")
            similarity_list = self.index.query(vector=vector, top_k=top_k, include_values=True, include_metadata=True)
            for similarity in similarity_list.matches:
                result_list.append(similarity)
        except Exception as e:
            print(f"=============== 索引 {self.index_name} 相似性检索异常: ===============")
            print(f"error = {e}")
        finally:
            return result_list
    
    # 退出
    def close(self):
        try:
            self.pinecone_connect.close()
            print(f"=============== Pinecone 的连接已关闭 ===============")
        except Exception as e:
            print(f"=============== Pinecone 退出异常 ===============")
            print(f"error = {e}")


# 百联连接
class BailianConnect:
    def __init__(self, conf: BaiLianConfig) -> None:
        self.url = conf.URL
        self.api_key = conf.API_KEY
        self.embed_model_name = conf.EMBED_MODEL_NAME
        self.dimension = conf.DIMENSION
        self.output_type = conf.OUTPUT_TYPE
    
    def query(self, text: Union[str, list[str]]) -> list[float]:
        embedding_list = []
        try:
            # 获取响应结果
            response = TextEmbedding.call(model=self.embed_model_name, api_key=self.api_key, dimension=self.dimension,
                                          input=text, output_type=self.output_type)
            
            # 解析数据
            if response.status_code == HTTPStatus.OK:
                embeddings = response.get("output").get("embeddings")
                for item in embeddings:
                    embedding = item.get("embedding")
                    embedding_list.append(embedding)
            else:
                print(f"=============== BaiLian 请求异常: ===============")
        except Error as e:
            print(f"=============== BaiLian 连接异常 ===============")
            print(f"error = {e}")
        finally:
            return embedding_list


# 高德地图
class AmapMap:
    def __init__(self, conf: AmapConfig) -> None:
        self.base_url = conf.BASE_URL
        self.api_key = conf.API_KEY
        self.retry = conf.RETRY
        self.interval = conf.INTERVAL
        self.status_codes = conf.STATUS_CODES
        self.timeout = conf.TIMEOUT
        
        self.session: Session = None
        
    # 请求
    def request(self, url: str = None, params: dict = None) -> dict:
        # 1. 创建 session 对象
        if self.session is None:
            self.create_session()
        
        if url is None:
            url = self.base_url
        
        # 2. 发送请求
        params["key"] = self.api_key
        response = self.session.get(url=url, params=params, timeout=self.timeout)
        response.raise_for_status()
        
        # 3. 解析数据
        data = response.json()
        return data
    
    # 协议转换：https -> http
    def multi_request(self, url: str = None, params: dict = None):
        response = None
        if url is None:
            url = self.base_url
        
        try:
            response = self.request(url=url, params=params)
        except SSLError as e:
            print(f"=============== 高德地图 SSL 错误 ===============")
            print(f"error = {e}")
            url = url.replace("https", "http")
            response = self.request(url=url, params=params)
        finally:
            return response
        
    # 创建 session
    def create_session(self):
        # 1. 创建 session 对象
        self.session = Session()
        
        # 2. 创建重试策略
        policy = Retry(total=self.retry, backoff_factor=self.interval, status_forcelist=self.status_codes)
        
        # 3. 创建 HttpAdapter 对象
        adapter = HTTPAdapter(max_retries=policy)
        
        # 4. 添加适配器与 session 关联
        self.session.mount(prefix="https://", adapter=adapter)
        self.session.mount(prefix="http://", adapter=adapter)


# 模型连接
class CloudModelConnect:
    def __init__(self, conf: CloudModelConfig) -> None:
        self.llm = ChatOpenAI(base_url=conf.URL, model=conf.MODEL_NAME, api_key=conf.API_KEY, )
        
    # 大模型回答
    def query(self, query: str, instruction: str = None) -> Output:
        # 创建提示词模板
        template = ChatPromptTemplate.from_messages([("system", "{instruction}"),("human", "{query}")])
        
        # 创建链 --> 通过 LCEL 创建链
        chain = template | self.llm
        
        # 执行大模型
        response = chain.invoke({"query": query, "instruction": instruction})
        return response
    
        
if __name__ == '__main__':
    """
    sql = "select * from orders"
    
    with MysqlConnection(conf=MysqlConfig()) as mysql:
        results = mysql.query_data(query=sql,  print_query=True)
        
    # mysql = MysqlConnection(conf=MysqlConfig())
    # mysql.connect()
    # results = mysql.query_data(query=sql, print_query=True)
    # mysql.close()
    
    for result in results:
        print(f"result = {result}")
    """
    
    """
    bailian = BailianConnect(conf=BaiLianConfig())
    result = bailian.query(text=["hello world", "i am ai"])
    
    print(f"result = {result}")
    print(f"length = {len(result)}")
    """
    
    """
    pine = PineConeConnection(conf=PineConeConfig())
    pine.connect()
    is_has = pine.has_index()
    print(f"is_has = {is_has}")
    
    pine.close()
    """
    
    llm = CloudModelConnect(conf=CloudModelConfig())
    res = llm.query(query="自我介绍一下", instruction="你是一个中国厨师，用中文回答我的问题。")
    print(f"res = {res}")
