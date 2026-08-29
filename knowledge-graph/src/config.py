#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph  
    FileName       ：  config 
    CreateTime     ：  2026-07-04 13:14:45 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os.path import dirname, abspath
from torch import float16, int32


# 路径配置类
class PathConfig:
    # ============================== 基本路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                              # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    
    # ============================== 数据路径 ==============================
    RAW_DATA_PATH = abspath(path=f"{PROJECT_DIR}/data/mark.json")    # 原始数据路径
    RAW_DATA_TYPE = RAW_DATA_PATH.split(".")[-1]                     # 原始数据类型
    PROCESSED_DATA_PATH = abspath(path=f"{PROJECT_DIR}/data")        # 处理后的数据路径
    
    TRAIN_PATH = abspath(path=f"{PROCESSED_DATA_PATH}/train")        # 训练数据路径
    TEST_PATH = abspath(path=f"{PROCESSED_DATA_PATH}/test")          # 测试数据路径
    VALID_PATH = abspath(path=f"{PROCESSED_DATA_PATH}/valid")        # 验证数据路径
    
    # ============================== 配置路径 ==============================
    BERT_MODEL = "google-bert/bert-base-chinese"                     # BERT 模型名称
    SAVED_MODEL_PATH = abspath(path=f"{PROJECT_DIR}/model")          # 模型保存路径
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")                    # 日志保存位置
    CHECK_POINT_DIR = abspath(path=f"{PROJECT_DIR}/check-point")     # 检查点保存位置

    
# 数据字段配置类
class FieldConfig:
    # ============================== 字段标识 ==============================
    TRAIN_FLAG = "train"                                             # 训练标志
    TEST_FLAG = "test"                                               # 测试标志
    VALID_FLAG = "valid"                                             # 验证标志
    CONTENT_FIELD = "text"                                           # 文本字段
    LABEL_FIELD = "label"                                            # 标签字段
    START_FIELD = "start"                                            # 开始字段
    END_FIELD = "end"                                                # 结束字段
    
    # ============================== 字段标识 ==============================
    RAW_REMOVE_COLUMNS = ["id", "annotator", "annotation_id", "created_at", "updated_at", "lead_time"]
    SAVE_REMOVE_COLUMNS = [CONTENT_FIELD, LABEL_FIELD]               # 保存字段
    
    START_FLAG = "B"                                                 # 开始
    MIDDLE_FLAG = "I"                                                # 中间
    OUT_FLAG = "O"                                                   # 外部
    LABELS = [START_FLAG, MIDDLE_FLAG, OUT_FLAG]                     # 标签
    MARK_LABEL = -100                                                # 标记标签
    
    TARGET_FIELD = "labels"                                          # 输出字段
    INPUT_ID_FIELD = "input_ids"                                     # 输入字段
    DATASET_FORMAT = "torch"                                         # 数据集格式
    MODEL_SUFFIX = "pt"                                              # 模型后缀
    
    # ============================== 字符编码 ==============================
    IS_TRUNCATION = True                                             # 是否截断
    IS_SPLIT_WORDS = True                                            # 是否拆分词
    MAX_LENGTH = 32                                                  # 最大长度


# 训练参数配置类
class TrainConfig:
    # ============================== 数据选择 ==============================
    TRAIN_SELECT_NUMBER = 0                                          # 训练数据选择数量
    VALID_SELECT_NUMBER = 0                                          # 验证数据选择数量
    TEST_SELECT_NUMBER = 0                                           # 测试数据选择数量
    
    # ============================== 数据类型 ==============================
    TORCH_FLOAT_TYPE = float16                                       # 浮点类型
    TORCH_INT_TYPE = int32                                           # 整数类型
    IS_AUTO_CAST = True                                              # 是否自动转换类型
    
    # ============================== 数据整理器 ==============================
    IS_PADDING = True                                                # 是否填充
    IS_TRUNCATION = FieldConfig.IS_TRUNCATION                        # 是否截断
    IS_SPLIT_WORDS = FieldConfig.IS_SPLIT_WORDS                      # 是否拆分词
    MAX_LENGTH = FieldConfig.MAX_LENGTH                              # 最大长度
    RETURN_TENSORS = "pt"                                            # 返回张量类型
    IS_RETURN_OFFSET_MAPPING = True
    
    # ============================== 训练超参数 ==============================
    BATCH_SIZE = 8                                                   # 批处理大小
    IS_SHUFFLE = True                                                # 是否打乱数据
    
    EPOCHS = 30                                                      # 训练轮数
    LEARNING_RATE = 1e-5                                             # 学习率
    SAVE_STEP = 10                                                   # 每批次保存
    SAVE_STRATEGY = "steps"                                          # 保存策略
    CHECK_POINT_COUNT = 3                                            # 检查点数量
    IS_FP16 = True                                                   # 是否使用混合精度训练
    EVAL_METRIC = "overall_f1"                                       # 评估指标
    GREATER_IS_BETTER = True                                         # 评估指标是否越大越好
    IS_BEST_MODEL = True                                             # 是否加载最佳模型
    EARLY_STOPPING_PATIENCE = 30                                     # 提前停止容忍度
    
    # ============================== 评估参数 ==============================
    SEQEVAL = "seqeval"                                              # 评估指标


