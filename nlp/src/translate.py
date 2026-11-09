#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  translate 
    CreateTime     ：  2026-06-21 14:01:28 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os.path import abspath
from math import sin as math_sin, cos as math_cos
from pandas import read_json, read_csv, DataFrame
from sklearn.model_selection import train_test_split
from nltk import TreebankWordTokenizer, TreebankWordDetokenizer
from torch import long as torch_long, bool as torch_bool, float as torch_float, zeros as torch_zeros
from torch import pow as torch_pow, exp as torch_exp, sin as torch_sin, cos as torch_cos, log as math_log
from torch import tensor, Tensor, softmax, cat, bmm, argmax, full, arange, no_grad, stack
from torch.nn import Module, Embedding, Transformer, Linear, CrossEntropyLoss, GRU
from torch.nn.utils.rnn import pad_sequence
from torch.optim import Optimizer, Adam
from torch.utils.data import DataLoader
from tqdm import tqdm
from common import BaseConfig, BaseDataset, BaseModel, BaseTrainer, BasePredictor, BaseTester


class TranslateConfig(BaseConfig):
    # =================================== 参数路径 ===================================
    PROJECT_NAME = "translate"
    
    SAVED_MODEL_PATH = abspath(path=f"{BaseConfig.MODEL_DIR}/{PROJECT_NAME}.pt")
    RAW_DATASET_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/cmn.txt")
    
    EN_VOCAB_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-en.vocab")
    ZH_VOCAB_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-zh.vocab")
    TRAIN_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-{BaseConfig.TRAIN_FLAG}.jsonl")
    TEST_PATH = abspath(path=f"{BaseConfig.DATASET_DIR}/{PROJECT_NAME}-{BaseConfig.TEST_FLAG}.jsonl")
    
    BOARD_DIR = abspath(path=f"{BaseConfig.PROJECT_DIR}/board/{PROJECT_NAME}")
    
    # =================================== 分词参数 ===================================
    MAX_VOCAB_LENGTH = 100 * 1000                                    # 词表最大序列长度
    MAX_SEQ_LENGTH = 128                                             # 序列最大长度
    ZH_COLUMN = "zh"                                                 # 中文列名
    EN_COLUMN = "en"                                                 # 英文列名
    
    # =================================== 模型参数 ===================================
    PADDING_ID = 0                                                   # 填充词索引
    EMBEDDING_DIM = 128                                              # 嵌入层维度
    HIDDEN_DIM = 256                                                 # 隐藏层维度
    
    DIM_MODEL = 128                                                  # Transformer 模型维度
    NUM_HEADS = 4                                                    # 注意力头数
    ENCODER_LAYERS = 2                                               # 编码器层数
    DECODER_LAYERS = 2                                               # 解码器层数
    DIM_FEEDFORWARD = 512                                            # 前馈网络维度
    DROPOUT = 0.1                                                    # Dropout 概率
    
    # ==================================== 超参数 ====================================
    LEARNING_RATE = 1e-3                                             # 学习率
    BATCH_SIZE = 1024                                                # 批处理大小
    EPOCHS = 10                                                      # 训练轮数
    

