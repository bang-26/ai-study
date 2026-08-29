#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  process 
    CreateTime     ：  2026-08-14 17:15:00 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""
from asyncio import run
from collections import deque
from datetime import datetime
from time import sleep
from typing import Optional, Union
from re import compile, sub, match
from json import dumps, loads
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import DataType
from requests import get, post, RequestException, Session
from config import MineruConfig, app_config, DataDict, PathConfig
from connect import CloudModelConnect, minio, embed, MilvusConnect, mongo, mcp, reranker
from logger import logger
from state import QueryGraphState
from util import FileUtil, PromptParser, ApiUtil, sse_util, task_util


class MineruProcess:
    def __init__(self, conf: MineruConfig):
        self.upload_url = conf.upload_url
        self.download_url = conf.download_url
        self.model_version = conf.model_version
        self.poll_interval = conf.poll_interval
        self.timeout = conf.timeout
        
        self.header = \
            {
                "Content-Type" : "application/json",
                "Authorization": f"Bearer {conf.token}"
            }
    
    # 获取上传文件的 url
    def __get_upload_urls(self, path_list: list[str]) -> dict[str, Union[str, list]]:
        file_path_list = []
        for path in path_list:
            name = FileUtil.get_file_name(file_path=path)
            file_path_list.append({"name": name})
        
        result = ()
        try:
            data = \
                {
                    "files"        : file_path_list,
                    "model_version": self.model_version
                }
            
            response = post(url=self.upload_url, headers=self.header, json=data)
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 0:
                    result = data.get("data")
                    logger.debug(f"获取上传地址成功：{result}")
            else:
                logger.error(f"请求失败：{response.status_code}，{response}")
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise RequestException(f"请求失败: {e}")
        finally:
            return result
        
    # 上传文件
    def __upload_file(self, file_path: str, upload_url: str) -> None:
        try:
            with Session() as session:
                session.trust_env = False
                file_data = FileUtil.read_io(file_path=file_path)
                response = session.put(url=upload_url, data=file_data)
            
            if response.status_code == 200:
                logger.info(f"文件上传成功：{file_path} ==> {upload_url}")
            else:
                logger.error(f"文件上传失败: {response.status_code}，{response}")
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise RequestException(f"请求失败: {e}")
            
    # 下载文件
    def __get_download_urls(self, batch_id: str) -> dict[str, Union[str, int, dict]]:
        result = { "status": 300, "files": {}, "success_count": 0, "fail_count": 0 }
        
        url = f"{self.download_url}/{batch_id}"
        try:
            response = get(url=url, headers=self.header)
            status_code = response.status_code
            
            if status_code == 200:
                result["status"] = 200
                code = response.json().get("code")
                if code == 0:
                    extract_result_list = response.json().get("data").get("extract_result")
                    logger.debug(f"获取文件下载的响应成功：{extract_result_list} ")
                    
                    for extract_result in extract_result_list:
                        file_name = extract_result.get("file_name")
                        
                        err_msg = extract_result.get("err_msg")
                        if err_msg:
                            result["fail_count"] += 1
                            logger.warning(f"文件 {file_name} 解析错误：{err_msg}")
                            continue
                            
                        state = extract_result.get("state")
                        if state == "done":
                            file = extract_result.get("full_zip_url")
                            result["files"][file_name] = file
                            result["success_count"] += 1
                            logger.info(f"文件 {file_name} 解析成功：{file}")
                        else:
                            logger.warning(f"文件 {file_name} 解析中，请稍等...")
                else:
                    logger.error(f"服务器返回内容错误：{response.json().get('msg')}")
            elif 500 <= status_code <= 600:
                result["status"] = 500
                logger.error(f"服务器解析失败：{response.status_code}，{response}")
            else:
                result["status"] = status_code
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise RequestException(f"请求失败: {e}")
        finally:
            return result
    
    # 下载文件
    def __download_file(self, url: str) -> Optional[bytes]:
        result = None
        
        try:
            response = get(url=url, headers=self.header, stream=True)
            if response.status_code == 200:
                result = response.content
                logger.info(f" zip 包下载成功：{url}")
            else:
                logger.error(f"zip 包下载失败：{response.status_code}，{response}")
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise RequestException(f"请求失败: {e}")
        finally:
            return result
    
    # 解析 pdf
    def get_parse_url(self, pdf_path_list: list[str]) -> dict[str, str]:
        # 1. 获取文件上传 url
        upload_info = self.__get_upload_urls(path_list=pdf_path_list)
        batch_id = upload_info.get("batch_id")                       # 文件批次号
        file_url_list = upload_info.get("file_urls")                 # 所有文件上传 url
        
        # 2. 上传文件
        for i in range(len(pdf_path_list)):
            self.__upload_file(file_path=pdf_path_list[i], upload_url=file_url_list[i])
        
        pdf_count = len(pdf_path_list)
        # 3. 获取解析 url
        url_dict = {}
        different = self.timeout
        while different > 0:
            different -= self.poll_interval
            
            file_info = self.__get_download_urls(batch_id=batch_id)
            logger.debug(f"批次 {batch_id} 解析结果：{file_info}")
            
            file_dict = file_info.get("files")
            url_dict.update(file_dict)
            
            file_count = file_info.get("success_count") + file_info.get("fail_count")
            if len(url_dict) == pdf_count or file_count == pdf_count:
                break
                
            status = file_info.get("status")
            if status == 500 or status == 200:
                sleep(self.poll_interval)
            else:
                break
        
        logger.info(f"本次文件 {pdf_path_list} 解析完成，解析结果：{url_dict}")
        return url_dict
    
    # 保存下载的 zip 文件
    def save_zip_file(self, zip_url: str, file_path: str) -> None:
        try:
            content = self.__download_file(url=zip_url)
            
            if content:
                FileUtil.write_io(file_path=file_path, file_io=content, is_override=False)
                logger.info(f"文件保存成功：{file_path}")
            else:
                logger.warning(f"zip 包下载失败：{zip_url}")
        except Exception as e:
            logger.error(f"保存 zip 文件失败: {e}")
            raise RequestException(f"保存 zip 文件失败: {e}")


