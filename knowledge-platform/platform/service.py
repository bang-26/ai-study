#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  service 
    CreateTime     ：  2026-07-20 20:54:42 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from collections.abc import AsyncGenerator
from re import sub

from agents import Runner, RunConfig, RunResultStreaming, ToolCallItem
from openai.types.realtime import ResponseTextDeltaEvent
from openai.types.responses import ResponseReasoningTextDeltaEvent, ResponseReasoningSummaryTextDeltaEvent

from config import PathConfig, DataDict
from logger import logger
from entry import ChatMessageRequest, UserSessionsResponse, UserSessionsRequest, ContentKind
from repository import SessionRepository
from tools import comprehensive_agent
from utils import ResponseFactory

session_repo = SessionRepository(storage_path=PathConfig.STORAGE_PATH)


# 流式服务类
class StreamService:
    @classmethod
    async def process_task(cls, chat_message: ChatMessageRequest) -> AsyncGenerator:
        logger.info(f"{chat_message}")
        
        # 1. 获取请求上下文的属性
        user_id = chat_message.context.user_id
        session_id = chat_message.context.session_id
        user_query = chat_message.query
        flag = chat_message.flag
        logger.info(f"用户 {user_id}-{session_id} 发送的待处理任务 {user_query}")
        
        # 2. 获取用户会话列表
        session_list = SessionService.process_session(user_id=user_id, session_id=session_id, user_input=user_query)
        
        # 3. 运行 Agent
        run_config = RunConfig(tracing_disabled=True)
        try:
            streaming_result = Runner.run_streamed(starting_agent=comprehensive_agent, input=session_list,
                                                   context=user_query, max_turns=5, run_config=run_config)
            
            # 4. 处理Agent的事件流（事件流）
            async for chunk in cls.process_stream_response(streaming_result=streaming_result):
                yield chunk
             
            # 5. 获取 Agent 的结果
            agent_result = streaming_result.final_output
            format_agent_result = sub(r'\n+', '\n', agent_result)
            
            # 6. 存储历史对话
            session_list.append({"role": "assistant", "content": format_agent_result})
            session_repo.save_session(user_id=user_id, session_id=session_id, data=session_list)
        except Exception as e:
            # 7. 捕获运行时错误，记录日志并返回错误标识
            logger.error(f"运行用户 {user_id}-{session_id} 的任务时出错: {e}")
            
            text = f"❌ 系统错误: {e}"
            kind = ContentKind.PROCESS
            yield "data: " + ResponseFactory.build_text(text=text, kind=kind).model_dump_json() + "\n\n"
            
            # 8. 返回错误标识
            if flag:
                text = f"🔄 正在尝试自动重试..."
                yield "data: " + ResponseFactory.build_text(text=text, kind=kind).model_dump_json() + "\n\n"
                
                # 递归调用进行重试
                chat_message.flag = False
                async for item in cls.process_task(chat_message=chat_message):
                    yield item
    
    # 处理 Agent 流式的事假
    @classmethod
    async def process_stream_response(cls, streaming_result: RunResultStreaming) -> AsyncGenerator:
        async for event in streaming_result.stream_events():
            # ------------------------------------------------------------------
            # 1. 文本与推理生成事件 (Text & Reasoning)
            # ------------------------------------------------------------------
            
            if event.type == "raw_response_event":
                # 1.1 常规文本输出 → ANSWER
                if isinstance(event.data, ResponseTextDeltaEvent):
                    delta_text = event.data.delta
                    data = ResponseFactory.build_text(delta_text, ContentKind.ANSWER).model_dump_json()
                    yield f"data: {data}\n\n"
                
                # 1.2 推理过程输出 → THINKING
                elif ResponseReasoningTextDeltaEvent and isinstance(event.data, ResponseReasoningTextDeltaEvent):
                    if event.data.delta:
                        data = ResponseFactory.build_text(event.data.delta, ContentKind.THINKING).model_dump_json()
                        yield f"data: {data}\n\n"
                
                # 1.3 推理摘要 → THINKING
                elif isinstance(event.data, ResponseReasoningSummaryTextDeltaEvent):
                    if event.data.delta:
                        data = ResponseFactory.build_text(event.data.delta, ContentKind.THINKING).model_dump_json()
                        
                        yield f"data: {data}\n\n"
            
            # ------------------------------------------------------------------
            # 2. 工具调用事件 (Tool Call)
            # ------------------------------------------------------------------
            elif event.type == "run_item_stream_event":
                if hasattr(event, "name") and event.name == "tool_called":
                    if isinstance(event.item, ToolCallItem) and event.item.type == "tool_call_item":
                        tool_name = event.item.raw_item.name
                        
                        text = DataDict.DISPLAY_NAME_TEMPLATE  % DataDict.TOOL_NAME_MAPPING.get(tool_name, tool_name)
                        data = ResponseFactory.build_text(text, ContentKind.PROCESS).model_dump_json()
                        
                        yield f"data: {data}\n\n"
            
            # ------------------------------------------------------------------
            # 3. 智能体状态更新
            # ------------------------------------------------------------------
            elif event.type == "agent_updated_stream_event":
                new_agent_name = event.new_agent.name
                
                text = DataDict.AGENT_NAME_TEMPLATE % DataDict.TOOL_NAME_MAPPING.get(new_agent_name, new_agent_name)
                data = ResponseFactory.build_text(text, ContentKind.PROCESS).model_dump_json()
                yield f"data: {data}\n\n"
            
            # ------------------------------------------------------------------
            # 4. 发送结束信号
            # ------------------------------------------------------------------
        yield "data: " + ResponseFactory.build_finish().model_dump_json() + "\n\n"
    

