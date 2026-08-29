#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph  
    FileName       ：  commerce_graph 
    CreateTime     ：  2026-07-04 13:11:28 
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

from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, BatchEncoding
from config import PathConfig, FieldConfig


# 数据处理类
class DataProcessor:
    def __init__(self):
        self.raw_data_path = PathConfig.RAW_DATA_PATH                # 原始数据路径
        self.raw_data_type = PathConfig.RAW_DATA_TYPE                # 原始数据类型
        self.processed_data_path = PathConfig.PROCESSED_DATA_PATH    # 处理后的数据路径
        self.model_name = PathConfig.BERT_MODEL                      # 模型名称
        self.tokenizer = None
    
    # 加载数据集
    def process_data(self):
        # 1. 加载数据集
        raw_dataset = self.load_data(data_path=self.raw_data_path, data_type=self.raw_data_type)
        
        # 2. 选择数据集
        select_dataset = raw_dataset[FieldConfig.TRAIN_FLAG]
        
        # 3. 删除不需要的列
        remove_dataset = select_dataset.remove_columns(column_names=FieldConfig.RAW_REMOVE_COLUMNS)
        
        # 4. 划分数据集
        dataset = remove_dataset.train_test_split(test_size=0.2)
        valid_test = dataset[FieldConfig.TEST_FLAG]
        dataset[FieldConfig.TEST_FLAG], dataset[FieldConfig.VALID_FLAG] = (valid_test.train_test_split(test_size=0.5)
                                                                           .values())
        
        # 5. 加载编码器
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=self.model_name)
        
        # 6. 数据编码
        dataset_dict = dataset.map(function=self.__encode_data, remove_columns=FieldConfig.SAVE_REMOVE_COLUMNS)
        
        # 7. 保存数据集
        self.save_data(dataset=dataset_dict, data_path=self.processed_data_path)
        
    # 读取数据集
    def load_data(self, data_path: str = None, data_type: str = None) -> DatasetDict:
        if data_path is None:
            data_path = self.processed_data_path
        
        if data_type is None:
            data_type = self.raw_data_type
            
        dataset = load_dataset(path=data_type, data_files=data_path)
        return dataset
    
    # 保存数据集
    def save_data(self, dataset: DatasetDict = None, data_path: str = None) -> None:
        if dataset is None:
            dataset = self.load_data()
        
        if data_path is None:
            data_path = self.processed_data_path
            
        dataset.save_to_disk(dataset_dict_path=data_path)
    
    # 数据编码
    def __encode_data(self, example: dict) -> BatchEncoding:
        # 1. 加载编码器
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=PathConfig.BERT_MODEL)
        
        # 2. 将文本数据转为字符列表
        token_list = list(example[FieldConfig.CONTENT_FIELD])
        
        # 3. 文本编码（使用 TrainConfig.MAX_LENGTH 确保截断一致性）
        encoded = self.tokenizer(text=token_list, is_split_into_words=FieldConfig.IS_SPLIT_WORDS,
                                 truncation=FieldConfig.IS_TRUNCATION, max_length=FieldConfig.MAX_LENGTH)
        
        # 4. 进行实体标注
        entries = example[FieldConfig.LABEL_FIELD]
        
        # 5. 定义标注列表，存放 id，标签初始值设为：O
        label_list = [FieldConfig.LABELS.index(FieldConfig.OUT_FLAG)] * len(token_list)
        
        # 6. 遍历标注数据，将字符级标签映射到 token 级
        for entry in entries:
            start = entry[FieldConfig.START_FIELD]
            end = entry[FieldConfig.END_FIELD]
            
            start_list = [FieldConfig.LABELS.index(FieldConfig.START_FLAG)]
            middle_list = [FieldConfig.LABELS.index(FieldConfig.MIDDLE_FLAG)] * (end - start - 1)
            label_list[start: end] = start_list + middle_list
        
        # 7. 使用 word_ids() 将字符级标签对齐到 token 级
        word_ids = encoded.word_ids()
        token_labels = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                # 特殊 token（[CLS]、[SEP]、[PAD]）→ -100
                token_labels.append(FieldConfig.MARK_LABEL)
            elif word_idx != previous_word_idx:
                # 单词的第一个子词 token → 使用该字符的标签
                token_labels.append(label_list[word_idx])
            else:
                # 同一单词的后续子词 token → -100（不参与损失计算）
                token_labels.append(FieldConfig.MARK_LABEL)
            previous_word_idx = word_idx
        
        # 8. 添加标签数据
        encoded[FieldConfig.TARGET_FIELD] = token_labels
        
        return encoded


if __name__ == '__main__':
    process = DataProcessor()
    process.process_data()
