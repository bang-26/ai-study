#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  statee 
    CreateTime     ：  2026-08-12 17:47:13 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from copy import deepcopy
from typing import TypedDict, List


# 图的状态定义，包含所有节点产生和消费的数据字段。
class ImportGraphState(TypedDict):
    task_id: str                                           # 任务唯一ID，用于追踪日志
    # --- 流程控制标记 ---
    is_md_read_enabled: bool                               # 是否启用 Markdown 读取路径
    is_pdf_read_enabled: bool                              # 是否启用 PDF 读取路径
    # --- 切块相关 --- 【没用】
    is_normal_split_enabled: bool                          # 是否开启标准化切割
    is_silicon_flow_api_enabled: bool                      # 是否启用硅流API切割
    is_advanced_split_enabled: bool                        # 是否启用高级切割
    is_vllm_enabled: bool                                  # 是否启用vLLM切割
    # --- 路径相关 ---
    local_dir: str                                         # 当前工作目录或输出目录
    local_file_path: str                                   # 原始输入文件路径
    file_title: str                                        # 文件标题（文件名去后缀）
    pdf_path: str                                          # PDF 文件路径 (如果输入是PDF)
    md_path: str                                           # Markdown 文件路径 (转换后或直接输入的)
    split_path: str                                        # 分块后的文件路径 【没用】
    embeddings_path: str                                   # 向量数据库文件路径【没用】
    # --- 内容数据 ---
    md_content: str                                        # Markdown 的全文内容
    chunks: list                                           # 切片后的文本列表，包含 metadata
    item_name: str                                         # 识别出的主体名称 (如: "万用表")，用于增强检索
    # --- 数据库相关 ---
    embeddings_content: list                               # 包含向量数据的列表，准备写入 Milvus


# 定义了整个查询流程中流转的数据结构。
class QueryGraphState(TypedDict):
    session_id: str                                        # 会话唯一标识
    original_query: str                                    # 用户原始问题
    embedding_chunks: list                                 # 普通向量检索回来的切片
    hyde_embedding_chunks: list                            # HyDE 检索回来的切片
    web_search_docs: list                                  # 网络搜索回来的文档
    rrf_chunks: list                                       # RRF 融合排序后的切片
    reranked_docs: list                                    # 重排序后的最终 Top-K 文档
    prompt: str                                            # 组装好的 Prompt
    answer: str                                            # 最终生成的答案
    item_names: List[str]                                  # 提取出的商品名称
    rewritten_query: str                                   # 改写后的问题
    history: list                                          # 历史对话记录
    is_stream: bool                                        # 是否流式输出标记


# 图状态初始化对象，方便后续使用
graph_default_state: ImportGraphState = \
    {
        "task_id"                    : "",
        "is_pdf_read_enabled"        : False,
        "is_md_read_enabled"         : False,
        "is_normal_split_enabled"    : True,
        "is_silicon_flow_api_enabled": True,
        "is_advanced_split_enabled"  : False,
        "is_vllm_enabled"            : False,
        "local_dir"                  : "",
        "local_file_path"            : "",
        "pdf_path"                   : "",
        "md_path"                    : "",
        "file_title"                 : "",
        "split_path"                 : "",
        "embeddings_path"            : "",
        "md_content"                 : "",
        "chunks"                     : [],
        "item_name"                  : "",
        "embeddings_content"         : []
    }


query_graph_default_state: QueryGraphState = \
    {
        "session_id"           : "",
        "original_query"       : "",
        "embedding_chunks"     : [],
        "hyde_embedding_chunks": [],
        "web_search_docs"      : [],
        "rrf_chunks"           : [],
        "reranked_docs"        : [],
        "prompt"               : "",
        "answer"               : "",
        "item_names"           : [],
        "rewritten_query"      : "",
        "history"              : [],
        "is_stream"            : False
    }


# 创建默认状态
def create_default_state(**over_ride_dict) -> ImportGraphState:
    """
    创建默认状态，支持覆盖

    Args:
        **over_ride_dict: 要覆盖的字段（关键字参数解包）

    Returns:
        新的状态实例

    Examples:
        state = create_default_state(task_id="task_001", local_file_path="doc.pdf")
    """
    
    state = deepcopy(x=graph_default_state)                          # 默认状态
    state.update(over_ride_dict)                                     # 用 overrides 覆盖默认值
    return state


# 返回一个新的状态实例，避免全局变量污染
def get_default_state() -> ImportGraphState:
    return deepcopy(x=graph_default_state)


# 创建查询流程的默认状态，支持覆盖字段
def create_query_default_state(**overrides) -> QueryGraphState:
    state = deepcopy(query_graph_default_state)
    state.update(overrides)
    return state


# 获取干净状态
def get_query_default_state() -> QueryGraphState:
    return deepcopy(query_graph_default_state)


# 复制现有状态并可覆盖字段，深拷贝，不污染原数据
def copy_query_state(state: QueryGraphState, **overrides) -> QueryGraphState:
    new_state = deepcopy(state)
    new_state.update(overrides)
    return new_state


if __name__ == "__main__":
    from logger import logger
    # 创建默认状态
    state = create_default_state(local_file_path="万用表RS-12的使用.pdf")
    logger.info(state)
