#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  service 
    CreateTime     ：  2026-08-09 14:48:32 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from asyncio import create_task
from os import walk
from os.path import join, abspath, exists, basename, normcase, relpath, getsize, getmtime
from sys import platform
from typing import Dict, List, Union
from uuid import uuid4

from fastapi import UploadFile
from fastapi.responses import FileResponse
from starlette.websockets import WebSocket
from config import PathConfig
from connect import cloud_model_connect
from entry import UploadResponse, TaskRequest, TaskResponse, QueryFileResponse, FileInfo
from logger import logger
from util import FileUtil


class TaskService:
    @staticmethod
    async def run_task(request: TaskRequest) -> TaskResponse:
        thread_id = request.thread_id or str(uuid4())
        query = request.query or ""
        
        result = TaskResponse(thread_id=thread_id)
        
        from agent import DeepSearchAgent
        from tool import generate_markdown, internet_search, get_assistant_list, list_sql_tables
        from tool import get_table_data, create_ask_delete, convert_md_to_pdf, read_file_content, execute_sql_query
        
        agent_tool_dict = \
            {
                "main"   : [generate_markdown, convert_md_to_pdf, read_file_content],
                "tavily" : [internet_search],
                "ragflow": [get_assistant_list, create_ask_delete],
                "db"     : [list_sql_tables, get_table_data, execute_sql_query]
            }
        
        agent = DeepSearchAgent(path=PathConfig.PROMPT_PATH, agent_tool_dict=agent_tool_dict,
                                model=cloud_model_connect.llm)
        try:
            create_task(agent.run_agent(task_query=query, session_id=thread_id))
            logger.info(f"Task started: {thread_id}")
            result.status = "started"
        except Exception as e:
            logger.error(f"Error starting task: {e}")
            result.status = "failed"
        finally:
            return result


# 文件服务类：负责处理文件上传和管理
class FileService:
    @staticmethod
    async def upload_files(files: List[UploadFile], thread_id: str) -> UploadResponse:
        result = UploadResponse(status="uploaded", files=[])
        
        target_dir = f"{PathConfig.UPDATE_DIR}/session_{thread_id}"
        FileUtil.ensure_dir_exists(file_path=target_dir)
        
        saved_files = []
        for file in files:
            file_path = join(target_dir, file.filename)
            FileUtil.save_io(file_path=file_path, file_io=file.file)
            saved_files.append(file.filename)
        
        result.files = saved_files
        return result
    
    @classmethod
    async def download_file(cls, file_path: str) -> Union[dict[str, str], dict[str, str], FileResponse]:
        # 安全检查
        abs_path = abspath(path=file_path)
        
        # 在 Windows 上统一大小写，避免 startswith 校验误判
        if platform == "win32":
            abs_path = normcase(s=abs_path)
            output_dir = normcase(s=PathConfig.OUTPUT_DIR)
        else:
            output_dir = PathConfig.OUTPUT_DIR
        
        if not abs_path.startswith(output_dir):
            return {"error": "Access denied: Path must be within output directory"}
        
        if not exists(abs_path):
            return {"error": "File not found"}
        
        return FileResponse(abs_path, filename=basename(abs_path))
    
    @classmethod
    async def list_files(cls, path):
        result = QueryFileResponse()
        abs_path = abspath(path=path)
        
        if not exists(abs_path):
            logger.error(f"路径不存在: {abs_path}")
            result.error = "Path not found"
            return result
        
        # 在 Windows 上，路径大小写可能不一致，统一使用 normcase 标准化
        if platform == "win32":
            abs_path = normcase(s=abs_path)
            output_dir = normcase(s=PathConfig.OUTPUT_DIR)
        else:
            output_dir = PathConfig.OUTPUT_DIR
        
        if not abs_path.startswith(output_dir):
            logger.error(f"路径必须以 {output_dir} 开头")
            result.error = "Access denied: Path must be within output directory"
            return result
            
        file_list = []
        try:
            # 使用 os.walk 递归遍历目录
            for root, dirs, filenames in walk(abs_path):
                for filename in filenames:
                    file_path = join(root, filename)
                    
                    # 计算相对于输出路径，用于生成 URL (保留，虽然下载用绝对路径)
                    rel_path = relpath(path=file_path, start=output_dir)
                    url_path = rel_path.replace("\\", "/")
                    
                    size = getsize(file_path)
                    mtime = getmtime(file_path)
                    file_info = FileInfo(name=filename, path=file_path, url=f"/outputs/{url_path}", size=size,
                                         mtime=mtime)
                    file_list.append(file_info)
        except Exception as e:
            logger.error(f"Walk failed: {e}")
            result.error = str(e)
            return result
        
        # 按时间倒序排列
        file_list.sort(key=lambda x: x.get("mtime", 0), reverse=True)
        logger.info(f"共找到 {len(file_list)} 个文件")
        
        result.files = file_list
        return result



class ConnectionManagerService:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        # 延迟绑定 loop，防止初始化时 loop 不一致
        self.loop = None
    
    # 显式设置事件循环
    def set_loop(self, loop):
        self.loop = loop
        logger.info(f"[Monitor] ConnectionManager manually bound to loop: {id(self.loop)}")
    
    # 建立连接
    async def connect(self, websocket: WebSocket, thread_id: str):
        await websocket.accept()
        logger.info(f"[Monitor] 存储当前会话id:{thread_id}对应的:{websocket}")
        self.active_connections[thread_id] = websocket
        logger.info(f"[Monitor] Client connected: {thread_id}")
    
    # 断开连接
    def disconnect(self, websocket: WebSocket, thread_id: str):
        if thread_id in self.active_connections:
            del self.active_connections[thread_id]
        logger.info(f"[Monitor] Client disconnected: {thread_id}")
    
    # 发送个人消息
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    # 发送消息到指定会话
    async def send_to_thread(self, message: dict, thread_id: str):
        if thread_id in self.active_connections:
            websocket = self.active_connections[thread_id]
            await websocket.send_json(message)
    
    # 广播消息到所有会话
    async def broadcast(self, message: dict):
        for websocket in self.active_connections.values():
            await websocket.send_json(message)


connect_manager_service = ConnectionManagerService()
