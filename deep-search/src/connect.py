#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  client 
    CreateTime     ：  2026-08-08 16:53:45 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from typing import Optional, Any
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from mysql.connector import Error
from mysql.connector.pooling import CNX_POOL_MAXSIZE, MySQLConnectionPool, PooledMySQLConnection
from ragflow_sdk import RAGFlow, DataSet, Chat
from tavily import TavilyClient
from config import MysqlConfig, ModelConfig, TavilyConfig, RagFlowConfig, app_config
from logger import logger
from util import FileUtil


# Mysql 连接
class MysqlConnect:
    # 初始化数据
    def __init__(self, conf: MysqlConfig) -> None:
        self.host = conf.host
        self.port = conf.port
        self.user = conf.user
        self.password = conf.password
        self.database = conf.database
        self.charset = conf.charset
        self.timeout = conf.timeout
        self.auto_commit = conf.auto_commit
        self.max_connections = conf.max_connection
        self.print_sql = conf.print_sql
        
        self.uri = f"{conf.user}@{conf.host}:{conf.port}/{conf.database}?charset={conf.charset}"
        self.pool: Optional[MySQLConnectionPool] = None
        self.client: Optional[PooledMySQLConnection] = None
        
    def __enter__(self):
        if self.pool is None:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        
        if exc_type:
            logger.info(f"=============== mysql 退出异常: ===============")
            logger.info(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 建立连接
    def connect(self) -> None:
        if self.pool is not None:
            return
        
        try:
            pool_size = min(self.max_connections, CNX_POOL_MAXSIZE)
            if pool_size < self.max_connections:
                logger.warning(f"最大连接数 {self.max_connections} 超过驱动上限 {CNX_POOL_MAXSIZE}，已调整为 {pool_size}")
            
            self.pool = MySQLConnectionPool(pool_name=f"mysql_pool_{self.host}_{self.port}",
                                            pool_size=pool_size, host=self.host, port=self.port,
                                            user=self.user, password=self.password, database=self.database,
                                            charset=self.charset, connect_timeout=self.timeout,
                                            autocommit=self.auto_commit)
            self.client = self.pool.get_connection()
            logger.info(f"=============== 连接到 {self.uri}，最大连接数 = {pool_size} ===============")
        except Error as e:
            logger.error(f" mysql 连接异常：{e}")
    
    # 查询数据
    def query_data(self, query: str, params: tuple = None, print_query: bool = False) -> Optional[list[dict]]:
        if self.pool is None:
            self.connect()
        
        if print_query or self.print_sql:
            logger.info(f"==================== sql ==>\n{query}\n========================================")
        
        result_list = []
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as mysql_cursor:
                    mysql_cursor.execute(operation=query, params=params)
                    result_list = list(mysql_cursor.fetchall())
        except Exception as e:
            logger.error(f"sql 查询异常：{e}")
        finally:
            return result_list
        
    # 关闭数据库连接
    def close(self) -> None:
        try:
            if self.client is not None:
                self.client.close()
                self.client = None
            logger.info(f"=============== {self.uri} 的连接已关闭 ===============")
        except Error as e:
            logger.error(f"mysql 关闭异常：{e}")
    

# 大模型配置
class CloudModelConnect:
    def __init__(self, conf: ModelConfig) -> None:
        self.url = conf.url
        self.api_key = conf.api_key
        self.name = conf.name
        self.timeout = conf.timeout
        self.temperature = conf.temperature
        self.max_token = conf.max_token
        
        self.llm: Optional[BaseChatModel] = None
    
    # 连接模型
    def connect(self) -> None:
        if self.llm:
            return
        
        try:
            self.llm = init_chat_model(model=self.name, base_url=self.url, api_key=self.api_key,
                                  temperature=self.temperature, timeout=self.timeout)
            logger.debug(f"=============== 云模型 {self.name} 加载成功 ===============")
        except Exception as e:
            logger.error(f"=============== 模型加载异常：{e} ===============")
    
    # 调用模型
    async def invoke(self, prompt: str) -> str:
        if self.llm is None:
            await self.connect()
        
        result = ""
        try:    
            response = self.llm.invoke(input=prompt)
            result = response.content
            logger.debug(f"=============== 模型调用成功 ===============")
        except Exception as e:
            logger.error(f"=============== 模型调用异常：{e} ===============")
        finally:
            return result
    
    # 异步调用
    async def ainvoke(self, prompt: str) -> AIMessage:
        if self.llm is None:
            await self.connect()
            
        response = await self.llm.ainvoke(input=prompt)
        return response


# Tavily 连接
class TavilyConnect:
    def __init__(self, conf: TavilyConfig) -> None:
        self.base_url = conf.base_url
        self.api_key = conf.api_key
        self.search_depth = conf.search_depth
        self.include_answer = conf.include_answer
        self.topic = conf.topic
        self.max_results = conf.max_results
        self.include_raw_content = conf.include_raw_content
        
        self.client: Optional[TavilyClient] = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        if exc_type:
            logger.info(f"=============== Tavily 退出异常: ===============")
            logger.info(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 建立连接
    def connect(self) -> None:
        if self.client is not None:
            return
        
        try:
            self.client = TavilyClient(api_base_url=self.base_url, api_key=self.api_key)
        except Exception as e:
            logger.error(f"=============== Tavily 连接异常：{e} ===============")
    
    # 搜索
    def search(self, query: str) -> dict[str, Any]:
        if self.client is None:
            self.connect()
        
        result = {}
        try:
            response = self.client.search(query=query, search_depth=self.search_depth, topic=self.topic,
                                          include_answer=self.include_answer, max_results=self.max_results,
                                          include_raw_content=self.include_raw_content)
            logger.debug(response)
            result = response.get("results", [])
        except Exception as e:
            logger.error(f"=============== Tavily 搜索异常：{e} ===============")
        finally:
            return result
    
    # 关闭连接
    def close(self) -> None:
        try:
            self.client.close()
            logger.info(f"=============== Tavily 连接已关闭 ===============")
        except Exception as e:
            logger.error(f"=============== Tavily 关闭异常：{e} ===============")


# RAGFlow 连接
class RagFlowConnect:
    def __init__(self, conf: RagFlowConfig) -> None:
        self.base_url = conf.base_url
        self.api_key = conf.api_key
        self.embedding_model = conf.embedding
        self.knowledge_base = conf.knowledge_base
        self.knowledge_description = conf.knowledge_description
        self.assistant_name = conf.assistant_name
        self.session_name = conf.session_name
        self.is_stream = conf.is_stream
        
        self.client: Optional[RAGFlow] = None
        
    def __enter__(self):
        if self.client is None:
            self.connect()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type:
            logger.info(f"=============== RAGFlow 退出异常: ===============")
            logger.info(f"type = {exc_type}, vlue = {exc_val}")
            return True
        else:
            return False
    
    # 建立连接
    def connect(self) -> None:
        try:
            self.client = RAGFlow(api_key=self.api_key, base_url=self.base_url)
            logger.debug(f"=============== RAGFlow 连接成功 ===============")
        except Exception as e:
            logger.error(f"=============== RAGFlow 连接异常：{e} ===============")
    
    # 创建知识库
    def create_dataset(self, database_name: str = None, description: str = None, embedding_model: str = None) -> None:
        if database_name is None:
            database_name = self.knowledge_base
        
        if description is None:
            description = self.knowledge_description
        
        if embedding_model is None:
            embedding_model = "default"
            
        try:
            database_id = self.query_dataset_id(database_name=database_name)
            if database_id:
                logger.warning(f"知识库 {database_name} 已存在")
            else:
                response = self.client.create_dataset(name=database_name, description=description,
                                                      embedding_model=embedding_model)
                
                logger.debug(f"知识库 {database_name} 创建成功：{response.to_json()}，{response.id}")
        except Exception as e:
            logger.error(f"=============== RAGFlow 创建数据集异常：{e} ===============")
    
    # 获取知识库
    def get_dataset(self, database_name: str = None) -> DataSet:
        if database_name is None:
            database_name = self.knowledge_base
        
        response = {}
        try:
            response = self.client.get_dataset(name=database_name)
            logger.debug(f"知识库获取成功：{database_name}: {response.to_json()}")
        except Exception as e:
            logger.error(f"=============== RAGFlow 获取数据集异常：{e} ===============")
        finally:
            return response
    
    # 查询知识库 ID
    def query_dataset_id(self, database_name: str = None) -> str:
        if database_name is None:
            database_name = self.knowledge_base
        
        database_id = ""
        try:
            response = self.get_dataset(database_name=database_name)
            database_id = response.id
            logger.debug(f"知识库查询成功：{database_name}: {database_id}")
        except Exception as e:
            logger.error(f"=============== RAGFlow 查询数据集异常：{e} ===============")
        finally:
            return database_id
    
    # 上传文件
    def upload_file(self, file_path_list: list[str], database_name: str = None) -> None:
        if not database_name:
            database_name = self.knowledge_base
        
        document_list = []
        for file_path in file_path_list:
            file_name = FileUtil.get_file_name(file_path=file_path)
            display_name = f"{database_name}-{file_name}"
            
            if file_name:
                with open(file=file_path, mode='rb') as f:
                    blob = f.read()
                    document = \
                        {
                            "display_name": display_name,
                            "name"        : file_name,
                            "blob"        : blob
                        }
                    document_list.append(document)
            else:
                logger.warning(f"文件路径为空，或文件不存在")
        try:
            database = self.get_dataset(database_name=database_name)
            
            if document_list and database:
                database.upload_documents(document_list=document_list)
                logger.info(f"文件成功上传：共上传 {len(document_list)} 个文件")
        except Exception as e:
            logger.error(f"=============== RAGFlow 上传文件异常：{e} ===============")
    
    # 获取所有助手
    def get_assistant(self, assistant_name: str = None) -> Chat:
        if not assistant_name:
            assistant_name = self.assistant_name
        
        result = None
        try:
            response = self.client.list_chats(name=assistant_name)
            result = response[0]
            logger.debug(f"助手获取成功：{assistant_name}: {result.to_json()}")
        except Exception as e:
            logger.error(f"=============== RAGFlow 获取助手异常：{e} ===============")
        finally:
            return result
    
    # 获取助手的知识库
    def get_assistant_knowledge(self, assistant_name: str = None) -> dict[str, str]:
        if not assistant_name:
            assistant_name = self.assistant_name
        
        result = {}
        try:
            response = self.get_assistant(assistant_name=assistant_name)
            
            if response:
                result = {dataset.get("id"): dataset.get("name") for dataset in response.datasets}
        except Exception as e:
            logger.error(f"=============== RAGFlow 获取助手知识库异常：{e} ===============")
        finally:
            return result
        
    # 会话聊天
    def session_chat(self, question: str, session_name: str = None, assistant_name: str = None) -> dict[str, Any]:
        if not assistant_name:
            assistant_name = self.assistant_name
        
        if not session_name:
            session_name = f"{assistant_name}-{self.session_name}-tmp"
        
        result = ""
        try:
            assistant = self.get_assistant(assistant_name=assistant_name)
            session = assistant.create_session(name=session_name)
            
            response_stream = session.ask(question=question, stream=self.is_stream)
            
            for stream in response_stream:
                result = stream.content
                logger.debug(f"会话聊天中：{result}")
            
            assistant.delete_sessions(ids=[session.id])
            logger.info(f"会话聊天成功：{question}")
        except Exception as e:
            logger.error(f"=============== RAGFlow 会话聊天异常：{e} ===============")
        finally:
            return result


# 创建数据库连接
mysql_connect = MysqlConnect(conf=app_config.mysql_config)
mysql_connect.connect()

# 创建Tavily连接
tavily_connect = TavilyConnect(conf=app_config.tavily_config)
tavily_connect.connect()

# 创建云模型连接
cloud_model_connect = CloudModelConnect(conf=app_config.model_config)
cloud_model_connect.connect()

# 知识库
rag_flow_connect = RagFlowConnect(conf=app_config.ragflow_config)
rag_flow_connect.connect()

    
if __name__ == '__main__':
    from json import dumps
    
    sql = "select * from drugs limit 10"
    with MysqlConnect(conf=app_config.mysql_config) as mysql:
        results = mysql.query_data(query=sql, print_query=True)
    
    print(f"results = {results}")
    for result in results:
        js = dumps(obj=result, indent=4, ensure_ascii=False, default=str)
        print(js)

    # async def model_test():
    #     model = CloudModelClient(conf=app_config.model_config)
    #
    #     response = await model.invoke("hello world")
    #     print(f"response = {response}")
    #
    # asyncio.run(model_test())
    #
    # with TavilyConnect(conf=app_config.tavily_config) as tavily:
    #     response = tavily.search("hello world")
    #     response = dumps(obj=response, indent=4, ensure_ascii=False)
    #     print(f"response = {response}")
    #
    # with RagFlowConnect(conf=app_config.ragflow_config) as rag:
    #     rag.upload_file(file_path_list=["../doc/深度搜索.md", "../doc/深度搜索.pdf"],
    #                     database_name="test")
    #
    #     assitant = rag.get_assistant(assistant_name="空调安装助手", database_name="test")
    #     js = dumps(obj=assitant.to_json(), indent=4, ensure_ascii=False)
    #     print(js)
    #     #
    #     knowledge = rag.get_assistant_knowledge(assistant_name="空调安装助手")
    #     print(f"knowledge = {knowledge}")
    #     response = rag.session_chat(question="怎么安装空调，给出详细的步骤", session_name="test", assistant_name="空调安装助手")
    #     print(f"response = {response}")
    
