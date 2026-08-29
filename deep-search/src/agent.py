#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  agent 
    CreateTime     ：  2026-08-09 20:30:01 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Optional
from deepagents import create_deep_agent
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph

from config import PathConfig
from context import context
from logger import logger
from monitor import monitor_service
from tool import read_file_content, generate_markdown, convert_md_to_pdf, internet_search, list_sql_tables
from tool import get_table_data, execute_sql_query, get_assistant_list, create_ask_delete
from util import YamlUtil, FileUtil


# 深度搜索 Agent
class DeepSearchAgent:
    def __init__(self, path: str, agent_tool_dict: dict, model: BaseChatModel) -> None:
        self.path = path
        self.agent_tool_dict = agent_tool_dict
        self.model = model
        
        self.main_agent_content: Optional[dict] = None
        self.sub_agents_content: Optional[dict[str, str]] = None
    
    # 获取提示词
    def __get_prompt(self) -> None:
        content = YamlUtil.load_yaml(file_path=self.path)
        self.main_agent_content = content.get("main_agent", "")
        self.sub_agents_content = content.get("sub_agents", {})
    
    # 创建子 Agent
    def __create_subagent(self, agent_name: str, agent_tools: list) -> dict:
        if self.sub_agents_content is None:
            self.__get_prompt()
        
        agent = self.sub_agents_content.get(agent_name, {})
        agent["tools"] = agent_tools
        
        return agent
    
    # 创建所有子 Agent
    def create_subagent_list(self) -> list:
        subagent_list = []
        
        for agent_name, agent_tools in self.agent_tool_dict.items():
            if agent_name == "main":                       # main 的工具属于主代理自身，不是子代理，跳过
                continue
            
            subagent = self.__create_subagent(agent_name, agent_tools)
            subagent_list.append(subagent)
        
        logger.info(f"subagent_list = {self.agent_tool_dict.keys()}")
        return subagent_list
    
    # 创建主 Agent
    def create_main_agent(self) -> CompiledStateGraph:
        if self.main_agent_content is None:
            self.__get_prompt()
        
        system_prompt = self.main_agent_content.get("system_prompt")
        tool_list = self.agent_tool_dict.get("main")
        
        subagent_list = self.create_subagent_list()
        checkpointer = InMemorySaver()
        
        main_agent = create_deep_agent(model=self.model, system_prompt=system_prompt, tools=tool_list,
                                       checkpointer=checkpointer, subagents=subagent_list)
        
        logger.info(f"main_agent = {main_agent.get_graph()}")
        return main_agent
    
    def __update_file(self, session_dir: str, session_id: str) -> list[str]:
        
        FileUtil.ensure_dir_exists(file_path=session_dir)
        
        updated_dir_path = f"{PathConfig.UPDATE_DIR}/session_{session_id}"
        file_list = FileUtil.get_all_files(dir_path=updated_dir_path)
        
        for file in file_list:
            dst_path = f"{session_dir}/{file.name}"
            FileUtil.copy_file(src_path=file, dst_path=dst_path)
            
        # 当前会话对应的文件夹地址推送给起前端！
        monitor_service.report_session_dir(path=session_dir)
        return file_list
    
    async def __get_agent_result(self, config: dict[str, dict], message_list: list[dict[str, str]]):
        main_agent = self.create_main_agent()
        
        response = main_agent.astream(input={"messages": message_list}, config=config)
        async for chunk in response:
            for node_name, state in chunk.items():
                if not state or "message" not in state:
                    continue
                
                message = state.get("message")
                if message and isinstance(message, list):
                    last_message = message[-1]
                    
                    if node_name == "model":
                        tool_call_list = last_message.tool_calls
                        if tool_call_list:
                            for tool_call in tool_call_list:
                                """
                                tool_call = {
                                    name: task
                                    args:{
                                        subagent_type:子智能体的名字
                                        description:子智能体的描述
                                    }
                                }
                                """
                                if tool_call['name'] == 'task':
                                    # 调用某个子智能体
                                    monitor_service.report_assistant(assistant_name=tool_call['args']['subagent_type'],
                                                                     args=tool_call['args']['description'])
                    elif last_message.content:
                        # 最终结果
                        logger.info(f"主智能体执行结果，最终结果：{last_message.content[:100]}")
                        monitor_service.report_task_result(result=last_message.content)
        
    # 运行 Agent
    async def run_agent(self, task_query: str, session_id: str) -> None:
        logger.info(f"当前会话的 main_agent 开始执行了！ 会话id:{session_id}")
        
        session_dir = f"{PathConfig.OUTPUT_DIR}/session_{session_id}"
        
        # 先存储上下文，再加载文件，保证 session_created 等事件能定向推送
        dir_token = context.set_session_context(path=session_dir)
        id_token = context.set_thread_context(thread_id=session_id)
        
        file_list = self.__update_file(session_dir=session_dir, session_id=session_id)
        
        relative_dir = FileUtil.get_file_name(file_path=PathConfig.OUTPUT_DIR)
        relative_session_dir = f"{relative_dir}/{session_dir}"
        
        updated_info_prompt = (f"\n    [已上传文件] 已加载到工作目录:\n" +
                               "\n".join([f"    - {f}" for f in file_list]) +
                               "\n    请优先使用工具（read_file_content）读取并参考这些文件。")
        path_instruction = f"【工作环境指令】\n工作目录: {relative_session_dir}\n{updated_info_prompt}"
        
        message_list = [{"role": "user", "content": task_query + path_instruction}]
        config = {"configurable": {"thread_id": session_id}}
        try:
            await self.__get_agent_result(config=config, message_list=message_list)
        except Exception as e:
            monitor_service.report_error(message=str(e))
            logger.error(f"运行 Agent 出错: {e}")
        finally:
            # 释放存储的地址和 session_id
            context.reset_session_context(dir_token, id_token)
        
        
if __name__ == '__main__':
    from asyncio import create_task, run
    from connect import cloud_model_connect
    
    async def test():
        agent_tool_dict = \
            {
                "main"   : [generate_markdown, convert_md_to_pdf, read_file_content],
                "tavily" : [internet_search],
                "ragflow": [get_assistant_list, create_ask_delete],
                "db"     : [list_sql_tables, get_table_data, execute_sql_query]
            }
            
        agent = DeepSearchAgent(path=PathConfig.PROMPT_PATH, agent_tool_dict=agent_tool_dict,
                                model=cloud_model_connect.llm)
        
        await create_task(agent.run_agent(task_query="如何安装空调", session_id="1234567890"))
    
    run(test())
