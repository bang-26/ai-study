#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  nodes 
    CreateTime     ：  2026-07-29 23:15:56 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from asyncio import sleep
from jieba.analyse import extract_tags
from langgraph.runtime import Runtime
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate, load_prompt
from logger import logger
from configs import DataDict, PathConfig
from agents import DataAgentContext, llm
from models import ValueInfoES, ColumnInfo, MetricInfo
from states import DataAgentState, TableInfoState, MetricInfoState
from utils import PromptParser


# 抽取关键字
async def extract_keywords(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    writer = runtime.stream_writer                         # 输出流
    writer("抽取关键字")                                    # 输出信息
    query = state["query"]                                 # 用户查询
    allow_pos = DataDict.ALLOW_POS                         # 对查询进行分词，只提取指定词性的词
    
    keywords = extract_tags(sentence=query, allowPOS=allow_pos)
    keywords = list(set(keywords + [query]))
    
    logger.info(f"抽取关键字: {keywords}")
    return {"keywords": keywords}
    

# 添加额外上下文信息
async def add_extra_context(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> None:
    writer = runtime.stream_writer                         # 输出流
    writer("添加额外上下文信息")                             # 输出信息
    # await sleep(0.5)                                       # 模拟耗时
    

# 生成 SQL
async def generate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> None:
    writer = runtime.stream_writer                         # 输出流
    writer("生成 SQL")                                     # 输出信息
    # await sleep(0.5)                                       # 模拟耗时
    

# 校验 SQL
async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    writer = runtime.stream_writer                         # 输出流
    writer("验证 SQL")                                     # 输出信息
    # await sleep(0.5)                                       # 模拟耗时
    return {"error": None}                                 # 返回错误信息
    

# 纠正 SQL
async def correct_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> None:
    writer = runtime.stream_writer                         # 输出流
    writer("校正 SQL")                                     # 输出信息
    # await sleep(0.5)                                       # 模拟耗时
    

# 执行 SQL
async def execute_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> None:
    writer = runtime.stream_writer                         # 输出流
    writer("执行 SQL")                                     # 输出信息
    # await sleep(0.5)                                       # 模拟耗时
    

# 过滤指标
async def filter_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> None:
    writer = runtime.stream_writer                         # 输出流
    writer("过滤指标")                                      # 输出信息
    # await sleep(0.5)                                       # 模拟耗时
    

# 过滤表格
async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> None:
    writer = runtime.stream_writer                         # 输出流
    writer("过滤表格")                                      # 模拟耗时
    # await sleep(0.5)                                       # 模拟耗时
    

# 召回字段信息
async def recall_column(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    writer = runtime.stream_writer
    writer("召回字段")
    
    query = state["query"]
    keywords = state["keywords"]
    
    embedding_client = runtime.context["embedding_client"]
    column_qdrant_repository = runtime.context["column_qdrant_repository"]
    
    # 使用 LLM 扩展关键词
    parser = PromptParser(PathConfig.PROMPT_PATH)
    template_key = DataDict.PROMPT_DICT.get("column-recall")
    template = parser.get_prompt(key=template_key)
    
    prompt = PromptTemplate(template=template, input_variables=["query"])
    output_parser = JsonOutputParser()
    
    chain = prompt | llm | output_parser
    
    result = await chain.ainvoke({"query": query})
    
    # 使用扩展后的关键词召回字段信息
    retrieved_columns_map: dict[str, ColumnInfo] = {}
    
    keywords = list(set(keywords + result))
    for keyword in keywords:
        embedding = await embedding_client.text_vector(keyword)
        
        payloads: list[ColumnInfo] = await column_qdrant_repository.search(vector=embedding)
        for payload in payloads:
            column_id = payload["id"]
            if column_id not in retrieved_columns_map:
                retrieved_columns_map[column_id] = payload
                
    retrieved_columns = list(retrieved_columns_map.values())
    
    logger.info(f"召回字段信息：{list(retrieved_columns_map.keys())}")
    return {"retrieved_columns": retrieved_columns}


# 召回字段取值信息
async def recall_value(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    writer = runtime.stream_writer
    writer("召回字段取值")
    
    query = state["query"]
    keywords = state["keywords"]
    
    value_es_repository = runtime.context["value_es_repository"]
    
    # 使用LLM扩展关键词
    parser = PromptParser(PathConfig.PROMPT_PATH)
    template_key = DataDict.PROMPT_DICT.get("value-recall")
    template = parser.get_prompt(key=template_key)
    
    prompt = PromptTemplate(template=template, input_variables=["query"])
    output_parser = JsonOutputParser()
    
    chain = prompt | llm | output_parser
    
    result = await chain.ainvoke({"query": query})
    
    # 使用扩展后的关键词召回字段取值
    values_map: dict[str, ValueInfoES] = {}
    keywords = list(set(keywords + result))
    for keyword in keywords:
        values: list[ValueInfoES] = await value_es_repository.search(keyword)
        for value in values:
            value_id = value["id"]
            if value_id not in values_map:
                values_map[value_id] = value
        
    retrieved_values = list(values_map.values())
    logger.info(f"召回字段取值：{list(values_map.keys())}")
    
    return {'retrieved_values': retrieved_values}


# 召回指标信息
async def recall_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    writer = runtime.stream_writer
    writer("召回指标")
    
    query = state["query"]
    keywords = state["keywords"]
    
    embedding_client = runtime.context['embedding_client']
    metric_qdrant_repository = runtime.context['metric_qdrant_repository']
    
    # 获取提示词
    parser = PromptParser(PathConfig.PROMPT_PATH)
    template_key = DataDict.PROMPT_DICT.get("value-recall")
    template = parser.get_prompt(key=template_key)
    
    # 使用LLM扩展关键词
    prompt = PromptTemplate(template=template, input_variables=["query"])
    output_parser = JsonOutputParser()
    
    chain = prompt | llm | output_parser
    
    result = await chain.ainvoke({"query": query})
    
    # 使用扩展后的关键词召回指标信息
    retrieved_metrics_map: dict[str, MetricInfo] = {}
    
    keywords = list(set(keywords + result))
    for keyword in keywords:
        embedding = await embedding_client.text_vector(string=keyword)
        payloads: list[MetricInfo] = await metric_qdrant_repository.search(embedding)
        for payload in payloads:
            metric_id = payload["id"]
            if metric_id not in retrieved_metrics_map:
                retrieved_metrics_map[metric_id] = payload
        
    retrieved_metrics = list(retrieved_metrics_map.values())
    
    logger.info(f"召回指标信息：{list(retrieved_metrics_map.keys())}")
    return {"retrieved_metrics": retrieved_metrics}


# 合并召回信息
async def merge_retrieved_info(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    writer = runtime.stream_writer
    writer("合并召回信息")
    
    retrieved_columns = state["retrieved_columns"]
    retrieved_values = state["retrieved_values"]
    retrieved_metrics = state["retrieved_metrics"]
    
    table_infos: list[TableInfoState] = []
    metric_infos: list[MetricInfoState] = []
    
    return {"table_infos": table_infos, "metric_infos": metric_infos}
