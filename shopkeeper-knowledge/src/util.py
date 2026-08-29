#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  util 
    CreateTime     ：  2026-08-12 16:00:11 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from asyncio import get_running_loop, CancelledError
from base64 import b64encode
from json import dumps, dump, load
from os import makedirs, walk, remove, chmod, rename
from os.path import basename, abspath, dirname, isdir, isfile, join
from time import time, sleep
from typing import Optional, BinaryIO, Dict, Any, List, Deque
from shutil import copy2, copyfileobj, rmtree
from stat import S_IWRITE
from queue import Queue, Empty
from zipfile import ZipFile

from numpy import array, float64
from numpy.linalg import norm
from fastapi import Request
from typing_extensions import AsyncGenerator

from logger import logger
from config import PathConfig, DataDict


# 文件处理
class FileUtil:
    # 获取路径的绝对路径
    @staticmethod
    def get_absolute_path(path: str) -> str:
        abs_path = ""
        
        dir_exist = FileUtil.judge_dir_exists(dir_path=path)
        file_exist = FileUtil.judge_file_exists(file_path=path)
        
        if dir_exist:
            logger.debug(f"文件 {path} 存在")
            abs_path = abspath(path=path)
        elif file_exist:
            logger.debug(f"文件夹 {path} 存在")
            abs_path = abspath(path=path)
        else:
            logger.warning(f"输入路径 {path} 不存在")
        return abs_path
    
    # 获取文件名
    @staticmethod
    def get_file_name(file_path: str) -> str:
        return basename(p=file_path)
    
    # 获取文件目录
    @staticmethod
    def get_file_dir(file_path: str) -> str:
        is_exist = FileUtil.judge_file_exists(file_path=file_path)
        
        if is_exist:
            file_path = abspath(path=file_path)
            return dirname(p=file_path)
        else:
            return ""

    # 获取去除文件后缀的文件名
    @staticmethod
    def get_file_name_without_suffix(file_path: str) -> str:
        file_name = FileUtil.get_file_name(file_path=file_path)
        name_without_suffix = file_name.split(".")[0]
        return name_without_suffix
        
    # 获取文件后缀
    @staticmethod
    def get_file_suffix(file_path: str) -> str:
        file_name = FileUtil.get_file_name(file_path=file_path)
        suffix = file_name.split(".")[-1]
        return suffix
        
    # 确保目录存在，如果不存在则创建
    @staticmethod
    def ensure_dir_exists(dir_path: str) -> None:
        if FileUtil.judge_dir_exists(dir_path=dir_path):
            logger.debug(f"目录 {dir_path} 已经存在，不会创建 ...... ")
        elif FileUtil.judge_file_exists(file_path=dir_path):
            logger.debug(f"传入的路径 {dir_path} 是已存在文件，不会创建父目录 ......")
        else:
            try:
                makedirs(dir_path, exist_ok=True)
                logger.warning(f"目录 {dir_path} 不存在，主动创建对应的文件夹 ....")
            except Exception as e:
                logger.error(f"创建目录失败: {dir_path}, 错误信息: {e}")
        
    # 判断文件是否存在
    @staticmethod
    def judge_dir_exists(dir_path: str) -> bool:
        result = False
        
        if dir_path and isdir(s=dir_path):
            result = True
        
        return result
    
    # 判断文件是否存在
    @staticmethod
    def judge_file_exists(file_path: str) -> bool:
        result = False
        
        if file_path and isfile(path=file_path):
            result = True
        
        return result
    
    # 获取目录中所有的文件
    @staticmethod
    def get_all_files(dir_path: str) -> list[str]:
        file_list = []
        
        try:
            is_exist = FileUtil.judge_dir_exists(dir_path=dir_path)
            if is_exist:
                for root, dirs, files in walk(top=dir_path):
                    for file in files:
                        file_path = join(root, file)
                        file_list.append(file_path)
                logger.info(f"获取目录 {dir_path} 中所有文件成功")
            else:
                logger.warning(f"目录 {dir_path} 不存在")
        except Exception as e:
            logger.error(f"获取目录中所有文件失败: {dir_path}, 错误信息: {e}")
        finally:
            return file_list
    
    # 删除文件/目录
    @staticmethod
    def delete_path(path: str) -> None:
        def __remove_readonly(func, path, exc) -> None:
            chmod(path=path, mode=S_IWRITE)
            func(path)
            
        max_retry = 3
        for attempt in range(max_retry):
            try:
                if FileUtil.judge_file_exists(file_path=path):
                    remove(path=path)
                    logger.info(f"删除文件: {path}")
                elif FileUtil.judge_dir_exists(dir_path=path):
                    rmtree(path=path, onexc=__remove_readonly)
                    logger.info(f"删除目录: {path}")
                else:
                    logger.warning(f"文件 {path} 不存在")
                return
            except Exception as e:
                if attempt < max_retry - 1:
                    sleep(0.5)
                else:
                    logger.error(f"删除文件失败: {path}, 错误信息: {e}")
    
    # 重命名文件或目录
    @staticmethod
    def rename_path(src_path: str, dst_path: str) -> None:
        if not FileUtil.judge_file_exists(file_path=src_path):
            logger.error(f"文件 {src_path} 不存在")
            return
        
        dir_path = dirname(p=dst_path)
        FileUtil.ensure_dir_exists(dir_path=dir_path)
        
        try:
            rename(src=src_path, dst=dst_path)
            logger.info(f"重命名文件: {src_path} -> {dst_path}")
        except Exception as e:
            logger.error(f"重命名文件失败: {src_path} -> {dst_path}, 错误信息: {e}")
    
    # 复制文件
    @staticmethod
    def copy_file(src_path: str, dst_path: str) -> None:
        FileUtil.ensure_dir_exists(dir_path=dirname(p=dst_path))
        
        try:
            copy2(src=src_path, dst=dst_path)
            logger.info(f"复制文件: {src_path} -> {dst_path}")
        except Exception as e:
            logger.error(f"复制文件失败: {src_path} -> {dst_path}, 错误信息: {e}")
    
    @staticmethod
    def read_io(file_path: str) -> Optional[bytes]:
        buffer = None
        
        if not FileUtil.judge_file_exists(file_path=file_path):
            logger.warning(f"文件 {file_path} 不存在 ......")
            return buffer
        
        try:
            with open(file=file_path, mode="rb") as fr:
                buffer = fr.read()
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return buffer
    
    # 保存 IO 流到文件
    @staticmethod
    def write_io(file_path: str, file_io: bytes, is_override: bool = True) -> None:
        logger.debug(f"准备保存到文件: {file_path}")
        
        dir_path = dirname(p=file_path)
        FileUtil.ensure_dir_exists(dir_path=dir_path)
        
        is_exist = FileUtil.judge_file_exists(file_path=file_path)
        if is_override:
            FileUtil.delete_path(path=file_path)
        elif is_exist:
            logger.warning(f"文件 {file_path} 已存在, 不会保存 ......")
            return
        
        try:
            with open(file=file_path, mode="wb") as fw:
                fw.write(file_io)
        
            logger.info(f"保存文件: {file_path}")
        except Exception as e:
            logger.error(f"保存文件失败: {file_path}, 错误信息: {e}")
    
    # 保存 IO 流到文件
    @staticmethod
    def write_stream(file_path: str, stream: BinaryIO, is_override: bool = True) -> None:
        logger.debug(f"准备保存到文件: {file_path}")
        
        dir_path = dirname(p=file_path)
        FileUtil.ensure_dir_exists(dir_path=dir_path)
        
        is_exist = FileUtil.judge_file_exists(file_path=file_path)
        if is_override:
            FileUtil.delete_path(path=file_path)
        elif is_exist:
            logger.warning(f"文件 {file_path} 已存在, 不会保存 ......")
            return
        
        try:
            with open(file=file_path, mode="wb") as fw:
                copyfileobj(fsrc=stream, fdst=fw)
        
            logger.info(f"保存文件: {file_path}")
        except Exception as e:
            logger.error(f"保存文件失败: {file_path}, 错误信息: {e}")
        
    # 读取文本文件的内容
    @staticmethod
    def read_text(file_path: str) -> str:
        content = ""
        
        if not FileUtil.judge_file_exists(file_path=file_path):
            logger.warning(f"文件 {file_path} 不存在 ......")
            return content
        
        try:
            with open(file=file_path, mode="r", encoding="utf-8") as fr:
                content = fr.read()
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return content
        
    # 写入内容到文本文件
    @staticmethod
    def write_text(file_path: str, content: str = "") -> None:
        file_dir = FileUtil.get_file_dir(file_path=file_path)
        FileUtil.ensure_dir_exists(dir_path=file_dir)
        
        try:
            with open(file=file_path, mode="w", encoding="utf-8") as fw:
                fw.write(content)
                logger.debug(f"写入内容到文件: {file_path}")
        except Exception as e:
            logger.error(f"写入文件失败: {file_path}, 错误信息: {e}")
    
    # 将 JSON 数据写入文件
    @staticmethod
    def read_json(file_path: str) -> None:
        if not FileUtil.judge_file_exists(file_path=file_path):
            logger.warning(f"文件 {file_path} 不存在 ......")
            return None
        
        content = {}
        try:
            with open(file=file_path, mode="r", encoding="utf-8") as fr:
                content = load(fp=fr, object_hook=dict)
        except Exception as e:
            logger.error(f"读取 JSON 文件失败: {file_path}, 错误信息: {e}")
        finally:
            return content
        
    # 将 JSON 数据写入文件
    @staticmethod
    def write_json(file_path: str, content: list[str]) -> None:
        file_dir = FileUtil.get_file_dir(file_path=file_path)
        FileUtil.ensure_dir_exists(dir_path=file_dir)
        
        try:
            with open(file=file_path, mode="w", encoding="utf-8") as fw:
                dump(obj=content, fp=fw, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"写入 JSON 文件失败: {file_path}, 错误信息: {e}")
    
    # 将图片文件转换为 Base64 编码
    @staticmethod
    def image_to_base64(image_path: str):
        content = ""
        is_exist = FileUtil.judge_file_exists(file_path=image_path)
        
        if  is_exist:
            try:
                with open(file=image_path, mode="rb") as fr:
                    buffer = fr.read()
                    content = b64encode(buffer).decode("utf-8")
                    logger.debug(f"BASE64 编码文件成功: {image_path}")
            except Exception as e:
                logger.error(f"加载文件失败: {image_path}, 错误信息: {e}")
        else:
            logger.warning(f"文件 {image_path} 不存在 ......")
        return content
    

