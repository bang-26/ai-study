#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  web 
    CreateTime     ：  2026-08-12 17:08:01 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import environ
environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from typing import Any, Coroutine, List
from uvicorn import run
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from config import app_config, PathConfig
from entry import DeleteHistoryResponse, GetHistoryResponse, QueryRequest, TaskStatusResponse, UploadFileResponse
from logger import logger
from service import ImportService, QueryService
from util import FileUtil

# 初始化 FastAPI 应用实例
app = FastAPI(title=app_config.service_config.name, description=app_config.service_config.description)

# 跨域中间件配置：解决前端调用后端接口的跨域限制
app.add_middleware(middleware_class=CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"], )


# 健康状态
@app.get(path="/health", summary="健康状态检查接口", description="检查服务是否正常启动")
async def health() -> dict[str, str]:
    logger.info(f"触发后台检测检查接口，数据一切正常！！")
    return {"status": "ok"}


# 8080/import  -> import.html
@app.get(path="/import", response_class=FileResponse)
async def get_import_page() -> FileResponse:
    logger.info("访问导入页面 ... ")
    
    page = f"{PathConfig.WEB_DIR}/import.html"
    is_exist = FileUtil.judge_file_exists(file_path=page)
    
    if is_exist:
        return FileResponse(path=page, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="导入页面不存在！！")


# 返回 chat.html
@app.get(path="/chat", response_class=FileResponse, summary="聊天页面接口", description="返回聊天页面")
async def chat_html() -> FileResponse:
    page = f"{PathConfig.WEB_DIR}/chat.html"
    is_exist = FileUtil.judge_file_exists(file_path=page)
    
    if is_exist:
        return FileResponse(path=page, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="聊天页面不存在！！")
        
    
# 文件上传 + 开启导入流程
@app.post(path="/upload", summary="文件上传接口", description="上传文件到服务器，并开启异步图任务")
async def upload_file(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)) -> UploadFileResponse:
    logger.info("开始文件上传 ... ")
    
    response = await ImportService.upload_file(background_tasks=background_tasks, files=files)
    logger.info(f"文件上传完成，并开启了异步任务！")
    
    return response


# 任务状态查询：前端轮询此接口获取单个任务的处理进度和状态
@app.get(path="/status/{task_id}", summary="任务状态查询", description="根据 TaskID 查询单个文件的处理进度和全局状态")
async def get_task_progress(task_id: str) -> TaskStatusResponse:
    logger.info(f"[{task_id}] 任务状态查询开始 ... ")
    
    result = await ImportService.get_task_progress(task_id=task_id)
    logger.info(f"[{task_id}] 任务状态查询完成 ...")
    
    return result


# 客户端 ==> 问题 ==> graph ==> 查到 rag 结果 ==> 返回即可
@app.post(path="/query", summary="查询接口", description="查询接口")
async def query(request: QueryRequest, background_tasks: BackgroundTasks):
    logger.info(f"开始查询 ... ")
    
    result = await QueryService.query(request=request, background_tasks=background_tasks)
    logger.info(f"查询完成 ...")
    
    return result


# sse 长连接接口
@app.get(path="/stream/{session_id}", summary="sse 长连接接口", description="sse 长连接接口")
async def stream(session_id: str, request: Request) -> StreamingResponse:
    logger.info(f"session_id = {session_id} 客户端，已经和后台建立了长连接！")
    
    stream_result = await QueryService.process_stream(session_id=session_id, request=request)
    return stream_result


# 历史对话查询
@app.get(path="/history/{session_id}", summary="历史对话接口", description="查询历史对话")
async def get_history(session_id: str, limit: int = 10) -> GetHistoryResponse:
    logger.info(f"session_id = {session_id} 获取历史对话开始 ... ")
    
    history_info = await QueryService.get_history(session_id=session_id, limit=limit)
    logger.info(f"session_id = {session_id} 获取历史对话完成 ...")
    
    return history_info
    

# 删除历史对话
@app.delete(path="/history/{session_id}", summary="删除历史对话接口", description="删除历史对话")
async def delete_history(session_id: str) -> DeleteHistoryResponse:
    logger.info(f"删除 session_id = {session_id} 的历史对话 ... ")
    
    delete_result = await QueryService.delete_history(session_id=session_id)
    logger.info(f"删除 session_id = {session_id} 的历史对话完成 ...")
    
    return delete_result


if __name__ == "__main__":
    run(app=app, host=app_config.service_config.host, port=app_config.service_config.port)
