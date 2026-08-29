#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  connect 
    CreateTime     ：  2026-08-12 15:51:34 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import environ
environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from json import dumps, loads
from typing import Optional, Union

from numpy import ndarray
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from minio import Minio
from minio.deleteobjects import DeleteObject
from pymilvus import MilvusClient, StructFieldSchema, AnnSearchRequest, WeightedRanker
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymongo import MongoClient, ASCENDING
from requests import RequestException
from torch.cuda import device, is_available
from agents.mcp import MCPServerStreamableHttp
from FlagEmbedding import FlagReranker
from config import MilvusConfig, app_config, MinioConfig, CloudModelConfig, EmbedModelConfig, MongoDBConfig, McpConfig, RerankModelConfig
from logger import logger
from util import FileUtil


# Minio 客户端
class MinioConnect:
    def __init__(self, conf: MinioConfig):
        self.endpoint = conf.endpoint
        self.is_secure = conf.is_secure
        self.access_key = conf.access_key
        self.secret_key = conf.secret_key
        self.bucket_name = conf.bucket_name
        self.image_folder = conf.image_folder
        
        self.policy = \
            {
                "Version"  : "2012-10-17",
                "Statement": [{
                    "Effect"   : "Allow",
                    "Principal": {"AWS": ["*"]},        # *表示所有匿名用户（S3兼容标识）
                    "Action"   : ["s3:GetObject"],      # 仅授权文件获取/访问操作
                    "Resource" : [f"arn:aws:s3:::{self.bucket_name}/*"]
                }]
            }
        
        self.client: Optional[Minio] = None
        
    # 连接到 Minio 服务器
    def connect(self) -> None:
        if self.client:
            logger.warning("已连接到 Minio 服务器，无需重复连接 ...... ")
            return
        try:
            self.client = Minio(endpoint=self.endpoint, access_key=self.access_key,
                                secret_key=self.secret_key, secure=self.is_secure)
            logger.debug(f"已连接到 Minio 服务器：{self.access_key}@{self.endpoint}/{self.bucket_name}")
        except Exception as e:
            logger.error(f"连接到 Minio 服务器失败: {e}")
            raise RequestException(f"连接到 Minio 服务器失败: {e}")
        
    # 创建存储桶
    def create_bucket(self, bucket_name: str = None) -> None:
        if not bucket_name:
            bucket_name = self.bucket_name
        
        try:
            if self.client.bucket_exists(bucket_name=bucket_name):
                logger.info(f"存储桶 {bucket_name} 已存在")
            else:
                self.client.make_bucket(bucket_name=bucket_name)
                
                policy = dumps(obj=self.policy)
                self.client.set_bucket_policy(bucket_name=bucket_name, policy=policy)
                
                logger.info(f"存储桶 {bucket_name} 创建成功")
        except Exception as e:
            logger.error(f"存储桶 {bucket_name} 创建失败: {e}")
            raise RequestException(f"存储桶 {bucket_name} 创建失败: {e}")
    
    # 删除存储桶
    def delete_bucket(self, bucket_name: str = None) -> None:
        if not bucket_name:
            bucket_name = self.bucket_name
        
        try:
            if self.client.bucket_exists(bucket_name=bucket_name):
                self.client.remove_bucket(bucket_name=bucket_name)
                logger.info(f"存储桶 {bucket_name} 删除成功")
            else:
                logger.info(f"存储桶 {bucket_name} 不存在")
        except Exception as e:
            logger.error(f"存储桶 {bucket_name} 删除失败: {e}")
            raise RequestException(f"存储桶 {bucket_name} 删除失败: {e}")
    
    # 获取存储桶内的文件列表
    def list_files(self, bucket_name: str = None, file_path: str = None) -> list:
        if not bucket_name:
            bucket_name = self.bucket_name
        
        if file_path:
            prefix = f"{self.image_folder}/{file_path}"
        else:
            prefix = self.image_folder
        
        result = []
        try:
            files = self.client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True)
            result = [file.object_name for file in files]
            logger.debug(f"存储桶 {bucket_name} 内的 {prefix} 共有 {len(result)} 个文件")
        except Exception as e:
            logger.error(f"获取存储桶 {bucket_name} 内的 {prefix} 文件列表失败: {e}")
            raise RequestException(f"获取存储桶 {bucket_name} 内的文件列表失败: {e}")
        finally:
            return result
    
    # 删除存储桶内的文件
    def delete_files(self, file_path_list: list[str], bucket_name: str = None) -> None:
        if not file_path_list:
            logger.warning("删除的文件路径列表为空 ......")
            return
        elif isinstance(file_path_list, str):
            file_path_list = [file_path_list]
        
        if not bucket_name:
            bucket_name = self.bucket_name
        
        delete_object_list = [DeleteObject(name=object_name) for object_name in file_path_list]
        try:
            errors = self.client.remove_objects(bucket_name=bucket_name, delete_object_list=delete_object_list)
            for error in errors:
                logger.warning(f"MinIO 文件删除失败：{error}")
            
            logger.debug(f"共删除存储桶 {bucket_name} 内的 {len(file_path_list)} 个文件")
        except RequestException:
            raise
        except Exception as e:
            logger.error(f"删除存储桶 {bucket_name} 内的文件失败: {e}")
            raise RequestException(f"删除存储桶 {bucket_name} 内的文件失败: {e}")
            
    # 上传文件到 Minio
    def upload_file(self, file_path: str, upload_path: str = None, bucket_name: str = None) -> Optional[str]:
        if not file_path:
            logger.warning("上传的文件路径为空 ......")
            return None
        
        if not upload_path:
            upload_path = FileUtil.get_file_name(file_path)
        
        if not bucket_name:
            bucket_name = self.bucket_name
        
        url = ""
        try:
            response = self.client.fput_object(file_path=file_path, object_name=upload_path, bucket_name=bucket_name)
            protocol = "https" if self.is_secure else "http"
            
            url = f"{protocol}://{self.endpoint}/{self.bucket_name}/{response.object_name}"
            logger.info(f"文件 {file_path} 上传到 Minio：{url}")
        except Exception as e:
            logger.error(f"文件 {file_path} 上传失败: {e}")
            raise RequestException(f"文件 {file_path} 上传失败: {e}")
        finally:
            return url
    
    # 批量化上传图片到 Minio
    def upload_images(self, image_path_list: list[str], upload_dir: str = None, bucket_name: str = None) -> None:
        if not image_path_list:
            logger.warning("上传的文件路径为空 ......")
            return
        
        if not bucket_name:
            bucket_name = self.bucket_name
        
        if not upload_dir:
            upload_dir = self.image_folder
        else:
            upload_dir = f"{self.image_folder}/{upload_dir}"
        
        for image_path in image_path_list:
            file_name  = FileUtil.get_file_name(image_path)
            upload_path = f"{upload_dir}/{file_name}"
            self.upload_file(file_path=image_path, upload_path=upload_path, bucket_name=bucket_name)
            