# 处理图片
class ImageProcess:
    
    # 扫描文件下的所有图片
    @staticmethod
    def scan_images(dir_path: str, suffix_set: set[str] = DataDict.IMAGE_SUFFIX_LIST) -> list[str]:
        file_list = FileUtil.get_all_files(dir_path=dir_path)
        
        image_list = []
        for file_path in file_list:
            suffix = FileUtil.get_file_suffix(file_path=file_path)
            if suffix in suffix_set:
                image_path = FileUtil.get_absolute_path(path=file_path)
                image_list.append(image_path)
        
        logger.debug(f"获取目录 {dir_path} 下的图片文件，共 {len(image_list)} 个文件")
        return image_list
    
    # 查询图片内容
    @staticmethod
    def query_image_context(image_list: list[str], content: str, context_length: int = 100) -> list[dict[str, str]]:
        use_image_list = []
        
        for image_path in image_list:
            image_name = FileUtil.get_file_name(file_path=image_path)
            
            pattern = compile(pattern=r"!\[.*?\]\(.*?" + image_name + r".*?\)")
            image_list = []
            for item in pattern.finditer(string=content):
                start, end = item.span()                             # 获取匹配的起始和结束位置
                
                pre_start = max(0, start - context_length)           # 计算前文起始位置
                pre_text = content[pre_start: start]                 # 获取前文内容
                
                post_end = min(len(content), end + context_length)   # 计算后文结束位置
                post_text = content[end: post_end]                   # 获取后文内容
                
                image_list.append({"image_path": image_path, "pre_text": pre_text, "post_text": post_text})
            
            if image_list:
                use_image_list.append(image_list[0])
        
        logger.info(f"共 {len(use_image_list)} 张图片匹配成功 ... ")
        return use_image_list
    
    # 获取图片摘要
    @staticmethod
    def get_image_summary(image_info_list: list[dict[str, str]]) -> dict[str, str]:
        llm = CloudModelConnect(conf=app_config.model_config)
        llm.connect()
        
        prompt_parser = PromptParser(prompt_path=PathConfig.PROMPT_PATH)
        raw_prompt = prompt_parser.get_prompt(key="image-summary")
        
        request_time = deque()
        summary_dict = {}
        for image_info in image_info_list:
            image_path = image_info.get("image_path")
            pre_text = image_info.get("pre_text")
            post_text = image_info.get("post_text")
            
            # 机型限速：60s 可访问 10 次
            ApiUtil.apply_api_rate_limit(request_times=request_time, max_requests=10, window_seconds=60)
            
            prompt = raw_prompt.format(image_path=image_path, pre_text=pre_text, post_text=post_text)
            response = llm.image_invoke(image_path = image_path, prompt=prompt)
            
            summary = response.strip().replace("\n", "")
            if summary:
                summary_dict[image_path] = summary
                
        logger.info(f"共 {len(summary_dict)} 张图片摘要完成 ... ")
        return summary_dict
    
    # 将文件图片上传的 minio
    @staticmethod
    def transform_images(content: str, image_summary_dict: dict[str, str], upload_dir: str) -> str:
        minio.create_bucket()                                        # 创建桶
        file_path_list = minio.list_files(file_path=upload_dir)      # 列出文件
        minio.delete_files(file_path_list=file_path_list)            # 删除文件
        
        for image_path, summary in image_summary_dict.items():
            image_name = FileUtil.get_file_name(file_path=image_path)
            
            upload_path = f"{upload_dir}/{image_name}"
            image_url= minio.upload_file(file_path=image_path, upload_path=upload_path)
            
            pattern = compile(pattern=r"!\[.*?\]\(.*?" + image_name + r".*?\)")
            content = sub(pattern=pattern, repl=f"![{summary}]({image_url})", string=content)
            
        logger.info(f"图片内容替换成功，共 {len(image_summary_dict)} 张图片 ... ")
        return content
        

