#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  common 
    CreateTime     ：  2026-09-18 17:21:21 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import environ
from typing import Union

environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from os.path import abspath, dirname
from time import strftime
from jieba import lcut
from torch import tensor, Tensor, device, cuda, no_grad, topk
from torch import long as torch_long, save as torch_save, load as torch_load
from torch.nn import Module, CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm


# 配置类
class BaseConfig:
    # =================================== 参数路径 ===================================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=f"{PYTHON_PATH}")                         # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    PROJECT_NAME = "nlp"                                             # 项目名称
    
    MODEL_DIR = abspath(path=f"{PROJECT_DIR}/models")                # 模型存储目录
    RAW_MODEL_PATH = abspath(path=f"{MODEL_DIR}/model.pt")           # 原始模型路径
    MODEL_PATH = abspath(path=f"{MODEL_DIR}/model.pt")         # 微调后，保存模型路径
    
    DATASET_DIR = abspath(path=f"{PROJECT_DIR}/data")                # 数据集目录
    RAW_DATASET_PATH = abspath(path=f"{DATASET_DIR}/raw")            # 原始数据集路径
    PROCESSED_DATASET_PATH = abspath(path=f"{DATASET_DIR}/process")  # 处理后数据集目录
    VOCAB_PATH = abspath(path=f"{DATASET_DIR}/{PROJECT_NAME}.vocab") # 词典路径
    
    BOARD_DIR = abspath(path=f"{PROJECT_DIR}/board/{PROJECT_NAME}")  # TensorBoard 目录
    
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")                    # 日志目录
    LOG_PATH = abspath(path=f"{LOG_DIR}/log.log")                    # 日志路径
    
    # =================================== 字段标识 ===================================
    TRAIN_FLAG = "train"                                             # 训练标志
    VALID_FLAG = "valid"                                             # 验证标志
    TEST_FLAG = "test"                                               # 测试标志
    UNKNOWN_TOKEN = "<unk>"                                          # 未知词标记
    PAD_TOKEN = "<pad>"                                              # 填充词标记
    START_TOKEN = "<sos>"                                            # 开始词标记
    END_TOKEN = "<eos>"                                              # 结束词标记
    
    # ==================================== 超参数 ====================================
    DEVICE = device("cuda" if cuda.is_available() else "cpu")        # 设备
    LEARNING_RATE = 1e-3                                             # 学习率
    EPOCHS = 50                                                      # 训练轮数
    IS_TRUNCATION = True                                             # 是否截断
    BATCH_SIZE = 16                                                  # 批处理大小
    
    MAX_COUNTER = 3                                                  # 最大计数器
    MIN_LOSS = float("inf")                                          # 最小损失
    
    IS_TRAIN_SHUFFLE = True                                          # 训练集是否打乱
    IS_VALID_SHUFFLE = True                                          # 验证集是否打乱
    IS_TEST_SHUFFLE = True                                           # 测试集是否打乱
    
    PADDING_TYPE = "max_length"                                      # 填充方式
    SEQ_LEN = 128                                                    # 最大序列长度
    
    RETURN_TENSORS = "pt"                                            # 返回张量类型
    IS_PADDING = True                                                # 是否填充
    

# 数据集类
class BaseDataset(Dataset):
    # 初始化
    def __init__(self, data_path: str):
        self.data_path = data_path                                   # 数据集目录
        self.data = []                                               # 数据集数据
        
    # 获取数据集长度
    def __len__(self):
        length = len(self.data) if self.data else 0                  # 数据集长度
        return length
    
    # 获取数据集元素
    def __getitem__(self, index: int) -> tuple[Tensor, Tensor]:
        input_tensor = tensor(data=self.data[index].get("input"), dtype=torch_long)
        target_tensor = tensor(data=self.data[index].get("target"), dtype=torch_long)
        return input_tensor, target_tensor


