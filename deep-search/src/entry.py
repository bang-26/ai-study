#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  entry 
    CreateTime     ：  2026-08-09 14:42:07 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""
from contextvars import ContextVar
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from config import DataDict



# ============================== 请求实体 ============================== #
class TaskRequest(BaseModel):
    query: str = Field(default="", description="查询内容")
    thread_id: str = Field(default=None, description="线程ID")
    
    
# ============================== 响应实体 ============================== #
class TaskResponse(BaseModel):
    status: str = Field(default="started", description="查询内容")
    thread_id: str = Field(default=None, description="线程ID")


class UploadResponse(BaseModel):
    status: str = Field(default="success", description="上传状态")
    files: list[str] = Field(default=[], description="上传文件列表")


class FileInfo(BaseModel):
    name: str = Field(default="", description="文件名")
    type: str = Field(default="file", description="文件类型")
    path: str = Field(default="", description="文件路径")
    url: str = Field(default="", description="文件URL")
    size: float = Field(default=0, description="文件大小")
    mtime: float = Field(default=datetime.now(), description="文件修改时间")
    

class QueryFileResponse(BaseModel):
    error: str = Field(default="", description="错误信息")
    files: list[FileInfo] = Field(default=[], description="文件列表")
    
    
class WebsocketData(BaseModel):
    received: dict = Field(default={}, description="数据")
    
    
class WebsocketResponse(BaseModel):
    type: str = Field(default="pong", description="类型")
    message: Union[WebsocketData, str] = Field(default=WebsocketData(received={}), description="消息")
    

# ==============================
class Context(BaseModel):
    __session_context: ContextVar[Optional[str]] = ContextVar(DataDict.SESSION_DIR, default=None)
    __thread_context: ContextVar[Optional[str]] = ContextVar(DataDict.THREAD_ID, default=None)


class PayLoad(BaseModel):
    type: str = Field(default="monitor_event", description="事件类型")
    event: str = Field(default="", description="事件名称")
    message: str = Field(default="", description="事件消息")
    data: dict = Field(default={}, description="事件数据")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="事件时间戳")


class AgentInfo(BaseModel):
    name: str = Field(default="", description="代理名称")
    description: str = Field(default="", description="代理描述")
    system_prompt: str = Field(default="", description="代理系统提示")
    tools: list = Field(default=[], description="代理工具")
