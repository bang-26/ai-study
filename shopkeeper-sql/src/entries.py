#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  entry 
    CreateTime     ：  2026-07-26 18:17:44 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field


# 用户聊天请求的入参结构
class ChatRequest(BaseModel):
    query: str = Field(default="", description="用户查询内容")        # 用户输入的查询文本
    

# 用户聊天响应的结构
class ChatResponse(BaseModel):
    stage: Optional[str] = Field(default="", description="查询步骤")  # 用户输入的查询文本
    result: Optional[List[Dict[str, Any]]] = Field(default=[], description="查询数据")   # 查询结果
