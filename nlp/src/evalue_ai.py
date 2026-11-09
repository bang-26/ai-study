#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  evalue_ai 
    CreateTime     ：  2026-06-21 23:44:50 
    Author         ：  lihuashiyu
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from os.path import dirname, abspath
from unittest import TestCase
from datasets import load_dataset, ClassLabel, load_from_disk
from transformers import AutoTokenizer, AutoModel, BatchEncoding
from torch import device, cuda, load, no_grad, save, sigmoid
from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss, Module, Linear
from torch.utils.data import DataLoader
from tqdm import tqdm


# 数据预处理
class DataProcessor:
    def __init__(self, raw_path: str):
        self.raw_path = raw_path
        self.tokenizer = AutoTokenizer.from_pretrained(Config.TOKENIZER_PATH)
        
    # 数据处理
    def process_data(self) -> None:
        # 加载原始 CSV 数据
        contents = load_dataset(path=Config.RAW_DATA_SUFFIX, data_files=self.raw_path)
        datas = contents[Config.TRAIN_FLAG]                          # 获取训练数据
        
        # 去掉 cat 列
        removes = datas.remove_columns(column_names=[Config.CATEGORY_FIELD])
        
        # 过滤空评论和非二分类标签
        filters = removes.filter(function=self.filter_valid_examples)
        
        # 将标签转换为 ClassLabel 类型
        label = ClassLabel(names=Config.EMOTION_SCORE)               # 创建标签
        datasets = filters.cast_column(column=Config.LABEL_FIELD, feature=label)
        
        # 划分训练集和测试集
        data_dict = datasets.train_test_split(test_size=0.2, seed=42, stratify_by_column=Config.LABEL_FIELD)
        
        # 对数据集集进行编码，并删除字段
        remove_columns = [Config.REVIEW_FIELD, Config.LABEL_FIELD,]
        dataset_dict = data_dict.map(function=self.tokenize_encode, batched=True, remove_columns=remove_columns)
        
        # 保存结果到文件
        dataset_dict[Config.TRAIN_FLAG].save_to_disk(dataset_path=Config.TRAIN_PATH)
        dataset_dict[Config.TEST_FLAG].save_to_disk(dataset_path=Config.TEST_PATH)
        
        print(f"{Config.TRAIN_FLAG} = {dataset_dict[Config.TRAIN_FLAG]}")
        print(f"{Config.TEST_FLAG} = {dataset_dict[Config.TEST_FLAG]}")
        
    # 过滤空评论和非二分类标签
    @staticmethod
    def filter_valid_examples(example: dict) -> bool:
        review = example.get(Config.REVIEW_FIELD)
        label = example.get(Config.LABEL_FIELD)
        # 保持与原来 lambda 相同的语义：review 非空且非空白字符串，并且 label 在允许的范围内
        return review is not None and str(review).strip() != "" and label in Config.LABEL_SCORE
    
    # 编码函数
    def tokenize_encode(self, example: dict) -> BatchEncoding:
        encoded = self.tokenizer(example[Config.REVIEW_FIELD], max_length=Config.SEQ_LEN,
                                 truncation=Config.IS_TRUNCATION, padding=Config.PADDING_TYPE)
        encoded[Config.LABEL_FIELD] = example[Config.LABEL_FIELD]
        return encoded


# 自定义数据集
class ReviewDataset:
    def __init__(self, data_path: str):
        self.data_path = data_path
    
    # 获取数据集
    def get_dataset(self):
        datasets = load_from_disk(dataset_path=self.data_path)
        
        # 设置为 PyTorch 格式，列自动转换为 tensor
        # datasets.set_format(type="torch", columns=Config.DATASET_COLUMNS)
        datasets.set_format(type="torch")
        return datasets
    
    # 获取数据加载器
    def get_dataloader(self) -> DataLoader:
        datasets = self.get_dataset()
        dataloader = DataLoader(dataset=datasets, batch_size=Config.BATCH_SIZE, shuffle=Config.IS_SHUFFLE)
        return dataloader