# 处理文档
class DocumentProcess:
    @staticmethod
    def split_by_title(md_content: str, file_title: str) -> tuple[str, int, list[dict[str, str]]]:
        line_list = md_content.split("\n")                           # 按行分割
        
        current_title = ""                                           # 当前标题
        current_lines = []                                           # 当前行
        title_count = 0                                              # 标题数量
        is_code_block = False                                        # 是否是代码块
        section_list = []                                            # 存储的列表
        
        for line in line_list:
            strip_line = line.strip()
            
            # 1. 代码块处理
            if strip_line.startswith("```") or strip_line.startswith("~~~"):
                is_code_block = not is_code_block
                current_lines.append(line)
                continue
            
            # 2. 标题处理
            title_pattern = r"^\s*#{1,6}\s+.+"                       # 标题匹配模式
            is_match = match(pattern=title_pattern, string=strip_line)
            
            # 判断是否为标题
            if (not is_code_block) and is_match:
                if current_title:
                    content = "\n".join(current_lines)
                    section = {"title": current_title, "file_title": file_title, "content": content}
                    section_list.append(section)
                    current_lines.clear()
                    
                current_title = strip_line
                current_lines.append(line)
                title_count += 1
                continue
            else:
                current_lines.append(line)
            
        # 3. 获取 section_list
        if current_title:
            content = "\n".join(current_lines)
            section = {"title": current_title, "file_title": file_title, "content": content}
            section_list.append(section)
        
        logger.info(f"根据标题分割，共 {title_count} 个标题")
        # result_dict = {"file_title": file_title, "sections": section_list, "title_count": title_count}
        return file_title, title_count, section_list
    
    # 精炼分块
    @staticmethod
    def refine_chunks(section_list: list[dict[str, Union[str, int]]], min: int = 1024, max: int = 4096, overlap: int = 256):
        result_list = []
        
        # 1. # 超过的先切碎
        for section in section_list:
            content = section.get("content")
            
            if len(content) > max:
                seps = ["\n\n", "\n", " ", ""]
                splitter = RecursiveCharacterTextSplitter(chunk_size=max, chunk_overlap=overlap, separators=seps)
                chunks = splitter.split_text(content)
                
                sub_content = ""
                index = 1
                for chunk in chunks:
                    sub_content += chunk.strip()
                    
                    if len(sub_content) > max:
                        sub_section = \
                            {
                                "title": section.get("title"),
                                "file_title": section.get("file_title"),
                                "content": sub_content,
                                "part": index
                            }
                        result_list.append(sub_section)
                        index += 1
                        sub_content = ""
                
                if sub_content:
                    sub_section = \
                        {
                            "title": section.get("title"),
                            "file_title": section.get("file_title"),
                            "content": sub_content,
                            "part": index
                        }
                    result_list.append(sub_section)
            else:
                section.setdefault("part", 1)
                result_list.append(section)
        
        logger.info(f"对较长的标题再次切分，共 {len(result_list)} 个分块")
        return result_list


