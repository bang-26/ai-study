#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  review_analysis 
    CreateTime     ：  2026-10-13 09:35:54 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from common import BaseConfig, JiebaTokenizer, BaseDataset, BaseModel, BaseTrainer, BaseTester, BasePredictor
from os.path import abspath
from pandas import read_csv, read_json, DataFrame
from sklearn.model_selection import train_test_split
from jieba import lcut
from torch import Tensor, tensor, arange, no_grad, sigmoid, long as torch_long, float as torch_float
from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss, Linear, Embedding, LSTM
from torch.utils.data import DataLoader


# 配置类
class ReviewAnalysisConfig(BaseConfig):
    # =================================== 参数路径 ===================================
    PROJECT_NAME = "review-analysis"
    
    SAVED_MODEL_PATH = abspath(path=f"{BaseConfig.MODEL_DIR}/{PROJECT_NAME}.pt")
    RAW_DATASET_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/online_shopping_10_cats.csv")
    
    VOCAB_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}.vocab")
    TRAIN_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-{BaseConfig.TRAIN_FLAG}.jsonl")
    TEST_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-{BaseConfig.TEST_FLAG}.jsonl")
    
    BOARD_DIR = abspath(path=f"{BaseConfig.PROJECT_DIR}/board/{PROJECT_NAME}")
    
    # =================================== 分词参数 ===================================
    MAX_SEQ_LENGTH = 128                                             # 词表最大序列长度
    
    # =================================== 模型参数 ===================================
    PADDING_ID = 1                                                   # 填充词索引
    EMBEDDING_DIM = 128                                              # 嵌入层维度
    HIDDEN_DIM = 256                                                 # 隐藏层维度
    
    # ==================================== 超参数 ====================================
    LEARNING_RATE = 1e-3                                             # 学习率
    BATCH_SIZE = 128                                                 # 批处理大小
    EPOCHS = 10                                                      # 训练轮数
    

# 分词器
class ReviewAnalysisTokenizer(JiebaTokenizer):
    def __init__(self, config: ReviewAnalysisConfig):
        super().__init__(config=config)
        
        self.device = config.DEVICE                                  # 设备
        self.max_seq_length = config.MAX_SEQ_LENGTH                  # 最大序列长度
    
    # 编码方法
    def encode(self,text: str) -> Tensor:
        token_list = lcut(text)                                      # 对文本进行分词
        
        if len(token_list) > self.max_seq_length:
            token_list = token_list[:self.max_seq_length]
        elif len(token_list) < self.max_seq_length:
            token_list += [self.pad_token] * (self.max_seq_length - len(token_list))
        
        word_id_list = [self.word_id_dict.get(token, self.unknown_id) for token in token_list]
        word_tensor = tensor(data=[word_id_list], dtype=torch_long)  # 转换为张量
        
        return word_tensor.to(device=self.device)


# 数据集
class ReviewAnalysisDataset(BaseDataset):
    def __init__(self, data_path: str):
        super().__init__(data_path=data_path)
        
        data_frame = read_json(path_or_buf=self.data_path, lines=True, orient="records")
        self.data = data_frame.to_dict(orient="records")
    
    def __getitem__(self, index: int) -> tuple[Tensor, Tensor]:
        item = self.data[index]                                      # 获取数据项
        review = tensor(data=item.get("review"), dtype=torch_long)   # 获取评论并转换为张量
        label = tensor(data=item.get("label"), dtype=torch_float)    # 标签转为浮点型，匹配 BCEWithLogitsLoss
        return review, label