# 基础分词器
class TranslateTokenizer:
    def __init__(self, config: TranslateConfig) -> None:
        self.unknown_token = config.UNKNOWN_TOKEN                    # 未知词标记
        self.pad_token = config.PAD_TOKEN                            # 填充词标记
        self.start_token = config.START_TOKEN                        # 开始词标记
        self.end_token = config.END_TOKEN                            # 结束词标记
        self.device = config.DEVICE                                  # 设备
        self.max_vocab_length = config.MAX_VOCAB_LENGTH              # 词表最大序列长度
        
        self.word_id_dict = {}                                       # 词 -> ID
        self.id_word_dict = {}                                       # ID -> 词
        self.pad_id = 0                                              # 填充词标记 ID
        self.unknown_id = 1                                          # 未知词标记 ID
        self.start_id = 2                                            # 开始词标记 ID
        self.end_id = 3                                              # 结束词标记 ID
        self.vocab_length = 0                                        # 词典长度
        
    # 编码（将文本分词、id 化），并指定序列长度
    def encode(self, text: str, mark: bool = False) -> list:
        token_list = self.tokenize(text)                             # 分词
        if mark:                                                     # 如果是目标序列，就在前后加入标记
            token_list = [self.start_token] + token_list + [self.end_token]
        
        token_id_list = [self.word_id_dict.get(token, self.unknown_id) for token in token_list]  # id 化
        return token_id_list
        
    # 解码（将 id 反向编码为文本），并去除标记
    def decode(self, token_id_list: list[int]) -> str:
        token_list = [self.id_word_dict.get(id, self.unknown_token) for id in token_id_list]
        text = ''.join(token_list)
        return text
    
    # 分词，类方法
    @classmethod
    def tokenize(self, text: str) -> list:
        pass
    
    # 构建词表，并保存到文件
    def build_vocab(self, sentence_list: list[str], vocab_path: str) -> None:
        vocab_set = set()                                            # 针对训练集分词，构建词表
        for sentence in sentence_list:
            token_list = self.tokenize(text=sentence)                # 分词
            vocab_set.update(token_list)                             # 添加到集合中
        
        vocab_list = [self.pad_token, self.unknown_token, self.start_token, self.end_token] + list(vocab_set)
        self.vocab_length = len(vocab_list)                          # 词典长度
        
        # 保存词表到文件
        vocab_string = "\n".join(vocab_list[:self.max_vocab_length]) # 词表字符串
        with open(file=vocab_path, mode='w', encoding='utf-8') as f:
            f.write(vocab_string)
        
        print(f"Vocab saved to {vocab_path}")                        # 词表保存路径
        
    # 从文件加载词表，并创建分词器对象实例
    def load_vocab(self, vocab_path: str):
        # 获取词表
        with open(file=vocab_path, mode='r', encoding='utf-8') as f:
            content_list = f.readlines()                             # 获取词表
        
        vocab_list = []                                              # 词表
        for content in content_list:
            vocab = content.strip()                                  # 去除空白符
            vocab_list.append(vocab)                                 # 添加到词表
            
        self.vocab_length = len(vocab_list)                          # 词典长度
        self.word_id_dict = {vocab: i for i, vocab in enumerate(vocab_list)}   # 词 -> ID
        self.id_word_dict = {i: vocab for i, vocab in enumerate(vocab_list)}   # ID -> 词


# 中文分词器
class ChineseTokenizer(TranslateTokenizer):
    def __init__(self, config: TranslateConfig) -> None:
        super().__init__(config=config)
        
    @classmethod
    def tokenize(cls, text: str) -> list:
        tokens = list(text)                                          # 分词
        return tokens


# 英文分词器
class EnglishTokenizer(TranslateTokenizer):
    def __init__(self, config: TranslateConfig) -> None:
        super().__init__(config=config)
    
    # 分词
    @classmethod
    def tokenize(cls, text: str) -> list[str]:
        tokenizer = TreebankWordTokenizer()                          # 创建分词器
        token_list = tokenizer.tokenize(text)                        # 分词
        return token_list
    
    # 解码（将 id 反向编码为文本），并去除标记
    def decode(self, token_id_list: list) -> str:
        detokenizer = TreebankWordDetokenizer()                      # 创建分词器
        token_list = [self.id_word_dict.get(id, self.unknown_token) for id in token_id_list]
        text = detokenizer.detokenize(token_list)                    # token_list 逆向编码为文本
        return text
        
        
# 自定义数据集类
class TranslationDataset(BaseDataset):
    # 初始化
    def __init__(self, data_path: str):
        super().__init__(data_path=data_path)
        
        data_frame = read_json(path_or_buf=self.data_path, lines=True, orient="records")
        self.data = data_frame.to_dict(orient="records")
        
    # 根据 index，获取数据集元素
    def __getitem__(self, index: int):
        item = self.data[index]                                      # 获取数据集元素
        inputs = tensor(data=item.get("zh"), dtype=torch_long)       # 获取输入序列
        targets = tensor(data=item.get("en"), dtype=torch_long)      # 获取目标序列
        return inputs, targets
        