# 分词器类
class JiebaTokenizer:
    def __init__(self, config: BaseConfig):
        self.vocab_path = config.VOCAB_PATH                          # 词典路径
        self.unknown_token = config.UNKNOWN_TOKEN                    # 未知词标记
        self.pad_token = config.PAD_TOKEN                            # 填充词标记
        self.start_token = config.START_TOKEN                        # 开始词标记
        self.end_token = config.END_TOKEN                            # 结束词标记
        
        self.word_id_dict = {}                                       # 词 -> ID
        self.id_word_dict = {}                                       # ID -> 词
        self.unknown_id = -1                                         # 未知词标记 ID
        self.pad_id = -1                                             # 填充词标记 ID
        self.start_id = -1                                           # 开始词标记 ID
        self.end_id = -1                                             # 结束词标记 ID
        self.vocab_length = 0                                        # 词典长度
        
    # 加载词典
    def load_vocab(self):
        # 加载词典
        with open(file=self.vocab_path, mode="r", encoding="utf-8") as f:
            content_list = [line.strip("\n") for line in f.readlines()]  # 去除每行的换行符
        
        # 填充词典
        for index, word in enumerate(content_list):
            self.word_id_dict[word] = index                          # 词 -> ID
            self.id_word_dict[index] = word                          # ID -> 词
        
        self.unknown_id = self.word_id_dict.get(self.unknown_token, -1)
        self.pad_id = self.word_id_dict.get(self.pad_token, -1)
        self.start_id = self.word_id_dict.get(self.start_token, -1)
        self.end_id = self.word_id_dict.get(self.end_token, -1)
        self.vocab_length = len(self.word_id_dict)
        print(f"vocab loaded from {self.vocab_path}, vocab length: {self.vocab_length}")
        
    # 保存词表
    def save_vocab(self):
        vocab_list = list(self.word_id_dict.keys())                  # 词表
        vocab_str = "\n".join(vocab_list)                            # 词表字符串
        
        with open(file=self.vocab_path, mode="w", encoding="utf-8") as f:
            f.write(vocab_str)
        print(f"Vocab saved to {self.vocab_path}")                   # 词表保存路径
    
    # 构建词表
    def build_vocab(self, sentence_list: list[str]):
        vocab_set = set()                                            # 词表集合
        for sentence in sentence_list:
            if sentence.strip():
                vocabs = lcut(sentence)                              # 分词
                vocab_set.update(vocabs)                             # 更新词表集合
        
        vocab_list = [self.unknown_token, self.pad_token] + list(vocab_set)    # 词表列表
        self.word_id_dict = { word: i for i, word in enumerate(vocab_list) }   # 词 -> ID
        self.id_word_dict = { i: word for word, i in enumerate(vocab_list) }   # ID -> 词
        self.vocab_length = len(vocab_list)                          # 词典长度
        
    # 分词编码
    def encode(self, text: str) -> Tensor:
        token_list = lcut(text)                                      # 分词
        
        word_id_list = [self.word_id_dict.get(token, self.unknown_id) for token in token_list]
        word_tensor = tensor(data=[word_id_list], dtype=torch_long)  # 转换为张量
        
        return word_tensor
    
    # 解码
    def decode(self, id_list: list[int]) -> list[str]:
        if isinstance(id_list, Tensor):
            id_list = id_list.tolist()
        
        token_list = [self.id_word_dict.get(i, self.unknown_token) for i in id_list]
        return token_list
    

class BaseModel(Module):
    def __init__(self, config: BaseConfig):
        super().__init__()
        self.device = config.DEVICE                                  # 设备
        self.model_path = config.MODEL_PATH                    # 模型保存路径
        
    def save_model(self):
        torch_save(obj=self.state_dict(), f=self.model_path)         # 保存当前模型参数
        print(f"模型已保存到 {self.model_path}")
        
    # 加载模型
    def load_model(self):
        model_param =  torch_load(f=self.model_path)                 # 加载模型参数
        self.load_state_dict(state_dict=model_param)                 # 加载模型参数到当前模型
        self.to(device=self.device)                                  # 设置模型到设备
        