# 处理类
class ReviewAnalysisProcess:
    def __init__(self, config: ReviewAnalysisConfig, tokenizer: ReviewAnalysisTokenizer):
        self.raw_data_path = config.RAW_DATASET_PATH                 # 原始数据路径
        self.batch_size = config.BATCH_SIZE                          # 批处理大小
        self.dataset_dir = config.DATASET_DIR                        # 处理后数据集目录
        self.is_shuffle = config.IS_TRAIN_SHUFFLE                    # 是否打乱数据
        
        self.tokenizer = tokenizer                                   # 分词器
    
    # 加载数据
    def load_data(self, test_size: float = 0.2) -> tuple[DataFrame, DataFrame]:
        # 1. 读取 CSV 文件
        csv_df = read_csv(filepath_or_buffer=self.raw_data_path, usecols=["label", "review"], encoding="utf-8").dropna()
        
        # 2. 分割训练集和测试集
        train_df, test_df = train_test_split(csv_df, test_size=test_size, stratify=csv_df["label"])
        
        return train_df, test_df
    
    # 构建词典
    def build_vocab(self, data_df: DataFrame) -> None:
        sentence_list = data_df["review"].tolist()                   # 转换为列表
        self.tokenizer.build_vocab(sentence_list=sentence_list)      # 构建词典
        self.tokenizer.save_vocab()                                  # 保存词典
        
    # 构建数据集
    def build_dataset(self, data_df: DataFrame, save_path: str) -> None:
        self.tokenizer.load_vocab()                                  # 加载词典
        # 必须将 Tensor 转为 Python 原生列表，否则 to_json 用 ujson 序列化 Tensor 会无限递归报错
        data_df["review"] = data_df["review"].apply(lambda text: self.tokenizer.encode(text=text).flatten().tolist())
        
        data_df.to_json(path_or_buf=save_path, orient="records", force_ascii=False, lines=True)
        print(f"数据集已保存到：{save_path}")
    
    # 构建数据加载器
    def build_dataloader(self, data_path: str) -> DataLoader:
        dataset = ReviewAnalysisDataset(data_path=data_path)         # 创建数据集
        dataloader = DataLoader(dataset=dataset, batch_size=self.batch_size, shuffle=self.is_shuffle)
        print(f"数据集已加载：{data_path}")
        
        return dataloader


# 模型类
class ReviewAnalysisModel(BaseModel):
    def __init__(self, config: ReviewAnalysisConfig, vocab_size: int = 128):
        super().__init__(config=config)
        
        self.vocab_size = vocab_size                                 # 词典大小
        self.embedding_dim = config.EMBEDDING_DIM                    # 嵌入层维度
        self.hidden_dim = config.HIDDEN_DIM                          # 隐藏层维度
        self.padding_id = config.PADDING_ID                          # 填充索引
        
        self.embedding = Embedding(num_embeddings=self.vocab_size, embedding_dim=self.embedding_dim,
                                   padding_idx=self.padding_id)
        self.lstm = LSTM(input_size=self.embedding_dim, hidden_size=self.hidden_dim, batch_first=True)
        self.full_connection = Linear(in_features=self.hidden_dim, out_features=1)
        
    def forward(self, input: Tensor) -> Tensor:
        embedding = self.embedding.forward(input=input)              # 嵌入层
        lstm_output, (_, _) = self.lstm.forward(input=embedding)     # LSTM 层
        
        indices = arange(lstm_output.shape[0])                       # 获取索引
        length = (input != self.embedding.padding_idx).sum(dim=1)    # 获取序列长度
        feature = lstm_output[indices, length - 1]                   # 取真实最后一个时间步的输出作为特征
        
        output = self.full_connection.forward(input=feature)         # 全连接层
        return output.squeeze(-1)


# 训练类
class ReviewAnalysisTrainer(BaseTrainer):
    def __init__(self, config: ReviewAnalysisConfig, model: ReviewAnalysisModel):
        super().__init__(config=config, model=model)
        
        self.loss_function = BCEWithLogitsLoss()                     # 损失函数
        self.optimizer = Adam(params=self.model.parameters(), lr=self.learning_rate)


# 预测
class ReviewAnalysisPredictor:
    def __init__(self, model: ReviewAnalysisModel, tokenizer: ReviewAnalysisTokenizer):
        self.model = model                                           # 模型
        self.tokenizer = tokenizer                                   # 分词器
        
        self.tokenizer.load_vocab()                                  # 加载词典
        self.model.load_model()                                      # 加载已训练模型权重
        
    # 预测多个词
    def predict(self, text_list: list[str]) -> list[float]:
        if isinstance(text_list, str):                               # 如果输入是字符串，则转换为列表
            text_list = [text_list]                                  # 转换为列表
            
        self.model.eval()                                            # 设置模型为评估模式
        predict_list = []                                            # 初始化预测结果列表
        for text in text_list:
            review_tensor = self.tokenizer.encode(text=text)         # 分词编码
            
            with no_grad():                                          # 禁用梯度计算
                label_tensor = self.model.forward(review_tensor)     # 前向传播
                
            label = sigmoid(input=label_tensor).item()               # 取概率标量，避免返回嵌套列表
            predict_list.append(label)                               # 添加预测结果到列表
            
        return predict_list
        
    # 输入预测
    def input_predict(self) -> None:
        while True:
            words = input(">>> ")                                    # 输入词元
            if words == "e" or words == "q":                         # 如果输入为 e 或 q，则退出循环
                break
            
            label = self.predict(text_list=[words])[0]               # 预测标签
            if label >= 0.5:                                         # 判断评价
                print(f"Positive：{label:.4f}")                      # 输出正面评价
            else:
                print(f"Negative：{label:.4f}")                      # 输出负面评价
