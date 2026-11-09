#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  couplet 
    CreateTime     ：  2026-06-23 18:53:04 
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
environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

from os.path import abspath
from typing import cast
from datasets import load_from_disk, Dataset
from transformers import AutoTokenizer, PreTrainedModel, BartForConditionalGeneration, DataCollatorForSeq2Seq
from transformers import BatchEncoding, PreTrainedTokenizerBase
from torch import no_grad
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm
from common import BaseConfig, BaseTrainer


# 配置类
class CoupletConfig(BaseConfig):
    # ============================== 参数路径 ==============================
    PROJECT_NAME = "couplet"                                         # 项目名称
    BART_MODEL = "OpenMOSS-Team/bart-base-chinese"                   # BART 模型名称
    # BART_MODEL = abspath(path=f"{BaseConfig.MODEL_DIR}/bart-base-chinese")
    
    RAW_IN_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/in.txt")   # 上联数据路径
    RAW_OUT_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/out.txt") # 下联数据路径
    DATASET_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}")    # 训练数据路径
    MODEL_PATH = abspath(path=f"{BaseConfig.MODEL_DIR}/{PROJECT_NAME}")        # 模型保存路径
    BOARD_DIR = abspath(path=f"{BaseConfig.PROJECT_DIR}/board/{PROJECT_NAME}") # 日志保存路径
    
    # ============================== 数据字段 ==============================
    INPUT_FIELD = "inputs"                                           # 输入字段
    TARGET_FIELD = "targets"                                         # 输出字段
    RETURN_TENSORS = "pt"                                            # 返回张量类型
    IS_PADDING = True                                                # 是否填充
    
    # ============================== 训练超参数 ==============================
    IS_SHUFFLE = True                                                # 是否打乱数据
    IS_TRUNCATION = True                                             # 是否截断
    
    SEQ_LEN = 128                                                    # 最大序列长度
    BATCH_SIZE = 1024                                                # 批处理大小
    LEARNING_RATE = 1e-5                                             # 学习率
    EPOCHS = 3                                                      # 训练轮数
    MAX_LENGTH = 32                                                  # 生成最大长度
    NUM_BEAMS = 5                                                    # 束搜索
    

# 数据预处理
class CoupletDataProcessor:
    def __init__(self, config: CoupletConfig):
        self.bart_path = config.BART_MODEL                           # BART 模型路径
        self.in_path = config.RAW_IN_PATH                            # 上联数据路径
        self.out_path = config.RAW_OUT_PATH                          # 下联数据路径
        self.save_path = config.DATASET_PATH                         # 数据集保存路径
        self.batch_size = config.BATCH_SIZE                          # 批处理大小
        self.device = config.DEVICE                                  # 设备
        
        self.input_field = config.INPUT_FIELD                        # 输入字段
        self.target_field = config.TARGET_FIELD                      # 输出字段
        self.is_padding = config.IS_PADDING                          # 是否填充
        self.is_shuffle = config.IS_SHUFFLE                          # 是否打乱数据
        self.is_truncation = config.IS_TRUNCATION                    # 是否截断
        self.seq_len = config.SEQ_LEN                                # 最大序列长度
        self.return_tensors = config.RETURN_TENSORS                  # 返回张量类型
        self.data_encoding = "utf-8"                                 # 数据编码
        self.dataset_format = "torch"                                # 数据集格式
        
        self.model: PreTrainedModel                                  # BART 模型
        self.tokenizer: PreTrainedTokenizerBase                      # BART 分词器
        
    # 读取数据
    def read_data(self, text_path: str):
        content_list = []
        with open(file=text_path, mode="r", encoding=self.data_encoding) as fr:
            for line in fr.readlines():
                content = line.strip().replace(" ", "")
                if content:
                    content_list.append(content)
        return content_list
        
    # 数据处理
    def process(self) -> None:
        # 1. 读取数据
        inputs = self.read_data(text_path=self.in_path)              # 上联数据
        targets = self.read_data(text_path=self.out_path)            # 下联数据
        
        # 2. 构建一个字典，调用 from_dict 方法直接构建 dataset
        data_dict = {self.input_field: inputs, self.target_field: targets}     # 数据字典
        datasets = Dataset.from_dict(mapping=data_dict)               # 数据集
        
        # 3. 创建分词器
        self.__load_bart()
        
        # 4. 构建数据集
        remove_columns = [self.input_field, self.target_field] if self.input_field and self.target_field else None
        filters = datasets.map(function=self.__batch_encode, batched=True, remove_columns=remove_columns)
        
        # 5. 保存数据集
        filters.save_to_disk(dataset_path=self.save_path)
    
    # 构建数据加载器
    def build_loader(self) -> DataLoader:
        # 1. 加载数据集
        data = load_from_disk(dataset_path=self.save_path)           # 加载数据集
        dataset = cast(Dataset, data)                                # 数据集转换
        dataset.set_format(type=self.dataset_format)                 # 设置数据集格式
        
        # 2. 加载 BART 模型
        self.__load_bart()
        
        # 3. 数据整理方法
        collate_fn = DataCollatorForSeq2Seq(tokenizer=self.tokenizer, model=self.model,
                                            padding=self.is_padding, return_tensors=self.return_tensors)
        
        # 4. 加载数据
        dataloader = DataLoader(dataset=dataset, batch_size=self.batch_size, shuffle=self.is_shuffle,
                                collate_fn=collate_fn)
        return dataloader
        
    # 加载 BART 模型和分词器
    def __load_bart(self) -> None:
        # 1. 加载 BART 模型（仅用于 DataCollator 读取 config，保留在 CPU 上，避免占用显存）
        if not hasattr(self, "model"):
            self.model = BartForConditionalGeneration.from_pretrained(pretrained_model_name_or_path=self.bart_path)
        
        # 2. 加载分词器
        if not hasattr(self, "tokenizer"):
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=self.bart_path)
        
    # 批量向量化
    def __batch_encode(self, example: dict) -> BatchEncoding:
        encoded = self.tokenizer(text=example[self.input_field], text_target=example[self.target_field],
                                 max_length=self.seq_len, truncation=self.is_truncation,
                                 return_token_type_ids=False)
        return encoded
        
        
