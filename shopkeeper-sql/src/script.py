#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  script 
    CreateTime     ：  2026-07-28 16:13:16 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from argparse import ArgumentParser
from logger import logger
from clients import MysqlClient, QDrantClient, ElasticSearchClient, EmbeddingModel
from configs import PathConfig, MetaConfig, load_config, app_config
from service import MetaKnowledgeService


# 构建元数据服务
async def build(conf: MetaConfig, meta_client: MysqlClient, dw_client: MysqlClient, column_qdrant: QDrantClient,
                metric_qdrant: QDrantClient, es_client: ElasticSearchClient, model: EmbeddingModel) -> None:
    
    if meta_client.session is None:
        await meta_client.connect()
    
    if dw_client.session is None:
        await dw_client.connect()
    
    if column_qdrant.client is None:
        await column_qdrant.connect()
    
    if metric_qdrant.client is None:
        await metric_qdrant.connect()
    
    if es_client.client is None:
        await es_client.connect()
    
    if model.embedding is None:
        model.connect()
    
    mete_service = MetaKnowledgeService(meta_client=meta_client, dw_client=dw_client, column_qdrant=column_qdrant,
                                        metric_qdrant=metric_qdrant, es_client=es_client, model=model)
    
    await mete_service.process_table_info(table_config_list=conf.tables)
    await mete_service.process_metric_info(metric_config_list=conf.metrics)
    
    if meta_client.session:
        await meta_client.close()
    
    if dw_client.session:
        await dw_client.close()

    if metric_qdrant.client:
        await metric_qdrant.close()
        
    if column_qdrant.client:
        await column_qdrant.close()
    
    if es_client.client:
        await es_client.close()
        

# 处理命令行参数，加载配置文件
def process_args() -> MetaConfig:
    parser = ArgumentParser()
    arg_list = ["-c", "--conf"]
    parser.add_argument(*arg_list, dest='config', help='config path',
                        default=PathConfig.META_DB_CONF_PATH)
    args = parser.parse_args()
    meta_config = load_config(config_file=args.config, schema_cls=MetaConfig)
    logger.info(f"解析配置文件成功：{args.config}")
    
    return meta_config


# 运行程序，初始化客户端，构建元数据服务
async def run() -> None:
    meta = MysqlClient(conf=app_config.mysql_config)
    dw = MysqlClient(conf=app_config.warehouse_config)
    column_qdrant = QDrantClient(conf=app_config.qdrant_column_config)
    metric_qdrant = QDrantClient(conf=app_config.qdrant_metric_config)
    es = ElasticSearchClient(conf=app_config.elasticsearch_config)
    model = EmbeddingModel(conf=app_config.embedding_config)
    logger.info("初始化客户端完成")
    
    meta_config = process_args()
    await build(conf=meta_config, meta_client=meta, dw_client=dw, column_qdrant=column_qdrant,
                metric_qdrant=metric_qdrant, es_client=es, model=model)
    

if __name__ == '__main__':
    import asyncio
    
    asyncio.run(run())
