#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  graph 
    CreateTime     ：  2026-07-29 23:35:37 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from agents import DataAgentContext
from nodes import extract_keywords, recall_column, recall_value, recall_metric
from nodes import merge_retrieved_info, filter_metric, filter_table, add_extra_context
from nodes import generate_sql, validate_sql, correct_sql, execute_sql
from states import DataAgentState

graph_builder = StateGraph(state_schema=DataAgentState, context_schema=DataAgentContext)

# 添加节点
graph_builder.add_node(node="extract_keywords", action=extract_keywords)
graph_builder.add_node(node="recall_column", action=recall_column)
graph_builder.add_node(node="recall_value", action=recall_value)
graph_builder.add_node(node="recall_metric", action=recall_metric)
graph_builder.add_node(node="merge_retrieved_info", action=merge_retrieved_info)
graph_builder.add_node(node="filter_metric", action=filter_metric)
graph_builder.add_node(node="filter_table", action=filter_table)
graph_builder.add_node(node="add_extra_context", action=add_extra_context)
graph_builder.add_node(node="generate_sql", action=generate_sql)
graph_builder.add_node(node="validate_sql", action=validate_sql)
graph_builder.add_node(node="correct_sql", action=correct_sql)
graph_builder.add_node(node="execute_sql", action=execute_sql)

# 添加关系
graph_builder.add_edge(start_key=START, end_key="extract_keywords")
graph_builder.add_edge(start_key="extract_keywords", end_key="recall_column")
graph_builder.add_edge(start_key="extract_keywords", end_key="recall_value")
graph_builder.add_edge(start_key="extract_keywords", end_key="recall_metric")
graph_builder.add_edge(start_key="recall_column", end_key="merge_retrieved_info")
graph_builder.add_edge(start_key="recall_value", end_key="merge_retrieved_info")
graph_builder.add_edge(start_key="recall_metric", end_key="merge_retrieved_info")
graph_builder.add_edge(start_key="merge_retrieved_info", end_key="filter_table")
graph_builder.add_edge(start_key="merge_retrieved_info", end_key="filter_metric")
graph_builder.add_edge(start_key="filter_table", end_key="add_extra_context")
graph_builder.add_edge(start_key="filter_metric", end_key="add_extra_context")
graph_builder.add_edge(start_key="add_extra_context", end_key="generate_sql")
graph_builder.add_edge(start_key="generate_sql", end_key="validate_sql")

path_map = {"execute_sql": "execute_sql", "correct_sql": "correct_sql"}
path_func = lambda state: "execute_sql" if state["error"] is None else "correct_sql"
graph_builder.add_conditional_edges(source="validate_sql", path=path_func, path_map=path_map)

graph_builder.add_edge(start_key="correct_sql", end_key="execute_sql")
graph_builder.add_edge(start_key="execute_sql", end_key=END)

graph = graph_builder.compile()


if __name__ == '__main__':
    import asyncio
    from clients import QDrantClient, ElasticSearchClient, EmbeddingModel, MysqlClient
    from repositories import ColumnRepository, MetricRepository, ValueRepository, MetaRepository
    from configs import app_config

    async def test():
        # 初始化并连接所有客户端
        meta_client = MysqlClient(conf=app_config.mysql_config)
        column_qdrant = QDrantClient(conf=app_config.qdrant_column_config)
        metric_qdrant = QDrantClient(conf=app_config.qdrant_metric_config)
        es = ElasticSearchClient(conf=app_config.elasticsearch_config)
        embedding_model = EmbeddingModel(conf=app_config.embedding_config)
        
        await meta_client.connect()
        await column_qdrant.connect()
        await metric_qdrant.connect()
        await es.connect()
        embedding_model.connect()

        # 初始化仓库
        meta_repository = MetaRepository(client=meta_client)
        column_repository = ColumnRepository(client=column_qdrant, model=embedding_model)
        metric_repository = MetricRepository(client=metric_qdrant, model=embedding_model)
        value_repository = ValueRepository(client=es)
        
        # 构建完整的 context
        context = DataAgentContext(embedding_client=embedding_model, column_qdrant_repository=column_repository,
                                   value_es_repository=value_repository, metric_qdrant_repository=metric_repository,
                                   meta_mysql_repository=meta_repository)  # 假设没有使用 MetaRepository

        state = DataAgentState(query="查询2023年的销售数据")
        async for chunk in graph.astream(input=state, context=context, stream_mode="custom"):
            print(chunk)
            
            
        await es.close()
        await column_qdrant.close()
        await metric_qdrant.close()
        await meta_client.close()
    asyncio.run(test())
