#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  web 
    CreateTime     ：  2026-07-26 20:27:30 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from logger import logger
from configs import app_config
from entries import ChatRequest, ChatResponse
from service import StreamService


app = FastAPI(title="Shopkeeper Bill API")
router = APIRouter()                                       # 定义请求路由器
app.include_router(router=router)                          # 注册各种路由

# 返回数据
@router.post(path="/api/query", summary="智能体对话接口", response_model=ChatResponse)
async def query(request: ChatRequest) -> ChatResponse:
    user_query = request.query
    logger.info(f"user-query = {user_query}")
    
    response = StreamService.process_task(user_query=user_query)
    return response


if __name__ == '__main__':
    try:
        logger.info("启动 Web 服务器 ......")
        uvicorn.run(app=app, host=app_config.service_config.host, port=app_config.service_config.port)
    except KeyboardInterrupt as e:
        logger.error(f"关闭 Web 服务器: {e}")
    except Exception as e:
        logger.error(f"启动 Web 服务器失败: {e}")
    finally:
        logger.info("关闭 Web 服务器成功 ......")
