#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  service 
    CreateTime     ：  2026-07-20 20:37:31 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import makedirs, remove
from os.path import basename, exists, splitext
from time import sleep, time
from typing import Any, Union

from aiofiles.tempfile import NamedTemporaryFile
from fastapi import HTTPException, UploadFile
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from starlette.concurrency import run_in_threadpool
from tqdm import tqdm

from config import CloudModelConfig, DataDict, KnowledgeConfig, PathConfig, VectorRepositoryConfig
from crawler import KnowledgeCrawler
from entry import CrawlerResponse, QueryResponse, UploadResponse
from repository import FileRepository, RetrievalRepository, VectorStoreRepository
from utils import FileReaderWriter, MarkDownUtil, ParseHtmlUtil, PromptParser


# 爬虫获取知识点
class CrawlerService:
    @staticmethod
    def get_knowledge(max_no: int = KnowledgeConfig.MAX_NO) -> CrawlerResponse:
        crawler = KnowledgeCrawler(conf=KnowledgeConfig())           # 创建爬虫对象
        parse_html = ParseHtmlUtil(data_dict=DataDict())             # 创建转换对象
        reader_writer = FileReaderWriter()                           # 创建文件读写对象
        
        success = 0
        fail = 0
        for no in range(1, max_no + 1):
            html = crawler.fetch_content(knowledge_no=no)            # 获取网络知识
            if not html:
                continue
            
            content = html.get("content", "")                        # 获取内容
            if content:
                # 获取标题，并清洗，作为文件名
                title = html.get("title", DataDict.HTML_TITLE).replace(" ",  "").strip()
                clean_title = reader_writer.clean_filename(filename=title)
                process_title = clean_title[: DataDict.FILE_NAME_MAX_LENGTH].rstrip("_")
                file_path = f"{PathConfig.KNOWLEDGE_PATH}/{no:04d}-{process_title}.md"
                
                # 解析 HTML 为 MarkDown
                md = parse_html.parse_html(html=html, knowledge_no=no)
                
                # 写入文件
                reader_writer.write(file_path=file_path, content=md)
            
                success += 1
                print(f"成功获取知识编号：{no}，成功写入文件：{file_path}")
            else:
                fail += 1
                print(f"获取知识编号：{no} 失败")
                
            sleep(KnowledgeConfig.SLEEP_TIME)
            
        print(f"成功获取知识：{success}，失败获取知识：{fail}")
        return CrawlerResponse(success_no=success, fail_no=fail)
    

class StorageService:
    # 文档完整操作：文件的加载 -> 文档的切割 -> 文档的存储
    @staticmethod
    def ingest_file(document_path: str) -> int:
        # 1. 创建向量仓库对象
        store_repository = VectorStoreRepository(conf=VectorRepositoryConfig())
        
        total_chunk = 0
        try:
            # 3. 定义文档加载器：根据文件的路径加载得到文档列表
            text_loader = TextLoader(file_path=document_path, encoding="utf-8")
            
            # 4. 加载文件返回文档列表(TextLoader 返回的文档列表中有且只有一个文档对象)
            document_list = text_loader.load()
        
            for doc in document_list:
                doc.metadata["title"] = MarkDownUtil.extract_title(document_path)
            
            # 5.切分文档得到文档块列表
            chunk_list = StorageService.__process_document(document_list=document_list)
            
            # 6.切分后文档块的元数据校验(过滤不被向量数据库支持的元数据清除掉)
            clean_chunk_list = filter_complex_metadata(documents=chunk_list)
            
            # 7. 无效性检查（校验 page_content 的是否合法（不能为空））
            valid_chunk_list = [document for document in clean_chunk_list if document.page_content.strip()]
            
            # 8. 存储文档块到向量数据库
            total_chunk = store_repository.add_document(documents=valid_chunk_list)
        except Exception as e:
            print(f"文件：{document_path}没有加载到，原因：{str(e)}")
        finally:
            return total_chunk
     
    @staticmethod
    def ingest_directory(directory_path: str) -> Union[int, None, Any]:
        file_repository = FileRepository()                                     # 创建文件仓库对象
        file_list = file_repository.list_files(directory=directory_path)       # 获取目录下的所有文件
        unique_list = file_repository.remove_duplicate_files(file_paths=file_list)  # 获取去重后的文件列表
        
        success_count = 0
        fail_count = 0
        start_time = time()
        with tqdm(iterable=unique_list, desc="知识库处理进度") as bar:
            for file_path in bar:
                try:
                    StorageService.ingest_file(document_path=file_path)
                    success_count += 1
                except Exception as e:
                    print(f"文件：{file_path}处理失败，原因：{str(e)}")
                    fail_count += 1
                finally:
                    bar.set_postfix({"成功": success_count, "失败": fail_count})
        end_time = time()
        print(f"处理完成，耗时：{end_time - start_time}秒")
        
        return success_count
        
    # 文档块处理：文档块的切分 -> 文档块的元数据过滤 -> 文档块的过滤 -> 文档块的存储
    @staticmethod
    def __process_document(document_list: list[Document], document_length: int = 3000) -> list[Document]:
        # 1. 定义文档块切分器
        document_spliter = RecursiveCharacterTextSplitter(chunk_size=VectorRepositoryConfig.CHUNK_SIZE,
                                                          chunk_overlap=VectorRepositoryConfig.CHUNK_OVERLAP,
                                                          separators=VectorRepositoryConfig.SEPARATORS)
        chunk_list = []
        for doc in document_list:
            if len(doc.page_content) < document_length:              # 评估一下小文件的内容长度（获取一个平均值）
                chunk_list.append(doc)                               # 不用切分
            else:
                split_list = document_spliter.split_documents(document_list)
                # 每个文档块的注入标题，作为块的背景
                for chunk in split_list:
                    md_path = chunk.metadata.get("source")            # 获取每一个文档块的标题
                    title = basename(md_path)                         # 获取标题
                    
                    # 拼接到每一个文档块的 page_content上
                    chunk.page_content = f"文档来源:{title}\n{chunk.page_content}"
                chunk_list.extend(split_list)
        return chunk_list


