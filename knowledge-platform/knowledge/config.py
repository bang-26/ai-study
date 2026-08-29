#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  config 
    CreateTime     ：  2026-07-20 18:23:03 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os.path import dirname, abspath
from random import random


# 路径配置类
class PathConfig:
    # ============================== 基本路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                              # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    
    # ============================== 数据路径 ==============================
    KNOWLEDGE_PATH = abspath(path=f"{PROJECT_DIR}/data/knowledge")   # 知识库路径
    REPOSITORY_PATH = abspath(path=f"{PROJECT_DIR}/data/vector")     # 向量仓库路径
    TMP_FOLDER_PATH = abspath(path=f"{PROJECT_DIR}/data/tmp")        # 临时文件路径
    PROMPT_PATH = abspath(path=f"{PROJECT_DIR}/data/prompt.txt")     # 提示词路径
    
  
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


# 模型服务配置类
class CloudModelConfig:
    URL = "https://api.deepseek.com"                                 # 模型服务 URL
    API_KEY = "****************"                                     # 模型服务 API Key
    MODEL_NAME = "deepseek-v4-flash"                                 # 模型名称
    TEMPERATURE = 0                                                  # 模型服务温度
    MAX_TOKEN = 10240                                                # 模型服务最大 tokens
    

class CrawlerConfig:
    HEADERS = \
        {
            "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
            "Accept"         : "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q="
        }
    
    TIME_OUT = 10                                                    # 超时时间
    MAX_RETRY = 3                                                    # 最大重试次数
    MAX_CONNECTIONS = 10                                             # 最大连接数
    MAX_CONCURRENCY = 10                                             # 最大并发数
    MAX_REQUESTS = 1000                                              # 最大请求数
    SLEEP_TIME = round(random(), 2)                                  # 休眠时间


class KnowledgeConfig(CrawlerConfig):
    KNOWLEDGE_DOMAIN = "https://iknow.lenovo.com.cn"                 # 爬虫原始数据网址
    KNOWLEDGE_URI = "knowledgeapi/api/knowledge/knowledgeDetails"    # 爬虫原始数据路径
    MAX_NO = 1000                                                    # 最大知识编号
    
    
class DataDict:
    # ======================================== HTML ========================================
    HTML_TITLE = "暂无标题"                                           # HTML 标题
    HTML_DIGEST = "暂无摘要"                                          # HTML 摘要
    HTML_KEY_WORDS = ""                                              # HTML 关键词
    HTML_CONTENT = ""                                                # HTML 内容
    HTML_FIRST_TOPIC_NAME = ""                                       # HTML 主分类
    HTML_SUB_TOPIC_NAME = ""                                         # HTML 子分类
    HTML_QUESTION_CATEGORY_NAME = ""                                 # HTML 问题类别
    
    # ======================================== 文件 ========================================
    FILE_NAME_MAX_LENGTH = 50                                        # 文件名最大长度
    
    # ======================================= 提示词 =======================================
    PROMPT_KEY = "knowledge"                                         # 提示词 KEY
    
    
class VectorRepositoryConfig:
    REPOSITORY_DIRECTORY = PathConfig.REPOSITORY_PATH                # 向量仓库路径
    COLLECTION_NAME = "knowledge"                                    # 向量仓库名称
    URL = "https://api.openai-proxy.org/v1"                          # 模型服务 URL
    API_KEY = "****************"                                     # 模型服务 API Key
    EMBED_MODEL_NAME = "text-embedding-3-large"                      # 嵌入模型名称
    MAX_RETRY = 3                                                    # 最大重试次数
    MAX_CONCURRENCY = 10                                             # 最大并发数
    TIME_OUT = 3                                                     # 超时时间
    
    CHUNK_SIZE = 1500                                                # 长文档内容分块的阈值（略大一些。永远考虑语义优先）
    CHUNK_OVERLAP = 200                                              # 给一定重合度
    SEPARATORS = ["\n## ", "\n**""\n\n", "\n", " ", ""]              # 分割符
    
    DIMENSION = 1536                                                 # 维度
    OUTPUT_TYPE = "dense&sparse"                                     # 输出类型
    
class RetrievalConfig:
    RETRIEVAL_MODEL_NAME = "text-embedding-3-large"                  # 检索模型名称