# 提示语解析器
class PromptParser:
    def __init__(self, prompt_path: str):
        self.prompt_path = prompt_path
        self.prompt_dict = None
    
    def reader(self, sep: str = "%%"):
        self.prompt_dict = {}
        with open(file=self.prompt_path, mode="r", encoding="utf-8") as fr:
            content_list = fr.readlines()
        
        key = ""
        value = ""
        for content in content_list:
            if content.strip().startswith(sep):
                if key:
                    self.prompt_dict[key] = value
                    value = ""
                key = content.split(sep)[1].strip().split()[0]
            else:
                value = value + content
        
        if value:
            self.prompt_dict[key] = value
    
    def get_prompt(self, key: str):
        if self.prompt_dict is None:
            self.reader()
        
        prompt = self.prompt_dict.get(key, "")
        return prompt


# 解压缩和压缩
class CompressionUtil:
    # 解压文件
    @staticmethod
    def unzip_file(zip_path: str, extract_path: str) -> None:
        logger.debug(f"解压文件: {zip_path} -> {extract_path}")
        
        # 确保文件存在
        if not FileUtil.judge_file_exists(file_path=zip_path):
            logger.warning(f"文件 {zip_path} 不存在 ......")
            return
        
        FileUtil.ensure_dir_exists(dir_path=extract_path)
        
        try:
            with ZipFile(file=zip_path, mode="r") as zip_read:
                zip_read.extractall(path=extract_path)
                
            logger.info(f"解压文件完成: {zip_path} -> {extract_path}")
        except Exception as e:
            logger.error(f"解压文件失败: {zip_path} -> {extract_path}, 错误信息: {e}")
            

