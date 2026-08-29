#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  repository 
    CreateTime     ：  2026-07-20 20:41:16 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import makedirs, listdir
from os.path import exists, dirname, isdir, join
from typing import List, Dict, Any
from hashlib import md5
from re import sub, DOTALL
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity
from config import VectorRepositoryConfig
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from jieba import lcut
from utils import MarkDownUtil


# 向量仓库
class VectorStoreRepository:
    def __init__(self, conf: VectorRepositoryConfig):
        self.path = conf.REPOSITORY_DIRECTORY                        # 向量仓库路径
        self.model = conf.EMBED_MODEL_NAME                           # 嵌入模型名称
        self.url = conf.URL                                          # 模型服务 URL
        self.api_key = conf.API_KEY                                  # 模型服务 API Key
        self.retry = conf.MAX_RETRY                                  # 重试次数
        self.timeout = conf.TIME_OUT                                 # 超时
        self.collection_name = conf.COLLECTION_NAME                  # 向量集合名称
        self.dimension = conf.DIMENSION                              # 向量维度
        
        self.vector_store = None                                     # 向量仓库
        self.embedding = None                                        # 嵌入模型
        
    # 创建向量仓库
    def create_vector_store(self) -> None:
        # 创建向量存储库
        is_exist = exists(path=self.path)
        if not is_exist:
            makedirs(name=self.path)
            
        self.embedding = OpenAIEmbeddings(model=self.model, openai_api_base=self.url, openai_api_key=self.api_key,
                                          dimensions=self.dimension, max_retries=self.retry,
                                          request_timeout=self.timeout)
        
        self.vector_store = Chroma(persist_directory=self.path, collection_name=self.collection_name,
                                   embedding_function=self.embedding)
        
    # 将切分之后的文档块保存到向量数据库中
    def add_document(self, documents: list[Document], batch_size: int = 16) -> int:
        if self.vector_store is None:
            self.create_vector_store()
        
        # 1. 获取到文档块的总数量
        document_count = len(documents)
        
        # 2. 分批次保存
        added_count = 0
        try:
            for i in range(0, document_count, batch_size):
                bath = documents[i: i + batch_size]
                self.vector_store.add_documents(bath)
                added_count = added_count + len(bath)
                
                print(f"成功将文档块:{added_count}/{document_count}保存到向量数据库...")
        except Exception as e:
            print(f"文档块列表:{documents}保存到向量数据库失败: {e}")
        finally:
            return added_count
    
    # 对输入内容进行向量化
    def vector_document(self, input_document: str) -> list[float]:
        if self.embedding is None:
            self.create_vector_store()
        
        result = self.embedding.embed_query(input_document)
        return result
        
    # 对查询内容进行向量化
    def vector_documents(self, input_list: list[str]) -> list[float]:
        if self.embedding is None:
            self.create_vector_store()
        
        result = self.embedding.embed_documents(input_list)
        return result