# 自定义模型
class ReviewAnalysisModel(Module):
    def __init__(self, freeze_bert: bool = True):
        super().__init__()
        
        # BERT 层：加载本地预训练的 BERT 模型
        self.bert = AutoModel.from_pretrained(Config.BERT_MODEL_NAME)
        
        # 冻结参数
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False
                
        # 线性层：接收 [CLS] 向量 → 输出二分类的得分
        self.linear = Linear(in_features=self.bert.config.hidden_size, out_features=1)
    
    # 前向传播过程
    def forward(self, input_ids, attention_mask, token_type_ids):
        # 获取 BERT，输出是命名元组，包含多个字段，其中 last_hidden_stat e最后一层所有 token 的输出
        berts = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        
        # 提取 [CLS] token（第一个位置）的输出向量：(batch_size, hidden_size)
        cls_outputs = berts.last_hidden_state[:, 0, :]
        
        outputs = self.linear(cls_outputs)                           # 通过线性层生成 results
        results = outputs.squeeze(-1)                                # 返回形状: (batch_size,)
        return results


# 训练模型
class Trainer:
    def __init__(self):
        self.epochs = Config.EPOCHS
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.dataloader = ReviewDataset(data_path=Config.TRAIN_PATH).get_dataloader()
        self.model = ReviewAnalysisModel(freeze_bert=False).to(device=self.device)
        self.optimizer = Adam(params=self.model.parameters(), lr=Config.LEARNING_RATE)
        self.loss_func = BCEWithLogitsLoss()

    # 训练模型
    def train(self) -> None:
        best_loss = float("inf")                                     # 最佳损失
        for epoch in range(self.epochs):                             # 多轮训练
            average_loss = self.train_one_epoch()
            print(f"第 {epoch + 1} 轮训练集损失 loss = {average_loss:.4f}")
            
            if average_loss < best_loss:                             # 保存训练好的模型
                best_loss = average_loss
                save(obj=self.model.state_dict(), f=Config.MODEL_PATH)
            
    # 训练一个 epoch
    def train_one_epoch(self) -> float:
        self.model.train()                                           # 模型训练模式
        total_loss = 0                                               # 训练模型损失
        bar = tqdm(iterable=self.dataloader, desc="Training：")      # 进度条
        for batch in bar:
            input_ids = batch[Config.INPUT_IDS].to(self.device)      # 输入 IDs：(batch_size, seq_len)
            attention_mask = batch[Config.ATTENTION_MASK].to(self.device)      # 注意力掩码：(batch_size, seq_len)
            labels = batch[Config.LABEL_FIELD].float().to(self.device)         # 标签：(batch_size)
            token_type_ids = batch[Config.TOKEN_TYPE_IDS].to(self.device)      # token_type_ids：(batch_size, seq_len)
            self.optimizer.zero_grad()                               # 清除历史梯度
            # 前向传播过程
            
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
            loss_value = self.loss_func(input=outputs, target=labels)          # 计算损失
            loss_value.backward()                                    # 反向传播并更新参数
            self.optimizer.step()                                    # 更新参数
            total_loss += loss_value.item()                          # 累加损失
        
        average_loss = total_loss / len(self.dataloader)             # 计算平均损失
        return average_loss