# 数据处理
class TranslateDataProcess:
    def __init__(self, config: TranslateConfig):
        self.raw_data_path = config.RAW_DATASET_PATH                 # 原始数据路径
        self.zh_column = config.ZH_COLUMN                            # 中文列名
        self.en_column = config.EN_COLUMN                            # 英文列名
        self.en_vocab_path = config.EN_VOCAB_PATH                    # 英文词典路径
        self.zh_vocab_path = config.ZH_VOCAB_PATH                    # 中文词典路径
        self.train_path = config.TRAIN_PATH                          # 训练数据路径
        self.test_path = config.TEST_PATH                            # 测试数据路径
        
        self.batch_size = config.BATCH_SIZE                          # 批处理大小
        self.is_shuffle = config.IS_TRAIN_SHUFFLE                    # 是否打乱数据
    
    # 数据处理
    def load_data(self) -> tuple[DataFrame, DataFrame]:
        # 1. 以 csv 格式读取 txt 文件，得到 DataFrame；并提取两列，去除缺失值
        content = read_csv(self.raw_data_path, sep='\t', usecols=[0, 1],
                           names=[self.en_column, self.zh_column], encoding='utf-8')
        
        # 2. 删除缺失值
        data_frame = content.dropna()
        
        # 3. 对原始语料做划分
        train_df, test_df = train_test_split(data_frame, test_size=0.2, random_state=42)
        
        return train_df, test_df
    
    # 构建词表
    def build_vocab(self, data_frame: DataFrame, tokenizer: TranslateTokenizer, is_zh: bool = True):
        if is_zh:
            sentence_list = data_frame[self.zh_column].tolist()
            vocab_path = self.zh_vocab_path
        else:
            sentence_list = data_frame[self.en_column].tolist()
            vocab_path = self.en_vocab_path
        
        tokenizer.build_vocab(sentence_list=sentence_list, vocab_path=vocab_path)
    
    # 构建数据集
    def build_dataset(self, data_frame: DataFrame, zh_tokenizer: TranslateTokenizer,
                      en_tokenizer: TranslateTokenizer, is_train: bool = True):
        # 1. 加载词表
        zh_tokenizer.load_vocab(vocab_path=self.zh_vocab_path)
        en_tokenizer.load_vocab(vocab_path=self.en_vocab_path)
        
        # 2. 构建数据集
        data_frame["zh"] = data_frame["zh"].apply(lambda x: zh_tokenizer.encode(text=x, mark=False))
        data_frame["en"] = data_frame["en"].apply(lambda x: en_tokenizer.encode(text=x, mark=True))
        
        # 3. 获取数据集保存路径
        if is_train:
            data_path = self.train_path
        else:
            data_path = self.test_path
        
        data_frame.to_json(path_or_buf=data_path, orient="records", lines=True)
        print(f"Dataset saved to {data_path}")
    
    # 构建数据加载器
    def build_loader(self, data_path: str):
        dataset = TranslationDataset(data_path=data_path)
        data_loader = DataLoader(dataset=dataset, batch_size=self.batch_size,
                                 shuffle=self.is_shuffle, collate_fn=self.collate_fn)
        return data_loader
    
    # 整理函数，将一批数据长度对齐（填充）
    @classmethod
    def collate_fn(cls, batch: list):
        # 先分成 inputs 和 targets 两个列表
        input_tensor_list = [ item[0] for item in batch ]
        target_tensor_list = [ item[1] for item in batch ]
        
        # 合并成长度对齐的一个 batch tensor
        inputs_tensor = pad_sequence(sequences=input_tensor_list, batch_first=True, padding_value=0)
        targets_tensor = pad_sequence(sequences=target_tensor_list, batch_first=True, padding_value=0)
        
        return inputs_tensor, targets_tensor
        

# 自定义注意力机制
class Attention(Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, decoder_hidden: Tensor, encoder_output: Tensor) -> Tensor:
        encoder_transpose = encoder_output.transpose(dim0=1, dim1=2) # 转置 encoder_output
        score = bmm(input=decoder_hidden, mat2=encoder_transpose)    # 1. 计算注意力评分(N * L * L)
        weight = softmax(input=score, dim=-1)                        # 2. 计算注意力权重(N * L)
        context = bmm(input=weight, mat2=encoder_output)             # 3. 计算上下文向量(N * L * H)
        return context
        