# 训练器类
class BaseTrainer:
    def __init__(self, config: BaseConfig, model: Union[BaseModel, Module]):
        self.device = config.DEVICE                                  # 运行设备
        self.learning_rate = config.LEARNING_RATE                    # 学习率
        self.epochs = config.EPOCHS                                  # 训练轮数
        self.is_truncation = config.IS_TRUNCATION                    # 是否截断
        self.batch_size = config.BATCH_SIZE                          # 批处理大小
        self.max_counter = config.MAX_COUNTER                        # 最大计数器
        self.min_loss = config.MIN_LOSS                              # 最小损失
        self.saved_model_path = config.MODEL_PATH              # 保存模型路径
        self.bord_dir = config.BOARD_DIR                             # TensorBoard 目录
        
        self.loss_function = CrossEntropyLoss()                      # 损失函数
        self.model = model                                           # 模型
        self.optimizer = Adam(params=model.parameters(), lr=self.learning_rate)
        
    # 训练一个 epoch，计算平均损失
    def train_one_epoch(self, train_loader: DataLoader, is_bar: bool = False) -> float:
        if is_bar:
            bar = tqdm(iterable=train_loader, desc="batch：", colour="red", ncols=100, leave=False)
        else:
            bar = train_loader
        
        self.model.train()                                           # 设置模型为训练模式
        total_loss = 0.0                                             # 初始化总损失为 0.0
        for input_tensor, target_tensor in bar:
            input_tensor = input_tensor.to(self.device)              # 将输入数据移到设备
            target_tensor = target_tensor.to(self.device)            # 将目标数据移到设备
            
            output_tensor = self.model.forward(input_tensor)         # 前向传播
            loss = self.loss_function(output_tensor, target_tensor)  # 计算损失
            loss.backward()                                          # 反向传播
            self.optimizer.step()                                    # 更新参数
            self.optimizer.zero_grad()                               # 清空梯度
            
            total_loss += loss.item()                                # 累加损失
        average_loss = total_loss / len(train_loader)                # 计算平均损失
        print(f"训练集平均损失: {average_loss:.4f}")
        
        return average_loss
    
    # 模型训练
    def train(self, train_loader: DataLoader) -> list[float]:
        self.model.to(device=self.device)                            # 设置模型到设备
        
        loss_list = []                                               # 初始化损失列表
        counter = 0                                                  # 初始化计数器为 0
        writer = self.__get_bord()                                   # 获取 TensorBoard 写入器
        bar = tqdm(iterable=range(self.epochs), desc="training ", colour="green", ncols=100, leave=False)
        for epoch in bar:
            average_loss = self.train_one_epoch(train_loader=train_loader, is_bar=False) # 训练一个 epoch
            loss_list.append(average_loss)                           # 记录平均损失
            writer.add_scalar(tag="loss", scalar_value=average_loss, global_step=epoch + 1)
            
            bar.set_postfix(loss=average_loss)                       # 设置进度条的后缀为损失
            print(f"epoch：{epoch + 1}, loss: {average_loss:.4f}")
            
            # 如果损失没有下降，并且计数器超过最大计数器，则提前结束训练，避免过拟合
            if average_loss > self.min_loss and counter > self.max_counter:
                break                                                # 提前结束训练
            elif average_loss < self.min_loss:
                self.min_loss = average_loss                         # 更新最小损失
            else:
                counter += 1                                         # 计数器加 1
                
        writer.close()                                               # 关闭 TensorBoard 写入器
        
        # 保存模型
        try:
            self.model.save_model()                                  # 基本模型保存
        except Exception:
            self.model.save_pretrained(save_directory=self.saved_model_path)   # 预训练模型保存
        finally:
            print(f"模型已保存到 {self.saved_model_path}")
        
        return loss_list
    
    # 获取 TensorBoard 写入器
    def __get_bord(self):
        time_dir = strftime("%m-%d-%H-%M")
        bord_path = abspath(path=f"{self.bord_dir}/{time_dir}")      # TensorBoard 路径
        writer = SummaryWriter(log_dir=bord_path)                    # TensorBoard 写入器
        return writer
        
        