# 会话服务
class SessionService:
    DEFAULT_SESSION_ID = "default"
    SYSTEM_PROMPT = "你是一个有记忆的智能助手，请基于上下文历史会话用户问题 (会话ID %s)"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    
    # 获取用户会话列表
    @classmethod
    def get_user_sessions(cls, user_id: str) -> UserSessionsResponse:
        result = UserSessionsResponse(user_id=user_id)               # 初始化返回数据
        
        # 1. 加载历史会话
        history_list = session_repo.get_all_session(user_id=user_id)
        if not history_list:
            logger.warning(f"用户 {user_id} 没有会话数据")

        try:
            session_list = []
            for session_id, create_time, session_data in history_list:
                sessions = [data for data in session_data if data["role"] != "system"]
                
                session_dict = \
                    {
                        "session_id"    : session_id,
                        "create_time"   : create_time,
                        "session_data"  : sessions,
                        "total_messages": len(sessions)
                    }
                session_list.append(session_dict)
             
            result.success = True
            result.total_sessions = len(session_list)
            result.sessions = session_list
            logger.info(f"获取用户 {user_id} 的所有会话记忆数据")
        except Exception as e:
            # 5. 异常处理：捕获服务层抛出的未知错误，记录日志并返回错误标识
            logger.error(f"获取用户 {user_id} 的会话数据时出错: {e}")
            result.error = str(e)
        finally:
            return result
    
    # 处理会话
    @classmethod
    def process_session(cls, user_id: str, session_id: str, user_input: str, limit: int = 3) -> list[dict[str, any]]:
        # 1. 加载系统历史会话
        system_list= session_repo.get_role_session(user_id=user_id, session_id=session_id, role=cls.SYSTEM)
        assistant_list = session_repo.get_role_session(user_id=user_id, session_id=session_id,
                                                       role=cls.ASSISTANT, limit=limit)
        user_list = session_repo.get_role_session(user_id=user_id, session_id=session_id,
                                                  role=cls.USER, limit=limit)
        
        # 2. 拼接会话数据
        session_list = system_list[:]
        for i in range(len(user_list)):
            session_list.append(assistant_list[i])
            session_list.append(user_list[i])
        
        # 3. 判断历史会话是否为空
        if not session_list:
            logger.warning(f"用户 {user_id} 没有会话数据")
            
            system_prompt = cls.SYSTEM_PROMPT % cls.DEFAULT_SESSION_ID
            system_session = {"role": "system", "content": system_prompt}
            session_list.append(system_session)
        
        # 3. 拼接用户新消息
        session_list.append({"role": "user", "content": user_input})
        return session_list
        

if __name__ == '__main__':
    from json import dumps
    
    # user_sessions = SessionService.get_user_sessions(user_id="alice")
    # user_session = dumps(obj=dict(user_sessions), indent=4, ensure_ascii=False)
    # print(user_session)
    #
    # print("=" * 100)
    #
    # session_list = SessionService.process_session(user_id="toms", session_id="default", user_input="你好")
    # sessions = dumps(obj=session_list, indent=4, ensure_ascii=False)
    # print(sessions)
    #
    # session_list.append({"role": "assistant", "content": "你好，我是一个智能助手"})
    # SessionService.save_session(user_id="test", session_id="default", session_list=session_list)
    