# Milvus 工具类
class MilvusUtil:
    # 转义规则：
    #     1. 反斜杠（\）→ 双反斜杠（\\）：Milvus表达式转义规则
    #     2. 双引号（"）→ 转义双引号（\"）：避免截断字符串表达式
    #     3. 换行/回车/制表符 → 空格：防止表达式换行导致解析失败
    @staticmethod
    def escape_milvus_string(value: str = "") -> str:
        result = ""
        if value:
            value = str(value)  # 确保输入为字符串类型，避免非字符串值报错
            
            string = value.replace("\\", "\\\\").replace('"', '\\"')  # 按 Milvus 规则转义特殊字符
            # 替换换行/回车/制表符为空格，保证表达式单行有效
            result = string.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        return result


# JSON 格式化工具类
class JsonFormatUtil:
    @staticmethod
    def format_state(state: Dict[str, Any], indent: int = 4, ensure_ascii: bool = False,
                     sort_keys: bool = False) -> str:
        """
        专门用于格式化工作流状态（ImportGraphState）
        
        Args:
            state       : ImportGraphState 工作流状态字典
            indent      : JSON 缩进空格数，默认 4
            ensure_ascii: 是否使用 ASCII 编码，默认 False
            sort_keys   : 是否对键进行排序，默认 False
            
        Returns:
            格式化后的 JSON 字符串
            
        Example:
            >>> state = {"task_id": "001", "pdf_path": "test.pdf"}
            >>> json_string = JsonFormatUtil.format_state(state)
            >>> print(json_string)
            {
                "task_id": "001",
                "pdf_path": "test.pdf"
            }
        """
        json_string = dumps(obj=state, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys)
        return json_string
    
    @staticmethod
    def format_json(data: Any, indent: int = 4, ensure_ascii: bool = False, sort_keys: bool = False) -> str:
        """
        通用 JSON 格式化函数

        Args:
            data: 需要格式化的数据（字典、列表等可序列化对象）
            indent: JSON 缩进空格数，默认 4
            ensure_ascii: 是否转义非 ASCII 字符，默认 False（保留中文等字符）

        Returns:
            格式化后的 JSON 字符串

        Example:
            >>> data = {"name": "测试", "value": 123}
            >>> json_string = JsonFormatUtil.format_json(data)
            >>> print(json_string)
            {
                "name": "测试",
                "value": 123
            }
        """
        json_string = dumps(obj=data, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys)
        return json_string


