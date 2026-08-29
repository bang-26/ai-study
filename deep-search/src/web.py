#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  web 
    CreateTime     ：  2026-08-09 14:39:52 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import uvicorn
from asyncio import get_running_loop
from typing import List, Any
from fastapi import WebSocket, WebSocketDisconnect, UploadFile, File, Form, FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import app_config
from entry import TaskRequest, TaskResponse, UploadResponse, WebsocketData, WebsocketResponse
from logger import logger
from monitor import monitor_service
from service import TaskService, FileService, connect_manager_service

app = FastAPI(title="DeepAgents API")
app.add_middleware(middleware_class=CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"], )


@app.post(path="/api/task", response_model=TaskResponse, description="运行任务")
async def run_task(request: TaskRequest) -> TaskResponse:
    logger.info(f"收到任务请求: {request}")
    result = await TaskService.run_task(request)
    logger.info(f"任务请求处理结果: {result}")
    return result


# 上传文件到 updated/session_{thread_id} 目录
@app.post(path="/api/upload", response_model=UploadResponse, description="上传文件到指定目录")
async def upload_files(files: List[UploadFile] = File(...), thread_id: str = Form(...)) -> UploadResponse:
    logger.info(f"线程 {thread_id} 上传文件")
    result = await FileService.upload_files(files=files, thread_id=thread_id)
    logger.info(f"线程 {thread_id} 文件上传完成: {files}")
    return result


# 下载指定文件
@app.get(path="/api/download", description="下载指定文件")
async def download_file(path: str):
    logger.info(f"下载文件请求: {path}")
    
    result = await FileService.download_file(file_path=path)
    return result


# 列出指定目录下的文件
@app.get("/api/files")
async def list_files(path: str):
    logger.info(f"列出文件请求: {path}")
    result = await FileService.list_files(path=path)
    return result


# 在应用启动时，将正确的事件循环绑定到 manager
@app.on_event(event_type="startup")
async def startup_event():
    loop = get_running_loop()
    monitor_service.set_websocket_manager(manager=connect_manager_service)
    connect_manager_service.set_loop(loop)
    logger.info(f"WebSocket Manager bound to loop: {id(loop)}")


@app.websocket(path="/ws")
async def websocket_legacy(websocket: WebSocket) -> None:
    await websocket.accept()
    result = WebsocketResponse(type="error", message="Client outdated. Please refresh page.")
    await websocket.send_json(result)
    await websocket.close(code=1000, reason="Client outdated")


@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    await connect_manager_service.connect(websocket, thread_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            received = WebsocketData(received=data)
            result = WebsocketResponse(message=received)
            await websocket.send_json(data=result.model_dump())
    except WebSocketDisconnect:
        logger.error(f"WebSocket Disconnect: {thread_id}")
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
    finally:
        connect_manager_service.disconnect(websocket, thread_id)


if __name__ == "__main__":
    uvicorn.run(app="web:app", host=app_config.service_config.host,
                port=app_config.service_config.port, reload=True)