# 识别处理
class RecognitionProcess:
    # 构建上下文
    @staticmethod
    def build_context(chunk_list: list[dict[str, str]]):
        context_string = ""                                        # 上下文字符串
        context = ""                                               # 上下文
        
        for i in range(len(chunk_list)):
            title = chunk_list[i].get("title")
            content = chunk_list[i].get("content")
            
            context += content
            end = DataDict.CONTEXT_MAX - len(context) + 1
            context_string += f"切片：{i + 1}，标题：{title}，内容：{content[:end]}" + "\n\n"
            
            if len(context) > DataDict.CONTEXT_MAX:
                break
            
        logger.info(f"构建上下文完成，长度为：{len(context)}")
        return context_string.strip()
    
    # 调用 LLM
    @staticmethod
    def call_llm(context: str, file_title: str):
        prompt_parser = PromptParser(prompt_path=PathConfig.PROMPT_PATH)   # 创建 PromptParser 对象
        
        # 1. 构建系统提示词
        human_raw_prompt = prompt_parser.get_prompt(key="item-name-recognition")  # 获取 prompt
        human_prompt = human_raw_prompt.format(file_title=file_title, context=context)
        
        system_prompt = prompt_parser.get_prompt(key="product-recognition-system")
        
        # 2. 创建 LLM 连接对象
        llm = CloudModelConnect(conf=app_config.model_config)
        llm.connect()
        
        # 调用大模型
        response = llm.invoke(system_prompt=system_prompt, human_prompt=human_prompt)
        if not response:
            response = file_title
        
        logger.info(f"查询商品类型完成：{response[:16]}")
        return response
    
    @staticmethod
    def generate_vector(text: str) -> tuple[list[float], list[float]]:
        vector_info = embed.generate_vector(text_list=[text])        # 获取向量
        dense = vector_info.get("dense")[0]                          # 稠密向量
        sparse = vector_info.get("sparse")[0]                        # 稀疏向量
        return dense, sparse
    
    @staticmethod
    def save_item_vector(file_title: str, item_name: str, dense_vector: list[float], sparse_vector: list[float]):
        dimension = len(dense_vector)
        # 1. 创建字段配置
        
        field_config_list = \
            [
                {"field_name": "pk",            "data_type": DataType.INT64,        "params": {"is_primary": True, "auto_id": True}},
                {"field_name": "file_title",    "data_type": DataType.VARCHAR,      "params": {"max_length": 65535}},
                {"field_name": "item_name",     "data_type": DataType.VARCHAR,      "params": {"max_length": 65535}},
                {"field_name": "dense_vector",  "data_type": DataType.FLOAT_VECTOR, "params": {"dim": dimension}},
                {"field_name": "sparse_vector", "data_type": DataType.SPARSE_FLOAT_VECTOR},
            ]
            
        # 2. 创建索引配置
        index_config_list = [
            { "field_name": "dense_vector", "index_name": "dense_vector_index", "index_type": "HNSW",
              "params": {"metric_type": "COSINE", "M": 16, "efConstruction": 200} },
            { "field_name": "sparse_vector", "index_name": "sparse_vector_index", "index_type": "SPARSE_INVERTED_INDEX",
              "params": {"metric_type": "IP", "inverted_index_algo": "DAAT_MAXSCORE", "quantization": "none"}}
        ]
        
        # 3. 创建集合
        collection_name = "item_names"
        with MilvusConnect(conf=app_config.milvus_config) as milvus:
            milvus.create_collection(field_config_list=field_config_list, index_config_list=index_config_list,
                                     collection_name=collection_name)
            
            # 4. 删除已存在的数据
            filter_condition = f"item_name == '{item_name}'"
            milvus.delete_data(collection_name=collection_name, filter_condition=filter_condition)
            
            # 5. 插入数据
            data_item = \
                {
                    "file_title": file_title,
                    "item_name": item_name,
                    "dense_vector": dense_vector,
                    "sparse_vector": sparse_vector
                }
            milvus.insert_data(data_list=[data_item], collection_name=collection_name)
        
        
class ContentProcess:
    # 获取商品描述向量
    @staticmethod
    def get_chunk_vector(chunk_list: list[dict[str, str]], batch_size: int = 10) -> list[dict[str, str]]:
        length = len(chunk_list)
        
        result_list = []
        for i in range(0, length, batch_size):
            item_list = chunk_list[i: i + batch_size]
            
            batch_list = []
            for item in item_list:
                item_name = item.get("item_name")
                item_content = item.get("content")
                
                item_text = f"商品：{item_name}，内容介绍：{item_content}"
                batch_list.append(item_text)
                
            item_vector_dict = embed.generate_vector(text_list=batch_list)
            for j in range(len(item_list)):
                item_copy = item_list[j].copy()
                
                item_copy["dense_vector"] = item_vector_dict.get("dense")[j]
                item_copy["sparse_vector"] = item_vector_dict.get("sparse")[j]
                item_copy.setdefault("part", "1")
                result_list.append(item_copy)
                
        logger.info(f"获取商品描述向量完成，共 {len(result_list)} 个")
        return result_list
    
    # 保存到 Milvus
    @staticmethod
    def save_chunk_vector(chunk_list: list[dict[str, str]]):
        dimension = 1024
        # 1. 创建字段配置
        field_config_list = \
            [
                {"field_name": "chunk_id",      "data_type": DataType.INT64,        "params": {"is_primary": True, "auto_id": True}},
                {"field_name": "file_title",    "data_type": DataType.VARCHAR,      "params": {"max_length": 65535}},
                {"field_name": "item_name",     "data_type": DataType.VARCHAR,      "params": {"max_length": 65535}},
                {"field_name": "content",       "data_type": DataType.VARCHAR,      "params": {"max_length": 65535}},
                {"field_name": "title",         "data_type": DataType.VARCHAR,      "params": {"max_length": 65535}},
                {"field_name": "part",          "data_type": DataType.INT8,         "params": {}},
                {"field_name": "dense_vector",  "data_type": DataType.FLOAT_VECTOR, "params": {"dim": dimension}},
                {"field_name": "sparse_vector", "data_type": DataType.SPARSE_FLOAT_VECTOR},
            ]
        
        # 2. 创建索引配置
        index_config_list = [
            {"field_name": "dense_vector", "index_name": "dense_vector_index", "index_type": "HNSW",
             "params"    : {"metric_type": "COSINE", "M": 32, "efConstruction": 300}},
            {"field_name": "sparse_vector", "index_name": "sparse_vector_index", "index_type": "SPARSE_INVERTED_INDEX",
             "params"    : {"metric_type": "IP", "inverted_index_algo": "DAAT_MAXSCORE"}}
        ]
        
        # 3. 创建集合
        collection_name = "chunks"
        with MilvusConnect(conf=app_config.milvus_config) as milvus:
            milvus.create_collection(field_config_list=field_config_list, index_config_list=index_config_list,
                                     collection_name=collection_name)
                
            # 4. 删除已存在的数据
            item_name = chunk_list[0].get("item_name")
            filter_condition = f"item_name == '{item_name}'"
            milvus.delete_data(collection_name=collection_name, filter_condition=filter_condition)
        
            # 5. 插入数据
            response = milvus.insert_data(data_list=chunk_list, collection_name=collection_name)
        
        id_list = response.get("ids")
        if len(chunk_list) != len(id_list):
            logger.warning("插入数据失败 ......")
            raise RequestException("插入数据失败：插入数据和完成数据长度不一致")
        
        for i in range(len(chunk_list)):
            chunk_list[i]["chunk_id"] = id_list[i]
        
        logger.info(f"保存商品描述向量完成，共 {len(chunk_list)} 个")
        return chunk_list