# 大模型连接
class CloudModelConnect:
    def __init__(self, conf: CloudModelConfig):
        self.url = conf.url
        self.api_key = conf.api_key
        self.name = conf.name
        self.timeout = conf.timeout
        self.temperature = conf.temperature
        self.max_token = conf.max_token
        self.max_retry = conf.max_retry
        self.extra_body = {"enable_thinking": conf.enable_thinking}
        
        
        self.client: Optional[ChatOpenAI] = None
    
    # 连接到大模型服务器
    def connect(self) -> None:
        if self.client:
            logger.warning("已连接到大模型服务器，无需重复连接 ...... ")
            return
        try:
            self.client = ChatOpenAI(base_url=self.url, model=self.name, api_key=self.api_key,
                                     temperature=self.temperature, extra_body=self.extra_body,
                                     max_tokens=self.max_token)
            
            logger.info(f"已连接到大模型服务器：{self.name}@{self.url}")
        except Exception as e:
            logger.error(f"连接到大模型服务器失败: {e}")
            raise RequestException(f"连接到大模型服务器失败: {e}")
    
    # 调用大模型
    def image_invoke(self, image_path: str, prompt: str) -> Union[str, None]:
        image_base64 = FileUtil.image_to_base64(image_path)
        
        prompt_content = { "type": "text", "text": prompt }
        image_content = { "type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"} }
        human_message = HumanMessage(content=[prompt_content, image_content])
        
        summary = ""
        try:
            response = self.client.invoke(input=[human_message])
            summary = response.content
            logger.debug(f"图片 {image_path} 调用成功")
        except Exception as e:
            logger.error(f"图片 {image_path} 调用失败: {e}")
            raise RequestException(f"图片 {image_path} 提示词 {prompt} 调用失败: {e}")
        finally:
            return summary
    
    # 调用大模型
    def invoke(self, human_prompt: str, system_prompt: str = None) -> str:
        if system_prompt:
            messages = [HumanMessage(content=human_prompt), SystemMessage(content=system_prompt)]
        else:
            messages = [HumanMessage(content=human_prompt)]
        
        result = ""
        try:
            response = self.client.invoke(input=messages)
            result = response.content
            if result.startswith("```"):
                result = result[7:-3].strip()
            
            logger.debug(f"调用大模型查询成功：{result[:16]}...")
        except Exception as e:
            logger.error(f"调用大模型失败: {e}")
            raise RequestException(f"调用大模型失败: {e}")
        finally:
            return result