class MatrixUtil:
    # 对稀疏向量做 L2 归一化（仅处理非零维度，不影响零维度）
    @staticmethod
    def normalize_sparse_vector(sparse_vector: array) -> dict[int, float]:
        if not sparse_vector:  # 空向量直接返回
            return sparse_vector
        
        vector_value = sparse_vector.values()  # 获取非零维度的数值
        vector_list = list(vector_value)  # 转换为列表
        values = array(object=vector_list, dtype=float64)  # 转换为 numpy 数组
        
        l2_norm = norm(values)  # 计算 L2 范数（避免除以 0）
        if l2_norm < 1e-9:  # 范数接近 0 时，直接返回原向量
            return sparse_vector
        normalized_values = values / l2_norm  # 归一化：每个数值除以 L2 范数
        
        keys = sparse_vector.keys()  # 获取非零维度的索引
        vector_item = zip(keys, normalized_values)  # 将索引和归一化后的数值配对
        vector = dict(vector_item)  # 重建稀疏向量 dict
        
        return vector


# SSE 工具类
class SseUtil:
    READY = "ready"                                                  # 连接建立
    PROGRESS = "progress"                                            # 任务节点进度
    DELTA = "delta"                                                  # LLM 流式输出增量
    FINAL = "final"                                                  # 最终完整答案
    ERROR = "error"                                                  # 错误信息
    CLOSE = "__close__"                                              # 关闭连接信号
    _session_stream: Dict[str, Queue] = {}                           # 全局 SSE 会话队列存储
    
    # 获取指定 session 的队列
    @classmethod
    def get_sse_queue(cls, session_id: str) -> Optional[Queue]:
        return cls._session_stream.get(session_id)
    
    # 创建并注册一个新的 SSE 队列
    @classmethod
    def create_sse_queue(cls, session_id: str) -> Queue:
        print(f"[SSE] Creating queue for session: {session_id}")
        queue = Queue()
        cls._session_stream[session_id] = queue
        return queue
    
    # 删除指定 session 的队列
    @classmethod
    def remove_sse_queue(cls, session_id: str) -> None:
        print(f"[SSE] Removing queue for session: {session_id}")
        cls._session_stream.pop(session_id, None)
    
    # 打包 SSE 消息格式
    @classmethod
    def _sse_pack(cls, event: str, data: Dict[str, Any]) -> str:
        payload = dumps(data, ensure_ascii=False)
        return f"event: {event}\ndata: {payload}\n\n"
    
    # 通过 session_id 推送事件
    @classmethod
    def push_to_session(cls, session_id: str, event: str, data: Dict[str, Any]) -> None:
        stream_queue = cls.get_sse_queue(session_id)
        if stream_queue:
            stream_queue.put({"event": event, "data": data})
        else:
            # 客户端已断开/前端提前关闭连接时，队列可能已被清理，属预期行为，直接丢弃
            logger.warning(f"[SSE] Warning: No queue found for session {session_id} when pushing {event}")

    # SSE 生成器，用于 FastAPI 的 StreamingResponse
    @classmethod
    async def sse_generator(cls, session_id: str, request: Request) -> AsyncGenerator[str, None]:
        logger.info(f"[SSE] Generator started for session: {session_id}")
        stream_queue = cls.get_sse_queue(session_id)
        
        if stream_queue is None:
            # 队列可能已被上一次连接清理（断线重连场景），重建队列避免连接直接失败
            logger.info(f"[SSE] 队列未找到 {session_id}，重新创建队列，有效 session: {list(cls._session_stream.keys())}")
            stream_queue = cls.create_sse_queue(session_id)
        
        loop = get_running_loop()
        last_heartbeat = time()
        try:
            # 发送连接建立信号
            logger.info(f"[SSE] 已经准备好向 {session_id} 发送消息......")
            yield cls._sse_pack(event="ready", data={})
            
            while True:
                # 若客户端断开，尽快退出
                if await request.is_disconnected():
                    logger.info(f"[SSE] 客户端 {session_id} 未连接")
                    break
                
                try:
                    msg = await loop.run_in_executor(executor=None, func=stream_queue.get, block=True, timeout=15.0)
                except Empty:
                    # 队列为空：发送 SSE 心跳注释（浏览器忽略），防止代理/网关空闲超时断开连接
                    now = time()
                    if now - last_heartbeat >= 15:
                        yield ": ping\n\n"
                        last_heartbeat = now
                    continue
                
                last_heartbeat = time()
                event = msg.get("event")
                data = msg.get("data")
                
                # 特殊关闭事件
                if event == "__close__":
                    logger.info(f"[SSE] 向 {session_id} 发送关闭信号")
                    break
                
                yield cls._sse_pack(event, data)
        except (CancelledError, ConnectionResetError, BrokenPipeError):
            logger.warning(f"[SSE] 生成器 {session_id} 被取消/客户端断开：静默退出未连接......")
            return
        except Exception as e:
            logger.error(f"[SSE] 错误：生成器 {session_id} 遇到错误：{e}")
        finally:
            logger.info(f"[SSE] 生成器 {session_id} 的连接已结束......")
            # 仅删除本生成器持有的队列对象，避免误删重连/新查询创建的新队列
            if cls.get_sse_queue(session_id) is stream_queue:
                cls.remove_sse_queue(session_id)


