#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge
    FileName       ：  config
    CreateTime     ：  2026-08-12 15:51:19
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
    APP_CONF_PATH = abspath(path=f"{PROJECT_DIR}/data/application.yml")   # 配置文件路径
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")          # 日志路径
    WEB_DIR = abspath(path=f"{PROJECT_DIR}/static")        # 前端资源文件所在目录
    
    # ============================== 模型路径 ==============================
    PROMPT_PATH = abspath(path=f"{PROJECT_DIR}/data/prompt.txt")     # 提示词路径
    UPDATE_DIR = abspath(path=f"{PROJECT_DIR}/data/update")          # 更新目录
    OUTPUT_DIR = abspath(path=f"{PROJECT_DIR}/data/output")          # 输出目录
    

# 数据字典
class DataDict:
    # ======================================== 所示 ========================================
    PROMPT_DICT = \
        {
            "answer-out"                : "answer-out",
            "hyde-prompt"               : "hyde-prompt",
            "image-summary"             : "image-summary",
            "item-name-recognition"     : "item-name-recognition",
            "product-recognition-system": "product-recognition-system",
            "rewritten-query-names"     : "rewritten-query-names",
        }
    
    DATE_FORMAT = "%Y%m%d"
    
    TASK_STATUS_PENDING = "pending"
    TASK_STATUS_PROCESSING = "processing"
    TASK_STATUS_COMPLETED = "completed"
    TASK_STATUS_FAILED = "failed"
    
    IMAGE_SUFFIX_LIST = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
    
    NODE_NAME_TO_CN = \
        {
            "upload_file"               : "开始上传文件",
            "node_entry"                : "检查文件",
            "node_pdf_to_md"            : "PDF转Markdown",
            "node_md_img"               : "Markdown图片处理",
            "node_item_name_recognition": "主体名称识别",
            "node_document_split"       : "文档切分",
            "node_bge_embedding"        : "向量生成",
            "node_import_kg"            : "导入知识图谱",
            "node_import_milvus"        : "导入向量库",
            "__end__"                   : "处理完成",
            "END"                       : "处理完成",
            "node_item_name_confirm"    : "确认问题产品",
            "node_answer_output"        : "生成答案",
            "node_rerank"               : "重排序",
            "node_rrf"                  : "倒排融合",
            "node_web_search_mcp"       : "网络搜索",
            "node_search_embedding"     : "切片搜索",
            "node_search_embedding_hyde": "切片搜索(假设性文档)",
            "node_multi_search"         : "多路搜索",
            "node_query_kg"             : "查询知识图谱",
            "node_join"                 : "多路搜索合并",
        }
    
    MIN_CONTENT_LENGTH = 512
    MAX_CONTENT_LENGTH = 2048
    OVERLAP_SIZE = 128
    
    CHUNK_TOP = 5
    CONTEXT_MAX = 2560
    
    RERANK_MAX_TOPK = 10                                   # 动态 TopK 硬上限：最多取前 N 条（<=10）
    RERANK_MIN_TOPK = 1                                    # 最小 TopK：至少保留前 N 条（>=1，且 <= RERANK_MAX_TOPK）
    RERANK_GAP_RATIO = 0.25                                # 断崖阈值（相对）
    RERANK_GAP_ABS = 0.5                                   # 最大间断分值
    _IMAGE_BLOCK_MARKER = "【图片】"
    MAX_CONTEXT_CHARS = 12000                              # 限制 prompt 的长度
    IMAGE_SUFFIX = (".png",".jpg",".jpeg",".gif",".webp")
    
    
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


@dataclass
class MineruConfig:
    upload_url: str                                        # 文件上传地址
    download_url: str                                      # 文件下载地址
    token: str                                             # 数据库端口
    model_version: str                                     # 模型版本
    poll_interval: int                                     # 两次请求的间隔
    timeout: int                                           # 连接超时时间


# MInIO 配置类
@dataclass
class MinioConfig:
  endpoint: str                                            # 链接地址
  is_secure: bool                                          # 是否使用 HTTPS
  access_key: str                                          # 用户名
  secret_key: str                                          # 密码
  bucket_name: str                                         # 使用的桶名
  image_folder: str                                        # 图片文件夹
  max_connection: int                                      # 最大连接数


# 云模型
@dataclass
class CloudModelConfig:
    url: str                                               # 模型地址
    api_key: str                                           # API 密钥
    name: str                                              # 模型名称
    timeout: int                                           # 超时时间
    max_retry: int                                         # 最大重试次数
    temperature: int                                       # 模型服务温度
    max_token: int                                         # 模型服务最大 tokens
    enable_thinking: bool                                  # 是否开启思考模式


# 嵌入模型配置类
@dataclass
class EmbedModelConfig:
    model_path: str                                        # 模型路径
    device: str                                            # 使用的设备
    enable_fp16: bool                                      # 是否启用 FP16
    dimension: int                                         # 向量维度


# 嵌入模型配置类
@dataclass
class RerankModelConfig:
    model_path: str                                        # 模型路径
    device: str                                            # 使用的设备
    enable_fp16: bool                                      # 是否启用 FP16
    dimension: int                                         # 向量维度


# 视觉模型配置类（图片摘要等视觉任务使用，需支持 image_url 多模态输入）
@dataclass
class MilvusConfig:
    url: str                                               # 连接地址
    collection_name: str                                   # 集合名称
    auto_id: bool                                          # 是否自增
    enable_dynamic_field: bool                             # 是否启用动态字段
    
    entity_name: str                                       # 实体名称集合
    item_name: str                                         # 存储文档对应实体类的集合名称
    dimension: int                                         # 向量维度
    metric_type: str                                       # 度量类型
    index_type: str                                        # 索引类型
    index_param: dict[str, str]                            # 索引参数
    search_param: dict[str, str]                           # 搜索参数
    timeout: int                                           # 超时时间
    
    
# Mysql 配置类
@dataclass
class MongoDBConfig:
    protocol: str                                          # 连接协议
    host: str                                              # 数据库地址
    port: int                                              # 数据库端口
    user: str                                              # 数据库用户名
    password: str                                          # 密码
    database: str                                          # 数据库名称
    collection: str                                        # 集合名称


@dataclass
class McpConfig:
    name: str                                              # MCP 名称
    url: str                                               # 连接地址
    api_key: str                                           # API 密钥
    count: int                                             # 模型数量
    tool: str                                              # 工具名称
    max_retry: int                                         # 最大重试次数
    timeout: int                                           # 超时时间


@dataclass
class AppConfig:
    mineru_config: MineruConfig                            # 文档转换配置
    service_config: ServiceConfig                          # 服务配置
    log_config: LogConfig                                  # 日志配置
    minio_config: MinioConfig                              # Minio 配置
    model_config: CloudModelConfig                         # 模型配置
    embed_config: EmbedModelConfig                         # 嵌入模型配置
    milvus_config: MilvusConfig                            # Milvus 配置
    mongo_config: MongoDBConfig                            # MongoDB 数据库配置
    mcp_config: McpConfig                                  # MCP 配置
    rerank_config: RerankModelConfig                       # 重排序模型配置


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
    
