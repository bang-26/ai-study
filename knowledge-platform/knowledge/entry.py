#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  entry 
    CreateTime     ：  2026-07-20 20:37:58 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from pydantic import BaseModel


# 爬取数据
class CrawlerRequest(BaseModel):
    max_no: int = 10                             # 爬取最数量


class CrawlerResponse(BaseModel):
    success_no: int                              # 成功数量
    fail_no: int                                 # 失败数量


# 文件上传的响应数据模型
class UploadResponse(BaseModel):
    status: str                                  # 响应状态
    message: str                                 # 响应的消息内容
    file_name: str                               # 上传的文件名
    chunks_added: int                            # 上传文档切分之后的文档块数量


# 查询的响应数据模型
class QueryResponse(BaseModel):
    question: str                                # 用户提问问题
    answer: str                                  # 模型的回答


# 查询的请求数据模型
class QueryRequest(BaseModel):
    question: str                                # 用户提问问题
