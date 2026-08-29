#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  query_node 
    CreateTime     ：  2026-08-21 00:54:15 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from sys import _getframe

from connect import mongo
from process import ItemConfirmProcess, SearchProcess, MergeProcess, AnswerProcess
from state import QueryGraphState, create_query_default_state
from logger import logger
from util import task_util, sse_util


# 节点处理函数：item_name 确认
def node_item_name_confirm(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    # 1. 获取历史条件记录，并保存当前次的聊天记录
    condition = {"session_id": state.get("session_id")}
    chat_list = mongo.query_data(filter_condition=condition, limit=4)
    
    # 2. 利用模型 lm 重写提问内容：消除歧义，明确用户意图；补全上下文；去掉口语和冗余；润色问题，增加召回率
    original_query = state.get("original_query")
    rewrite_query_dict = ItemConfirmProcess.rewrite_query(original_query=original_query, chat_list=chat_list)
    logger.info(rewrite_query_dict)
    
    # 3. 进行 item_name 的向量数据库查询
    item_names = rewrite_query_dict.get("item_names", [])
    rewritten_query = rewrite_query_dict.get("rewritten_query")
    
    if len(item_names) > 0:
        query_result = ItemConfirmProcess.vector_query(item_names=item_names)
        
        # 4. 对 item_name 结果进行打分分类处理
        item_info_dict = ItemConfirmProcess.classify(query_info_list=query_result)
        
        # 5. 补充 state 状态
        state = ItemConfirmProcess.save_chat(state=state, item_info_dict=item_info_dict, chat_list=chat_list,
                                                 rewritten_query=rewritten_query)
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")
    return state
    

# 节点处理函数：搜索嵌入向量
def node_search_embedding(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    embed_dict = SearchProcess.embedding_search(state=state)
    state["embedding_chunks"] = embed_dict
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")
    
    return state


# 节点处理函数：搜索嵌入向量（HyDE）
def node_search_embedding_hyde(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    model_result = SearchProcess.model_search(state=state)
    state["hyde_embedding_chunks"] = model_result
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")
    return state


# 节点处理函数：Web 搜索（MCP）
def node_web_search_mcp(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    web_result = SearchProcess.web_search(state=state)
    state["web_search_docs"] = web_result
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")
    return state


# 节点处理函数：RRF
def node_rrf(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    rrf_response = SearchProcess.rrf(state=state)
    state["rrf_chunks"] = rrf_response
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")
    return state


# 节点处理函数：重排序
def node_rerank(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    chunk_info_list = MergeProcess.merge_mcp(state=state)
    
    chunk_score_list = MergeProcess.rerank_chunk(state=state, chunk_info_list=chunk_info_list)
    
    rerank_chunk = MergeProcess.filter_chunk(chunk_score_list=chunk_score_list)
    state["reranked_docs"] = rerank_chunk
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")
    return state
    
    
# 节点处理函数：答案输出
def node_answer_output(state: QueryGraphState):
    function_name = _getframe().f_code.co_name
    task_util.add_running_task(task_id=state["session_id"], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 节点处理开始！")
    
    is_answer = AnswerProcess.check_answer(state=state)              # 判断是否含有问题的答案
    if not is_answer:
        prompt = AnswerProcess.generate_prompt(state=state)
        
        is_stream = state.get("is_stream", False)
        session_id = state.get("session_id")
        answer = AnswerProcess.generate_answer(prompt=prompt, session_id=session_id, is_stream=is_stream)
        state["answer"] = answer
    
    task_util.add_done_task(task_id=state['session_id'], node_name=function_name, is_stream=state.get("is_stream"))
    logger.info(f">>> [{function_name}] 执行处理结束！")

    # 流式查询：无论是否含图片，统一推送最终答案事件，确保前端能收到 final 并关闭连接
    if state.get("is_stream", False):
        session_id = state.get("session_id")
        answer = state.get("answer") or ""
        chunk_list = state.get("reranked_docs", [])
        image_list = AnswerProcess.extract_images_url(chunk_list=chunk_list)
        data = \
            {
                "answer"    : answer,
                "status"    : "completed",
                "image_urls": image_list
            }
        sse_util.push_to_session(session_id=session_id, event=sse_util.FINAL, data=data)

    return state


if __name__ == '__main__':
    from json import dumps
    
    # state = create_query_default_state(session_id="test-1", original_query="HAK180烫金机好用吗？",
    #                                    is_stream=False)
    # result = node_item_name_confirm(state=state)
    # format_string = dumps(obj=result, indent=4, ensure_ascii=False, default=str)
    # print(f"{'=' * 100}\n{format_string}\n{'=' * 100}")
    #
    state = create_query_default_state(session_id="test-1", original_query="HAK 180 烫金机怎么操作？",
                                       rewritten_query="HAK 180 烫金机的具体操作步骤是什么？",
                                       item_names=["HAK 180 烫金机"], is_stream=False)
    
    state = node_search_embedding(state=state)
    state = node_search_embedding_hyde(state=state)
    state = node_web_search_mcp(state=state)
    state = node_rrf(state=state)
    state = node_rerank(state=state)
    state = node_answer_output(state=state)
    
    format_string = dumps(obj=state, indent=4, ensure_ascii=False, default=str)
    print(f"{'=' * 100}\n{format_string}\n{'=' * 100}")
