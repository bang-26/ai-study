#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph  
    FileName       ：  web.py 
    CreateTime     ：  2026-07-05 16:43:30 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_neo4j import Neo4jVector
from pydantic import BaseModel
from uvicorn import run
from fastapi import FastAPI
from langchain_community.embeddings import HuggingFaceEmbeddings
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from neo4j_graphrag.types import SearchType
from connnect import GraphConnection
from config import WebConfig, Neo4jConfig


class Question(BaseModel):
    message: str


class Answer(BaseModel):
    message: str


class IndexUtil:
    def __init__(self):
        self.graph = GraphConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                                     password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
        
        self.embedding_model = HuggingFaceEmbeddings(model_name=WebConfig.EMBED_MODEL, encode_kwargs=WebConfig.ENCODE_KWARGS)
    
    # 创建全文索引
    def create_full_text_index(self, name: str, label: str, properties: str = "name"):
        cypher = f"CREATE FULLTEXT INDEX {name} IF NOT EXISTS FOR (n:{label}) ON EACH [n.{properties}]"
        result = self.graph.query_data(query=cypher)
    
    # 创建向量索引
    def create_vector_index(self, name: str, label: str, source_property: str, embedding_property: str) -> None:
        embedding_dim = self.__generate_embedding(label=label, source=source_property, embedding=embedding_property)
        
        cypher = f"""
                    CREATE VECTOR INDEX {name} IF NOT EXISTS
                    FOR (n:{label})
                    ON  n.{embedding_property}
                    OPTIONS {{ indexConfig: {{
                        `vector.dimensions`: {embedding_dim},
                        `vector.similarity_function`: 'cosine'
                        }}
                    }}
                  """
        self.graph.query_data(query=cypher)
    
    # 内部方法：生成嵌入向量，并添加到节点属性中，返回向量维度
    def __generate_embedding(self, label: str, source: str, embedding: str) -> int:
        # 1. 查询所有节点对应的源属性值，作为模型的输入；还需要查出节点 id
        cypher = f"MATCH (n:{label}) RETURN n.{source} AS text, id(n) AS id"
        result_list = self.graph.query_data(query=cypher)
        
        # 2. 获取查询结果中的文本内容
        doc_list = [result["text"] for result in result_list]
        
        # 3. 调用嵌入模型，得到嵌入向量
        embedding_list = self.embedding_model.embed_documents(doc_list)
        
        # 4. 将 id 和嵌入向量组合成字典形式
        batch_list = []
        for result, embedding in zip(result_list, embedding_list):
            item = {"id": result["id"], "embedding": embedding}
            batch_list.append(item)
        
        # 5. 执行cypher，按 id 查节点，写入新的嵌入向量属性
        cypher = f"UNWIND $batch AS item MATCH (n:{label}) WHERE id(n) = item.id SET n.{embedding} = item.embedding"
        r = self.graph.query_data(query=cypher, params={"batch": batch_list})
        return len(embedding_list[0])
    
    # 内部方法：创建索引
    def create_index(self) -> None:
        self.create_full_text_index("trademark_fulltext_index", "Trademark", "name")
        # self.create_vector_index("trademark_vector_index", "Trademark", "name", "embedding")
        
        self.create_full_text_index('spu_fulltext_index', 'SPU', 'name')
        self.create_vector_index('spu_vector_index', 'SPU', 'name', 'embedding')
        self.create_full_text_index('sku_fulltext_index', 'SKU', 'name')
        self.create_vector_index('sku_vector_index', 'SKU', 'name', 'embedding')
        
        self.create_full_text_index('category1_fulltext_index', 'Category1', 'name')
        self.create_vector_index('category1_vector_index', 'Category1', 'name', 'embedding')
        self.create_full_text_index('category2_fulltext_index', 'Category2', 'name')
        self.create_vector_index('category2_vector_index', 'Category2', 'name', 'embedding')
        self.create_full_text_index('category3_fulltext_index', 'Category3', 'name')
        self.create_vector_index('category3_vector_index', 'Category3', 'name', 'embedding')
        
        
