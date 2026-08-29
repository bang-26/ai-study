#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  service 
    CreateTime     ：  2026-08-17 21:28:23 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os.path import abspath
from typing import List
from datetime import datetime
from uuid import uuid4

from fastapi import BackgroundTasks, UploadFile, Request
from starlette.responses import StreamingResponse

from config import DataDict, PathConfig
from connect import mongo
from entry import DeleteHistoryResponse, GetHistoryResponse, QueryRequest, QueryResponse, TaskStatusResponse, UploadFileResponse
from graph import file_import_graph, query_graph
from state import create_query_default_state, get_default_state
from util import FileUtil, sse_util, task_util
from logger import logger


class ImportService:
    # 保存上传的文件，并调用导入图处理文件
    @staticmethod
    async def upload_file(background_tasks: BackgroundTasks, files: List[UploadFile]) -> UploadFileResponse:
        # 1. 整理下输出的位置 output / 日期文件夹
        today_str = datetime.now().strftime(DataDict.DATE_FORMAT)
        base_out_path = abspath(path=f"{PathConfig.UPDATE_DIR}/{today_str}")
        
        # 2. 记录下每个文件上传的任务 id
        
        result = UploadFileResponse()
        
        # 3. 循环处理每个上传的文件（存储到本地） + 进行异步图任务调用
        try:
            task_id_list = []
            for file in files:
                task_id = str(uuid4())                               # 创建任务 ID
                task_id_list.append(task_id)                         # 添加任务 ID
                
                task_util.add_running_task(task_id=task_id, node_name="upload_file") # 记录下进行文件上传了
                
                update_dir = abspath(f"{base_out_path}/{task_id}")   # 文件的 update_dir
                FileUtil.ensure_dir_exists(dir_path=update_dir)      # 确保目录存在
                
                file_name = file.filename                            # 文件名
                file_path = abspath(path=f"{update_dir}/{file_name}")  # 文件保存路径
                FileUtil.write_stream(file_path=file_path, stream=file.file)
                
                # 执行图
                output_dir = abspath(path=f"{PathConfig.OUTPUT_DIR}/{task_id}")
                background_tasks.add_task(func=ImportService.__run_import_graph, task_id=task_id,
                                          file_path=file_path, output_dir=output_dir)
                
                # 添加完成节点
                task_util.add_done_task(task_id=task_id, node_name="upload_file")
                logger.info(f"{task_id} 节点上传文件成功")
                
            result.code = 200
            result.message = f"完成了文件上传，并开启了异步任务！文件数量为: {len(files)}"
            result.task_ids = task_id_list
            logger.info(result.message)
        except Exception as e:
            logger.error(f"文件上传失败！！错误信息：{e}")
            result.message = f"文件上传失败！！{e}"
        finally:
            # 4. 最终返回结果即可
            return result
        
    # 前端轮询此接口（如每秒 1 次），获取任务的实时处理进度
    @staticmethod
    async def get_task_progress(task_id: str) -> TaskStatusResponse:
        result = TaskStatusResponse(task_id=task_id)
        
        try:
            status = task_util.get_task_status(task_id)
            done_list = task_util.get_done_task_list(task_id)
            running_list = task_util.get_running_task_list(task_id)
            
            result.code = 200
            result.status = status
            result.done_list = done_list
            result.running_list = running_list
            
            logger.info(f"[{task_id}] 状态：{status}，已完成节点：{done_list}，正在运行的节点：{running_list}")
        except Exception as e:
            logger.exception("任务状态查询异常")
            result.code = 500
            result.status = "failed"
        finally:
            return result
    
    # 开启图的执行和调用
    @classmethod
    async def __run_import_graph(cls, task_id: str, file_path: str, output_dir: str):
        task_util.update_task_status(task_id=task_id, status_name="processing")
        
        try:
            init_state = get_default_state()                         # 创建默认状态
            init_state["task_id"] = task_id                          # 添加任务 ID
            init_state["local_file_path"] = file_path                # 添加文件路径
            init_state["local_dir"] = output_dir                     # 添加工作目录
            
            # 执行图
            events = file_import_graph.process_stream(init_state)
            for event in events:
                for node_name, result in event.items():
                    logger.info(f"任务{task_id} 的节点 [{node_name}] 已经完成执行 ....")
                    
            task_util.update_task_status(task_id=task_id, status_name="completed")
            logger.info(f"{task_id}:图状态执行完毕！！")
        except Exception as e:
            logger.exception("====== 图执行失败 ======")
            task_util.update_task_status(task_id=task_id, status_name="failed")