class MilvusConnect:
    def __init__(self, conf: MilvusConfig):
        self.url = conf.url
        self.collection_name = conf.collection_name
        self.auto_id = conf.auto_id
        self.enable_dynamic_field = conf.enable_dynamic_field
        self.dimension = conf.dimension
        self.timeout = conf.timeout
        self.entity_name = conf.entity_name
        self.metric_type = conf.metric_type
        self.index_type = conf.index_type
        self.index_param = conf.index_param
        self.search_param = conf.search_param
        
        
        self.client: Optional[MilvusClient] = None
    
    def __enter__(self):
        self.connect()
        return self
    
    # 退出 with 代码块时关闭连接；返回 False 不吞掉异常
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False
    
    # 连接至 Milvus
    def connect(self) -> None:
        if self.client:
            try:
                # 探活：close() 后 self.client 仍存在但底层连接已失效，需重建
                self.client.list_collections()
                logger.warning("已连接至 Milvus 服务器，无需重复连接 ...... ")
                return
            except Exception:
                logger.warning("Milvus 连接已失效，正在重新建立连接 ......")
                self.client = None
        
        try:
            self.client = MilvusClient(uri=self.url, timeout=self.timeout)
            logger.debug(f"已连接至 Milvus 服务器：{self.url}")
        except Exception as e:
            logger.error(f"连接至 Milvus 服务器失败: {e}")
            raise RequestException(f"连接至 Milvus 服务器失败: {e}")
            
    # 创建集合
    def create_collection(self, field_config_list: list[dict], index_config_list: list[dict],
                          collection_name: str = None) -> None:
        if not collection_name:
            collection_name = self.collection_name
            
        try:
            # 检查集合是否存在
            if self.client.has_collection(collection_name):
                logger.warning(f"已存在名为 {collection_name} 的集合，无需重复创建 ...... ")
            else:
                # 创建集合 Schema：自增主键 + 动态字段，适配灵活的数据存储
                schema = self.client.create_schema(auto_id=self.auto_id,
                                                   enable_dynamic_field=self.enable_dynamic_field)
                # 添加字段
                for field_config in field_config_list:
                    schema.add_field(field_name=field_config.get("field_name"),
                                     datatype=field_config.get("data_type"),
                                     **(field_config.get("params") or {}))
                
                # 构建索引参数：为向量字段创建索引，提升检索性能
                index_params = self.client.prepare_index_params()
                for index_config in index_config_list:
                    index_params.add_index(field_name=index_config.get("field_name"),
                                           index_type=index_config.get("index_type"),
                                           index_name=index_config.get("index_name"),
                                           **(index_config.get("params") or {}))

                self.client.create_collection(collection_name=collection_name, schema=schema,
                                              index_params=index_params, timeout=self.timeout)
                
                self.client.load_collection(collection_name=collection_name)
                logger.info(f"已创建名为 {collection_name} 的集合")
        except Exception as e:
            logger.error(f"创建集合 {collection_name} 失败: {e}")
            raise RequestException(f"创建集合 {collection_name} 失败: {e}")
    
    def insert_data(self, data_list: list[dict], collection_name: str = None) -> dict[str, str]:
        if not collection_name:
            collection_name = self.collection_name
        
        if not data_list:
            logger.warning("插入的数据为空 ......")
            return {}
        
        response = {}
        try:
            self.client.load_collection(collection_name=collection_name)
            
            response = self.client.insert(collection_name=collection_name, data=data_list)
            self.client.load_collection(collection_name=collection_name)
            
            logger.debug(f"已插入 {response.get('insert_count')} 条数据到集合 {collection_name}")
        except Exception as e:
            logger.error(f"插入数据到集合 {collection_name} 失败: {e}")
            raise RequestException(f"插入数据到集合 {collection_name} 失败: {e}")
        finally:
            return response
        
    # 获取字段数据
    def delete_data(self, collection_name: str = None, filter_condition: str = None) -> dict[str, int]:
        if not collection_name:
            collection_name = self.collection_name
        
        response = {}
        try:
            self.client.load_collection(collection_name=collection_name)
            
            response = self.client.delete(collection_name=collection_name, filter=filter_condition)
            logger.debug(f"已从集合 {collection_name} 中删除 {response.get('delete_count')} 条数据")
        except Exception as e:
            logger.error(f"删除集合 {collection_name} 的字段数据失败: {e}")
            raise RequestException(f"删除集合 {collection_name} 的字段数据失败: {e}")
        finally:
            return response
    
    # 查询集合数据
    def __hybrid_request(self, dense_vector: list[float], sparse_vector: list[float], dense_params: dict = None,
                         sparse_params: dict = None, filter_condition: str = None, collection_name: str = None,
                         limit: int = 1000) -> list[dict]:
        
        if not collection_name:
            collection_name = self.collection_name
        
        if not dense_params:
            dense_params = {"metric_type": "COSINE"}
        
        if not sparse_params:
            sparse_params = {"metric_type": "IP"}
        
        result = []
        try:
            self.client.load_collection(collection_name=collection_name)
            
            dense_response = AnnSearchRequest(data=[dense_vector], anns_field="dense_vector",
                                              param=dense_params, expr=filter_condition, limit=limit)
            
            sparse_response = AnnSearchRequest(data=[sparse_vector], anns_field="sparse_vector",
                                               param=sparse_params, expr=filter_condition, limit=limit)
            
            result = [dense_response, sparse_response]
            logger.info(f"查询 {len(result)} 条数据完成 ......")
        except Exception as e:
            logger.error(f"数据查询失败: {e}")
            raise RequestException(f"数据查询失败: {e}")
        finally:
            return result
    
    def hybrid_query(self, dense_vector: list[float], sparse_vector: list[float], filter_condition: str = None,
                     collection_name: str = None, ranker_weights: tuple = (0.5, 0.5), norm_score: bool = False,
                     hybrid_request=None, limit: int = 5, output_fields: list[str] = None, search_params=None) -> list[list[dict[str, any]]]:
        
        if not collection_name:
            collection_name = self.collection_name
        
        if output_fields is None:
            output_fields = ["item_name"]
        
        rerank = WeightedRanker(ranker_weights[0], ranker_weights[1], norm_score=norm_score)
        
        if not hybrid_request:
            hybrid_request = self.__hybrid_request(dense_vector=dense_vector, sparse_vector=sparse_vector,
                                                   filter_condition=filter_condition, collection_name=collection_name,
                                                   limit=limit)
        
        result = []
        try:
            self.client.load_collection(collection_name=collection_name)
            
            result = self.client.hybrid_search(collection_name=collection_name, reqs=hybrid_request, ranker=rerank,
                                               limit=limit, output_fields=output_fields, search_params=search_params)
            logger.info(f"数据查询完成，返回 {len(result)} 条数据")
        except Exception as e:
            logger.error(f"数据查询失败: {e}")
            raise RequestException(f"数据查询失败: {e}")
        finally:
            return result
        
    # 关闭连接
    def close(self) -> None:
        if self.client:
            self.client.close()
            self.client = None
            logger.debug("已关闭 Milvus 连接")
        else:
            logger.warning("未连接至 Milvus ...... ")


