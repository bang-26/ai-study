#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  models 
    CreateTime     ：  2026-07-28 17:10:30 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Optional, Union, TypedDict
from sqlalchemy import String, Text
from sqlalchemy.types import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# 表信息
class ColumnInfo(Base):
    __tablename__ = "column_info"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="列编号")
    name: Mapped[Optional[str]] = mapped_column(String(128), comment="列名称")
    type: Mapped[Optional[str]] = mapped_column(String(64), comment="数据类型")
    role: Mapped[Optional[str]] = mapped_column(String(32), comment="列类型(primary_key,foreign_key,measure,dimension)")
    examples: Mapped[Union[dict, list, None]] = mapped_column(JSON, comment="数据示例")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="列描述")
    alias: Mapped[Union[dict, list, None]] = mapped_column(JSON, comment="列别名")
    table_id: Mapped[Optional[str]] = mapped_column(String(64), comment="所属表编号")


# 列指标信息
class ColumnMetric(Base):
    __tablename__ = "column_metric"
    
    column_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="列编号")
    metric_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="指标编号")


# 指标信息
class MetricInfo(Base):
    __tablename__ = "metric_info"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="指标编码")
    name: Mapped[Optional[str]] = mapped_column(String(128), comment="指标名称")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="指标描述")
    relevant_columns: Mapped[Union[dict, list, None]] = mapped_column(JSON, comment="关联字段")
    alias: Mapped[Union[dict, list, None]] = mapped_column(JSON, comment="指标别名")


# 表信息
class TableInfo(Base):
    __tablename__ = "table_info"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="表编号")
    name: Mapped[Optional[str]] = mapped_column(String(128), comment="表名称")
    role: Mapped[Optional[str]] = mapped_column(String(32), comment="表类型(fact/dim)")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="表描述")


# Qdrant 列信息
class QdrantColumn(TypedDict):
    id: str                                                         # 列 ID
    name: str                                                       # 列名称
    type: str                                                       # 数据类型
    role: str                                                       # 列类型
    examples: list                                                  # 数据示例
    description: str                                                # 列描述
    alias: list                                                     # 列别名
    table_id: str                                                   # 所属表编号


# Qdrant 指标信息
class QdrantMetric(TypedDict):
    id: str                                                          # 指标ID
    name: str                                                        # 指标名称
    description: str                                                 # 描述
    relevant_columns: list                                           # 相关字段
    alias: list                                                      # 别名


class ValueInfoES(TypedDict):
    id: str                                                          # 值ID
    value: str                                                       # 值
    type: str                                                        # 值类型
    column_id: str                                                   # 所属的字段ID
    column_name: str                                                 # 所属的字段名称
    table_id: str                                                    # 所属的表ID
    table_name: str                                                  # 所属的表名称
