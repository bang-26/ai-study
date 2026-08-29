#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill
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

from typing import Optional, Sequence, Any, Union
from uuid import uuid4
from json import loads
from langchain_core.messages import AIMessage
from sqlalchemy import text, RowMapping
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct, UpdateResult, PointVectors, QueryResponse
from qdrant_client.models import VectorParams
from elasticsearch import AsyncElasticsearch
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from logger import logger
from configs import MysqlConfig, QDrantConfig, ElasticSearchConfig, EmbeddingConfig, ModelConfig


# Mysql 连接
class MysqlClient:
    # 初始化数据
    def __init__(self, conf: MysqlConfig) -> None:
        self.pool_size = conf.pool_size
        self.auto_flush = conf.auto_flush
        self.auto_begin = conf.auto_begin
        self.auto_commit = conf.auto_commit
        self.expire_on_commit = conf.expire_on_commit
        self.print_sql = conf.print_sql
        
        self.uri = f"{conf.host}:{conf.port}/{conf.database}"
        self.url = (f"{conf.protocol}://{conf.user}:{conf.password}@{conf.host}:{conf.port}"
                    f"/{conf.database}?charset={conf.charset}")
        
        self.engine: Optional[AsyncEngine] = None
        self.session: Optional[async_sessionmaker] = None
    
    # 初始化数据
    async def __aenter__(self):
        if self.session is None:
            await self.connect()
        return self
    
    # 关闭数据库连接
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.session is not None:
            await self.close()
        
        if exc_type:
            logger.warning(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
        
    # 连接数据库
    async def connect(self) -> None:
        try:
            if self.engine is None:
                self.engine = create_async_engine(url=self.url, pool_size=self.pool_size, pool_pre_ping=True,
                                                  echo=self.print_sql)
            if self.session is None:
                self.session = async_sessionmaker(bind=self.engine, autoflush=self.auto_flush,
                                                  autobegin=self.auto_begin, expire_on_commit=self.expire_on_commit)
                logger.info(f"=============== 连接到 {self.uri} ===============")
        except Exception as e:
            logger.error(f"=============== mysql 连接异常：{e} ===============")
            logger.error(f"error = {e}")
    
    # 查询数据
    async def query_data(self, sql: str, params: tuple = None, print_sql: bool = False) -> Sequence[RowMapping]:
        if self.session is None:
            await self.connect()
        
        if print_sql or self.print_sql:
            logger.info(f"\n{sql}\n")
        
        statement = text(text=sql)
        dict_tuple = []
        async with self.session() as session:
            try:
                response = await session.execute(statement=statement, params=params)
                dict_tuple = response.mappings().fetchall()          # 获取数据
                await session.commit()
                logger.debug(f"=============== 查询成功 ===============")
            except Exception as e:
                await session.rollback()
                logger.error(f"=============== 查询异常：{e} ===============")
            finally:
                return dict_tuple
    
    # 查询数据
    async def query_entry(self, entity: Union, field: str = None) -> Union:
        if self.session is None:
            await self.connect()
        
        result = None
        async with self.session() as session:
            try:
                result = await session.get(entity=entity, ident=field)
                await session.commit()
                logger.debug(f"=============== 查询成功 ===============")
            except Exception as e:
                await session.rollback()
                logger.error(f"=============== 查询异常：{e} ===============")
            finally:
                return result
    
    # 插入数据
    async def insert_data(self, data_list: list) -> None:
        if self.session is None:
            await self.connect()
        
        try:
            async with self.session.begin() as begin:
                begin.add_all(instances=data_list)
                logger.debug(f"=============== 插入数据：{len(data_list)} ===============")
        except Exception as e:
            logger.error(f"=============== 插入数据异常：{e} ===============")
    
    # 关闭数据库连接
    async def close(self) -> None:
        try:
            await self.engine.dispose()
            logger.info(f"=============== {self.uri} 的连接已关闭 ===============")
        except Exception as e:
            logger.error(f"=============== mysql 关闭异常：{e} ===============")
    

# Qdrant 连接
class QDrantClient:
    def __init__(self, conf: QDrantConfig) -> None:
        self.protocol = conf.protocol
        self.host = conf.host
        self.port = conf.port
        self.user = conf.user
        self.password = conf.password
        self.collection_name = conf.collection_name
        self.dimension = conf.dimension
        self.similarity = conf.similarity
        self.timeout = conf.time_out
        self.pool_size = conf.pool_size
        self.score = conf.score
        self.url = f"{self.protocol}://{self.host}:{self.port}"
        
        self.client: Optional[AsyncQdrantClient] = None
    
    # 初始化数据
    async def __aenter__(self):
        if self.client is None:
            await self.connect()
        return self
    
    # 关闭数据库连接
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.client is not None:
            await self.close()
            
        if exc_type:
            logger.warning(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 连接数据库
    async def connect(self) -> None:
        try:
            if self.client is None:
                self.client = AsyncQdrantClient(url=self.url, api_key=self.password, verify=True,
                                                https=True, pool_size=self.pool_size, timeout=self.timeout)
                logger.info(f"=============== 连接到 {self.url} ===============")
        except Exception as e:
            logger.error(f"=============== qdrant 连接异常：{e} ===============")
    
    # 创建集合 
    async def create_collection(self) -> None:
        is_exist = await self.client.collection_exists(collection_name=self.collection_name)
        
        if is_exist:
            logger.warning(f"=============== {self.collection_name} 已存在 ===============")
        else:
            vectors_config = VectorParams(size=self.dimension, distance=self.similarity)
            try:
                await self.client.create_collection(collection_name=self.collection_name,
                                                    vectors_config=vectors_config)
                logger.debug(f"=============== 创建 {self.collection_name} 成功 ===============")
            except Exception as e:
                logger.error(f"=============== 创建 {self.collection_name} 异常：{e} ===============")
    
    # 查询数据
    async def query_data(self, query: Union[str, list[float]], top_k: int = 10) -> QueryResponse:
        if self.client is None:
            await self.connect()
        
        result = {}
        try:
            result = await self.client.query_points(collection_name=self.collection_name, query=query,
                                                         score_threshold=self.score, limit=top_k)
            logger.debug(f"=============== 查询数据成功 ===============")
        except Exception as e:
            logger.error(f"=============== 查询数据异常：{e} ===============")
        finally:
            return result
        
    # 批量插入数据点
    async def upsert_point(self, data_list: list[dict[str, Union[int, list[float], dict[str, Any]]]]) -> UpdateResult:
        point_list = []
        
        for data in data_list:
            index = data.get("id", uuid4())
            vector = data.get("vector", [])
            payload = data.get("payload", {})
            
            point = PointStruct(id=index, vector=vector, payload=payload)
            point_list.append(point)
        
        upsert_result = {}
        try:
            upsert_result = await self.client.upsert(collection_name=self.collection_name, points=point_list)
            logger.debug(f"=============== qdrant 更新数据点成功：{len(point_list)} ===============")
        except Exception as e:
            logger.error(f"=============== qdrant 更新数据点异常：{e} ===============")
        finally:
            return upsert_result
        
    # 批量插入数据向量
    async def upsert_vector(self, data_list: list[list[float]]) -> UpdateResult:
        if data_list and isinstance(data_list[0], float):
            data_list = [data_list]
        
        vector_list = []
        for index, data in enumerate(data_list):
            vector = PointVectors(id=index, vector=data)
            vector_list.append(vector)
        
        upsert_result = {}
        try:
            upsert_result = await self.client.update_vectors(collection_name=self.collection_name, points=vector_list)
            logger.debug(f"=============== qdrant 更新向量成功：{len(vector_list)} ===============")
        except Exception as e:
            logger.error(f"=============== qdrant 更新向量异常：{e} ===============")
        finally:
            return upsert_result
        
    # 关闭连接
    async def close(self) -> None:
        try:
            await self.client.close()
            logger.info(f"=============== {self.url} 的连接已关闭 ===============")
        except Exception as e:
            logger.error(f"=============== qdrant 断开异常：{e} ===============")
    

# ElasticSearch 连接
class ElasticSearchClient:
    def __init__(self, conf: ElasticSearchConfig) -> None:
        self.protocol = conf.protocol
        self.host = conf.host
        self.port = conf.port
        self.index = conf.index
        self.mapping = loads(conf.mapping)
        self.timeout = conf.time_out
        self.url = f"{self.protocol}://{self.host}:{self.port}"
        self.auth = (conf.user, conf.api_key)
        
        self.client: Optional[AsyncElasticsearch] = None
    
    # 上下文的形式创建连接
    async def __aenter__(self):
        if self.client is None:
            await self.connect()
        return self
    
    # 上下文的形式进行退出
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.client is not None:
            await self.close()
            
        if exc_type:
            logger.warning(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 连接数据库
    async def connect(self) -> None:
        try:
            self.client = AsyncElasticsearch(hosts=self.url, basic_auth=self.auth, request_timeout=self.timeout)
            logger.info(f"=============== 连接到 {self.url} ===============")
        except Exception as e:
            logger.error(f"=============== elasticsearch 连接异常：{e} ===============")
    
    # 创建索引
    async def create_index(self) -> dict[str, any]:
        is_exist = await self.client.indices.exists(index=self.index)
        
        create_result = {}
        if is_exist:
            logger.debug(f"=============== {self.index} 已存在 ===============")
        else:
            try:
                create_result = await self.client.indices.create(index=self.index, mappings=self.mapping)
                logger.info(f"=============== 创建 {self.index} 成功 ===============")
            except Exception as e:
                logger.error(f"=============== 创建 {self.index} 异常：{e} ===============")
        return create_result
    
    # 批量插入数据
    async def insert_data(self, data_list: list[dict[str, any]]) -> dict[str, any]:
        option_list = []
        for data in data_list:
            option = {"index": {"_index": self.index, "_id": data.get("id", uuid4())}}
            option_list.append(option)
            option_list.append(data)
        
        response = {}
        try:
            response = await self.client.bulk(index=self.index, operations=option_list)
            logger.debug(f"=============== 插入 ES 数据成功：{len(data_list)} ===============")
        except Exception as e:
            logger.error(f"=============== 插入数据异常：{e} ===============")
        finally:
            return response
    
    # 查询数据
    async def query_data(self, query: Union[str, list[float]], size: int = 10, min_score:float=0.6) -> dict[str, any]:
        result_dict = {}
        if self.client is None:
            await self.connect()
        
        try:
            query_mapping = {"match": {"content": query}}
            result_dict = await self.client.search(index=self.index, query=query_mapping, size=size, min_score=min_score)
            logger.debug(f"=============== 查询 ES 数据成功：===============")
        except Exception as e:
            logger.error(f"=============== 查询数据异常：{e} ===============")
        finally:
            return result_dict
            
    # 关闭连接
    async def close(self) -> None:
        try:
            await self.client.close()
            logger.info(f"=============== {self.url} 的连接已关闭 ===============")
        except Exception as e:
            logger.error(f"=============== elasticsearch 断开异常：{e} ===============")
    
    
# 嵌入模型
class EmbeddingModel:
    def __init__(self, conf: EmbeddingConfig) -> None:
        self.url = conf.url
        self.api_key = conf.api_key
        self.name = conf.name
        self.path = conf.path
        self.dimension = conf.dimension
        self.timeout = conf.time_out
        self.max_retry = conf.max_retry
        
        self.embedding: Optional[OpenAIEmbeddings] = None
        
    # 加载模型
    def connect(self) -> None:
        try:
            self.embedding = OpenAIEmbeddings(model=self.name, openai_api_base=self.url, openai_api_key=self.api_key,
                                              dimensions=self.dimension, max_retries=self.max_retry,
                                              request_timeout=self.timeout)
            logger.info(f"=============== 模型加载成功 ===============")
        except Exception as e:
            logger.error(f"=============== embedding 模型加载异常：{e} ===============")
        
    # 字符串向量化
    async def text_vector(self, string: str) -> list[float]:
        if self.embedding is None:
            self.connect()
            
        response = []
        try:
            response = await self.embedding.aembed_query(text=string)
            logger.debug(f"=============== 向量化数据 ===============")
        except Exception as e:
            logger.error(f"=============== 向量化数据异常：{e} ===============")
        finally:
            return response
        
    # 字符文本串批量向量化
    async def texts_vector(self, text_list: list[str]) -> list[list[float]]:
        if self.embedding is None:
            self.connect()
            
        response = []
        try:
            response = await self.embedding.aembed_documents(texts=text_list)
            logger.debug(f"=============== 向量化数据 ===============")
        except Exception as e:
            logger.error(f"=============== 向量化数据异常：{e} ===============")
        finally:
            return response
        

# 大模型配置
class CloudModelClient:
    def __init__(self, conf: ModelConfig) -> None:
        self.url = conf.url
        self.api_key = conf.api_key
        self.name = conf.name
        self.timeout = conf.timeout
        self.temperature = conf.temperature
        self.max_token = conf.max_token
        
        self.llm: Optional[BaseChatModel] = None
    
    # 连接模型
    def connect(self) -> None:
        if self.llm:
            return
        
        try:
            self.llm = init_chat_model(model=self.name, base_url=self.url, api_key=self.api_key,
                                  temperature=self.temperature, timeout=self.timeout)
            logger.debug(f"=============== 云模型 {self.name} 加载成功 ===============")
        except Exception as e:
            logger.error(f"=============== 模型加载异常：{e} ===============")
    
    # 调用模型
    def invoke(self, prompt: str) -> AIMessage:
        if self.llm is None:
            self.connect()
        response = self.llm.invoke(input=prompt)
        return response
    
    # 异步调用
    async def ainvoke(self, prompt: str) -> AIMessage:
        if self.llm is None:
            self.connect()
            
        response = await self.llm.ainvoke(input=prompt)
        return response


if __name__ == '__main__':
    import asyncio
    from  random import random
    from json import loads, dump, dumps
    from configs import app_config
    
    # async def mysql_test():
    #     async with MysqlClient(conf=app_config.mysql_config) as mysql:
    #         results = await mysql.query_data(sql="select * from fact_order order by order_id limit 10")
    #
    #     for result in results:
    #         print(result)
    # asyncio.run(mysql_test())
    
    # async def qdrant_test():
    #     async with QDrantClient(conf=app_config.qdrant_config) as qdrant:
    #         await qdrant.connect()
    #         await qdrant.create_collection()
    #         collections = await qdrant.client.get_collections()
    #         for collection in collections:
    #             print(f"collection = {collection}")
    #
    #         datas = []
    #         for i in range(100):
    #             data = [random() for _ in range(qdrant.vector_size)]
    #             datas.append(data)
    #         response = await qdrant.upsert_data(data_list=datas)
    #         print(f"response = {response}")
    #
    #         query = [random() for _ in range(qdrant.vector_size)]
    #         print(f"query = {query}")
    #         results = await qdrant.query_data(query=query)
    #         for result in results:
    #             print(f"result = {result[1]}")
    # asyncio.run(qdrant_test())
    
    async def es_test():
        async with ElasticSearchClient(conf=app_config.elasticsearch_config) as es:
            await es.connect()
            result = await es.create_index()
            print(f"result = {result}")
            
            indices = await es.client.indices.get(index=es.index)
            for index in indices:
                print(f"index = {index}")
    asyncio.run(es_test())
    
    # async def embed_test():
    #     embed = EmbeddingModel(conf=app_config.embedding_config)
    #
    #     vector1 = await embed.text_vector("hello world")
    #     print(f"vector1 = {vector1}")
    #     print(f"len1 = {len(vector1)}")
    #
    #     vector2 = await embed.texts_vector(["hello", "world", "hello world"])
    #     print(f"vector2 = {vector2}")
    #     print(f"len2 = {len(vector2)}")
    #
    # asyncio.run(embed_test())
    