class EmbedConnect:
    def __init__(self, conf: EmbedModelConfig):
        self.model_path = conf.model_path
        self.device = "cuda" if is_available() else "cpu"
        self.dimension = conf.dimension
        self.enable_fp16 = conf.enable_fp16
        
        self.client: Optional[BGEM3EmbeddingFunction] = None
    
    # 连接至 Embed 模型
    def connect(self) -> None:
        if self.client:
            logger.warning("已连接至 Embed 服务器，无需重复连接 ...... ")
            return
        
        try:
            self.client = BGEM3EmbeddingFunction(model_name=self.model_path, device=self.device,
                                                 use_fp16=self.enable_fp16, normalize_embeddings=True)
            
            logger.info(f"Embed 模型初始化完成：{self.model_path}")
        except Exception as e:
            logger.error(f"Embed 模型初始化失败: {e}")
            raise RequestException(f"Embed 模型初始化失败: {e}")
    
    # 生成嵌入向量
    def generate_vector(self, text_list: list[str]) -> dict[str, list[float]]:
        if not self.client:
            self.connect()
        
        if not text_list:
            logger.warning(f"生成向量入参不合法，text_list 必须为非空列表")
            raise ValueError("参数 text_list 必须是包含文本的非空列表")
        
        if isinstance(text_list, str):
            text_list = [text_list]
        
        result_list = {}
        try:
            # 模型编码生成向量，返回 dense（稠密向量）和 sparse（CSR格式稀疏向量）
            embedding_list = self.client.encode_documents(documents=text_list)
            length = len(text_list)
            logger.debug(f"模型编码完成，开始解析稀疏向量格式，共{length}条")
            
            # 初始化稀疏向量处理结果，解析为字典格式（适配序列化/存储）
            vector_list = []
            for i in range(length):
                start_index= embedding_list["sparse"].indptr[i]
                end_index= embedding_list["sparse"].indptr[i + 1]
                
                # 提取第 i 个文本的稀疏向量索引
                sparse_index = embedding_list["sparse"].indices[start_index: end_index].tolist()
                
                # 提取第 i 个文本的稀疏向量权重
                sparse_data = embedding_list["sparse"].data[start_index: end_index].tolist()
                
                # 构造 特征索引: 归一化权重的稀疏向量字典
                sparse_dict = {k: v for k, v in zip(sparse_index, sparse_data)}
                vector_list.append(sparse_dict)
                
            # 嵌套列表，与输入文本一一对应
            dense_list = [embedding.tolist() for embedding in embedding_list["dense"]]
            
            result_list = {"dense": dense_list, "sparse": vector_list}
            logger.info(f"{len(text_list)} 条文本向量生成完成")
        except Exception as e:
            logger.error(f"嵌入向量生成失败: {e}")
            raise RequestException(f"嵌入向量生成失败: {e}")
        finally:
            return result_list
    
    
