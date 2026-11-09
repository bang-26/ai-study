#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  input_method 
    CreateTime     ：  2026-09-18 17:11:37 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from common import BaseConfig, BaseModel, JiebaTokenizer, BaseDataset, BaseTrainer, BaseTester, BasePredictor

from os.path import abspath
from pandas import read_json, DataFrame
from sklearn.model_selection import train_test_split
from jieba import lcut
from torch import Tensor
from torch.optim import Adam
from torch.nn import CrossEntropyLoss, Linear, Embedding, RNN
from torch.utils.data import DataLoader


# 配置类
class InputMethodConfig(BaseConfig):
    # =================================== 参数路径 ===================================
    SAVED_MODEL_PATH = abspath(path=f"{BaseConfig.MODEL_DIR}/input-method.pt")
    RAW_DATASET_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/synthesized_.jsonl")
    PROJECT_NAME = "input-method"
    
    VOCAB_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}.vocab")
    TRAIN_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-train.json")
    VALID_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-valid.json")
    TEST_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-test.json")
    
    BOARD_DIR = abspath(path=f"{BaseConfig.PROJECT_DIR}/board/{PROJECT_NAME}")
    
    # =================================== 字段标识 ===================================
    TRAIN_FLAG = "train"                                             # 训练标志
    VALID_FLAG = "valid"                                             # 验证标志
    TEST_FLAG = "test"                                               # 测试标志
    
    # =================================== 模型参数 ===================================
    VECTOR_LENGTH = 5                                                # 向量大小
    EMBEDDING_DIM = 128                                              # 嵌入层维度
    HIDDEN_DIM = 256                                                 # 隐藏层维度
    
    # ==================================== 超参数 ====================================
    LEARNING_RATE = 1e-5                                             # 学习率
    BATCH_SIZE = 1024                                                 # 批处理大小
    EPOCHS = 50                                                      # 训练轮数
    
    
# 输入法数据集
class InputMethodDataset(BaseDataset):
    def __init__(self, data_path: str):
        super().__init__(data_path=data_path)
        data_frame = read_json(path_or_buf=self.data_path, lines=True, orient="records")
        self.data = data_frame.to_dict(orient="records")


# 原始数据处理器
class RawDataProcessor(JiebaTokenizer):
    def __init__(self, config: InputMethodConfig):
        super().__init__(config=config)
        
        self.raw_data = config.RAW_DATASET_PATH                      # 原始数据路径
        self.batch_size = config.BATCH_SIZE                          # 批处理大小
        self.dataset_dir = config.DATASET_DIR                        # 处理后数据集目录
        self.data_length = config.VECTOR_LENGTH                      # 词表数据长度
    
    # 加载数据
    def load_data(self, sample_factor: float = 0.1) -> tuple[list[str], list[str]]:
        json_df = read_json(path_or_buf=self.raw_data, lines=True, orient="records")
        sample_df = json_df.sample(frac=sample_factor, random_state=42)
        
        sentence_list = []
        for dialog in sample_df["dialog"]:
            for content in dialog:
                sentence = content.split("：")[1]
                sentence_list.append(sentence)
        
        train_sentence_list, test_sentence_list = train_test_split(sentence_list, test_size=0.2,
                                                                   random_state=42)
        return train_sentence_list, test_sentence_list
        
    # 构建数据集
    def build_dataset(self, sentence_list: list[str], save_path: str) -> None:
        # 1. 将句子转换为词元 ID
        sentence_id_list = [ [ self.word_id_dict.get(token, 0) for token in lcut(sentence) ] for sentence in sentence_list ]
        
        data_list = []
        # 2. 创建 Dataset
        for id_list in sentence_id_list:
            for i in range(len(id_list) - self.data_length):
                input_data = id_list[i: i + self.data_length]
                label_data = id_list[i + self.data_length]
                data_list.append({"input": input_data, "target": label_data})
        
        # 3. 保存数据集
        df = DataFrame(data_list)
        df.to_json(path_or_buf=save_path, orient="records", force_ascii=False, lines=True)
    
    # 构建数据加载器
    def build_dataloader(self, data_path: str) -> DataLoader:
        dataset = InputMethodDataset(data_path=data_path)
        dataloader = DataLoader(dataset=dataset, batch_size=self.batch_size, shuffle=True)
        return dataloader
    