class ChatService:
    def __init__(self):
        self.graph = GraphConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                                     password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
        
        self.embedding_model = HuggingFaceEmbeddings(model_name=WebConfig.EMBED_MODEL,
                                                     encode_kwargs=WebConfig.ENCODE_KWARGS)
    
        self.llm = ChatDeepSeek(model=WebConfig.DEEP_SEEK_MODEL, api_key=WebConfig.API_KEY)
        
        self.__gen_vector_dict()
        
        self.json_parser = JsonOutputParser()
        self.str_parser = StrOutputParser()
    
    # 核心聊天服务流程
    def chat(self, question: str) -> str:
        cypher = self.__generate_cypher(question, self.graph.schema)
        cypher_query = cypher['cypher_query']
        entities_to_align = cypher['entities_to_align']
        entities = self.__entity_align(entities_to_align)
        params = {entity['param_name']: entity['entity'] for entity in entities}
        query_result = self.graph.query_data(query=cypher_query, params=params)
        answer = self.__generate_answer(question=question, query_result=query_result)
        return answer
    
    #  内部方法：生成向量索引
    def __gen_vector(self, name: str) -> Neo4jVector:
        vector = Neo4jVector.from_existing_index(
                embedding=self.embedding_model,
                index_name=f"{name.lower()}_vector_index",
                search_type=SearchType.HYBRID,
                keyword_index_name=f"{name.lower()}_fulltext_index",
                url=f"neo4j://{Neo4jConfig.HOST}:{Neo4jConfig.PORT}/{Neo4jConfig.DATABASE}",
                username=Neo4jConfig.USER,
                password=Neo4jConfig.PASSWORD,
        )
        
        return vector
    
    # 内部方法：生成向量索引
    def __gen_vector_dict(self) -> None:
        self.vector_dict = {}
        
        # index_list = ["Trademark", "SPU", "SKU", "Category1", "Category2", "Category3"]
        index_list = ["SPU", "SKU", "Category1", "Category2", "Category3"]
        for index in index_list:
            vector = self.__gen_vector(name=index)
            self.vector_dict[index] = vector
    
    # 内部方法：生成cypher
    def __generate_cypher(self, question: str, schema_info: str):
        template = PromptTemplate(input_variables=WebConfig.CYPHER_VARIABLES, template=WebConfig.CYPHER_TEMPLET)
        cypher_prompt = template.format(question=question, schema_info=schema_info)
        answer = self.llm.invoke(input=cypher_prompt)
        cypher = self.json_parser.invoke(input=answer)
        return cypher
    
    # 内部方法：使用向量+关键词检索修正实体名称
    def __entity_align(self, entities_to_align: list[dict[str, str]]) -> list[dict[str, str]]:
        for node in entities_to_align:
            if node['label'] in self.vector_dict:
                results = self.vector_dict[node['label']].similarity_search(node['entity'], k=1)
                if results:
                    node['entity'] = results[0].page_content
        return entities_to_align

    # 将 Cypher 查询结果生成自然语言答案
    def __generate_answer(self, question: str, query_result: list[dict[str, str]]) -> str:
        template = PromptTemplate(input_variables=WebConfig.ANSWER_VARIABLES, template=WebConfig.ANSWER_TEMPLET)
        prompt = template.format(question=question, query_result=query_result)
        answer = self.llm.invoke(prompt)
        result = self.str_parser.invoke(answer)
        return result
    
    
app = FastAPI()
app.mount(path=WebConfig.STATIC_PATH, app=StaticFiles(directory=WebConfig.STATIC_DIR), name=WebConfig.STATIC_NAME)

chat = ChatService()


@app.get("/")
def read_root() -> RedirectResponse:
    return RedirectResponse("static/index.html")


@app.post("/api/chat")
def read_item(question: Question) -> Answer:
    result = chat.chat(question=question.message)
    return Answer(message=result)


if __name__ == "__main__":
    run(app=WebConfig.APP_NAME, host=WebConfig.HOST, port=WebConfig.PORT, reload=WebConfig.IS_RELOAD)
