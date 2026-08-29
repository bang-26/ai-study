#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  entry 
    CreateTime     ：  2026-07-20 20:47:40 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from enum import Enum
from typing import Optional, Union, List, Literal
from pydantic import BaseModel, Field


# 用户上下文信息，用于标识请求来源
class UserContext(BaseModel):
    user_id: str                                                          # 当前用户的唯一标识
    session_id: Optional[str] = Field(description="会话ID", default=None)  # 可选的会话标识，用于多轮对话追踪


# 用户发起聊天请求的入参结构
class ChatMessageRequest(BaseModel):
    query: str                                             # 用户输入的查询文本
    context: UserContext                                   # 用户上下文信息
    flag: bool = True                                      # 预留标志位（当前默认为 True）


# 获取用户历史会话列表的请求体
class UserSessionsRequest(BaseModel):
    user_id: str = Field(description="用户唯一标识符")       # 用于查询该用户的所有会话记录


# 获取用户历史会话列表的响应体
class UserSessionsResponse(BaseModel):
    success: bool = Field(default=False, description="是否成功")
    user_id: str = Field(description="用户唯一标识符")       # 用户唯一标识符
    total_sessions: int = Field(default=0, description="该用户总共的会话数量")                                    # 该用户总共的会话数量
    sessions: List[dict] = Field(default=[], description="会话列表")     # 会话列表
    error: str = Field(default="", description="错误信息")  # 错误信息

# 内容语义分类：用于前端区分 UI 渲染逻辑
class ContentKind(str, Enum):
    THINKING = 'THINKING'                                  # 思考/推理内容 (渲染在折叠区域)
    PROCESS = 'PROCESS'                                    # 系统流程/工具调用 (渲染在折叠区域)
    ANSWER = 'ANSWER'                                      # 最终回答 (渲染在主聊天气泡)


# 流状态：控制 SSE 连接的生命周期
class StreamStatus(str, Enum):
    IN_PROGRESS = 'IN_PROGRESS'                            # 流传输中
    FINISHED = 'FINISHED'                                  # 传输结束


# 结束原因：仅当状态为 FINISHED 时有效
class StopReason(str, Enum):
    NORMAL = 'NORMAL'                                      # 正常结束
    MAX_TOKENS = 'MAX_TOKENS'                              # 达到长度限制
    ERROR = 'ERROR'                                        # 异常结束


# 消息体基类
class MessageBody(BaseModel):
    contentType: str                                       # 消息内容类型


# 文本消息体：承载具体的流式内容
class TextMessageBody(MessageBody):
    contentType: Literal['sagegpt/text'] = 'sagegpt/text' # 消息内容类型
    text: str = Field(default='', description="实际文本内容")
    kind: ContentKind = Field(..., description="内容分类：THINKING/PROCESS/ANSWER")


# 结束信号体：不包含内容，仅作为结束标志
class FinishMessageBody(MessageBody):
    contentType: Literal['sagegpt/finish'] = 'sagegpt/finish'


# 数据包元数据
class PacketMeta(BaseModel):
    createTime: str                                        # 创建时间
    finishReason: Optional[StopReason] = None              # 结束原因
    errorMessage: Optional[str] = None                     # 错误信息


# SSE 流数据包 (原 MessageResponse)：这是后端 yield 给前端的最小数据单元
class StreamPacket(BaseModel):
    id: str                                                # 数据包唯一标识符
    content: Union[TextMessageBody, FinishMessageBody]     # 消息体
    status: StreamStatus                                   # 流状态
    metadata: PacketMeta                                   # 数据包元数据


# 知识库返回的答案结构
class KnowledgeAnswer(BaseModel):
    answer: str                                            # 知识库返回的答案
    source: str = '知识库'                                  # 答案来源标识
    confidence: float = 0.9                                # 答案置信度


# 知识库返回的错误结构
class KnowledgeError(BaseModel):
    error: str                                              # 错误描述
    fallback: str = '请尝试重新提问或联系人工客服'             # 建议用户重新提问或联系人工客服
