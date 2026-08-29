#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  repositories 
    CreateTime     ：  2026-07-28 16:50:40 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from logger import logger
from configs import DataDict, PathConfig
from clients import MysqlClient, QDrantClient, ElasticSearchClient, EmbeddingModel
from models import TableInfo, ColumnInfo, MetricInfo, ColumnMetric, QdrantColumn, QdrantMetric, ValueInfoES
from utils import SqlParser


# 元数据仓库
class MetaRepository:
    def __init__(self, client: MysqlClient) -> None:
        self.client = client
    
    # 保存表信息
    async def save_table_info(self, table_list: list[TableInfo]) -> None:
        await self.client.insert_data(data_list=table_list)
    
    # 保存字段信息
    async def save_column_info(self, column_list: list[ColumnInfo]) -> None:
        await self.client.insert_data(data_list=column_list)
    
    # 保存指标信息
    async def save_metric_info(self, metric_list: list[MetricInfo]) -> None:
        await self.client.insert_data(data_list=metric_list)
    
    # 保存字段指标信息
    async def save_column_metric(self, column_metric_list: list[ColumnMetric]) -> None:
        await self.client.insert_data(data_list=column_metric_list)
    
    # 获取表信息
    async def get_column_info_by_id(self, id: str) -> ColumnInfo:
        column_info = await self.client.query_entry(entity=ColumnInfo, field=id)
        return column_info
    
    
# 宽表仓库
class DwRepository:
    def __init__(self, client: MysqlClient, sql_path: str = PathConfig.SQL_PATH) -> None:
        self.client = client
        self.sql_parser = SqlParser(path=sql_path)
    
    # 获取字段类型
    async def get_column_types(self, table_name: str) -> dict[str, str]:
        sql = self.sql_parser.get_sql(key=DataDict.GET_COLUMNS_KEY) % table_name
        
        data_list = await self.client.query_data(sql=sql)
        result_dict = {data.Field: data.Type for data in data_list}
        return result_dict
    
    # 获取字段值
    async def get_column_values(self, table_name: str, column_name: str, limit: int = 10) -> list[str]:
        sql = self.sql_parser.get_sql(key=DataDict.GET_COLUMN_VALUES_KEY) % (column_name, table_name, limit)
        data_list = await self.client.query_data(sql=sql)
        result_list = [data.get(column_name) for data in data_list]
        return result_list


# 宽表仓库
class ColumnRepository:
    def __init__(self, client: QDrantClient, model: EmbeddingModel) -> None:
        self.client = client
        self.model = model
        
    # 创建向量索引
    async def create_collection(self) -> None:
        await self.client.create_collection()
    
    # 批量保存字段向量
    async def upsert_column(self, point_list: list[dict[str, any]], batch_size: int = 100) -> None:
        for i in range(0, len(point_list), batch_size):
            batch_list = point_list[i: i + batch_size]
            
            vector_str_batch = [batch.get("vector") for batch in batch_list]
            vector_list = await self.model.texts_vector(text_list=vector_str_batch)
            logger.info(f"向量化 {len(batch_list)} 个文本完成")
            
            for index, vector in enumerate(vector_list):
                batch_list[index]["vector"] = vector
                
            await self.client.upsert_point(data_list=batch_list)
            logger.info(f"添加 {len(batch_list)} 个文本向量成功")
    
    # 批量查询字段向量
    async def search(self, vector: list[float], top_k: int = 10) -> list[ColumnInfo]:
        response = await self.client.query_data(query=vector, top_k=top_k)
        result_list = [point.payload for point in response.points]
        return result_list
    
    
# 指标仓库
class MetricRepository:
    def __init__(self, client: QDrantClient, model: EmbeddingModel) -> None:
        self.client = client
        self.model = model
    
    # 创建向量索引
    async def create_collection(self) -> None:
        await self.client.create_collection()
    
    # 批量保存指标向量
    async def upsert_metric(self, point_list: list[dict[str, any]], batch_size: int = 100) -> None:
        for i in range(0, len(point_list), batch_size):
            batch_list = point_list[i: i + batch_size]
            
            vector_str_batch = [batch.get("vector") for batch in batch_list]
            vector_list = await self.model.texts_vector(text_list=vector_str_batch)
            logger.info(f"向量化 {len(batch_list)} 个文本完成")
            
            for index, vector in enumerate(vector_list):
                batch_list[index]["vector"] = vector
            
            await self.client.upsert_point(data_list=batch_list)
            logger.info(f"添加 {len(batch_list)} 个指标向量成功")
    
    # 批量查询指标向量
    async def search(self, vector: list[float], top_k: int = 10) -> list[MetricInfo]:
        response = await self.client.query_data(query=vector, top_k=top_k)
        result_list = [point.payload for point in response.points]
        return result_list
    
    
class ValueRepository:
    def __init__(self, client: ElasticSearchClient) -> None:
        self.client = client
    
    # 创建 ES 索引
    async def create_index(self) -> None:
        await self.client.create_index()
    
    # 批量保存字段向量
    async def insert_data(self, data_list: list[ValueInfoES], batch_size: int = 100) -> None:
        for i in range(0, len(data_list), batch_size):
            batch_list = data_list[i: i + batch_size]
            await self.client.insert_data(data_list=batch_list)
    
    # 批量查询字段向量
    async def search(self, query: str, limit: int = 10) -> list[ValueInfoES]:
        response = await self.client.query_data(query=query, size=limit)
        
        hit_list = response.get("hits", {}).get("hits", [])
        result_list = [hit["_source"] for hit in hit_list]
        return result_list
        
    
if __name__ == '__main__':
    import asyncio
    from json import dumps
    from configs import app_config
    
    async def test():
        mysql = MysqlClient(conf=app_config.mysql_config)
        await mysql.connect()
        
        repository = DwRepository(client=mysql)
        results = await repository.get_column_values(table_name='dim_date', column_name='date_id', limit=10)
        json_str = dumps(obj=results, indent=4, ensure_ascii=False)
        print(json_str)
        await mysql.close()
    
    asyncio.run(test())