# 文件仓库
class FileRepository:
    @staticmethod
    # 计算文件的 MD 5哈希值
    def get_file_hash(file_path: str) -> str:
        hash_md5 = md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    # 去除重复文件
    @staticmethod
    def remove_duplicate_files(file_paths: List[str]) -> List[str]:
        unique_files = {}                                            # 用于记录 {hash: file_path}
        unique_file_paths = []                                       # 最终要返回的列表
        
        for file_path in file_paths:
            try:
                file_hash = FileRepository.get_file_hash(file_path)  # 尝试计算哈希
                
                # 只有计算成功了，才判断是否重复
                if file_hash not in unique_files:
                    unique_files[file_hash] = file_path
                    unique_file_paths.append(file_path)
                else:
                    # 这里打印一下，方便知道跳过了谁
                    print(f"发现重复文件，自动跳过: {file_path}")
            except Exception as e:
                print(f"文件读取异常，已跳过: {file_path} (错误: {str(e)})")
                continue
            
        return unique_file_paths
    
    # 读取文件内容
    @staticmethod
    def read_file_content(file_path: str) -> str:
        result = ""
        
        if not file_path or not exists(file_path):
            print(f"文件不存在或路径为空: {file_path}")
            return result
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                result = f.read()
        except UnicodeDecodeError:
            print(f"文件编码错误(非UTF-8): {file_path}")
        except OSError as e:
            print(f"读取文件IO错误: {file_path}, 原因: {e}")
        except Exception as e:
            print(f"读取未知错误: {file_path}, 原因: {e}")
        finally:
            return result
        
    # 保存内容到文件
    @staticmethod
    def save_file(content: str, file_path: str) -> None:
        try:
            if not content:
                print(f"内容为空，跳过保存: {file_path}")
                return
            
            directory = dirname(file_path)
            if directory:
                makedirs(directory, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except OSError as e:
            print(f"保存文件失败: {file_path},原因：{e}")
        except Exception as e:
            print(f"发生未知错误: {e}")
    
    # 列出目录下的文件
    @staticmethod
    def list_files(directory: str, extension: str = None) -> list[str]:
        files = []
        
        # 1. 基础校验
        if not directory or not directory.strip():
            print("目录路径为空")
        
        # 2. 确保它真的是个目录，而不是文件
        if not isdir(directory):
            print(f"路径不是一个有效的目录: {directory}")
        
        # 3. 列出目录下的所有文件
        try:
            # os.listdir 可能会因为权限问题报错
            file_list = listdir(directory)
            
            for filename in file_list:
                if extension:
                    if not filename.lower().endswith(extension.lower()):
                        continue
                        
                full_path = join(directory, filename)
                files.append(full_path)
        except PermissionError:
            print(f"权限不足，无法访问目录: {directory}")
        except OSError as e:
            print(f"遍历目录出错: {directory}, 原因: {e}")
        except Exception as e:
            print(f"未知错误: {directory}, 原因: {e}")
        finally:
            return files


class RetrievalRepository:
    def __init__(self, conf: VectorRepositoryConfig):
        store = VectorStoreRepository(conf=conf)
        store.create_vector_store()
        self.vector_path = store.path
        self.vector_store = store.vector_store
        self.embedding = store.embedding

    # 核心检索方法
    def retrieval(self, user_question: str) -> List[Document]:
        # 1. 第一路检索(基于嵌入模型的向量检索)
        candidates_vector = self.__search_based_vector(user_question=user_question)
        
        # 2. 第二路检索(基于jieba的分词匹配的检索)
        candidates_title = self.__search_based_title(user_query=user_question)
        
        # 3. 合并两路检索的文档列表
        candidates = candidates_vector + candidates_title
        
        # 4. 对合并后的文档列表去重
        candidates_unique = self.__deduplicate(total_candidates=candidates)
        
        # 5. 重新打分排序
        top_documents = self.__reranking(candidate_list=candidates_unique, user_question=user_question)
        
        # 6.返回指定 Top-N 个文档列表
        return top_documents
    
    # 对标题进行粗排
    @staticmethod
    def rough_ranking(user_query, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 1. 用户输入问题是否存在
        if not user_query:
            return []
        
        ROUGH_WORD_WEIGHT = 0.7
        # 2.遍历所有元数据
        for meta in metadata:
            # 2.1 获取标题
            title = meta.get("title")
            
            # 2.2 判断标题是否存在
            if not title and not title.strip():
                continue
                
            # 2.3 进行分词并计算得分
            query_char = set(user_query)
            title_char = set(title)
            unique_char = query_char | title_char
            char_score = len(query_char & title_char) / len(unique_char) if len(unique_char) > 0 else 0
            
            # 2.3.2 在用jieba词项切(影响因素大一些)
            query_word_set = set(lcut(user_query))
            title_word_set = set(lcut(title))
            unique_word = query_word_set | title_word_set
            word_score = len(query_word_set & title_word_set) / len(unique_word) if len(unique_word) > 0 else 0
            
            # 2.3.3 计算粗排分数：字符级+词性项级(侧重)
            roughing_score = word_score * ROUGH_WORD_WEIGHT + char_score * (1 - ROUGH_WORD_WEIGHT)
            
            meta['roughing_score'] = float(roughing_score)
        
        # 3.根据标题的元数据排序
        top = sorted(metadata, key=lambda x: x['roughing_score'], reverse=True)
        return top[:50]
        
    # 对标题进行精排
    def fine_ranking(self, user_query: str, rough_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 1. 判粗排元数据
        if not rough_metadata:
            return []
        
        # 2. 对问题向量化
        query_embedding = self.embedding.embed_query(text=user_query)
        
        # 3. 获取粗排后的标题
        roughing_title = [md_metadata['title'] for md_metadata in rough_metadata]
        
        # 4. 标题的向量值
        roughing_title_embeddings = self.embedding.embed_documents(roughing_title)

        # 5. 计算问题和粗排标题的相似度（余弦相似分数）分数值越大 代表问题和标题越相似
        similarity = cosine_similarity(X=[query_embedding], Y=roughing_title_embeddings).flatten()
        
        # 6. 遍历粗排元数据
        ROUGH_HEIGHT = 0.3
        SIM_HEIGHT = 0.7
        for index, metadata in enumerate(rough_metadata):
            # 6.1 获取精排分数(归一)
            sim = similarity[index]
            if sim < 0:
                sim = 0
            # 6.2 获取粗排
            roughing_score = metadata['roughing_score']
            
            # 6.3 加权求最终精排分数
            final_score = roughing_score * ROUGH_HEIGHT + sim * SIM_HEIGHT
            
            # 6.4 存放到 md_metadata 元数据中
            metadata['sim_score'] = sim
            metadata['final_score'] = final_score
        
        # 7. 排序
        sim_mds_metadata = sorted(rough_metadata, key=lambda x: x['final_score'], reverse=True)[:5]
        
        # 8. 返回
        return sim_mds_metadata
    
    # 基于语义相似度检索
    def __search_based_vector(self, user_question: str) -> List[Document]:
        # 1.返回带分数的文档列表
        document_list = self.vector_store.similarity_search_with_score(user_question)
        
        # 2. 不用距离得分
        candidate_list = []
        for document, _ in document_list:
            candidate_list.append(document)
        
        return candidate_list
    
    # 基于标题的关键词匹配检索
    def __search_based_title(self, user_query: str) -> List[Document]:
        # 1. 获取指定目录下的文件的标题
        mds_metadata = MarkDownUtil.collect_metadata(folder_path=self.vector_path)
        
        # 2. 关键词匹配（jieba）--->（比较对象：用户输入的问题 vs crawl目录下的文件标题）
        rough_metadata = self.rough_ranking(user_query, mds_metadata)
        
        # 3. 标题的语义匹配（比较对象：用户的输入问题  vs md目录下的 ）
        fine_metadata = self.fine_ranking(user_query, rough_metadata)
        
        # 4. 处理文档（根据标题读取标题对于的文档内容---Document(page_content,metadata={})）
        title_candidates = []
        for metadata in fine_metadata:
            try:
                # 4.1 打开文件
                with open(metadata['path'], "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    
                # 4.2 判断 content 内容长度
                if len(content) < 3000:
                    meta_dict = { "path" : metadata['path'], "title": metadata['title'] }
                    doc = Document(page_content=content, metadata=meta_dict)
                    title_candidates.append(doc)
                else:
                    doc_chunks = self.__deal_long_title_content(content=content, metadata=metadata, query=user_query)
                    title_candidates.extend(doc_chunks)  # doc_chunks 列表中元素打散了
            except Exception as e:
                print(f"发生错误：{e}")
        return title_candidates
    
    # 对合并后的文档列表去重
    @staticmethod
    def __deduplicate(total_candidates: List[Document]) -> List[Document]:
        if not total_candidates:
            return []
        
        # 2. 定义set集合
        seen = set()
        candidate_list = []
        # 3. 遍历合并后的每一个文档列表
        for document in total_candidates:
            pattern = r'^文档来源:.*?(?=(\n|#))'
            content = sub(pattern=pattern, repl='', string=document.page_content, flags=DOTALL).strip()
            
            key = (document.metadata['title'], content[:100])
            if key not in seen:
                seen.add(key)
                candidate_list.append(document)
        
        # 4. 返回唯一的
        return candidate_list
    
    # 重新计算打分&&排序
    def __reranking(self, candidate_list: List[Document], user_question: str) -> List[Document]:
        # 1. 判断去重合并之后文档列表是否有文档对象
        if not candidate_list:
            return []
        
        embedding_list = []
        candidate_index_list = []
        score_doc = []
        
        # 2. 遍历去重并合并之后的文档列表(Document,score)
        for index, candidate in enumerate(candidate_list):
            # 2.1 长文档
            if "chunk_index" in candidate.metadata and "similarity" in candidate.metadata:
                score_doc.append((candidate, candidate.metadata['similarity']))
            # 2.2 短文档
            else:
                embedding_list.append(candidate)
                candidate_index_list.append(index)
        
        # 3.处理需要重新计算分数的文档
        if embedding_list:
            # 3.1 计算用户问题的向量
            query_embedding = self.embedding.embed_query(user_question)
            
            # 3.2 获取到需要向量的文档内容
            embedding_docs_content = ["文档来源:" + doc.metadata['title'] + doc.page_content for doc in
                                      embedding_list]
            # 3.3 计算需要向量的文档内容
            doc_embeddings = self.embedding.embed_documents(embedding_docs_content)
            
            # 3.4 计算相似得分
            similarity = cosine_similarity([query_embedding], doc_embeddings).flatten()
            
            # 3.5 封装到带得分的文档列表
            for idx, index in enumerate(candidate_index_list):
                score_doc.append((candidate_list[index], similarity[idx]))
        
        # 4. 排序
        sorted_docs = sorted(score_doc, key=lambda x: x[1], reverse=True)
        
        # 5. 返回Top-N
        return [doc for doc, _ in sorted_docs[:2]]
    
    # 处理标题对应的长文本：切分-->文档块--->算文档块和问题的相似度
    def __deal_long_title_content(self, content: str, metadata: Dict[str, Any], query: str) -> List[Document]:
        # 1. 对长文本切分(换成适合)
        document_spliter = RecursiveCharacterTextSplitter(chunk_size=VectorRepositoryConfig.CHUNK_SIZE,
                                                          chunk_overlap=VectorRepositoryConfig.CHUNK_OVERLAP,
                                                          separators=VectorRepositoryConfig.SEPARATORS)
        chunks = document_spliter.split_text(content)
        
        # 2. 获取对应的标题
        doc_chunks_title = metadata['title']
        
        # 3. 标题注入到文档块中（第二次结构和第一次的拼接一定要一样）TODO
        doc_chunks_inject_title = [f"文档来源:{doc_chunks_title}" + doc_chunk for doc_chunk in chunks]
        
        # 4. 对问题向量
        query_embedding = self.embedding.embed_query(query)
        
        # 5. 对切分后的文档块向量化
        doc_chunk_embeddings = self.embedding.embed_documents(doc_chunks_inject_title)
        
        # 6. 计算相似性
        doc_chunks_similarity = cosine_similarity([query_embedding], doc_chunk_embeddings).flatten()
        
        # 7. 获取3个相似性分数值高的三个索引
        top_doc_chunks_indices = doc_chunks_similarity.argsort()[-3:][::-1]
        
        # 8. 构建最终文档对象列表(为每一个切分后的块)
        document_list = []
        for i, chunk_idx in enumerate(top_doc_chunks_indices):
            metadata = \
                {
                    "path"        : metadata['path'],
                    "title"       : metadata['title'],
                    "chunk_index:": int(chunk_idx),
                    "similarity"  : float(doc_chunks_similarity[chunk_idx])
                }
            
            doc = Document(page_content=doc_chunks_inject_title[chunk_idx], metadata=metadata)
            document_list.append(doc)
        
        return document_list


if __name__ == '__main__':
    vr = VectorStoreRepository(conf=VectorRepositoryConfig())
    # v = vr.vector_document(input_document="hello world")
    vr.add_document(documents=[Document(page_content="hello world")])