# MongoDB 客户端
class MongoConnect:
    def __init__(self, conf: MongoDBConfig):
        self.protocol = conf.protocol
        self.host = conf.host
        self.port = conf.port
        self.username = conf.user
        self.password = conf.password
        self.database = conf.database
        self.collection = conf.collection
        
        self.client: Optional[MongoClient] = None
    
    # 连接至 MongoDB
    def __enter__(self):
        if not self.client:
            self.connect()
        return self
    
    # 关闭连接
    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()
    
    # 连接至 MongoDB
    def connect(self) -> None:
        if self.client:
            logger.warning("已连接至 MongoDB，无需重复连接 ...... ")
            return
        
        try:
            url= f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
            self.client = MongoClient(url)
            logger.info(f"已连接至 MongoDB：{self.host}:{self.port}")
        except Exception as e:
            logger.error(f"连接 MongoDB 失败: {e}")
            raise RequestException(f"连接 MongoDB 失败: {e}")
    
    # 创建集合
    def create_collection(self, collection_name: str = None) -> None:
        if not collection_name:
            collection_name = self.collection
        
        try:
            collection = self.client[self.database][collection_name]
            collection.create_index(keys=[("session_id", 1), ("ts", -1)])
            logger.info(f"集合 {collection_name} 创建完成 ......")
        except Exception as e:
            logger.error(f"集合 {collection_name} 创建失败: {e}")
            raise RequestException(f"集合 {collection_name} 创建失败: {e}")
    
    # 插入数据
    def insert_data(self, data_list: list[dict], collection_name: str = None) -> dict[str, str]:
        if not collection_name:
            collection_name = self.collection
        
        result = {}
        if not data_list:
            logger.warning("插入的数据为空 ......")
            return result
        
        try:
            collection = self.client[self.database][collection_name]
            
            response = collection.insert_many(documents=data_list)
            result = {"inserted_ids": response.inserted_ids}
            
            logger.info(f"{len(data_list)} 条数据插入完成 ......")
        except Exception as e:
            logger.error(f"数据插入失败: {e}")
            raise RequestException(f"数据插入失败: {e}")
        finally:
            return result
    
    def update_data(self, filter_condition: dict[str, any], update_data: dict[str, any], collection_name: str = None) -> dict[str, int]:
        if not collection_name:
            collection_name = self.collection
        
        result = {}
        try:
            collection = self.client[self.database][collection_name]
            response = collection.update_many(filter=filter_condition, update=update_data)
            result = {"modified_count": response.modified_count}
            
            logger.info(f"更新 {response.modified_count} 条数据完成 ......")
        except Exception as e:
            logger.error(f"数据更新失败: {e}")
            raise RequestException(f"数据更新失败: {e}")
        finally:
            return result
    
    # 删除数据
    def delete_data(self, filter_condition: dict[str, any], collection_name: str = None) -> dict[str, int]:
        if not collection_name:
            collection_name = self.collection
        
        result = {}
        try:
            collection = self.client[self.database][collection_name]
            response = collection.delete_many(filter=filter_condition)
            result = {"deleted_count": response.deleted_count}
            
            logger.info(f"删除 {response.deleted_count} 条数据完成 ......")
        except Exception as e:
            logger.error(f"数据删除失败: {e}")
            raise RequestException(f"数据删除失败: {e}")
        finally:
            return result
    
    # 清空数据
    def clear_data(self, collection_name: str = None):
        self.delete_data(filter_condition={}, collection_name=collection_name)
    
    # 查询数据
    def query_data(self, filter_condition: dict[str, any], collection_name: str = None, limit: int = 1000) -> list[dict]:
        if not collection_name:
            collection_name = self.collection
        
        result = []
        try:
            collection = self.client[self.database][collection_name]
            response = collection.find(filter=filter_condition).sort(key_or_list="ts", direction=ASCENDING).limit(limit=limit)
            result = [data for data in response]
            
            # MongoDB 文档中的 _id 为 ObjectId 类型，Pydantic/FastAPI 无法直接序列化，统一转为字符串
            for data in result:
                if "_id" in data:
                    data["_id"] = str(data["_id"])
            
            logger.info(f"查询 {len(result)} 条数据完成 ......")
        except Exception as e:
            logger.error(f"数据查询失败: {e}")
            raise RequestException(f"数据查询失败: {e}")
        finally:
            return result
    
    # 关闭连接
    def close(self):
        self.client.close()


