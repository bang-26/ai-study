#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  entry 
    CreateTime     ：  2026-07-17 23:27:05 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Optional, List
from pydantic import BaseModel


# 配送范围查询请求
class DeliveryRequest(BaseModel):
    address: str                                           # 地址
    travel_mode: int = 2                                   # 0=步行, 2=骑电动车, 3=驾车


# 智能对话请求
class ChatRequest(BaseModel):
    query: str                                             # 查询内容


# 配送查询响应
class DeliveryResponse(BaseModel):
    success: bool                                          # 成功(True) or 失败的标识（False）
    in_range: bool                                         # 配送是否在配送范围内(True False)
    distance: float                                        # 配送距离(公里 km)
    formatted_address: str                                 # 格式化地址
    duration: float                                        # 配送时间（秒）
    message: str                                           # (前端要展示的配送完整消息内容)
    travel_mode: int                                       # 配送模式 (1:步行 2:骑电动车 3:驾车)
    input_address: str                                     # 输入原始内容


# 智能对话响应
class ChatResponse(BaseModel):
    success: bool                                          # 成功失败表示
    query: str                                             # 原始查询内容
    response: Optional[str] = None                         # 响应内容
    recommendation: Optional[str] = None                   # 推荐内容
    menu_ids: Optional[List[str]] = None                   # 推荐的菜品id


# 菜品列表响应
class MenuListResponse(BaseModel):
    success: bool                                          # 响应成功失败标识
    menu_items: List[dict]                                 # 菜品列表
    count: int                                             # 菜品数
    message: str                                           # 响应消息提示


# class MenuItems(Dict):
#     id:
#     dish_name,
#     price,
#     description,
#     category,
#     spice_level,
#     flavor,
#     main_ingredients,
#     cooking_method,
#     is_vegetarian,
#     allergens,
#     is_available
#