# 存储文档
class DocumentService:
    # 文件上传：文件的上传 -> 文档的存储
    @staticmethod
    async def upload_file(file: UploadFile) -> UploadResponse:
        result = UploadResponse(status="fail", message="上传失败", file_name=file.filename, chunks_added=0)
        
        # 1. 获取文件后缀
        file_suffix = splitext(file.filename)[1]
        
        # 2. 判断临时文件夹是否存在
        is_exist = exists(path=PathConfig.TMP_FOLDER_PATH)
        if not is_exist:
            makedirs(name=PathConfig.TMP_FOLDER_PATH)
        
        temp_path = ""
        # 3. 处理临时文件
        try:
            async with NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
                # 3.1 读取上传文件的内容
                while content := await file.read(size=1024 * 1024):
                    # 3.2 将读取到上传文件的内容写入到临时文件
                    await temp_file.write(content)
                    
                # 3.3 获取临时文件的路径
                temp_path = temp_file.name
            # 4. 存储文件
            chunk_count = await run_in_threadpool(StorageService.ingest_file, temp_path)
            result.status = "success"
            result.message = "文档上传知识库成功"
            result.chunks_added = chunk_count
        except Exception as e:
            print(f"文件上传到知识库失败:{str(e)}")
        finally:
            # 5. 清空临时文件路径
            if temp_path and exists(temp_path):
                remove(temp_path)
            return result
    
    # 查询文档
    @staticmethod
    def query(user_question: str) -> QueryResponse:
        result = QueryResponse(question=user_question, answer="")
        retrieval_repository = RetrievalRepository(conf=VectorRepositoryConfig())
        
        # 1. 参数校验
        if not user_question:
            raise HTTPException(status_code=500, detail="查询问题不存在")
        
        try:
            # 2. 调用检索器的检索方法
            retrieval_context = retrieval_repository.retrieval(user_question)
            
            # 3. 调用查询器的查询方法
            result.answer = DocumentService.__generate_answer(user_question, retrieval_context)
        except Exception as e:
            print(f"调用查询知识库服务失败，原因：{str(e)}")
            raise HTTPException(status_code=500, detail="服务内部出现异常")
        finally:
            return result
    
    @staticmethod
    def __generate_answer(user_question: str, retrieval_list: list[Document]) -> str:
        parser = PromptParser(path=PathConfig.PROMPT_PATH)
        prompt_template = parser.get_prompt(key=DataDict.PROMPT_KEY)
        
        content_list = []
        for index, document in enumerate(retrieval_list):
            content = f"资料{index + 1}:{document}"
            content_list.append(content)
        retrival_context = "\n\n".join(content_list)
        
        prompt = (prompt_template.replace("{user_question}", user_question)
                  .replace("{retrival_context}", retrival_context))
        
        config = CloudModelConfig()
        llm = ChatOpenAI(model_name=config.MODEL_NAME, openai_api_key=config.API_KEY, openai_api_base=config.URL,
                         temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKEN)
        
        response = llm.invoke(input=prompt)
        return response.content
    
        
if __name__ == '__main__':
    # cs = KnowledgeService()
    # cs.get_knowledge()
    
    # ss = StorageService()
    # ss.ingest_directory(directory_path=PathConfig.KNOWLEDGE_PATH)
    
    ds = DocumentService()
    ds.query(user_question="你是谁")