class McpConnect:
    def __init__(self, conf: McpConfig):
        self.name = conf.name
        self.url = conf.url
        self.api_key = conf.api_key
        self.count = conf.count
        self.tool = conf.tool
        self.max_retry = conf.max_retry
        self.timeout = conf.timeout
        
        self.client: Optional[MCPServerStreamableHttp] = None
    
    async def __aenter__(self):
        if not self.client:
            await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.client:
            await self.close()
            
    async def connect(self):
        if self.client:
            logger.warning("已连接至 MCP，无需重复连接 ...... ")
            return
        
        try:
            params = \
                {
                    "url"    : self.url,
                    "headers": {"Authorization": f"Bearer {self.api_key}"},
                    "timeout": self.timeout,
                }
            
            self.client = MCPServerStreamableHttp(name=self.name, params=params, max_retry_attempts=self.max_retry)
            await self.client.connect()
            
            logger.info(f"已连接至 MCP：{self.url}")
        except Exception as e:
            logger.error(f"连接 MCP 失败: {e}")
            raise RequestException(f"连接 MCP 失败: {e}")
    
    async def query_data(self, query: str = None, tool_name: str = None,
                         count: int = None) -> dict[str, Union[str, list[dict]]]:
        if not tool_name:
            tool_name = self.tool
        
        if not count:
            count = self.count
        
        if not self.client:
            await self.connect()
        
        result = {}
        try:
            arguments = { "query": query, "count": count }
            
            response = await self.client.call_tool(tool_name=tool_name, arguments=arguments)
            text = response.content[0].text
            result = loads(s=text)
            
            logger.debug(f"使用 MCP 服务查询数据完成 ......")
        except Exception as e:
            logger.error(f"数据查询失败: {e}")
            raise RequestException(f"数据查询失败: {e}")
        finally:
            await self.close()
            return result
    
    async def close(self):
        if self.client:
            await self.client.cleanup()


