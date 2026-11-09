#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  word2vecory 
    CreateTime     ：  2026-06-17 23:48:44 
    Author         ：  lihuashiyu
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""
from typing import Any

from jieba import lcut
from gensim.models import KeyedVectors
from torch import zeros, tensor, Tensor
from torch.nn import Embedding


# 1. 加预训练的词向量模型，并进行 OOV 处理
def load_wv_model(model_path: str, unknown_token: str = UNK_TOKEN) -> tuple[KeyedVectors, int, list[str], dict[str, int]]:
    wv_model = KeyedVectors.load_word2vec_format(fname=model_path)   # 1.1 加载模型
    vector_dim = wv_model.vector_size                                # 1.2 获取词向量维度
    print("词向量维度：", vector_dim)
    
    # 增加对 OOV 问题的处理
    index_word_list = [unknown_token] + wv_model.index_to_key            # 1.3 构建 index_word_list 映射
    word_index_dict = { word : id for id, word in enumerate(index_word_list) } # 1.4 构建 word_index_dict 映射
    
    return wv_model, vector_dim, index_word_list, word_index_dict


# 2. 构造词向量矩阵
def build_embedding_matrix(wv_model: KeyedVectors, vector_dim: int, word2id: dict) -> Tensor:
    vocab_size = len(word2id)                                        # 2.1 获取词表大小
    embedding_matrix = zeros(vocab_size, vector_dim)                 # 2.2 创建词向量矩阵
    for word, id in word2id.items():                                 # 2.3 填充词向量矩阵
        if word in wv_model:
            embedding_matrix[id] = tensor(wv_model[word])            # 2.4 填充词向量矩阵
    return embedding_matrix


# 3. 构建神经网络的嵌入层，并测试
def build_embedding_layer(embedding_matrix: Tensor, word2id: dict, text: str):
    # 3.1 构建嵌入层
    embedding = Embedding.from_pretrained(embeddings=embedding_matrix, freeze=False)
    tokens = lcut(text)                                              # 3.2 分词
    ids = [ word2id.get(word, word2id[UNK_TOKEN]) for word in tokens ] # 3.3 将语料 id 化
    print(f"ids : {ids}")
    
    input = tensor([ids])                                            # 3.4 构造输入数据
    output = embedding(input)                                        # 3.5 前向传播：查找词向量
    # print(f"output : {output}")
    print(f"output.shape : {output.shape}")
    

if __name__ == '__main__':
    UNK_TOKEN = 'OOV'
    wv_model, vector_dim, id2word, word2id = load_wv_model(model_path='../data/sgns.weibo.word.bz2')
    
    similarity = wv_model.most_similar(positive=["高铁", "火车"], negative=[])
    print(f"similarity : {similarity}")
    
    # embedding_matrix = build_embedding_matrix(wv_model, vector_dim, word2id)
    # build_embedding_layer(embedding_matrix, word2id, text='我喜欢乘坐宇宙飞船')
    # build_embedding_layer(embedding_matrix, word2id, text='我叫 lihuashiyu')
    # build_embedding_layer(embedding_matrix, word2id, text='老板是俊福')