# 输入法模型
class InputMethodModel(BaseModel):
    def __init__(self, config: InputMethodConfig, vocab_size: int = 100):
        super().__init__(config=config)
        
        self.vocab_size = vocab_size
        self.embedding_dim = config.EMBEDDING_DIM
        self.hidden_dim = config.HIDDEN_DIM
        
        # 定义嵌入层
        self.embedding = Embedding(num_embeddings=self.vocab_size, embedding_dim=self.embedding_dim)
        # 单层单项 RNN
        self.rnn = RNN(input_size=self.embedding_dim, hidden_size=self.hidden_dim, num_layers=1, batch_first=True)
        # 定义全连接层
        self.full_connection = Linear(in_features=self.hidden_dim, out_features=self.vocab_size)
    
    # 前向传播
    def forward(self, input_tensor) -> Tensor:
        embed = self.embedding.forward(input=input_tensor)           # 嵌入层
        rnn_output, _ = self.rnn.forward(input=embed)                # RNN
        feature = rnn_output[:, -1, :]                               # 取最后一个时间步的输出作为特征
        output_tensor = self.full_connection.forward(input=feature)  # 全连接层
        return output_tensor
        

# 输入法训练器
class InputMethodTrainer(BaseTrainer):
    def __init__(self, config: InputMethodConfig, model: InputMethodModel):
        super().__init__(config=config, model=model)
        
        self.loss_function = CrossEntropyLoss()                      # 损失函数
        self.model = model                                           # 模型
        
        self.optimizer = Adam(params=self.model.parameters(), lr=self.learning_rate)


# 输入法测试器
class InputMethodTester(BaseTester):
    def __init__(self, config: InputMethodConfig, model: InputMethodModel):
        super().__init__(config=config, model=model)
        
        self.loss_function = CrossEntropyLoss()                      # 损失函数
        self.model = model                                           # 模型
        

# 输入法预测器
class InputMethodPredictor(BasePredictor):
    def __init__(self, model: InputMethodModel, tokenizer: RawDataProcessor):
        super().__init__(model=model, tokenizer=tokenizer)
        
    # 输入预测
    def input_predict(self) -> None:
        history_words = ""                                           # 历史词元
        predict_words = []                                           # 预测词元
        
        while True:
            words = input(">>> ")                                    # 输入词元
            if words == "e" or words == "q":                         # 如果输入为 e 或 q，则退出循环
                break
            elif words.isdigit() and predict_words:                  # 如果输入为数字且有预测词元
                word_index = int(words)                              # 将输入转换为整数
                words = predict_words[word_index - 1]                # 获取预测词元
            
            history_words += words                                   # 将输入词元添加到历史词元字符串中
            if len(history_words) >= 5:                              # 如果历史词元列表长度大于等于5
                text = history_words[-5:]                           # 取最后5个历史词元作为文本列表
            else:
                text = history_words                                 # 取所有历史词元作为文本列表
            predict_words = self.predict(text_list=[text])[0]        # 预测词元
            print(f"Next: {predict_words}")
        
        
if __name__ == '__main__':
    config = InputMethodConfig()
    
    data_process = RawDataProcessor(config=config)
    trains, testes = data_process.load_data()

    data_process.build_vocab(sentence_list=trains)
    data_process.save_vocab()
    
    data_process.build_dataset(sentence_list=trains, save_path=config.TRAIN_PATH)
    data_process.build_dataset(sentence_list=testes, save_path=config.TEST_PATH)
    
    train_dataloader = data_process.build_dataloader(data_path=config.TRAIN_PATH)
    test_dataloader = data_process.build_dataloader(data_path=config.TEST_PATH)

    model = InputMethodModel(config=config, vocab_size=data_process.vocab_length)
    trainer = InputMethodTrainer(config=config, model=model)
    trainer.train(train_loader=train_dataloader)
    
    tester = InputMethodTester(config=config, model=model)
    average_loss = tester.test(test_loader=test_dataloader)
    print(f"Average Loss: {average_loss}")
    
