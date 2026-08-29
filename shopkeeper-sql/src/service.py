#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  service 
    CreateTime     ：  2026-07-26 20:29:11 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from uuid import uuid4
from clients import MysqlClient, QDrantClient, ElasticSearchClient, EmbeddingModel
from configs import TableConfig, MetricConfig
from entries import ChatResponse
from logger import logger
from models import TableInfo, ColumnInfo, ColumnMetric, MetricInfo, QdrantColumn, QdrantMetric, ValueInfoES
from repositories import MetaRepository, DwRepository, ColumnRepository, MetricRepository, ValueRepository


class StreamService:
    @classmethod
    def process_task(cls, user_query: str) -> ChatResponse:
        result = ChatResponse()
        
        return result


class MetaKnowledgeService:
    def __init__(self, meta_client: MysqlClient, dw_client: MysqlClient, column_qdrant: QDrantClient,
                 metric_qdrant: QDrantClient, es_client: ElasticSearchClient, model: EmbeddingModel):
        self.meta_repository = MetaRepository(client=meta_client)
        self.dw_repository = DwRepository(client=dw_client)
        self.column_repository = ColumnRepository(client=column_qdrant, model=model)
        self.metric_repository = MetricRepository(client=metric_qdrant, model=model)
        self.value_repository = ValueRepository(client=es_client)
    
    # 处理表信息
    async def process_table_info(self, table_config_list: list[TableConfig]):
        # 1. 保存表信息到 meta 数据库
        column_list = await self.__save_meta(table_list=table_config_list)
        
        # 2. 为字段信息建立向量索引
        await self.__save_column_info(column_list=column_list)
        
        # 3. 为字段取值建立全文索引
        await self.__save_value_info(table_list=table_config_list, column_list=column_list)
            
    # 处理指标信息
    async def process_metric_info(self, metric_config_list: list[MetricConfig]):
        # 1. 保存指标信息到 meta 数据库
        metric_list = await self.__save_metrics_meta(metric_config_list)
        
        # 2. 为指标信息建立向量索引
        await self.__save_metric_to_qdrant(metric_list=metric_list)
        
    # 保存字段信息到 meta 数据库
    async def __save_meta(self, table_list: list[TableConfig]) -> list[ColumnInfo]:
        table_info_list = []
        column_info_list = []
        for table in table_list:
            table_info = TableInfo(id=table.name, name=table.name, role=table.role, description=table.description)
            table_info_list.append(table_info)
            
            column_type_dict = await self.dw_repository.get_column_types(table_name=table.name)
            for column in table.columns:
                column_type = column_type_dict.get(column.name)
                column_value_list = await self.dw_repository.get_column_values(table_name=table.name,
                                                                               column_name=column.name, limit=10)
                
                column_info = ColumnInfo(id=f"{table.name}.{column.name}", name=column.name,
                                         type=column_type, role=column.role, examples=column_value_list,
                                         description=column.description, alias=column.alias, table_id=table.name)
                
                column_info_list.append(column_info)
        
        await self.meta_repository.save_table_info(table_info_list)
        logger.info("保存表信息到 meta 数据库")
        
        await self.meta_repository.save_column_info(column_info_list)
        logger.info("保存字段信息到 meta 数据库")
        
        return column_info_list
    
    # 为字段信息建立向量索引
    async def __save_column_info(self, column_list: list[ColumnInfo]) -> None:
        await self.column_repository.create_collection()
        
        point_list = []
        for column in column_list:
            column_id = uuid4()
            
            payload = QdrantColumn(id=column.id, name=column.name, type=column.type, role=column.role,
                                   examples=column.examples, description=column.description,
                                   alias=column.alias, table_id=column.table_id)
            
            point_list.append({"id": column_id, "vector": column.name, "payload": payload})
            
            description_id = uuid4()
            point_list.append({"id": description_id, "vector": column.description, "payload": payload})
            
            for alias in column.alias:
                alias_id = uuid4()
                point_list.append({"id": alias_id, "vector": alias, "payload": payload})
            
        await self.column_repository.upsert_column(point_list=point_list)
        logger.info("为字段信息建立向量索引")
    
    # 为字段取值建立全文索引
    async def __save_value_info(self, table_list: list[TableConfig], column_list: list[ColumnInfo]) -> None:
        await self.value_repository.create_index()
        
        column_sync_dict = {}
        for table in table_list:
            for column in table.columns:
                if column.sync:
                    column_sync_dict[f"{table.name}.{column.name}"] = column.sync
        
        info_list = []
        for column in column_list:
            sync = column_sync_dict.get(column.id, True)
            if sync:
                table_name = column.table_id
                column_name = column.name
                value_list = await self.dw_repository.get_column_values(table_name=table_name,
                                                                        column_name=column_name, limit=1000000)
                column_info_list = []
                for value in value_list:
                    info = ValueInfoES(id=f"{column.id}.{value}", value=value, type=column.type, column_id=column.id,
                                       column_name=column_name, table_id=column.table_id, table_name=table_name)
                    column_info_list.append(info)
                
                info_list.extend(column_info_list)
        
        await self.value_repository.insert_data(data_list=info_list)
        logger.info("为字段取值建立全文索引")
    
    # 保存指标信息到 meta 数据库
    async def __save_metrics_meta(self, metric_list: list[MetricConfig]):
        metric_info_list = []
        column_metric_list = []
        for metric in metric_list:
            metric_info = MetricInfo(id=metric.name, name=metric.name, description=metric.description,
                                     relevant_columns=metric.relevant_columns, alias=metric.alias)
            metric_info_list.append(metric_info)
            
            for relevant_column in metric.relevant_columns:
                column_metric = ColumnMetric(column_id=relevant_column, metric_id=metric.name)
                column_metric_list.append(column_metric)
        
        await self.meta_repository.save_metric_info(metric_list=metric_info_list)
        await self.meta_repository.save_column_metric(column_metric_list=column_metric_list)
        logger.info("保存指标信息到 meta 数据库")
        
        return metric_info_list
        
    # 为指标信息建立向量索引
    async def __save_metric_to_qdrant(self, metric_list: list[MetricInfo]):
        point_list = []
        for metric in metric_list:
            metric_id = uuid4()
            payload = QdrantMetric(id=metric.id, name=metric.name, description=metric.description,
                                   relevant_columns=metric.relevant_columns, alias=metric.alias)
            
            point_list.append({"id": metric_id, "vector": metric.name, "payload": payload})
            
            description_id = uuid4()
            point_list.append({"id": description_id, "vector": metric.description, "payload": payload})
            
            for alias in metric.alias:
                alias_id = uuid4()
                point_list.append({"id": alias_id, "vector": alias, "payload": payload})
        
        await self.metric_repository.create_collection()
        await self.metric_repository.upsert_metric(point_list=point_list)
        logger.info("为指标信息建立向量索引")
