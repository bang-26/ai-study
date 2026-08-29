#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge
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

from typing import List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field

    
# ============================== 请求实体 ============================== #
# 接收参数的类型
class QueryRequest(BaseModel):
    query: str = Field(default=..., title="查询内容，必须传递")
    session_id: str = Field(default=None, title="会话 id，可以不传递，后台 uuid 生成第一个！")
    is_stream: bool = Field(default=False, title="是否流式返回结果")


# ============================== 响应实体 ============================== #
class UploadFileResponse(BaseModel):
    code: int = Field(default=501, description="状态码")
    task_ids: List[str] = Field(default=[], description="任务 ID")
    message: str = Field(default="文件上传失败", description="文件上传信息")
    

class TaskStatusResponse(BaseModel):
    code: int = Field(default=501, description="状态码")
    task_id: str = Field(default=None, description="任务 ID")
    status: str = Field(default="failed", description="任务全局状态")  # pending/processing/completed/failed
    done_list: List[str] = Field(default=[], description="已完成节点/阶段列表")
    running_list: List[str] = Field(default=[], description="正在运行的节点/阶段列表")


class QueryResponse(BaseModel):
    answer: str = Field(default="", title="查询结果")
    session_id: str = Field(default=None, title="会话 id")
    message: str = Field(default="本次查询处理中....", title="查询结果信息")
    done_list: List[str] = Field(default=[], title="已完成节点/阶段列表")
    running_list: List[str] = Field(default=[], title="正在运行的节点/阶段列表")

class GetHistoryResponse(BaseModel):
    session_id: str = Field(default=None, title="会话 id")
    items: List[dict] = Field(default=[], title="历史会话列表")


class DeleteHistoryResponse(BaseModel):
    deleted_count: int = Field(default=0, title="删除的会话数量")
    message: str = Field(default="删除成功！", title="删除结果信息")
