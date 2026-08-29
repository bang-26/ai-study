#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill
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
from typing import TypeVar, Type, Optional
from dataclasses import dataclass
from omegaconf import OmegaConf


# 路径配置类
class PathConfig:
    # ============================== 基本路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                   # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                    # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")        # 项目路径
    
    # ============================== 配置路径 ==============================
    APP_CONF_PATH = abspath(path=f"{PROJECT_DIR}/conf/shopkeeper.yml")    # 配置文件路径
    META_DB_CONF_PATH = abspath(path=f"{PROJECT_DIR}/conf/meta-db.yml")   # 元数据库配置文件路径
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")                         # 日志路径
    
    PROMPT_PATH = abspath(path=f"{PROJECT_DIR}/data/shopkeeper.prompt")   # 提示词路径
    SQL_PATH = abspath(path=f"{PROJECT_DIR}/data/shopkeeper.sql")         # SQL 模板路径


# 数据字典
class DataDict:
    # ======================================== 所示 ========================================
    KNOWLEDGE_BASE_URL = "http://127.0.0.1:8001"           # 知识库地址
    
    GET_COLUMNS_KEY = "get_columns"                        # 从表里面查询该表的字段
    GET_COLUMN_VALUES_KEY = "get_column_values"            # 从表里面查询该字段的所有值
    
    # 词性配置
    ALLOW_POS = (
        "n",                 # 名词: 数据、服务器、表格
        "nr",                # 人名: 张三、李四
        "ns",                # 地名: 北京、上海
        "nt",                # 机构团体名: 政府、学校、某公司
        "nz",                # 其他专有名词: Unicode、哈希算法、诺贝尔奖
        "v",                 # 动词: 运行、开发
        "vn",                # 名动词: 工作、研究
        "a",                 # 形容词: 美丽、快速
        "an",                # 名形词: 难度、合法性、复杂度
        "eng",               # 英文
        "i",                 # 成语
        "l",                 # 常用固定短语
    )
    
    # ======================================== 提示词 ========================================
    PROMPT_DICT = \
        {
            "correct-sql": "correct-sql",
            "generate-sql": "generate-sql",
            "plan-sql": "plan-sql",
            "column-recall": "extend-keywords-for-column-recall",
            "metric-recall": "extend-keywords-for-metric-recall",
            "value-recall": "extend-keywords-for-value-recall",
            "filter-metric": "filter-metric-info",
            "filter-table": "filter-table-info",
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
    pool_size: int                                         # 连接池大小
    auto_flush: bool                                       # 是否自动刷新
    auto_commit: bool                                      # 是否自动提交
    auto_begin: bool                                       # 是否自动开始
    expire_on_commit: bool                                 # 是否在提交时过期
    print_sql: bool                                        # 是否打印 SQL


# Mysql 配置类
@dataclass
class WarehouseConfig(MysqlConfig):
    pass


# QDrantConfig 配置类
@dataclass
class QDrantConfig:
    protocol: str                                          # 连接协议
    host: str                                              # 连接地址
    port: int                                              # 连接端口
    user: str                                              # 用户名
    password: str                                          # 密码
    collection_name: str                                   # 集合名称
    dimension: int                                         # 向量大小
    similarity: str                                        # 相似度算法，可选值：Cosine, DotProduct, Euclidean
    time_out: int                                          # 超时时间
    pool_size: int                                         # 最大连接数
    score: float                                           # 搜索分数
    

# ElasticSearch 配置类
@dataclass
class ElasticSearchConfig:
    protocol: str                                          # 连接协议
    host: str                                              # 连接地址
    port: int                                              # 连接端口
    user: str                                              # 用户名
    api_key: str                                           # 密码
    mapping: str                                          # 文档名称
    index: str                                             # 索引名称
    time_out: int                                          # 超时时间
    max_connections: int                                   # 最大连接数


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


# 嵌入模型配置
@dataclass
class EmbeddingConfig:
    url: str                                               # 模型地址
    api_key: str                                           # api 密钥
    name: str                                              # 模型名称
    path: str                                              # 模型路径
    dimension: int                                         # 嵌入维度
    time_out: int                                          # 超时时间
    max_retry: int                                         # 最大重试次数
    

@dataclass
class AppConfig:
    service_config: ServiceConfig                         # 服务配置
    log_config: LogConfig                                 # 日志配置
    mysql_config: MysqlConfig                             # 数据库配置
    warehouse_config: WarehouseConfig                     # 数据仓库库配置
    qdrant_column_config: QDrantConfig                    # QDrant 配置
    qdrant_metric_config: QDrantConfig                    # QDrant 配置
    elasticsearch_config: ElasticSearchConfig             # ElasticSearch 配置
    model_config: ModelConfig                             # 模型配置
    embedding_config: EmbeddingConfig                     # 嵌入模型配置
    

# ========================================= meta-db ==========================================
# 表列配置类
@dataclass
class ColumnConfig:
    name: str                                              # 列名称
    role: str                                              # 列类型设置
    description: str                                       # 列注释说明
    alias: list[str]                                       # 列别名
    sync: bool                                             # 是否同步


# 数据表配置类
@dataclass
class TableConfig:
    name: str                                              # 表名称
    role: str                                              # 表设置类型
    description: str                                       # 表注释说明
    columns: list[ColumnConfig]                            # 表列配置


# 指标配置类
@dataclass
class MetricConfig:
    name: str                                              # 指标名称
    description: str                                       # 描述
    relevant_columns: list[str]                            # 关联列
    alias: list[str]                                       # 别名


# 元数据配置类
@dataclass
class MetaConfig:
    tables: Optional[list[TableConfig]] = None             # 数据表配置
    metrics: Optional[list[MetricConfig]] = None           # 指标配置
    

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
    meta_config = load_config(config_file=PathConfig.META_DB_CONF_PATH, schema_cls=MetaConfig)
    
    print(f"app_config: {app_config}")
    print(f"qdrant_column_config: {app_config.qdrant_column_config.collection_name}")
    print(f"qdrant_metric_config: {app_config.qdrant_metric_config.collection_name}")
    
    print(f"tables: {meta_config.tables}")
    print(f"metrics: {meta_config.metrics}")
