#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  config 
    CreateTime     ：  2026-07-17 16:38:16 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os.path import dirname, abspath


# 路径配置类
class PathConfig:
    # ============================== 基本路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                              # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    
    # ============================== 数据路径 ==============================
    SQL_PATH = abspath(path=f"{PROJECT_DIR}/data/dinner.sql")        # 原始数据路径
    PROMPT_PATH = abspath(path=f"{PROJECT_DIR}/data/prompt.txt")     # 提示语路径
    
  
# Mysql 配置类
class MysqlConfig:
    PROTOCOL = "mysql+pymysql"                                       # 连接协议
    HOST = "****************"                                        # 数据库地址
    PORT = 3306                                                      # 数据库端口
    USER = "****************"                                        # 数据库用户名
    PASSWORD = "****************"                                    # 密码
    DATABASE = "gmail"                                               # 数据库名称
    CHARSET = "utf8mb4"                                              # 字符集
    TIME_OUT = 10                                                    # 超时时间
    MAX_CONNECTIONS = 10                                             # 最大连接数
    PRINT_SQL = False                                                # 是否打印 SQL


# PineCone 配置类
class PineConeConfig:
    API_KEY = "****************"
    INDEX_NAME = "guigu-dinner"                                      # 索引名称
    CLOUD_NAME = "aws"                                               # 云
    REGION = "us-east-1"                                             # 地域
    MODEL_NAME = "text-embedding-ada-002"                            # 模型名称
    FILD_MAP = {"text": "chunk_text"}                                # 字段映射
    INDEX_TYPE = "dense"                                             # 索引类型
    DIMENSION = 1536                                                 # 维度
    METRIC = "cosine"                                                # 度量
    MAX_NODES = 1000                                                 # 节点数


# 阿里百炼
class BaiLianConfig:
    URL = "https://llm-t8pcm3a7gt9om5i5.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    API_KEY = "****************"
    EMBED_MODEL_NAME = "text-embedding-v4"                           # 嵌入模型名称
    DIMENSION = 1536                                                 # 维度
    OUTPUT_TYPE = "dense&sparse"                                     # 输出类型


class CloudModelConfig:
    URL = "https://api.deepseek.com"                                 # 模型服务 URL
    API_KEY = "****************"                                     # 模型服务 API Key
    MODEL_NAME = "deepseek-v4-flash"                                 # 模型名称


class AmapConfig:
    BASE_URL = "https://restapi.amap.com"                            # 基础 URL
    GEO_URL = f"{BASE_URL}/v3/geocode/geo"                           # 地理编码
    REGEO_URL = f"{BASE_URL}/v3/geocode/regeo"                       # 地理反编码
    PATH_URL = \
        {
            "walking": f"{BASE_URL}/v5/direction/walking",
            "bicycle": f"{BASE_URL}/v5/direction/bicycling",
            "electrobike": f"{BASE_URL}/v5/direction/electrobike",
            "driving": f"{BASE_URL}/v5/direction/driving",
            "transit": f"{BASE_URL}/v5/direction/transit/integrated",
        }
    
    API_KEY = "****************"                                     # 高德地图 API Key
    RETRY = 3                                                        # 重试次数
    INTERVAL = 0.5                                                   # 延迟时间
    STATUS_CODES = [429, 500, 502, 503, 504, 505]                    # 错误码
    TIMEOUT = 10                                                     # 请求超时时间
    
    MERCHANT_LONGITUDE = 116.365533                                  # 商户经度
    MERCHANT_LATITUDE = 40.102488                                    # 商户纬度
    DELIVERY_RADIUS = 2500                                           # 配送范围
    # 默认路径规划模式 (1-步行距离，2-骑行(电动车)距离，3-驾车距离)
    DEFAULT_PATH_MODE = 2


class DataDict:
    SPICE_LEVEL = {0: "不辣", 1: "微辣", 2: "中辣", 3: "重辣", 4: "特辣", 5: "极辣"}
    SPICE_LEVEL_DEFAULT = "未知辣度"
    
    IS_VEGETARIAN = {0: "否", 1: "是"}
    VEGETARIAN_DEFAULT = "未知状况"
    
    DESCRIPTION_DEFAULT = "暂无描述"
    MAIN_INGREDIENTS_DEFAULT = "暂无主要食材"
    ALLERGIES_DEFAULT = "暂无过敏源"
    
    DATA_TYPE = {0: "菜品", 1: "食材", 2: "菜谱"}
    
    GET_AVAILABLE_DISHES = "get_menu_items"                          # 获取可用的菜
    GENERAL_INQUIRY = "general-inquiry"                            # 客服字段
    MENU_INQUIRY = "menu-inquiry"                                        # 咨询字段
    ADAPT_PARSER = "adapt-parser"                                    # 适配
    
    MAX_MATCH_COUNT = 2
    
    PATH_MODE = { 0: "walking", 1: "bicycle", 2: "electrobike", 3: "driving", 4: "transit" }
    
    DINNER_COORDINATES = "116.365533,40.102488"
    
    MAX_DISTANCE = 25000