class ItemConfirmProcess:
    @staticmethod
    def rewrite_query(original_query: str, chat_list: list[dict[str, str]]) -> dict[str, str]:
        history_text = ""
        for chat in chat_list:
            history_text += (f"聊天角色：{chat.get('role')}，回答内容：{chat.get('text')}，"
                             f"重写问题：{chat.get('rewritten_query')}，关联主题：{''.join(chat.get('item_names', []))}，"
                             f"时间：{chat.get('ts')}")
        
        parser = PromptParser(prompt_path=PathConfig.PROMPT_PATH)
        human_raw_prompt = parser.get_prompt(key="rewritten-query-names")
        human_prompt = human_raw_prompt.format(history_text=history_text, query=original_query)
        
        llm = CloudModelConnect(conf=app_config.model_config)
        llm.connect()
        
        response = llm.invoke(human_prompt=human_prompt)
        content_dict = loads(s=response)
        
        content_dict.setdefault("item_names", [])
        content_dict.setdefault("rewritten_query", "")
        
        logger.info(f"重写查询完成 ...... ")
        return content_dict
    
    @staticmethod
    def vector_query(item_names: list[str]) -> list[dict[str, str]]:
        vector_info_list = embed.generate_vector(text_list=item_names)    # 获取向量
        
        result_list = []
        with MilvusConnect(conf=app_config.milvus_config) as milvus:
            for i in range(len(item_names)):
                dense = vector_info_list.get("dense")[i]                 # 稠密向量
                sparse = vector_info_list.get("sparse")[i]               # 稀疏向量
                
                result = milvus.hybrid_query(collection_name="item_names", dense_vector=dense, sparse_vector=sparse,
                                             ranker_weights=(0.6, 0.4), norm_score=True, limit=5)
                
                match_list = []
                if result and len(result) > 0:
                    for hit in result[0]:
                        entity = hit.get("entity", {})
                        hit_name = entity.get("item_name", "")
                        
                        if hit_name:
                            score = hit.get("distance", 0.0)
                            match_list.append({"item_name": hit_name, "score": score})
                
                result_list.append({ "extracted": item_names[i], "matches": match_list })
        
        logger.info(f"向量查询完成，共 {len(result_list)} 个")
        return result_list
    
    @staticmethod
    def classify(query_info_list: list[dict[str, Union[str, list[dict[str, str]]]]]) -> dict[str, list[Optional[str]]]:
        confirm_list =[]
        option_list =[]
        for query_info in query_info_list:
            extracted = query_info.get("extracted")
            match_list = query_info.get("matches", [])
            match_list.sort(key=lambda x: x.get("score", 0.0), reverse=True)
            
            high_score_list = [match for match in match_list if match.get("score", 0.0) > 0.85]
            middle_score_list = [match for match in match_list if 0.6 <= match.get("score", 0.0) <= 0.85]
            
            if len(high_score_list) >= 1:
                item_name = None
                for high in high_score_list:
                    if extracted == high.get("item_name"):
                        item_name = high.get("item_name")
                        break
                
                if not item_name:
                    item_name = high_score_list[0].get("item_name")
                
                confirm_list.append(item_name)
            else:
                logger.warning(f"无高分匹配，使用中等匹配 ...... ")
                for middle in middle_score_list[:2]:
                    item_name = middle.get("item_name")
                    option_list.append(item_name)
        
        confirm_list = list(set(confirm_list))
        option_list = list(set(option_list))
        logger.info(f"分类完成，确认列表：{confirm_list}，可选项列表：{option_list}")
        
        result = { "confirms": [], "answer": "没有匹配的商品名，请重新提问！！" }
        if len(confirm_list) > 0:
            result["confirms"] = confirm_list
        elif len(option_list) > 0:
            answer = f"您是想咨询以下哪个商品：{option_list}?请下次提问明确商品名称！！"
            result["answer"] = answer
        else:
            logger.warning("没有匹配的商品名！！")
            
        return result
    
    @staticmethod
    def save_chat(state: QueryGraphState, item_info_dict: dict[str, list],
                  chat_list: list[dict], rewritten_query: str) -> QueryGraphState:
        
        item_names = item_info_dict.get("confirms")
        session_id = state["session_id"]
        ts = datetime.now().timestamp()
        document = \
            {
                "session_id"     : session_id,                       # 会话ID，关联维度
                "role"           : "user",                           # 消息角色
                "text"           : state.get("original_query"),      # 消息内容
                "rewritten_query": rewritten_query,                  # 重写查询，空值处理为空字符串
                "item_names"     : item_names,                       # 关联商品名称列表
                "image_urls"     : state.get("image_urls", []),      # 关联图片URL列表
                "ts"             : ts                                # 时间戳，排序和时间筛选维度
            }
        
        mongo.insert_data(data_list=[document])
        logger.info(f"保存聊天记录完成，会话ID：{session_id}")
        
        if item_names:
            state['item_names'] = item_names
            
            if "answer" in state:
                del state["answer"]
        else:
            state["answer"] = item_info_dict.get("answer", "")
            
        state['rewritten_query'] =rewritten_query
        state['history'] = chat_list
        
        logger.info(f"保存聊天记录完成，会话ID：{session_id}")
        return state
        

