#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  web 
    CreateTime     ：  2026-07-18 10:20:45 
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
from entry import MenuListResponse, DeliveryResponse, DeliveryRequest, ChatResponse, ChatRequest
from service import DinnerService, AmapService, ChatService
from init import app, mysql_connect, pinecone_connect


# 测试项目根路径访问是否可用
@app.get("/")
def hello_world():
    return {"hello": "world"}


# 测试项目请求路径访问是否可用
@app.get("/healthy")
def healthy():
    return {"message": "请求路径访问健康"}


# 菜品列表区域展示
@app.get("/menu/list", response_model=MenuListResponse)
async def menu_list_endpoint() -> MenuListResponse:
    menu_items = DinnerService().get_menu_list()
    response = MenuListResponse(success=False, menu_items=[], count=0, message="暂无菜品列表可用")
    
    # 3.封装结果返回
    if menu_items:
        response.success = True
        response.menu_items = menu_items
        response.count = len(menu_items)
        response.message = f"成功查询到{len(menu_items)}道菜品信息"
    
    return response


# 检查指定地址是否在配送范围内
@app.post("/delivery", response_model=DeliveryResponse)
async def delivery_endpoint(request: DeliveryRequest):
    result = AmapService.verify_range(address=request.address, transport=request.travel_mode)
    return result


# 智能对话接口
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = ChatService.chat(query=request.query)
    return result


# 启动uvicorn的入口
def run():
    print("🍽️ AiMenu 智能点餐系统 v1.0")
    print("=" * 50)
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("=" * 50)
    
    try:
        uvicorn.run("web:app", host="0.0.0.0", port=8000, log_level="info")
        logger.info("🚀 启动uvicorn服务器成功...")
    except KeyboardInterrupt as e:
        logger.error(f"🚀 启动uvicorn服务器失败{e}...")
    finally:
        pinecone_connect.close()
        mysql_connect.close()
        

if __name__ == "__main__":
    run()
