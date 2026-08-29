#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  states 
    CreateTime     ：  2026-07-29 23:20:27 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import TypedDict
from models import ColumnInfo, ValueInfoES, MetricInfo


# 列信息
class ColumnInfoState(TypedDict):
    name: str                                    # 字段名
    type: str                                    # 数据类型
    role: str                                    # 列类型
    examples: list                               # 数据示例
    description: str                             # 列描述
    alias: str                                   # 列别名


# 表信息
class TableInfoState(TypedDict):
    name: str                                    # 表名
    role: str                                    # 表类型(fact/dim)
    description: str                             # 表描述
    columns: list[ColumnInfoState]               # 列信息


# 指标信息
class MetricInfoState(TypedDict):
    name: str                                    # 指标名
    description: str                             # 描述
    relevant_columns: list[str]                  # 关联列
    alias: str                                   # 别名


# 数据代理状态
class DataAgentState(TypedDict):
    query: str                                   # 用户查询
    keywords: list[str]                          # 用户查询的关键字
    retrieved_columns: list[ColumnInfo]          # 召回的字段信息
    retrieved_values: list[ValueInfoES]          # 召回的值信息
    retrieved_metrics: list[MetricInfo]          # 召回的指标信息
    table_infos: list[TableInfoState]            # 表信息
    metric_infos: list[MetricInfoState]          # 指标信息
    error: str                                   # 验证SQL时的错误信息