# 评估测试模型
class PredictEvaluate:
    def __init__(self):
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.model = ReviewAnalysisModel().to(device=self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(Config.BERT_MODEL_NAME)
        model_params = load(f=Config.MODEL_PATH, map_location=self.device)
        self.model.load_state_dict(state_dict=model_params)
    
    # 预测文本
    def predict_text(self, text: str) -> str:
        # 文本编码为张量形式（长度固定）
        tokenized = self.tokenizer(text=text, max_length=Config.SEQ_LEN,
                                   truncation=Config.IS_TRUNCATION, return_tensors="pt",
                                   padding=Config.PADDING_TYPE)
        
        inputs = tokenized[Config.INPUT_IDS].to(device=self.device)
        attention_mask = tokenized[Config.ATTENTION_MASK].to(device=self.device)
        
        # 模型预测
        prob = self.predict_batch(input_ids=inputs, attention_mask=attention_mask)[0]
        return prob
    
    # 预测一个批次
    def predict_batch(self, input_ids, attention_mask) -> list:
        self.model.eval()
        with no_grad():
            # 前向传播：(batch_size,)
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            
            probs = sigmoid(input=outputs)                           # 概率值 ∈ [0, 1]，表示为正面情感的置信度
            results = probs.tolist()                                 # 转为列表
        return results
    
    # 评估测试集
    def evaluate(self) -> float:
        self.model.eval()                                            # 模型评估模式
        correct = 0                                                  # 正确数量
        total = 0                                                    # 总数量
        
        dataloader = ReviewDataset(data_path=Config.TEST_PATH).get_dataloader()
        bar = tqdm(iterable=dataloader, desc="Evaluating：")          # 进度条
        for batch in bar:
            inputs = batch[Config.INPUT_IDS].to(device=self.device)   # (batch_size, seq_len)
            attention_mask = batch[Config.ATTENTION_MASK].to(device=self.device)    # (batch_size, seq_len)
            labels = batch[Config.LABEL_FIELD].to(device=self.device) # (batch_size,)
            
            #  预测每个样本的正面情感概率
            probs = self.predict_batch(input_ids=inputs, attention_mask=attention_mask)
            
            # 将概率转换为预测标签（>= 0.5 为正面）
            preds = [1 if prob >= 0.5 else 0 for prob in probs]
            
            # 计算准确数量
            for pred, label in zip(preds, labels):
                if pred == int(label.item()):
                    correct += 1
            total += len(labels)
        
        # 输出准确率
        if total > 0:
            accuracy = correct / total
        else:
            accuracy = 0
        return accuracy

        
# 配置类
class Config:
    # ============================== 参数路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                            # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                             # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                 # 项目路径
    RAW_DATA_SUFFIX = "csv"                                         # 原始数据后缀
    RAW_DATA_PATH = abspath(path=f"{PROJECT_DIR}/data/online_shopping_10_cats.csv")   # 原始数据路径
    # MODEL_PATH = abspath(path=f"{PROJECT_DIR}/models/bert-base-chinese")  # 模型名称
    TOKENIZER_PATH = "bert-base-chinese"                             # 分词器称
    TRAIN_PATH = abspath(path=f"{PROJECT_DIR}/data/train-ai")        # 训练数据路径
    TEST_PATH = abspath(path=f"{PROJECT_DIR}/data/test-ai")          # 测试数据路径
    MODEL_PATH = abspath(path=f"{PROJECT_DIR}/models/evalue-ai.pt")  # 训练模型路径
    BERT_MODEL_NAME = TOKENIZER_PATH                                 # BERT 模型名称
    
    # ============================== 数据字段 ==============================
    TRAIN_FLAG = "train"                                             # 训练标志
    TEST_FLAG = "test"                                               # 测试标志
    REVIEW_FIELD = "review"                                          # 评论字段
    LABEL_FIELD = "label"                                            # 标签字段
    CATEGORY_FIELD = "cat"                                           # 类别字段
    LABEL_SCORE = [0, 1]                                             # 标签范围
    EMOTION_SCORE = ["negative", "positive"]                         # 情感范围
    LABEL_MAP = dict(zip(LABEL_SCORE, EMOTION_SCORE))                # 标签映射
    INPUT_IDS = "input_ids"                                          # 输入 ID 字段
    ATTENTION_MASK = "attention_mask"                                # 注意力掩码字段
    TOKEN_TYPE_IDS = "token_type_ids"                                # 分词类型 ID 字段
    DATASET_COLUMNS = [INPUT_IDS, ATTENTION_MASK, LABEL_FIELD]       # 数据集字段
    
    # ============================== 训练超参数 ==============================
    IS_TRUNCATION = True                                             # 是否截断
    PADDING_TYPE = "max_length"                                      # 填充方式
    SEQ_LEN = 128                                                    # 最大序列长度
    BATCH_SIZE =16                                                   # 批处理大小
    IS_SHUFFLE = True                                                # 是否打乱数据
    LEARNING_RATE = 1e-5                                             # 学习率
    EPOCHS = 1                                                      # 训练轮数

"""
# 测试
class AITest(TestCase):
    @staticmethod
    def test_process():
        process = DataProcessor(raw_path=Config.RAW_DATA_PATH)
        process.process_data()
    
    @staticmethod
    def test_loader():
        dataset = ReviewDataset(data_path=Config.TRAIN_PATH)
        loader = dataset.get_dataloader()
        
        for batch in loader:
            for k, v in batch.items():
                print(f"{k} ==> {v.shape}")
            break
    
    @staticmethod
    def test_model():
        models = ReviewAnalysisModel(freeze_bert=True)
        print(models)
    
    @staticmethod
    def test_train():
        trainer = Trainer()
        trainer.train()
    
    @staticmethod
    def test_predict():
        predict = PredictEvaluate()
        while True:
            text = input(">>> ：").strip().lower()
            if not text:
                break
            else:
                prob = predict.predict_text(text=text)
                print(f"置信度：{prob:.2f}")
    
    @staticmethod
    def test_evaluate():
        evaluate = PredictEvaluate()
        accuracy = evaluate.evaluate()
        print(f"准确率：{accuracy:.4f}")
"""


if __name__ == '__main__':
    trainer = Trainer()
    trainer.train()