# 任务工具类
class TaskUtil:
    _tasks_running_list = {}
    _tasks_done_list = {}
    _tasks_status = {}
    _tasks_result = {}
    
    # 确保任务数据结构已初始化
    @classmethod
    def _ensure_task(cls, task_id: str) -> None:
        """确保 task_id 对应的数据结构已初始化。"""
        if task_id not in cls._tasks_running_list:
            cls._tasks_running_list[task_id] = []
        if task_id not in cls._tasks_done_list:
            cls._tasks_done_list[task_id] = []
        if task_id not in cls._tasks_result:
            cls._tasks_result[task_id] = {}
    
    # 节点名转中文展示名
    @staticmethod
    def _to_cn(node_name: str) -> str:
        """将节点名转换为中文展示名；若无映射则返回原名。"""
        return DataDict.NODE_NAME_TO_CN.get(node_name, node_name)
    
    # 添加正在运行的任务
    @classmethod
    def add_running_task(cls, task_id: str, node_name: str, is_stream: bool = False) -> None:
        """
        添加“正在运行”的节点任务。

        参数：
        - task_id: 任务ID
        - node_name: 节点名称(节点ID)
        """
        cls._ensure_task(task_id)
        running = cls._tasks_running_list[task_id]
        # 避免重复追加
        if node_name not in running:
            running.append(node_name)
        
        if is_stream:
            cls.task_push_queue(task_id)
    
    # 添加已完成的任务
    @classmethod
    def add_done_task(cls, task_id: str, node_name: str, is_stream: bool = False) -> None:
        """
        添加“已完成”的节点任务。

        注意：添加已完成任务时，会把同名的“正在运行”任务删除。

        参数：
        - task_id: 任务ID
        - node_name: 节点名称(节点ID)
        """
        cls._ensure_task(task_id)
        
        # 1) 从 running 中移除同名节点（可能出现重复，移除所有）
        running = cls._tasks_running_list[task_id]
        cls._tasks_running_list[task_id] = [n for n in running if n != node_name]
        
        # 2) 追加到 done（保持完成顺序），避免重复
        done = cls._tasks_done_list[task_id]
        if node_name not in done:
            done.append(node_name)
        
        if is_stream:
            cls.task_push_queue(task_id)
    
    # 存储任务结果
    @classmethod
    def set_task_result(cls, task_id: str, key: str, value: str) -> None:
        """
        存储任务结果字段（如 answer / error）。
        """
        cls._ensure_task(task_id)
        cls._tasks_result[task_id][key] = value
    
    # 获取任务结果
    @classmethod
    def get_task_result(cls, task_id: str, key: str, default: str = "") -> str:
        """
        获取任务结果字段（如 answer / error）。
        """
        cls._ensure_task(task_id)
        return cls._tasks_result.get(task_id, {}).get(key, default)
    
    # 获取任务状态
    @classmethod
    def get_task_status(cls, task_id: str) -> str:
        """
        获取当前任务状态。

        参数：
        - task_id: 任务ID

        返回：
        - str: 状态名称；如果未设置过则返回空字符串
        """
        return cls._tasks_status.get(task_id, "")
    
    # 获取已完成任务列表
    @classmethod
    def get_done_task_list(cls, task_id: str) -> List[str]:
        """
        获取已完成节点列表（中文展示）。


        """
        cls._ensure_task(task_id)
        done = cls._tasks_done_list.get(task_id, [])
        return [cls._to_cn(n) for n in done]
    
    # 获取正在运行任务列表
    @classmethod
    def get_running_task_list(cls, task_id: str) -> List[str]:
        """
        获取正在运行节点列表（中文展示）。

        """
        cls._ensure_task(task_id)
        running = cls._tasks_running_list.get(task_id, [])
        return [cls._to_cn(n) for n in running]
        
    # 更新任务状态
    @classmethod
    def update_task_status(cls, task_id: str, status_name: str, push_queue: bool = False) -> None:
        """
        更新任务状态。

        参数：
        - task_id: 任务ID
        - status_name: 状态名称（字符串）
        """
        cls._tasks_status[task_id] = status_name
        if push_queue:
            cls.task_push_queue(task_id)
    
    # 推送任务进度队列
    @classmethod
    def task_push_queue(cls, task_id: str):
        data = \
            {
                "status"      : cls.get_task_status(task_id),
                "done_list"   : cls.get_done_task_list(task_id),
                "running_list": cls.get_running_task_list(task_id),
            }
        sse_util.push_to_session(session_id=task_id, event="progress", data=data)
        
    # 清理任务数据
    @classmethod
    def clear_task(cls, task_id: str):
        cls._tasks_running_list.pop(task_id, None)
        cls._tasks_done_list.pop(task_id, None)
        cls._tasks_status.pop(task_id, None)
        cls._tasks_result.pop(task_id, None)