class SearchProcess:
    @staticmethod
    def embedding_search(state: QueryGraphState):
        rewritten_query = state.get("rewritten_query")
        item_names = state.get("item_names")
        
        vector_info = embed.generate_vector(text_list=[rewritten_query])
        dense_vector = vector_info.get("dense")[0]
        sparse_vector = vector_info.get("sparse")[0]
        
        item_name_str = ', '.join(f'"{item}"' for item in item_names)
        condition = f"item_name in [{item_name_str}]"
        output_fields = ["chunk_id", "content", "file_title", "title", "parent_title", "item_name"]
        with MilvusConnect(conf=app_config.milvus_config) as milvus:
            response_list = milvus.hybrid_query(dense_vector=dense_vector, sparse_vector=sparse_vector,
                                                filter_condition=condition, collection_name="chunks",
                                                ranker_weights=(0.7, 0.3), output_fields=output_fields,
                                                norm_score=True, limit=5)
        
        chunk_list = response_list[0] if response_list else []
        logger.info(f"向量搜索完成，共 {len(chunk_list)} 个")
        
        return chunk_list
        
    @staticmethod
    def model_search(state: QueryGraphState):
        rewritten_query = state.get("rewritten_query")
        
        parser = PromptParser(prompt_path=PathConfig.PROMPT_PATH)
        human_raw_prompt = parser.get_prompt(key="hyde-prompt")
        
        llm = CloudModelConnect(conf=app_config.model_config)
        llm.connect()
        
        human_prompt = human_raw_prompt.format(rewritten_query=rewritten_query)
        response = llm.invoke(human_prompt=human_prompt)
        logger.info(f"使用模型生成假设性答案，问题：{rewritten_query[:16]} ==> 答案：{response[:16]}")
        
        query_str = f"{rewritten_query} {response}"
        vector_info = embed.generate_vector(text_list=[query_str])
        
        item_names = state.get("item_names")
        item_name_str = ', '.join(f'"{item}"' for item in item_names)
        condition = f"item_name in [{item_name_str}]"
        
        dense_vector = vector_info.get("dense")[0]
        sparse_vector = vector_info.get("sparse")[0]
        output_fields = ["chunk_id", "content", "file_title", "title", "item_name"]
        
        with MilvusConnect(conf=app_config.milvus_config) as milvus:
            response = milvus.hybrid_query(dense_vector=dense_vector, sparse_vector=sparse_vector,
                                           filter_condition=condition, collection_name="chunks",
                                           ranker_weights=(0.9, 0.1), output_fields=output_fields,
                                           norm_score=True, limit=5)
        
        result = response[0] if response else []
        logger.info(f"向量搜索完成，共 {len(result)} 个")
        return result
    
    @staticmethod
    def web_search(state: QueryGraphState):
        query = state.get("rewritten_query")
        response = run(mcp.query_data(query=query))
        
        result = response.get("pages", [])
        logger.info(f"网页搜索完成，共 {len(result)} 个")
        
        return result
    
    @staticmethod
    def rrf(state: QueryGraphState, top_k: int = 5):
        chunk_list = state.get("embedding_chunks")
        hyde_list = state.get("hyde_embedding_chunks")
        
        score_dict = {}
        chunk_dict = {}
        
        source_with_weight = [(chunk_list, 1.0), (hyde_list, 1.0)]
        for source, weight in source_with_weight:
            for rank, chunk in enumerate(source, start=1):
                chunk_id = chunk.get("id") or chunk.get("entity").get("chunk_id")
                score_dict[chunk_id] = score_dict.get(chunk_id, 0.0) + (1.0 / (60 + rank)) * weight
                chunk_dict.setdefault(chunk_id, chunk)
        
        merged = []
        for chunk_id, score in score_dict.items():
            chunk = chunk_dict.get(chunk_id)
            merged.append((chunk, score))
        
        merged.sort(key=lambda x: x[1], reverse=True)
        merged = merged[: top_k]
        rank_chunks = [chunk for chunk, score in merged]
        
        logger.info(f"完成了 rrf 排序处理完毕，结果为：{rank_chunks}")
        return rank_chunks
        

