#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search
    FileName       ：  config 
    CreateTime     ：  2026-07-20 18:28:18 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os.path import dirname, abspath
from typing import TypeVar, Type, Optional, Literal, Union
from dataclasses import dataclass
from omegaconf import OmegaConf


# 路径配置类
class PathConfig:
    # ============================== 基本路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                   # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                    # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")        # 项目路径
    
    # ============================== 配置路径 ==============================
    APP_CONF_PATH = abspath(path=f"{PROJECT_DIR}/conf/application.yml")   # 配置文件路径
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")                         # 日志路径
    
    # ============================== 模型路径 ==============================
    PROMPT_PATH = abspath(path=f"{PROJECT_DIR}/data/prompts.yml")         # 提示词路径
    UPDATE_DIR = abspath(path=f"{PROJECT_DIR}/data/update")               # 更新目录
    OUTPUT_DIR = abspath(path=f"{PROJECT_DIR}/data/output")               # 输出目录
    

# 数据字典
class DataDict:
    # ======================================== 所示 ========================================
    KNOWLEDGE_BASE_URL = "http://127.0.0.1:8001"           # 知识库地址
    
    SESSION_DIR = "session_dir"                            # 会话目录
    THREAD_ID = "thread_id"                                # 线程 ID
    
    REPORT_DICT = \
        {
            "tool_start": "tool_start",
            "assistant_call": "assistant_call",
            "task_result": "task_result",
            "session_created": "session_created",
        }
    # ======================================== 提示词 ========================================
    AGENT_MAP = \
        {
            "main—agent"   : "main_agent",
            "sub-agent"     : "sub_agents"
        }
    
    PROMPT_DICT = \
        {
            "system_prompt": "system_prompt",
            "user_prompt": "user_prompt",
            "assistant_prompt": "assistant_prompt",
            "correct_sql": "correct_sql",
        }
    
    
# ======================================== shopkeeper ========================================
@dataclass
class ServiceConfig:
    name: str                                              # 服务名称
    version: str                                           # 服务版本
    description: str                                       # 服务描述
    host: str                                              # 服务地址
    port: int                                              # 服务端口


# 控制台日志配置类
@dataclass
class ConsoleConfig:
    enable: bool                                           # 是否启用控制台日志
    level: int                                             # 日志级别


# 文件日志配置类
@dataclass
class FileConfig:
    enable: bool                                           # 是否启用文件日志
    level: int                                             # 日志级别
    path: str                                              # 日志路径
    log_name: str                                          # 日志名称
    rotation: str                                          # 日志轮转时间
    retention: str                                         # 日志保留时间
    
    
# 日志配置
@dataclass
class LogConfig:
    level_dict: dict[str, int]                             # 日志级别
    pattern: str
    file: FileConfig
    console: ConsoleConfig


# Mysql 配置类
@dataclass
class MysqlConfig:
    protocol: str                                          # 连接协议
    host: str                                              # 数据库地址
    port: int                                              # 数据库端口
    user: str                                              # 数据库用户名
    password: str                                          # 密码
    database: str                                          # 数据库名称
    charset: str                                           # 字符集
    timeout: int                                           # 连接超时时间
    max_connection: int                                    # 最大连接数
    auto_flush: bool                                       # 是否自动刷新
    auto_commit: bool                                      # 是否自动提交
    print_sql: bool                                        # 是否打印 SQL


# 云模型
@dataclass
class ModelConfig:
    url: str                                               # 模型地址
    api_key: str                                           # API 密钥
    name: str                                              # 模型名称
    timeout: int                                           # 超时时间
    max_retrie: int                                        # 最大重试次数
    temperature: int                                       # 模型服务温度
    max_token: int                                         # 模型服务最大 tokens


# 云模型配置类
@dataclass
class TavilyConfig:
    base_url: str                                          # 基础 URL
    api_key: str                                           # API 密钥
    search_depth: str                                      # 搜索深度
    include_answer: bool                                   # 包含答案的类型
    topic: str                                             # 搜索主题
    max_results: int                                       # 最大结果数
    include_raw_content: bool                              # 是否包含原始内容


# RagFlow 配置类
@dataclass
class RagFlowConfig:
    base_url: str                                          # 基础 URL
    api_key: str                                           # API 密钥
    knowledge_base: str                                    # 知识库名称
    knowledge_description: str                             # 知识库描述
    embedding: str                                         # 嵌入模型
    assistant_name: str                                    # 助手名称
    session_name: str                                      # 会话名称
    is_stream: bool                                        # 是否流式输出


@dataclass
class AppConfig:
    service_config: ServiceConfig                          # 服务配置
    log_config: LogConfig                                  # 日志配置
    mysql_config: MysqlConfig                              # 数据库配置
    model_config: ModelConfig                              # 模型配置
    tavily_config: TavilyConfig                            # 云模型配置
    ragflow_config: RagFlowConfig                          # RagFlow 配置


# ========================================= 绑定配置类 ========================================
_T = TypeVar("_T")                                         # 类型变量


# 加载配置文件
def load_config(config_file: str, schema_cls: Type[_T]) -> _T:
    context = OmegaConf.load(file_=config_file)            # 加载配置文件
    schema = OmegaConf.structured(obj=schema_cls)          # 结构化配置
    config = OmegaConf.merge(schema, context)              # 合并配置
    config: _T = OmegaConf.to_object(cfg=config)           # 转换为对象
    return config


app_config: AppConfig = load_config(config_file=PathConfig.APP_CONF_PATH, schema_cls=AppConfig)


if __name__ == '__main__':
    print(f"app_config: {app_config}")
    