class ApiUtil:
    # 通用滑动窗口API速率限制器
    @staticmethod
    def apply_api_rate_limit(request_times: Deque[float], max_requests: int, window_seconds: int = 60) -> None:
        """
        （抽离为公共工具）
        核心逻辑：维护请求时间戳双端队列，窗口内请求数超上限则自动等待，防止触发第三方API限流
        :param request_times: 存储请求时间戳的双端队列，需外部初始化（全局/单例），跨调用复用
        :param max_requests: 速率限制窗口内的最大允许请求次数
        :param window_seconds: 速率限制滑动窗口时长，默认60秒（1分钟）
        :return: None，超出限制时会阻塞等待 2分钟！！
        """
        current_time = time()
        # 1. 清理滑动窗口外的过期请求时间戳，保证队列仅存窗口内的请求
        while request_times and current_time - request_times[0] >= window_seconds:
            request_times.popleft()
        # 2. 窗口内请求数达上限，计算并阻塞等待剩余时间
        if len(request_times) >= max_requests:
            # 计算需要等待的时长（窗口总时长 - 最早请求已存在的时长）
            sleep_duration = window_seconds - (current_time - request_times[0])
            if sleep_duration > 0:
                logger.debug(f"触发限速，窗口 {window_seconds} 秒内最多 {max_requests} 次，需等待：{sleep_duration:.2f}s")
                sleep(sleep_duration)
                # 等待后更新当前时间，重新清理过期请求（避免等待期间有请求过期）
                current_time = time()
                while request_times and current_time - request_times[0] >= window_seconds:
                    request_times.popleft()
        # 3. 记录当前请求时间戳，加入滑动窗口队列
        request_times.append(current_time)
        logger.debug(f"API请求时间戳已记录，当前{window_seconds}秒窗口内请求数：{len(request_times)}")


task_util = TaskUtil()
sse_util = SseUtil()

        
if __name__ == '__main__':
    
    # prompt = PromptParser(prompt_path=PathConfig.PROMPT_PATH)
    # prompt.reader()
    # for key, value in prompt.prompt_dict.items():
    #     print(f"{key}: {value}")
    
    zip_path = "../data/output/3040.pdf.zip"
    
    file_name =  FileUtil.get_file_name_without_suffix(zip_path)
    local_dir = f"{PathConfig.OUTPUT_DIR}/{file_name}"
    print(f"zip_path = {zip_path}")
    print(f"local_dir = {local_dir}")
    
    CompressionUtil.unzip_file(zip_path=zip_path, extract_path=local_dir)