# 自定义翻译编码器
class TranslateEncoder(Module):
    def __init__(self, config: TranslateConfig, vocab_size: int):
        super().__init__()
        
        self.vocab_size = vocab_size                                 # 词典大小
        self.embedding_dim = config.EMBEDDING_DIM                    # 嵌入层维度
        self.hidden_dim = config.HIDDEN_DIM                          # 隐藏层维度
        self.padding_id = config.PADDING_ID                          # 填充索引
        
        # 嵌入层
        self.embedding = Embedding(num_embeddings=self.vocab_size, embedding_dim=self.embedding_dim,
                                   padding_idx=self.padding_id)
        
        # GRU 层
        self.gru = GRU(input_size=self.embedding_dim, hidden_size=self.hidden_dim, batch_first=True)
    
    # 前向传播
    def forward(self, input_tensor: Tensor) -> tuple[Tensor, Tensor]:
        if input_tensor.dim() == 1:                                  # 单条序列，补上批量维度
            input_tensor = input_tensor.unsqueeze(dim=0)
        
        embedded = self.embedding.forward(input=input_tensor)        # 嵌入层
        gru_output, hidden = self.gru.forward(input=embedded)        # GRU 层
        indices = arange(gru_output.shape[0])                        # 批量索引
        lengths = (input_tensor != self.padding_id).sum(dim=1).clamp(min=1)   # 获取序列长度，避免全 padding 取到 -1
        features = gru_output[indices, lengths - 1]                  # 取真实最后一个时间步的输出作为特征
        return gru_output, features
        
        
# 自定义翻译解码器
class TranslateDecoder(Module):
    def __init__(self, config: TranslateConfig, vocab_size: int):
        super().__init__()
        
        self.vocab_size = vocab_size                                 # 词典大小
        self.embedding_dim = config.EMBEDDING_DIM                    # 嵌入层维度
        self.hidden_dim = config.HIDDEN_DIM                          # 隐藏层维度
        self.padding_id = config.PADDING_ID                          # 填充索引
        
        # 嵌入层
        self.embedding = Embedding(num_embeddings=self.vocab_size, embedding_dim=self.embedding_dim,
                                   padding_idx=self.padding_id)
        
        # GRU 层
        self.gru = GRU(input_size=self.embedding_dim, hidden_size=self.hidden_dim, batch_first=True)
        
        # 注意力机制
        self.attention = Attention()
        
        # 输出线性层
        self.linear = Linear(in_features=self.hidden_dim * 2, out_features=self.vocab_size)
        
    # 前向传播
    def forward(self, input_tensor: Tensor, hidden_first: Tensor, encoder_output: Tensor):
        embedded = self.embedding.forward(input=input_tensor)                       # 嵌入层
        gru_output, hidden_end = self.gru.forward(input=embedded, hx=hidden_first)  # GRU 层:N * L * H
        context_vector = self.attention.forward(gru_output, encoder_output)         # 获取上下文向量，避免全 padding 取到 -1
        combined = cat(tensors=[context_vector, gru_output], dim=-1)                # 组合上下文向量和输出
        output = self.linear.forward(input=combined)                                # 输出线性层
        return output, hidden_end
    

# 翻译模型
class TranslateModel(BaseModel):
    def __init__(self, config: TranslateConfig, en_vocab_size: int, zh_vocab_size: int):
        super().__init__(config=config)
        
        self.en_vocab_size = en_vocab_size
        self.zh_vocab_size = zh_vocab_size
        
        self.encoder = TranslateEncoder(config=config, vocab_size=zh_vocab_size)    # 翻译编码器
        self.decoder = TranslateDecoder(config=config, vocab_size=en_vocab_size)    # 翻译解码器
     
    # 前向传播
    def forward(self, input_tensor: Tensor, hidden_first: Tensor):
        gru_output, features = self.encoder.forward(input_tensor=input_tensor)    # 编码器
        output, hidden_end = self.decoder.forward(input_tensor=features, hidden_first=hidden_first,
                                                  encoder_output=gru_output)      # 解码器
        return output, hidden_end