# 数据模型训练
class CoupletTrainer(BaseTrainer):
    def __init__(self, config: CoupletConfig):
        model = BartForConditionalGeneration.from_pretrained(pretrained_model_name_or_path=config.BART_MODEL)
        super().__init__(config=config, model=model)
        
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=config.BART_MODEL)
        self.optimizer = Adam(params=self.model.parameters(), lr=self.learning_rate)
        
    # 训练一个 epoch
    def train_one_epoch(self, train_loader: DataLoader, is_bar: bool = False) -> float:
        if is_bar:
            bar = tqdm(iterable=train_loader, desc="batch：", colour="red", ncols=100, leave=False)
        else:
            bar = train_loader
        
        self.model.train()                                           # 设置模型为训练模式
        total_loss = 0.0                                             # 初始化总损失为 0.0
        for batch in bar:
            input_ids = batch["input_ids"].to(device=self.device)    # 输入张量
            labels = batch["labels"].to(device=self.device)          # 目标张量
            attention_mask = batch["attention_mask"].to(device=self.device)         # 注意力掩码
            decoder_input_ids = batch["decoder_input_ids"].to(device=self.device)   # 解码器输入张量
            
            output_tensor = self.model(input_ids=input_ids, attention_mask=attention_mask,
                                       decoder_input_ids=decoder_input_ids, labels=labels)  # 前向传播
            loss = output_tensor.loss                                # 计算损失
            loss.backward()                                          # 反向传播
            self.optimizer.step()                                    # 更新参数
            self.optimizer.zero_grad()                               # 清空梯度
            
            total_loss += loss.item()                                # 累加损失
        average_loss = total_loss / len(train_loader)                # 计算平均损失
        print(f"训练集平均损失: {average_loss:.4f}")
        
        return average_loss
    

# 数据模型预测
class CoupletPredictor:
    def __init__(self, config: CoupletConfig):
        self.model_path = config.MODEL_PATH                          # 模型保存路径
        self.bert_model = config.BART_MODEL                          # BART 模型路径
        self.max_length = config.MAX_LENGTH                          # 生成最大长度
        self.num_beams = config.NUM_BEAMS                            # 束搜索
        self.input_field = config.INPUT_FIELD                        # 输入字段
        self.target_field = config.TARGET_FIELD                      # 输出字段
        self.is_padding = config.IS_PADDING                          # 是否填充
        self.return_tensors = config.RETURN_TENSORS                  # 返回张量类型
        self.device = config.DEVICE                                  # 设备
        
        self.model: PreTrainedModel                                  # BART 模型
        self.tokenizer: PreTrainedTokenizerBase                      # BART 分词器
        
    # 预测模型
    def predict(self, input_text: str) -> str:
        self.__load_model()                                          # 加载模型和分词器
        
        # 文本编码为张量形式（长度固定）
        encoded = self.tokenizer(text=input_text, padding=self.is_padding, return_tensors=self.return_tensors,
                                 return_token_type_ids=False)
        inputs = encoded.get("input_ids").to(device=self.device)     # 将编码后的张量移动到指定设备
        
        with no_grad():
            tokens = self.model.generate(inputs, max_length=self.max_length, num_beams=self.num_beams,
                                         early_stopping=True, repetition_penalty=1.2, no_repeat_ngram_size=3)
            
        results = self.tokenizer.batch_decode(sequences=tokens, skip_special_tokens=True)
        return results[0].replace(" ", "")
        
    # 批量测试
    def predict_batch(self) -> None:
        exit_list = ["quit", "exit", "q", "e"]
        
        while True:
            user_input = input("请输入您的上联：").strip()
            if user_input in exit_list:
                break
            else:
                user_input = user_input.replace(" ", "").strip()
                results = self.predict(input_text=user_input)
                print(f"预测结果：{results}")
         
    # 加载模型和分词器
    def __load_model(self) -> None:
        if not hasattr(self, "model"):
            self.model = BartForConditionalGeneration.from_pretrained(pretrained_model_name_or_path=self.model_path)
            self.model.to(device=self.device)                        # 将模型移动到指定设备
            self.model.eval()                                        # 模型测试模式
            
        if not hasattr(self, "tokenizer"):
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=self.bert_model)
       
