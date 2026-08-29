#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  run 
    CreateTime     ：  2026-07-20 20:43:56 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from logger import logger
from entry import ChatMessageRequest, UserSessionsRequest, UserSessionsResponse
from service import StreamService, SessionService

router = APIRouter()                                       # 定义请求路由器


# FastAPI 应用生命周期管理：在应用启动时建立MCP连接，在应用关闭时清理连接
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # await mcp_connect()
        logger.info("MCP 连接建立完成")
    except Exception as e:
        logger.error(f"MCP 连接建立失败: {e}")
    yield                                                  # 应用运行期间，先别释放链接 去处理请求
    
    try:
        # await mcp_cleanup()                              # 应用关闭时执行
        logger.info("MCP 连接清理完成")
    except Exception as e:
        logger.error(f"MCP 连接清理失败: {e}")


# 返回数据：流式响应
@router.post(path="/api/query", summary="智能体对话接口", response_class=StreamingResponse)
async def query(request: ChatMessageRequest):
    logger.info(f"{request}")
    
    response = StreamService.process_task(chat_message=request)
    result = StreamingResponse(content=response, media_type="text/event-stream", status_code=200)
    return result


# 获取用户的所有会话记忆数据
@router.post(path="/api/user_sessions", summary="获取用户所有会话数据", response_model=UserSessionsResponse)
def get_user_sessions(request: UserSessionsRequest) -> UserSessionsResponse:
    user_id = request.user_id                                    # 从请求模型中获取目标用户 ID
    logger.info(f"接收到用户 {user_id} 的会话请求")
    result = UserSessionsResponse(user_id=user_id)
    response = SessionService.get_user_sessions(user_id=user_id)
    return response


# 创建 FastAPI 应用
def create_app() -> FastAPI:
    app = FastAPI(title="ITS API", lifespan=lifespan)      # 创建 FastApi 实例，绑定了生命周期事件
    # 处理跨域
    app.add_middleware(middleware_class=CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                       allow_methods=["*"], allow_headers=["*"], )
    app.include_router(router=router)                      # 注册各种路由
    return app


if __name__ == '__main__':
    try:
        uvicorn.run(app=create_app(), host="127.0.0.1", port=8000)
        logger.info("启动 Web 服务器成功 ......")
    except KeyboardInterrupt as e:
        logger.error(f"关闭 Web 服务器: {e}")
    except Exception as e:
        logger.error(f"启动 Web 服务器失败: {e}")
    finally:
        logger.info("关闭 Web 服务器成功 ......")