# 测试器
class BaseTester:
    def __init__(self, config: BaseConfig, model: BaseModel):
        self.model_path = config.MODEL_PATH                    # 模型路径
        self.device = config.DEVICE                                  # 设备
        self.model = model                                           # 模型
        self.loss_function = CrossEntropyLoss()                      # 损失函数
        
    # 测试模型
    def test(self, test_loader: DataLoader, top_k: int = 5):
        self.model.load_model()                                      # 加载模型
        self.model.eval()                                            # 设置模型为评估模式
        
        top1_count = 0                                               # 初始化 top1 计数器为 0
        topk_count = 0                                               # 初始化 topk 计数器为 0
        total_count = 0                                              # 初始化总计数器为 0
        with no_grad():
            bar = tqdm(iterable=test_loader, desc="testing：", colour="green", ncols=100, leave=False)
            for input_tensor, target_tensor in bar:
                input_tensor = input_tensor.to(self.device)          # 将输入数据移到设备
                target_tensor = target_tensor.to(self.device)        # 将目标数据移到设备
                
                output_tensor = self.model(input_tensor)             # 前向传播
                probability_tensor = topk(input=output_tensor, k=top_k)   # 获取前 k 个最大概率
                word_id_tensor = probability_tensor.indices          # 获取前 k 个最大概率的索引，形状 (batch_size, top_k)

                for predict_id_tensor, target_id_tensor in zip(word_id_tensor, target_tensor):
                    if predict_id_tensor[0] == target_id_tensor:     # top1 命中：第一个预测词等于目标词
                        top1_count += 1
                        topk_count += 1
                    elif (predict_id_tensor == target_id_tensor).any():  # topk 命中：目标词在前 k 个预测词中
                        topk_count += 1
                    total_count += 1
        
        top1_average = top1_count / total_count                      # 计算 top1 准确率
        topk_average = topk_count / total_count                      # 计算 topk 准确率
        return top1_average, topk_average


# 预测器
class BasePredictor:
    def __init__(self, model: BaseModel, tokenizer: JiebaTokenizer):
        self.model = model                                           # 模型
        self.tokenizer = tokenizer                                   # 分词器
        
        self.model.load_model()                                      # 加载模型
        self.tokenizer.load_vocab()                                  # 加载词表
        
        self.top_k = 5                                               # top_k 个预测结果
        
    # 预测一个词
    def __predict_one(self, text: str, top_k: int = 5) -> list[str]:
        input_tensor = self.tokenizer.encode(text=text)              # 分词
        self.model.eval()                                            # 设置模型为评估模式
        
        with no_grad():                                              # 禁用梯度计算
            output_tensor = self.model(input_tensor)                 # 前向传播（batch_size=1, vocab_size）
        
        probability_list = topk(input=output_tensor, k=top_k)        # 获取前 k 个最大概率
        word_id_list = probability_list.indices.tolist()[0]          # 获取最大概率的索引
        
        predict_word_list = self.tokenizer.decode(id_list=word_id_list)
        return predict_word_list
        
    # 预测多个词
    def predict(self, text_list: list[str]) -> list[list[str]]:
        if isinstance(text_list, str):                               # 如果输入是字符串，则转换为列表
            text_list = [text_list]                                  # 转换为列表
        
        if not self.tokenizer.word_id_dict:
            self.model.load_model()                                  # 加载模型
            self.tokenizer.load_vocab()                              # 加载词典
            
        predicted_words_list = []                                    # 初始化预测结果列表
        for text in text_list:
            predict_word = self.__predict_one(text=text, top_k=self.top_k)    # 预测词
            predicted_words_list.append(predict_word)                # 添加预测结果到列表
            
        return predicted_words_list
