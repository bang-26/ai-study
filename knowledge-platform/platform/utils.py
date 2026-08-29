#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  utils 
    CreateTime     ：  2026-07-20 20:47:09 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from datetime import datetime
from math import pi, atan, exp
from typing import Optional
from uuid import uuid4

from entry import ContentKind, StreamPacket, TextMessageBody, StreamStatus, PacketMeta, FinishMessageBody


# SQL 解析类
class SqlParser:
    def __init__(self, path: str):
        self.path = path
        self.sql_dict = None
    
    def reader(self):
        self.sql_dict = {}
        with open(file=self.path, mode="r", encoding="utf-8") as fr:
            content_list = fr.readlines()
            
        key = ""
        sql = ""
        for content in content_list:
            if content and not content.startswith("--"):
                if content.startswith("#"):
                    key = content.split("#")[-1].strip()
                else:
                    sql = sql + content
                    if content.strip().endswith(";"):
                        self.sql_dict[key] = sql.strip()
                        sql = ""
    
    def get_sql(self, key: str):
        if self.sql_dict is None:
            self.reader()
        
        sql = self.sql_dict.get(key, "")
        return sql


# 提示语解析器
class PromptParser:
    def __init__(self, path: str):
        self.path = path
        self.prompt_dict = None
    
    def reader(self, sep: str = "%%"):
        self.prompt_dict = {}
        with open(file=self.path, mode="r", encoding="utf-8") as fr:
            content_list = fr.readlines()
        
        key = ""
        value = ""
        for content in content_list:
            if content.strip().startswith(sep):
                if key:
                    self.prompt_dict[key] = value
                    value = ""
                key = content.split(sep)[1].strip().split()[0]
            else:
                value = value + content
        
        if value:
            self.prompt_dict[key] = value
    
    def get_prompt(self, key: str):
        if self.prompt_dict is None:
            self.reader()
        
        prompt = self.prompt_dict.get(key, "")
        return prompt


# 墨卡托投影转换
class MercatorLatitudeLongitude:
    @staticmethod
    def mercator_to_latitude_longitude(x: float, y: float) -> tuple[float, float]:
        EARTH_RADIUS = 6378137.0
        MERCATOR_LIMIT = pi * EARTH_RADIUS
        
        if x < -MERCATOR_LIMIT or x > MERCATOR_LIMIT or y < -MERCATOR_LIMIT or y > MERCATOR_LIMIT:
            return 0.0, 0.0
        
        longitude = 180.0 * x / MERCATOR_LIMIT
        latitude = 180.0 / pi * (2.0 * atan(exp(y / EARTH_RADIUS)) - pi / 2.0)
        
        return latitude, longitude


# SSE 响应构建工厂
class ResponseFactory:
    # 构建文本/推理片段响应
    @staticmethod
    def build_text(text: str, kind: ContentKind) -> StreamPacket:
        body = TextMessageBody(text=text, kind=kind)
        
        return StreamPacket(id=str(uuid4()), content=body, status=StreamStatus.IN_PROGRESS,
                            metadata=PacketMeta(createTime=str(datetime.now())))
    
    # 构建结束信号响应
    @staticmethod
    def build_finish(message_id: Optional[str] = None) -> StreamPacket:
        if message_id is None:
            message_id = str(uuid4())
        
        return StreamPacket(id=message_id, content=FinishMessageBody(), status=StreamStatus.FINISHED,
                            metadata=PacketMeta(createTime=str(datetime.now())))