# 预测参数配置类
class PredictConfig:
    # ============================== 分词配置 ==============================
    IS_SPLIT_WORDS = FieldConfig.IS_SPLIT_WORDS                      # 是否拆分词
    IS_PADDING = TrainConfig.IS_PADDING                              # 是否填充
    IS_TRUNCATION = FieldConfig.IS_TRUNCATION                        # 是否截断
    MAX_LENGTH = FieldConfig.MAX_LENGTH                              # 最大长度
    RETURN_OFFSET_MAPPING = True                                     # 是否返回偏移映射
    RETURN_TENSORS=TrainConfig.RETURN_TENSORS                        # 返回张量类型
    
    # ============================== 预测超参数 ==============================
    PREDICT_BATCH_SIZE = 256                                         # 预测批处理大小
    PREDICT_SEQ_LEN = 128                                            # 预测最大序列长度
    PREDICT_MAX_LENGTH = 32                                          # 预测生成最大长度
    PREDICT_NUM_BEAMS = 5                                            #


# Mysql 配置类
class MysqlConfig:
    HOST = "****************"                                        # 数据库地址
    PORT = 3306                                                      # 数据库端口
    USER = "****************"                                        # 数据库用户名
    PASSWORD = "****************"                                    # 密码
    DATABASE = "gmail"                                               # 数据库名称
    CHARSET = "utf8mb4"                                              # 字符集
    TIME_OUT = 10                                                    # 超时时间
    MAX_CONNECTIONS = 10                                             # 最大连接数


# Neo4J 配置类
class Neo4jConfig:
    PROTOCOL = "bolt"                                                # 连接协议
    HOST = "****************"                                        # 节点地址
    PORT = 7687                                                      # 端口
    USER = "****************"                                        # 用户名
    PASSWORD = "****************"                                    # 密码
    DATABASE = "neo4j"                                               # 密码
    TIME_OUT = 10                                                    # 超时
    MAX_CONNECTIONS = 10                                             # 最大连接数
    IS_AUTO_COMMIT = True                                            # 是否自动提交
    IS_READ_ONLY = False                                             # 是否只读
    BATCH_SIZE = 20                                                  # 批次大小


# Web 配置类
class WebConfig:
    APP_NAME = "web:app"                                             # 应用名称
    HOST = "0.0.0.0"                                                 # 监听地址
    PORT = 8000                                                      # 监听端口
    STATIC_DIR = "static"                                            # 静态文件目录
    STATIC_PATH = "/static"                                          # 静态文件路径
    STATIC_NAME = "static"                                           # 静态文件名称
    IS_DEBUG = True                                                  # 是否调试模式
    IS_RELOAD = True                                                 # 是否自动重载
    
    EMBED_MODEL = "BAAI/bge-large-zh-v1.5"                           # 嵌入模型名称
    ENCODE_KWARGS = { "normalize_embeddings": True }                 # 编码参数
    DEEP_SEEK_MODEL = "deepseek-chat"                                # 深度 seeking 模型名称
    API_KEY = "****************"                                     # API 密钥
    
    CYPHER_VARIABLES = ["question", "schema_info"]                   # 模板变量
    ANSWER_VARIABLES = ["question", "query_result"]                  # 回答变量
    
    CYPHER_TEMPLET = """
                你是一个专业的Neo4j Cypher查询生成器。你的任务是根据用户问题生成一条Cypher查询语句，用于从知识图谱中获取回答用户问题所需的信息。

                用户问题：{question}

                知识图谱结构信息：{schema_info}

                要求：
                1. 生成参数化Cypher查询语句，用param_0, param_1等代替具体值
                2. 识别需要对齐的实体
                3. 必须严格使用以下JSON格式输出结果
                {{
                  "cypher_query": "生成的Cypher语句",
                  "entities_to_align": [
                    {{
                      "param_name": "param_0",
                      "entity": "原始实体名称",
                      "label": "节点类型"
                    }}
                  ]
                }}"""
    ANSWER_TEMPLET = """你是一个电商智能客服，根据用户问题，以及数据库查询结果生成一段简洁、准确的自然语言回答。
                            用户问题: {question}
                            数据库返回结果: {query_result}
                     """
