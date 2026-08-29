#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  run 
    CreateTime     ：  2026-07-20 20:42:28 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import uvicorn
from fastapi import FastAPI, APIRouter, UploadFile, File
from entry import UploadResponse, QueryResponse, QueryRequest, CrawlerRequest, CrawlerResponse
from service import CrawlerService, DocumentService


app = FastAPI(title="Knowledge API")                                 # 创建 FastApi 实例
router = APIRouter()                                                 # 创建路由实例
app.include_router(router=router)                                    # 注册各种路由


@router.post(path="/crawler", response_model=CrawlerResponse, summary="爬取知识")
async def query(request: CrawlerRequest):
    max_no = request.max_no                                          # 获取最大数量
    response = CrawlerService.get_knowledge(max_no=max_no)           # 获取结果
    return response


# IO(对文件读写) 执行 SQL 网络请求 典型耗时任务
@router.post(path="/upload", response_model=UploadResponse, summary="处理知识库上传")
async def upload_file(file: UploadFile = File(...)):
    response = await DocumentService.upload_file(file=file)
    return response
    
    
@router.post(path="/query", response_model=QueryResponse, summary="查询知识库")
async def query(request: QueryRequest):
    user_question = request.question                                 # 获取用户问题
    response = DocumentService.query(user_question=user_question)    # 调用查询服务的查询方法
    return response


if __name__ == '__main__':
    print("启动服务...")
    uvicorn.run(app=app, host="0.0.0.0", port=8001)
    