# 自定义位置编码
class PositionalEncoding(Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        
        pe = torch_zeros(size=(max_len, d_model), dtype=torch_float) # 初始化位置编码矩阵
        pos = arange(0, max_len, dtype=torch_float).unsqueeze(1)     # 位置索引
        _2i = arange(0, d_model, step=2, dtype=torch_float)          # 偶数索引
        
        div_term = torch_pow(10000, ( _2i / d_model))                # 计算分母项
        pe[:, 0::2] = torch_sin(pos / div_term)                      # 偶数位置使用正弦函数
        pe[:, 1::2] = torch_cos(pos / div_term)                      # 奇数位置使用余弦函数
        
        # # 遍历矩阵
        # for pos in range(max_len):
        #     for _2i in range(0, d_model, 2):
        #         pe[pos, _2i] = math_sin(pos / (10000 ** ( _2i / d_model)))     # 偶数位置使用正弦函数
        #         pe[pos, _2i + 1] = math_cos(pos / (10000 ** (_2i / d_model)))  # 奇数位置使用余弦函数
        
        self.register_buffer(name="pe", tensor=pe)                   # 注册位置编码矩阵为缓冲区
        
    # 前向传播
    def forward(self, embedding: Tensor) -> Tensor:
        sequence_length = embedding.shape[1]                         # 获取序列长度
        part_pe = self.pe[0: sequence_length]                        # 取出对应长度的编码，并增加批量维度
        result = embedding + part_pe                                 # 将位置编码加到嵌入向量上
        return result


# 自定义翻译训练器
class TranslateTransformer(BaseModel):
    def __init__(self, config: TranslateConfig, en_vocab_size: int, zh_vocab_size: int):
        super().__init__(config=config)
        # 词嵌入层
        self.zh_embedding = Embedding(num_embeddings=zh_vocab_size, embedding_dim=config.DIM_MODEL,
                                      padding_idx=config.PADDING_ID)          # 中文嵌入层
        self.en_embedding = Embedding(num_embeddings=en_vocab_size, embedding_dim=config.DIM_MODEL,
                                      padding_idx=config.PADDING_ID)          # 英文嵌入层
        
        # 位置编码
        self.positional_encoding = PositionalEncoding(d_model=config.DIM_MODEL, max_len=config.MAX_SEQ_LENGTH)
        
        # Transformer 层
        self.transformer = Transformer(d_model=config.DIM_MODEL, nhead=config.NUM_HEADS,
                                       num_encoder_layers=config.ENCODER_LAYERS,
                                       num_decoder_layers=config.DECODER_LAYERS,
                                       dim_feedforward=config.DIM_FEEDFORWARD, batch_first=True)
        
        # 输出线性层
        self.output_linear = Linear(in_features=config.DIM_MODEL, out_features=en_vocab_size)
    
    # 前向传播
    def forward(self, src: Tensor, tgt: Tensor, src_pad_mask: Tensor = None, tgt_mask: Tensor = None) -> Tensor:
        memory = self._encode(src=src, src_pad_mask=src_pad_mask)   # 编码
        output = self._decode(tgt=tgt, memory=memory, tgt_mask=tgt_mask, memory_mask=src_pad_mask)     # 解码器
        return output
    
    # 编码方法
    def _encode(self, src: Tensor, src_pad_mask: Tensor = None) -> Tensor:
        embed = self.zh_embedding.forward(input=src)                 # 嵌入层
        input = self.positional_encoding.forward(embedding=embed)    # 位置编码
        memory = self.transformer.encoder.forward(src=input, src_key_padding_mask=src_pad_mask)    # Transformer 编码器
        return memory
        
    # 解码方法
    def _decode(self, tgt: Tensor, memory: Tensor, tgt_mask: Tensor = None, memory_mask: Tensor = None) -> Tensor:
        embed = self.en_embedding.forward(input=tgt)                 # 嵌入层
        input = self.positional_encoding.forward(embedding=embed)    # 位置编码
        output = self.transformer.decoder.forward(tgt=input, memory=memory, tgt_mask=tgt_mask,
                                                  memory_key_padding_mask=memory_mask)    # Transformer 解码器
        linear_output = self.output_linear.forward(input=output)     # 输出线性层
        return linear_output
        

# 翻译训练器
class TranslateTrainer(BaseTrainer):
    def __init__(self, config: TranslateConfig, model: TranslateModel):
        super().__init__(config=config, model=model)
        
        self.model = model
        self.loss_function = CrossEntropyLoss()                      # 损失函数
        self.optimizer = Adam(params=self.model.parameters(), lr=self.learning_rate)
        
    # 训练一个 epoch
    def train_one_epoch(self, train_loader: DataLoader, is_bar: bool = False):
        self.model.train()                                           # 训练模式
        
        if is_bar:
            bar = tqdm(iterable=train_loader, desc="Training：", dynamic_ncols=True, colour="green", ncols=100, ascii=True)
        else:
            bar = train_loader
            
        total_loss = 0.0                                             # 总损失
        for inputs, targets in bar:
            inputs = inputs.to(self.device)                          # 输入移动到 GPU
            targets =  targets.to(self.device)                       # 目标移动到 GPU
            gru_output, context_vector = self.model.encoder.forward(input_tensor=inputs)   # 编码器
            
            decoder_inputs = targets[:, :-1]                         # 输入的标签
            decoder_targets = targets[:, 1:]                         # 目标的标签
            hidden_first = context_vector.unsqueeze(0)               # 扩展维度
            decoder_outputs, _ = self.model.decoder.forward(input_tensor=decoder_inputs, hidden_first=hidden_first,
                                                            encoder_output=gru_output)
            
            loss_value = self.loss_function(decoder_outputs.transpose(1, 2), decoder_targets)  # 计算损失
            loss_value.backward()                                    # 反向传播
            self.optimizer.step()                                    # 优化器更新参数
            self.optimizer.zero_grad()                               # 清空梯度
            total_loss += loss_value.item()                          # 累计损失
            
        average_loss = total_loss / len(train_loader)                # 平均损失
        return average_loss
        
        
# 翻译训练器
class TranslateTransformerTrainer(BaseTrainer):
    def __init__(self, config: TranslateConfig, model: TranslateTransformer):
        super().__init__(config=config, model=model)
        
        self.model = model                                           # 模型
        self.loss_function = CrossEntropyLoss()                      # 损失函数
        self.optimizer = Adam(params=self.model.parameters(), lr=self.learning_rate)
        
    # 训练一个 epoch
    def train_one_epoch(self, train_loader: DataLoader, is_bar: bool = False):
        self.model.train()                                           # 训练模式
        
        if is_bar:
            bar = tqdm(iterable=train_loader, desc="Training：", dynamic_ncols=True, colour="green", ncols=100, ascii=True)
        else:
            bar = train_loader
            
        total_loss = 0.0                                             # 总损失
        for inputs, targets in bar:
            inputs = inputs.to(self.device)                          # 输入移动到 GPU
            targets =  targets.to(self.device)                       # 目标移动到 GPU
            
            decoder_inputs = targets[:, :-1]                         # 输入的标签
            decoder_targets = targets[:, 1:]                         # 目标的标签
            pad_mask = (inputs == self.model.zh_embedding.padding_idx)    # 填充掩码
            tgt_mask = self.model.transformer.generate_square_subsequent_mask(sz=decoder_inputs.shape[1])  # 生成目标掩码
            decoder_outputs = self.model.forward(src=inputs, tgt=decoder_inputs, src_pad_mask=pad_mask, tgt_mask=tgt_mask)
            
            loss_value = self.loss_function(decoder_outputs.transpose(dim0=1, dim1=2), decoder_targets)  # 计算损失
            loss_value.backward()                                    # 反向传播
            self.optimizer.step()                                    # 优化器更新参数
            self.optimizer.zero_grad()                               # 清空梯度
            total_loss += loss_value.item()                          # 累计损失
            
        average_loss = total_loss / len(train_loader)                # 平均损失
        return average_loss

    
# 翻译预测器
class TranslatePredictor:
    def __init__(self, model: BaseModel, config: TranslateConfig,
                 zh_tokenizer: ChineseTokenizer, en_tokenizer: EnglishTokenizer):
        self.model = model                                           # 模型
        self.zh_tokenizer = zh_tokenizer                             # 中文分词器
        self.en_tokenizer = en_tokenizer                             # 英语分词器
        self.device = config.DEVICE                                  # 设备
        self.max_seq_length = config.MAX_SEQ_LENGTH                  # 最大序列长度
        
        self.model.load_model()                                      # 加载模型
        self.zh_tokenizer.load_vocab(vocab_path=config.ZH_VOCAB_PATH)     # 加载词表
        self.en_tokenizer.load_vocab(vocab_path=config.EN_VOCAB_PATH)     # 加载词表
        
    def predict(self, zh_text: str):
        zh_token_list = self.zh_tokenizer.encode(text=zh_text)       # 分词编码
        input_tensor = tensor(data=[zh_token_list], dtype=torch_long)  # 增加批量维度：(1, seq_len)
        input_tensor = input_tensor.to(device=self.device)           # 移动到设备
        
        self.model.eval()                                            # 设置模型为评估模式
        token_id_list = []                                           # 令牌 ID 列表
        with no_grad():                                              # 禁用梯度计算
            gru_output, context_vector = self.model.encoder.forward(input_tensor=input_tensor)   # 编码器，形状 (batch, hidden)
            hidden_first = context_vector.unsqueeze(0)               # 扩展维度：(1, batch, hidden)
            batch_size = input_tensor.shape[0]                       # 获取批量大小
            
            # 起始符使用 <sos>，不能使用 vocab_length（越界）
            decoder_inputs = full(size=(batch_size, 1), fill_value=self.en_tokenizer.start_id,
                                  dtype=torch_long, device=self.device)
            
            is_eos_tensor = full(size=(batch_size,), fill_value=False, dtype=torch_bool, device=self.device)
            
            for i in range(self.max_seq_length):
                decoder_output, decoder_hidden = self.model.decoder.forward(input_tensor=decoder_inputs,
                                                                            hidden_first=hidden_first,
                                                                            encoder_output=gru_output)
                # decoder_output 形状 (batch, 1, vocab_size)，在词表维度取最大
                next_token_ids = argmax(input=decoder_output, dim=-1).squeeze(dim=1)   # (batch,)
                token_id_list.append(next_token_ids)                 # 收集张量，最后统一拼接
                
                decoder_inputs = next_token_ids.unsqueeze(dim=1)      # (batch, 1)，作为下一步输入
                hidden_first = decoder_hidden
                
                is_eos_tensor = is_eos_tensor | (next_token_ids == self.en_tokenizer.end_id)
                if is_eos_tensor.all():
                    break
        
        id_rows = stack(tensors=token_id_list, dim=1).tolist()       # (batch, seq_len)
        
        en_text_list = []                                            # 解码结果列表
        for ids in id_rows:
            if self.en_tokenizer.end_id in ids:                      # 截断 <eos> 及其之后的令牌
                ids = ids[:ids.index(self.en_tokenizer.end_id)]
            
            ids = [id for id in ids if id != self.en_tokenizer.pad_id]
            english = self.en_tokenizer.decode(token_id_list=ids)
            en_text_list.append(english)
            
        return en_text_list[0] if len(en_text_list) == 1 else en_text_list
    
    def transform_predict(self, zh_text: str):
        zh_token_list = self.zh_tokenizer.encode(text=zh_text)       # 分词编码
        input_tensor = tensor(data=[zh_token_list], dtype=torch_long)  # 增加批量维度：(1, seq_len)
        input_tensor = input_tensor.to(device=self.device)           # 移动到设备
        
        self.model.eval()                                            # 设置模型为评估模式
        token_id_list = []                                           # 令牌 ID 列表
        with no_grad():                                              # 禁用梯度计算
            pad_mask = (input_tensor == self.model.zh_embedding.padding_idx)    # 填充掩码
            memory = self.model._encode(src=input_tensor, src_pad_mask=pad_mask)  # 编码器
            
            batch_size = input_tensor.shape[0]                       # 获取批量大小
            # 起始符使用 <sos>，不能使用 vocab_length（越界）
            decoder_inputs = full(size=(batch_size, 1), fill_value=self.en_tokenizer.start_id,
                                  dtype=torch_long, device=self.device)
            
            is_eos_tensor = full(size=(batch_size,), fill_value=False, dtype=torch_bool, device=self.device)
            
            for i in range(self.max_seq_length):
                tgt_mask = self.model.transformer.generate_square_subsequent_mask(sz=decoder_inputs.shape[1])  # 生成目标掩码
                decoder_output = self.model._decode(tgt=decoder_inputs, memory=memory,
                                                    tgt_mask=tgt_mask, memory_mask=pad_mask)  # Transformer 解码器
                
                next_token_ids = argmax(input=decoder_output[:, -1, :], dim=-1, keepdim=True)
                token_id_list.append(next_token_ids[-1].item())                 # 收集张量，最后统一拼接
                
                decoder_inputs = cat(tensors=[decoder_inputs, next_token_ids], dim=-1)      # (1, seq_len)，作为下一步输入
                
                is_eos_tensor = is_eos_tensor | (next_token_ids.squeeze(1) == self.en_tokenizer.end_id)
                if is_eos_tensor.all():
                    break
        
        if self.en_tokenizer.end_id in token_id_list:                      # 截断 <eos> 及其之后的令牌
            token_id_list = token_id_list[:token_id_list.index(self.en_tokenizer.end_id)]
        
        token_id_list = [id for id in token_id_list if id != self.en_tokenizer.pad_id]
        english = self.en_tokenizer.decode(token_id_list=token_id_list)
        
        return english