class RerankConnect:
    def __init__(self, conf: RerankModelConfig):
        self.model_path = conf.model_path
        self.device = "cuda" if is_available() else "cpu"
        self.dimension = conf.dimension
        self.enable_fp16 = conf.enable_fp16
        
        self.client: Optional[FlagReranker] = None
    
    # 连接至 Embed 模型
    def connect(self) -> None:
        if self.client:
            logger.warning("已连接至 Embed 服务器，无需重复连接 ...... ")
            return
        
        try:
            self.client = FlagReranker(model_name_or_path=self.model_path, device=self.device,
                                       use_fp16=self.enable_fp16)
            
            logger.info(f"Embed 模型初始化完成：{self.model_path}")
        except Exception as e:
            logger.error(f"Embed 模型初始化失败: {e}")
            raise RequestException(f"Embed 模型初始化失败: {e}")
    
    # 重排序
    def compute_score(self, sentence_pair_list: list[tuple[str, str]], normalize: bool = True) -> ndarray:
        if not self.client:
            self.connect()
       
        result_list = []
        try:
            # 模型编码生成向量，返回 dense（稠密向量）和 sparse（CSR格式稀疏向量）
            result_list = self.client.compute_score(sentence_pairs=sentence_pair_list, normalize=normalize)
            
            logger.debug(f"模型编码完成，开始解析稀疏向量格式，共{len(result_list)}条")
        except Exception as e:
            logger.error(f"嵌入向量生成失败: {e}")
            raise RequestException(f"嵌入向量生成失败: {e}")
        finally:
            return result_list


minio = MinioConnect(conf=app_config.minio_config)
minio.connect()

embed = EmbedConnect(conf=app_config.embed_config)
embed.connect()

reranker = RerankConnect(conf=app_config.rerank_config)
reranker.connect()

mongo = MongoConnect(conf=app_config.mongo_config)
mongo.connect()


mcp = McpConnect(conf=app_config.mcp_config)


if __name__ == '__main__':
    from asyncio import run
    
    # minio.delete_bucket("test-1")
    # minio.create_bucket()
    # files = minio.list_files()
    # print(f"files = {files}")
    
    # minio.delete_files(file_path_list=["aaa"])
    # file_path = "../data/output/B3-211H/images/1b9acf872c0801d49d9a1a265b9a5a1408c91e2369e1f4ce80ab5d3383a52248.jpg"
    # url = minio.upload_file(file_path=file_path)
    # print(f"url = {url}")
    # minio.upload_images(image_path_list=[file_path], upload_dir="test")
    
    # model = ModelConnect(conf=app_config.model_config)
    # model.connect()
    #
    # response = model.client.invoke("hello")
    # print(f"response = {response}")
    
    # embed = EmbedConnect(conf=app_config.embed_config)
    # embed.connect()
    
    # result_dict = embed.generate_vector(text_list=["hello", "world"])
    # result = dumps(obj=result_dict, indent=4, sort_keys=True)
    # print(f"result = {result}")
    
    # milvus.create_collection()
    # milvus.insert_data(data_list=[{"id": 1, "vector": [0.1, 0.2, 0.3]}, {"id": 2, "vector": [0.4, 0.5, 0.6]}])
    # milvus.delete_data(filter_condition="id in [1, 2]")
    # milvus.close()
    
    # with MongoConnect(conf=app_config.mongo_config) as mongo:
    #     mongo.create_collection(collection_name="test")
    
    response = run(mcp.query_data(query="今天的天气怎么样？"))
    print(f"response = {response}")
    