class MergeProcess:
    @staticmethod
    def merge_mcp(state: QueryGraphState) -> list[dict]:
        chunk_list = state.get("rrf_chunks", [])
        chunk_info_list = []
        for chunk in chunk_list:
            entity = chunk.get('entity')
            
            chunk_info = \
                {
                    "chunk_id": entity.get('chunk_id'),
                    "text"    : entity.get('content'),
                    "title"   : entity.get('title'),
                    "source"  : "local",
                    "url"     : ""
                }
            
            chunk_info_list.append(chunk_info)
        
        web_search_list = state.get("web_search_docs", [])
        for web_info in web_search_list:
            
            chunk_info = \
                {
                    "chunk_id": "",
                    "text"    : web_info.get("snippet"),
                    "title"   : web_info.get("title"),
                    "source"  : "web",
                    "url"     : web_info.get("url")
                }
            
            chunk_info_list.append(chunk_info)
        
        logger.info(f"完成了网页搜索和本地搜索的合并处理，共 {len(chunk_info_list)} 个")
        return chunk_info_list
    
    @staticmethod
    def rerank_chunk(state: QueryGraphState, chunk_info_list: list[dict]) -> list[dict]:
        rewritten_query = state.get("rewritten_query") or state.get("original_query")
        text_list = [chunk_info['text'] for chunk_info in chunk_info_list]
        questions_pairs = [[rewritten_query, text] for text in text_list]
        
        score_list = reranker.compute_score(sentence_pair_list=questions_pairs)
        
        chunk_score_list = []
        for chunk_info, score in zip(chunk_info_list, score_list):
            chunk_info['score'] = score
            chunk_score_list.append(chunk_info)
        
        chunk_score_list.sort(key=lambda x: x['score'], reverse=True)
        logger.info(f"完成了 chunk 的重排序和打分处理，结果为：{chunk_score_list}")
        
        return chunk_score_list
    
    @staticmethod
    def filter_chunk(chunk_score_list: list[dict]):
        top_k = min(DataDict.RERANK_MAX_TOPK, len(chunk_score_list))
        
        if top_k > DataDict.RERANK_MIN_TOPK:
            for index in range(DataDict.RERANK_MIN_TOPK - 1, top_k - 1):
                first = chunk_score_list[index].get('score', 0.0)
                second = chunk_score_list[index + 1].get('score', 0.0)
                
                gap = first - second
                
                rel = gap / (abs(first) + 1e-6)
                if gap >= DataDict.RERANK_GAP_ABS or rel >= DataDict.RERANK_GAP_RATIO:
                    top_k = index + 1
                    logger.info(f"数据集合 {index} 和 {index + 1} 的位置发生了断崖，结束循环！！")
                    break
        
        result_list = chunk_score_list[:top_k]
        logger.info(f"完成了 chunk 的过滤处理，结果为：{result_list}")
        
        return result_list
                