class QueryService:
    # 查询接口
    @staticmethod
    async def query(request: QueryRequest, background_tasks: BackgroundTasks) -> QueryResponse:
        query = request.query
        session_id = request.session_id or str(uuid4())
        is_stream = request.is_stream
        
        result = QueryResponse(session_id=session_id)
        
        # 判断是不是流式处理 （异步 -》 先返回一个结果 开始处理 | 后台运行图，结果向前端推送）
        if is_stream:
            # 创建当前session_id对应的队列 =》 _session_stream
            sse_util.create_sse_queue(session_id)
            # 异步执行  立即返回结果前端 || 中间的过程 sse 一点一点推送给前端
            background_tasks.add_task(func=QueryService.__run_query_graph, query=query,
                                      session_id=session_id, is_stream=is_stream)
            logger.info(f"query：{query}已经开启了异步和流式处理！！")
        else:
            # 同步执行
            QueryService.__run_query_graph(query=query, session_id=session_id, is_stream=is_stream)
            # 获取最后一个节点插入的结果！ node_answer_output (answer)
            answer = task_util.get_task_result(task_id=session_id, key="answer")  # task_utils 封装的一个存储会话结果函数
            result.answer = answer
            result.message = "本次查询处理完毕！"
            # 补齐阶段进度：非流式查询完成后，将 task_util 中记录的已完成节点列表返回给前端展示
            result.done_list = task_util.get_done_task_list(task_id=session_id)
            result.running_list = task_util.get_running_task_list(task_id=session_id)
            # 返回对应的json数据即可
            logger.info(f"query:{query}开启同步处理！处理结果为：{answer}!")

        return result
    
    # 流式处理接口
    @staticmethod
    async def process_stream(session_id: str, request: Request) -> StreamingResponse:
        content = sse_util.sse_generator(session_id, request)
        stream_result = StreamingResponse(content=content, media_type="text/event-stream")
        return stream_result
    
    # 获取历史对话
    @staticmethod
    async def get_history(session_id: str, limit: int = 10) -> GetHistoryResponse:
        # 获取历史对话
        query = {"session_id": session_id}
        chats = mongo.query_data(filter_condition=query, limit=limit)
        
        history_info = GetHistoryResponse(session_id=session_id, items=chats)
        logger.info(f"获取历史对话，session_id = {session_id} 成功，数量：{len(chats)}！")
        
        return history_info
    
    # 删除历史对话
    @staticmethod
    async def delete_history(session_id: str) -> DeleteHistoryResponse:
        delete_condition = {"session_id": session_id}
        response = mongo.delete_data(filter_condition=delete_condition)
        
        deleted_count = response.get("deleted_count")
        delete_info = DeleteHistoryResponse(deleted_count=deleted_count, message=f"{session_id} 聊天记录删除成功！")
        logger.info(f"删除历史对话，session_id = {session_id} 成功，删除数量：{deleted_count}！")
        
        return delete_info
    
    # 运行查询图
    @staticmethod
    def __run_query_graph(query: str, session_id: str, is_stream: bool):
        # 本次任务开启了！ is_stream = True 把结果加入到队列，sse 可以取到
        task_util.update_task_status(session_id, "processing", is_stream)
        
        state = create_query_default_state(session_id=session_id, original_query=query, is_stream=is_stream)
        try:
            query_graph.invoke(input=state)
            # 本次任务开启了！ is_stream = True 把结果加入到队列，sse可以取到
            task_util.update_task_status(session_id, "completed", is_stream)
            # 流式任务正常结束：主动关闭 SSE 连接，避免连接永久悬挂
            if is_stream:
                sse_util.push_to_session(session_id, sse_util.CLOSE, {})
        except Exception as e:
            logger.exception(f"---session_id = {session_id},查询流程出现异常！！{str(e)}")
            # 修改 event = process
            task_util.update_task_status(session_id, "failed", is_stream)
            # 推送指定类型的事件
            if is_stream:
                sse_util.push_to_session(session_id, sse_util.ERROR, {"error": str(e)})
                # 推送错误后同样关闭 SSE 连接
                sse_util.push_to_session(session_id, sse_util.CLOSE, {})
            logger.error(f"session_id = {session_id}, 查询流程出现异常！！{str(e)}")
