#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
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


# 路径配置类
class PathConfig:
    # ============================== 基本路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                              # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    
    # ============================== 数据路径 ==============================
    LOG_PATH = abspath(path=f"{PROJECT_DIR}/logs")                   # 日志路径
    SQL_PATH = abspath(path=f"{PROJECT_DIR}/data/repair.sql")        # 原始数据路径
    PROMPT_PATH = abspath(path=f"{PROJECT_DIR}/data/prompt.txt")     # 提示语路径
    STORAGE_PATH = abspath(path=f"{PROJECT_DIR}/data/memory")        # 记忆存储


# 日志配置
class LogConfig:
    LOG_DEBUG_NAME = f"{PathConfig.LOG_PATH}/debug.log"              # 调试日志名称
    LOG_INFO_NAME = f"{PathConfig.LOG_PATH}/info.log"                # 信息日志名称
    LOG_WARN_NAME = f"{PathConfig.LOG_PATH}/warn.log"                # 警告日志名称
    LOG_ERROR_NAME = f"{PathConfig.LOG_PATH}/error.log"              # 错误日志名称
    
    LOG_NAME = "platform"                                            # 平台名称
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"                                # 时间格式
    FILE_FORMAT = "[%(asctime)s]-|-<%(levelname)s>-|-%(name)s/%(filename)s:%(lineno)d-|-{%(message)s}"
    CONSOLE_FORMAT = "[%(asctime)s]-|-<%(levelname)s>-|-%(name)s/%(filename)s:%(lineno)d-|-{%(message)s}"
    
    LEVEL_DICT = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40, "FATAL": 50}    # 日志级别
    CONSOLE_LEVEL = LEVEL_DICT.get("INFO")                           # 控制台级别
    FILE_LEVEL = LEVEL_DICT.get("INFO")                              # 文件级别
    
    
# Mysql 配置类
class MysqlConfig:
    PROTOCOL = "mysql+pymysql"                                       # 连接协议
    HOST = "****************"                                        # 数据库地址
    PORT = 3306                                                      # 数据库端口
    USER = "****************"                                        # 数据库用户名
    PASSWORD = "****************"                                    # 密码
    DATABASE = "test"                                                # 数据库名称
    CHARSET = "utf8mb4"                                              # 字符集
    TIME_OUT = 10                                                    # 超时时间
    MAX_CONNECTIONS = 10                                             # 最大连接数
    PRINT_SQL = False                                                # 是否打印 SQL


# 阿里百炼
class BaiLianConfig:
    URL = "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" # 调用访问地址
    API_KEY = "****************"
    NAME = "大模型联网搜索"                                            # 名称
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}                 # 鉴权
    TOOL_NAME = "bailian_web_search"                                 # 使用工具
    CACHE_TOOL_LIST = True                                           # 缓存工具列表
    TIMEOUT = 30                                                     # 超时时间
    

# 百度
class BaiDuConfig:
    URL = "https://mcp.map.baidu.com/sse"                            # 调用访问地址
    API_KEY = "****************"                                     # API Key
    TOOL_NAME_LIST = ["map_geocode", "map_ip_location", "map_uri"]   # 使用工具链
    NAME = "百度地图定位"                                             # 名称
    CACHE_TOOL_LIST = True                                           # 缓存工具列表
    TIMEOUT = 30                                                     # 超时时间


# 云模型
class ModelConfig:
    URL = "https://llm-t8pcm3a7gt9om5i5.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    API_KEY = "****************"
    MODEL_NAME = ""                                                  # 模型名称
    TIMEOUT = 60                                                     # 超时时间
    MAX_RETRIE = 3                                                   # 最大重试次数
    TEMPERATURE = 0                                                  # 模型服务温度
    MAX_TOKEN = 10240                                                # 模型服务最大 tokens


# 主模型配置类
class MainModelConfig(ModelConfig):
    MODEL_NAME = "qwen3.7-max"                                       # 模型名称


# 子模型配置类
class SubModelConfig(ModelConfig):
    MODEL_NAME = "qwen3.7-plus"                                       # 模型名称


# 智能体配置类
class BaseAgentConfig:
    NAME= ""                                                         # 智能体名称
    PROMPT_KEY = ""                                                  # 提示词
    PROMPT_PATH = PathConfig.PROMPT_PATH                             # 提示词文件
    TEMPERATURE = 0                                                  # 模型温度
    MAX_TOKEN = 2048                                                 # 最大 token


# 主调度智能体
class OrchestratorAgentConfig(BaseAgentConfig):
    NAME = "主调度智能体"                                              # 智能体名称
    PROMPT_KEY = "orchestrator-agent"                                # 提示词


# 技术智能体
class TechnicalAgentConfig(BaseAgentConfig):
    NAME= "资讯与技术专家"                                             # 智能体名称
    PROMPT_KEY = "technical-agent"                                   # 提示词
    

# 全能业务智能体
class ComprehensiveAgentConfig(BaseAgentConfig):
    NAME = "全能业务智能体"                                            # 智能体名称
    PROMPT_KEY = "comprehensive-agent"                               # 提示词
    

# 数据字典
class DataDict:
    # ======================================== 所示 ========================================
    KNOWLEDGE_BASE_URL = "http://127.0.0.1:8001"                     # 知识库地址
    
    SQL_KEY = "get_repair"                                           # 获取查询 sql 的 key
    
    TOOL_NAME_MAPPING = \
        {
            # 搜索MCP工具
            "bailian_web_search"                  : "联网搜索",
            "search_mcp"                          : "联网搜索",
            
            # 百度地图MCP工具
            "map_geocode"                         : "地址解析",
            "map_ip_location"                     : "IP定位",
            "map_search_places"                   : "地点搜索",
            "map_uri"                             : "生成导航链接",
            "baidu_map_mcp"                       : "百度地图查询",
            
            # 本地工具
            "query_knowledge"                     : "查询知识库",
            "resolve_user_location_from_text"     : "位置解析",
            "query_nearest_repair_shops_by_coords": "查询附近服务站",
            "geocode_address"                     : "地址转坐标",
            
            # 新架构：Agent Tools
            "consult_technical_expert"            : "咨询技术专家",
            "query_service_station_and_navigate"  : "服务站与地理位置专家",
        }
    
    DISPLAY_NAME_TEMPLATE = """
        <div class="tech-process-card tool-call">
            <div class="tech-process-header">
                <span class="tech-icon">🔄</span>
                <span class="tech-label">正在调用工具</span>
            </div>
            <div class="tech-process-flow">
                <span class="tech-node source">调度中心</span>
                <span class="tech-arrow">➔</span>
                <span class="tech-node target">%s</span>
            </div>
        </div>
    """
    
    AGENT_NAME_TEMPLATE = """
        <div class="tech-process-card agent-update">
            <div class="tech-process-header">
                <span class="tech-icon">🤖</span>
                <span class="tech-label">智能体切换</span>
            </div>
            <div class="tech-process-body">
                <span class="tech-text">当前接管: <strong class="highlight">%s</strong></span>
            </div>
        </div>
    """
    
    ROLE_DICT = {0: "user", 1: "assistant", 2: "system", 3: "tool", }
    