class AnswerProcess:
    @staticmethod
    def check_answer(state: QueryGraphState) -> bool:
        result = False
        
        answer = state.get("answer")
        is_stream = state.get("is_stream", False)
        if answer:
            if is_stream:
                sse_util.push_to_session(state["session_id"], sse_util.DELTA, {"delta": answer})

            else:
                task_util.set_task_result(task_id=state["session_id"], key="answer", value=answer)
            result = True
        
        return result

    
    @staticmethod
    def generate_prompt(state: QueryGraphState) -> str:
        chunk_list = state.get("reranked_docs", [])
        
        content_list = []
        text_length = 0
        for i in range(len(chunk_list)):
            text = chunk_list[i].get("text")
            source = chunk_list[i].get("source")
            title = chunk_list[i].get("title")
            score = chunk_list[i].get("score")
            
            content = f"[{i + 1}][source={source}][title={title}][score={score}]\n\n{text}"
            if text_length + len(content) > DataDict.MAX_CONTEXT_CHARS:
                logger.info(f"文本长度超过限制，已截断")
                break
            else:
                text_length += len(content)
                content_list.append(content)
        
        history_list = state.get("history", [])
        history_string = ""
        if history_list:
            for i in range(len(history_list)):
                role = history_list[i].get("role")
                text = history_list[i].get("text")
                
                if role == "user" and text:
                    history_string += f"【用户】: {text}\n"
                elif role == "assistant" and text:
                    history_string += f"【助手】: {text}\n"
                
                if text_length > DataDict.MAX_CONTEXT_CHARS:
                    logger.info(f"本次内容停止追加了！已经大于限制长度！")
                    break
        else:
            history_string = "没有历史对话记录！"
        
        item_name_list = state.get("item_names", [])
        item_names_string = ",".join(item_name_list)
        
        question = state.get("rewritten_query") or state.get("original_query")
        
        parser = PromptParser(prompt_path=PathConfig.PROMPT_PATH)
        raw_prompt = parser.get_prompt(key="answer-out")
        
        context = "\n\n".join(content_list)
        prompt = raw_prompt.format(context=context, history=history_string,
                                   question=question, item_names=item_names_string)
        
        logger.info(f"生成综合提示词为：\n{prompt[:16]}")
        return prompt
        
    @staticmethod
    def generate_answer(prompt: str, session_id: str, is_stream: bool = True):
        llm = CloudModelConnect(conf=app_config.model_config)
        llm.connect()
        
        answer = ""
        if is_stream:
            for chunk in llm.client.stream(input=prompt):
                delta = chunk.content
                answer += chunk.content
                sse_util.push_to_session(session_id, sse_util.DELTA, {"delta": delta})

        else:
            answer = llm.invoke(human_prompt=prompt)
            task_util.set_task_result(task_id=session_id, key="answer", value=answer)
            
        logger.info(f"生成答案为：\n{answer[:16]}")
        return answer
    
    @staticmethod
    def extract_images_url(chunk_list: list[dict]) -> list[str]:
        image_pattern = compile(r"!\[.*?\]\((.*?)\)")
        
        image_set = set()
        image_list = []
        for chunk in chunk_list:
            url = chunk.get("url")
            if url and  url.endswith(DataDict.IMAGE_SUFFIX) and url not in image_set:
                image_set.add(url)
                image_list.append(url)
                
            text = chunk.get("text")
            if text:
                images = image_pattern.findall(text)
                if images:
                    for image in images:
                        if image not in image_set:
                            image_set.add(image)
                            image_list.append(image)
        
        logger.info(f"提取的图片链接共 {len(image_list)} 个")
        return image_list
    
    @staticmethod
    def save_history(state: QueryGraphState):
        answer = state.get("answer")
        
        if answer:
            data = \
                {
                    "session_id" : state.get("session_id"),
                    "answer"     : answer,
                    "question"   : state.get("rewritten_query") or state.get("original_query"),
                    "item_names" : state.get("item_names", [])
                }
            
            mongo.insert_data(data_list=[data])
            logger.info(f"保存历史记录为：{data}")

        logger.info(f"完成了本次对话的记录存储！")
        
        
        
if __name__ == '__main__':
    from random import random
    
    # data = mineru_process.get_parse_url(pdf_path_list=["../data/update/3040.pdf", "../data/update/B3-211H.pdf"])
    #
    # datas = {
    #     '3040.pdf'   : 'https://cdn-mineru.openxlab.org.cn/pdf/2026-07-29/b5af3031-8f63-4a15-9889-8dde2158f2de.zip',
    #     'B3-211H.pdf': 'https://cdn-mineru.openxlab.org.cn/pdf/2026-07-29/be6bdab2-41a7-41a4-ac24-e69a80c4dc25.zip'
    # }
    # for file_name, url in datas.items():
    #     mineru_process.save_zip_file(zip_url=url, file_path=f"{PathConfig.OUTPUT_DIR}/{file_name}.zip")
    
    # images = ImageProcess.scan_images(dir_path="../data/output/3040/images")
    # print(images)
    
    # md_path = "../data/output/B3-211H/B3-211H_new.md"
    # md_content = FileUtil.read_text(file_path=md_path)
    # _, _, section_list = DocumentProcess.split_by_title(md_content=md_content, file_title="B3-211H")
    #
    # title_list = [section.get("title") for section in section_list]
    #
    # json_string = dumps(obj=section_list, indent=4, ensure_ascii=False, default=str)
    # print(json_string)
    
    dense_vector = [random() for _ in range(1024)]
    RecognitionProcess.save_item_vector(file_title="", item_name="", dense_vector=dense_vector, sparse_vector=[])
    
    # json_string = dumps(obj=section_list, indent=4, ensure_ascii=False, default=str)
    # print(json_string)
