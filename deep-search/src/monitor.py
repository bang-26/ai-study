#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  monitor 
    CreateTime     ：  2026-08-12 13:18:13 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""
import builtins
from typing import Optional, Dict, Any

from context import context
from entry import PayLoad
from logger import logger
from service import ConnectionManagerService


# 工具监控类，用于在工具执行过程中上报进度和状态
class MonitorService:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(MonitorService, cls).__new__(cls)
            cls.__instance.websocket_manager = None  # 预留给 FastAPI WebSocketManager
        return cls.__instance
    
    # 设置 FastAPI 的 WebSocket 管理器
    def set_websocket_manager(self, manager: ConnectionManagerService):
        self.websocket_manager = manager
    
    # 内部发送方法
    def __emit(self, event_type: str, message: str, data: Optional[Dict[str, Any]] = None):
        payload = PayLoad(event=event_type, message=message, data=data or {})
        
        # 1. 优先尝试通过 FastAPI WebSocket 发送
        if self.websocket_manager:
            try:
                manager = self.websocket_manager
                loop = getattr(manager, 'loop', None)
                if loop:
                    payload_dict = payload.model_dump()
                    thread_id = context.get_thread_context()
                    
                    if thread_id:
                        # 有会话上下文：定向推送
                        coro = manager.send_to_thread(payload_dict, thread_id)
                    else:
                        # 工具线程拿不到 ContextVar 时：广播兜底，保证前端能收到
                        coro = manager.broadcast(payload_dict)
                    
                    from asyncio import run_coroutine_threadsafe
                    future = run_coroutine_threadsafe(coro, loop)
                    future.add_done_callback(self.__on_send_done)
            except Exception as e:
                logger.error(f"[Monitor] WebSocket send failed: {e}")
        
        # 2. 尝试通过全局 runtime 输出 (DeepAgents 脚本模式)
        # 这使得 simple_agents.py 中的 MockRuntime 能接收到数据
        if builtins and hasattr(builtins, 'runtime') and hasattr(builtins.runtime, 'stream_writer'):
            try:
                builtins.runtime.stream_writer(payload)
            except Exception as e:
                logger.error(f"[Monitor] Runtime stream writer failed: {e}")
        
        # 3. 控制台保底输出 (方便调试)
        # 加上特殊前缀，方便肉眼识别
        logger.info(f"\n[Monitor:{event_type}] {message}")
    
    # 消费 run_coroutine_threadsafe 返回的 Future，避免异常丢失
    @staticmethod
    def __on_send_done(future) -> None:
        try:
            future.result()
        except Exception as e:
            logger.error(f"[Monitor] WebSocket send future failed: {e}")
    
    # 报告工具开始执行
    def report_tool(self, tool_name: str, args: Dict[str, Any] = None):
        data_dict = {"tool_name": tool_name, "args": args}
        self.__emit(event_type="tool_start", message=f"开始执行工具: {tool_name}", data=data_dict)
    
    # 报告正在调用的子智能体进度
    def report_assistant(self, assistant_name: str, args: Dict[str, Any] = None):
        data_dict = {"assistant_name": assistant_name, "args": args}
        self.__emit(event_type="assistant_call", message=f"正在调用助手: {assistant_name}", data=data_dict)
    
    # 报告任务最终结果
    def report_task_result(self, result: str):
        data_dict = {"result": result}
        self.__emit(event_type="task_result", message="任务执行完成", data=data_dict)
    
    # 报告任务工作目录
    def report_session_dir(self, path: str):
        data_dict = {"path": path}
        self.__emit(event_type="session_created", message=f"工作目录已创建: {path}", data=data_dict)

    def report_error(self, message: str):
        self.__emit(event_type="error", message=message)
    
    
monitor_service = MonitorService()
