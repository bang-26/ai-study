#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  product-classify  
    FileName       ：  product_classify 
    CreateTime     ：  2026-06-24 23:35:06 
    Author         ：  Administrator
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from typing import Any, Union, cast, Optional
from os.path import dirname, abspath, exists
from time import strftime
from datasets import load_dataset, load_from_disk, ClassLabel, DatasetDict
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from transformers import AutoTokenizer, DataCollatorWithPadding, BatchEncoding, AutoModelForSequenceClassification
from torch import device, cuda, no_grad, Tensor, argmax, float16, int32, autocast, GradScaler, save, load
from torch.optim import Adam
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


# 配置类
class Config:
    # ============================== 参数路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=f"{PYTHON_PATH}")                         # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    PROJECT_NAME = "product-classify"                                # 项目名称
    
    DATA_DIR = abspath(path=f"{PROJECT_DIR}/data")                   # 数据目录
    TRAIN_PATH = abspath(path=f"{DATA_DIR}/train.txt")               # 训练数据路径
    TEST_PATH = abspath(path=f"{DATA_DIR}/test.txt")                 # 测试数据路径
    VALID_PATH = abspath(path=f"{DATA_DIR}/valid.txt")               # 验证数据路径
    LABELS_PATH = abspath(path=f"{DATA_DIR}/labels.txt")             # 标签保存路径
    
    MODEL_DIR = abspath(path=f"{PROJECT_DIR}/models")                # 模型保存路径
    BERT_MODEL = "google-bert/bert-base-chinese"                     # BERT 模型名称
    # BERT_MODEL = f"{MODEL_DIR}/bert-base-chinese"                    # BERT 模型名称
    MODEL_PATH = abspath(path=f"{MODEL_DIR}/{PROJECT_NAME}")         # 模型保存路径
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")                    # 日志保存位置
    CHECK_POINT_DIR = abspath(path=f"{DATA_DIR}/check.pt")           # 检查点保存位置
    
    # ============================== 数据字段 ==============================
    TRAIN_FLAG = "train"                                             # 训练标志
    TEST_FLAG = "test"                                               # 测试标志
    VALID_FLAG = "valid"                                             # 验证标志
    RAW_SUFFIX = "csv"                                               # 原始数据后缀
    RAW_DELIMITER = "\t"                                             # 原始数据分隔符
    CONTENT_FIELD = "text_a"                                         # 文本字段
    LABEL_FIELD = "label"                                            # 标签字段
    
    TARGET_FIELD = "labels"                                          # 输出字段
    INPUT_ID_FIELD = "input_ids"                                     # 输入字段
    DATASET_FORMAT = "torch"                                         # 数据集格式
    MODEL_SUFFIX = "pt"                                              # 模型后缀
    
    REMOVE_COLUMNS = [LABEL_FIELD, CONTENT_FIELD]                    # 数据集字段
    METRICS_LOSS = "loss"                                            # 损失
    METRICS_ACCURACY = "accuracy"                                    # 准确率
    METRICS_F1 = "f1"                                                # F1
    METRICS_RECALL = "recall"                                        # 召回率
    METRICS_PRECISION = "precision"                                  # 精准率
    METRICS_F1_TYPE = "weighted"                                     # F1 评价指标类型
    METRICS_PRECISION_TYPE = "weighted"                              # 准确率评价指标类型
    METRICS_RECALL_TYPE = "weighted"                                 # 召回率评价指标类型
    STOP_METRIC = METRICS_F1                                         # 提前停止指标
    STOP_PATIENCE = 3                                                # 提前停止容忍度
    
    RETURN_TENSORS = "pt"                                            # 返回张量类型
    IS_PADDING = True                                                # 是否填充
    IS_TRUNCATION = True                                             # 是否截断
    IS_BATCHED = False                                               # 是否批量处理
    
    CHECK_MODEL_KEY = "model_staste_dict"                            # 检查点模型键
    CHECK_OPTIMIZER_KEY = "optimizer_staste_dict"                    # 检查点优化器键
    CHECK_SCALE_FACTOR_KEY = "scale_factor_dict"                     # 检查点缩放因子键
    CHECK_STEP_KEY = "step"                                          # 检查点迭代步数键
    CHECK_BEST_SCORE_KEY = "best_score"                              # 检查点最佳得分键
    CHECK_STOP_COUNTER_KEY = "stop_counter"                          # 检查点停止计数键
    CHECK_SCHEDULER_KEY = "scheduler_staste_dict"                    # 检查点学习率键
    CHECK_EPOCH_KEY = "epoch"                                        # 检查点迭代轮数键
    
    # ============================== 训练超参数 ==============================
    DEVICE = device("cuda" if cuda.is_available() else "cpu")        # 设备，默认使用 GPU
    TRAIN_SELECT_NUMBER = 0                                          # 训练数据选择数量
    VALID_SELECT_NUMBER = 0                                          # 验证数据选择数量
    TEST_SELECT_NUMBER = 0                                           # 测试数据选择数量
    
    TORCH_FLOAT_TYPE  = float16                                      # 浮点类型
    TORCH_INT_TYPE = int32                                           # 整数类型
    IS_AUTO_CAST = True                                              # 是否自动转换类型
    
    RANDOM_SEED = 42                                                 # 随机种子
    IS_SHUFFLE = True                                                # 是否打乱数据
    SEQ_LEN = 128                                                    # 最大序列长度
    BATCH_SIZE = 128                                                 # 批处理大小
    LEARNING_RATE = 1e-5                                             # 学习率
    SAVE_STEP = 100                                                  # 每批次保存
    EPOCHS = 10                                                      # 训练轮数
    MAX_LENGTH = 32                                                  # 生成最大长度
    NUM_BEAMS = 5                                                    # 束搜索
    
    
# 数据预处理
class ProductDataProcess:
    def __init__(self, config: Config) -> None:
        self.train_path = config.TRAIN_PATH                          # 训练数据路径
        self.test_path = config.TEST_PATH                            # 测试数据路径
        self.valid_path = config.VALID_PATH                          # 验证数据路径
        
        self.data_path = config.DATA_DIR                             # 数据集保存路径
        self.label_path = config.LABELS_PATH                         # 标签保存路径
        self.check_point_path = config.CHECK_POINT_DIR               # 检查点保存路径
        self.check_point_path = config.CHECK_POINT_DIR               # 检查点保存路径
        self.saved_model_path = config.MODEL_PATH              # 模型保存路径
        self.log_dir = config.LOG_DIR                                # 日志保存位置
        
        self.train_flag = config.TRAIN_FLAG                          # 训练标志
        self.test_flag = config.TEST_FLAG                            # 测试标志
        self.valid_flag = config.VALID_FLAG                          # 验证标志
        self.raw_suffix = config.RAW_SUFFIX                          # 原始数据后缀
        self.raw_delimiter = config.RAW_DELIMITER                    # 原始数据分隔符
        self.content_field = config.CONTENT_FIELD                    # 文本字段
        self.label_field = config.LABEL_FIELD                        # 标签字段
        self.is_batch = config.IS_BATCHED                            # 是否批量处理
        self.remove_columns = config.REMOVE_COLUMNS                  # 移除字段
        self.target_field = config.TARGET_FIELD                      # 输出字段
        self.is_truncation = config.IS_TRUNCATION                    # 是否截断
        self.is_padding = config.IS_PADDING                          # 是否填充
        self.return_tensors = config.RETURN_TENSORS                  # 返回张量类型
        self.batch_size = config.BATCH_SIZE                          # 批处理大小
        self.is_shuffle = config.IS_SHUFFLE                          # 是否打乱数据、
        self.random_seed = config.RANDOM_SEED                        # 随机种子
        self.dataset_format = config.DATASET_FORMAT                  # 数据集格式
        
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=config.BERT_MODEL)
        self.labels = None
        
    # 获取数据集
    def process_data(self, ratio: float = 1.0) -> None:
        # 1. 数据集名称和对应的路径
        file_dict = \
            {
                self.train_flag: self.train_path,
                self.test_flag : self.test_path,
                self.valid_flag: self.valid_path,
            }
        
        # 2. 从文件中加载数据集
        dataset_dict = load_dataset(path=self.raw_suffix, data_files=file_dict, delimiter=self.raw_delimiter)
        
        # 3. 获取所有分类的名称，并使用 set 去重
        labels = dataset_dict[self.train_flag][self.label_field]
        
        # 4. 保存标签
        self.labels = Utils.save_labels(labels=labels, label_path=self.label_path)
        
        # 5. 随机采样指定比例的数据，ratio 为 1.0 时保留全量
        if ratio < 1.0:
            split_data_dict = {}
            for split, dataset in dataset_dict.items():
                indices = range(max(1, int(len(dataset) * ratio)))   # 生成随机索引
                filter_dataset = dataset.shuffle(seed=self.random_seed).select(indices=indices)    # 随机采样
                split_data_dict[split] = filter_dataset              # 添加到字典中
            
            dataset_dict = DatasetDict(split_data_dict)              # 创建 DatasetDict
            print(f"采样比例 {ratio}：{ {split: len(dataset) for split, dataset in dataset_dict.items()} }")
            
        # 6. 使用 map 将字符串标签转换为对应的整数 ID
        map_dict = dataset_dict.map(function=self.__map_label, )
        
        # 7. 列转换编码
        feature = ClassLabel(names=self.labels)
        transform_dict = map_dict.cast_column(column=self.label_field, feature=feature)
        
        # 8. 处理标题文本，得到模型输入
        input_dict = transform_dict.map(function=self.__batch_encode, batched=self.is_batch,
                                        remove_columns=self.remove_columns)
        
        # 9. 保存数据集
        input_dict.save_to_disk(dataset_dict_path=self.data_path)
        print(f"数据集保存到 {self.data_path} 成功 ... ")
    
    # 获取数据加载器
    def get_dataloader(self, dataset_path: str, select: int = 0) -> DataLoader:
        # 1. 加载数据集
        dataset = load_from_disk(dataset_path=dataset_path)
        
        # 2. 如果传入的是 DatasetDict 根目录，自动选择训练集
        if isinstance(dataset, DatasetDict):
            dataset = dataset[self.train_flag]
        
        # 3. 选取数据
        if select > 0:
            dataset = dataset.select(indices=range(select))
        
        # 4. 设置格式为 tensor
        dataset.set_format(type=self.dataset_format)
        
        # 5. 创建收集器
        collate_fn = DataCollatorWithPadding(tokenizer=self.tokenizer, padding=self.is_padding,
                                             return_tensors=self.return_tensors)
        # 6. 创建 DataLoader
        dataloader = DataLoader(dataset=cast(Dataset, dataset), batch_size=self.batch_size,
                                shuffle=self.is_shuffle, collate_fn=collate_fn)
        return dataloader
        
    # 使用 map 将字符串标签转换为对应的整数 ID
    def __map_label(self, example: dict[str, Union[str, int]]) -> dict[str, Union[str, int]]:
        feature = ClassLabel(names=self.labels)
        label_index = feature.str2int(values=cast(str, example[self.label_field]))
        example[self.label_field] = label_index
        return example
        
    # 处理标题文本，得到模型输入
    def __batch_encode(self, examples: dict[str, Any]) -> BatchEncoding:
        encoded = self.tokenizer(text=examples[self.content_field], truncation=self.is_truncation)
        encoded[self.target_field] = examples[self.label_field]
        return encoded
        
    
# 模型操作
class ProductModel:
    def __init__(self, config: Config) -> None:
        self.model_path = config.MODEL_PATH                          # 模型保存路径
        self.label_path = config.LABELS_PATH                         # 标签路径
        self.device = config.DEVICE                                  # 设备
        
        self.model: Optional[AutoModelForSequenceClassification] = None   # 模型
        
    # 加载模型
    def load_model(self) -> None:
        labels = Utils.load_labels(label_path=self.label_path)       # 加载标签
        label2id, id2label = Utils.get_label_map(labels=labels)      # 获取标签映射关系
        
        # 创建模型
        self.model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=self.model_path,
                                                                         num_labels=len(labels), id2label=id2label,
                                                                        label2id=label2id)
        self.model.to(device=self.device)                            # 将模型移动到 GPU
        
    #  保存模型
    def save_model(self) -> None:
        self.model.save_pretrained(save_directory=self.model_path)   # 保存模型
        tqdm.write(f"[ Time：{strftime('%Y-%m-%d %H:%M:%S')}：模型保存成功 ... ")
    
    
# 训练操作
class ProductTrainer:
    def __init__(self, config: Config, product_model: ProductModel) -> None:
        self.product_model = product_model                           # 模型操作
        
        self.bert_model = config.BERT_MODEL                          # BERT 模型路径
        self.model_path = config.MODEL_PATH                          # 模型保存路径
        self.device = config.DEVICE                                  # 设备
        self.epochs = config.EPOCHS                                  # 训练轮数
        
        self.train_path = f"{config.DATA_DIR}/{Config.TRAIN_FLAG}"   # 训练数据路径
        self.test_path = f"{config.DATA_DIR}/{Config.TEST_FLAG}"     # 测试数据路径
        self.valid_path = f"{config.DATA_DIR}/{Config.VALID_FLAG}"   # 验证数据路径
        self.label_path = config.LABELS_PATH                         # 标签路径
        self.check_point_path = config.CHECK_POINT_DIR               # 检查点保存路径
        self.log_dir = config.LOG_DIR                                # 日志保存位置
        self.learning_rate = config.LEARNING_RATE                    # 学习率
        
        self.stop_metric = config.STOP_METRIC                        # 停止指标
        self.stop_patience = config.STOP_PATIENCE                    # 停止容忍度
        self.float_type = config.TORCH_FLOAT_TYPE                    # 浮点类型
        self.is_auto_cast = config.IS_AUTO_CAST                      # 是否使用自动混合精度
        self.save_step = config.SAVE_STEP                            # 保存步数
        self.target_field = config.TARGET_FIELD                      # 目标字段
        self.metric_loss = config.METRICS_LOSS                       # 损失指标
        self.check_model_key = config.CHECK_MODEL_KEY                # 检查点保存键
        self.check_optimizer_key = config.CHECK_OPTIMIZER_KEY        # 优化器保存键
        self.check_scale_factor_key = config.CHECK_SCALE_FACTOR_KEY  # 缩放因子保存键
        self.check_step_key = config.CHECK_STEP_KEY                  # 步数保存键
        self.check_best_score_key = config.CHECK_BEST_SCORE_KEY      # 最佳分数保存键
        self.check_stop_counter_key = config.CHECK_STOP_COUNTER_KEY  # 停止计数器保存键
        
        self.min_loss = float("inf")                                 # 最小损失
        self.step = 1                                                # 全局迭代次数
        self.best_score = -float("inf")                              # 全局最佳评估得分
        self.stop_counter = 0                                        # 停止计数器
        
        self.writer: Optional[SummaryWriter] = None                  # TensorBoard 日志器
        self.model: Optional[AutoModelForSequenceClassification] = None  # 模型
        self.optimizer: Optional[Adam] = None                        # 优化器
        self.scaler: Optional[GradScaler] = None                     # 自动混合精度缩放器
        self.tokenizer: Optional[AutoTokenizer] = None               # 分词器
        
    # 训练模型
    def train(self, train_loader: DataLoader, valid_loader: DataLoader) -> None:
        self.__load_param()                                          # 加载参数
        self.__load_checkpoint()                                     # 加载检查点
        self.model.train()                                           # 训练模式
        
        # 2. 双重 for 循环
        for epoch in range(self.epochs):
            # 内部 for 循环，遍历每个 epoch 中的所有批次
            bar = tqdm(iterable=train_loader, desc=f"[ epoch：{epoch + 1} ]", colour="green", ncols=80, leave=False)
            for batch in bar:
                this_loss = self.__train_one_step(batch=batch)       # 训练一个批次
                
                # 如果达到步数，就记录训练损失
                if self.step % self.save_step == 0:
                    # 打印训练损失
                    tqdm.write(f"[ Epoch：{epoch + 1} ]-[ Step：{self.step} ]-[ Loss：{this_loss} ]")
                    self.writer.add_scalar(tag="train_loss", scalar_value=this_loss, global_step=self.step)
                    
                    valid_metrics = self.__evaluate(valid_loader=valid_loader) # 得到验证指标
                    metrics_str = "-|-".join([f"{k}：{v:.4f}" for k, v in valid_metrics.items()])
                    tqdm.write(f"Evaluate：{metrics_str}")           # 输出验证指标
                    
                    self.__save_checkpoint()                         # 保存检查点
                    self.__is_stop(metrics=valid_metrics)            # 判断是否需要停止
                self.step += 1                                       # 步数加一
            
    # 加载参数
    def __load_param(self) -> None:
        # # 创建 TensorBoard 日志
        if not self.writer:
            log_dir = f"{self.log_dir}/{strftime('%Y-%m-%d-%H-%M-%S')}"
            self.writer = SummaryWriter(log_dir=log_dir)
        
        # 创建模型
        if not self.model:
            labels = Utils.load_labels(label_path=self.label_path)   # 加载标签
            label2id, id2label = Utils.get_label_map(labels=labels)  # 获取标签映射关系
            
            self.model = AutoModelForSequenceClassification.from_pretrained(
                pretrained_model_name_or_path=self.bert_model,
                num_labels=len(labels), id2label=id2label, label2id=label2id)
            self.model.to(device=self.device)
        
        # 创建优化器
        if not self.optimizer:
            self.optimizer = Adam(params=self.model.parameters(), lr=self.learning_rate)
        
        # 创建自动混合精度缩放器
        if not self.scaler:
            self.scaler = GradScaler()
        
        # 创建分词器
        if not self.tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(self.bert_model)
        
    # 训练一轮
    def __train_one_step(self, batch: dict[str, Tensor]) -> float:
        inputs = { k: v.to(self.device) for k, v in batch.items() }  # 移动数据到 GPU
        
        # 前向传播，使用自动混合精度训练
        with autocast(device_type=self.device.type, dtype=self.float_type, enabled=self.is_auto_cast):
            outputs = self.model.forward(**inputs)                   # 获取模型输出
            loss = outputs.loss                                      # 获取损失
            
        # 反向传播，使用自动混合精度训练
        self.scaler.scale(loss).backward()                           # 缩放损失
        self.scaler.step(self.optimizer)                             # 更新参数
        self.scaler.update()                                         # 更新缩放因子
        self.optimizer.zero_grad()                                   # 清空梯度
        return loss.item()                                           # 返回损失

    # 评估模型
    def __evaluate(self, valid_loader: DataLoader) -> dict[str, float]:
        self.model.eval()                                            # 验证模式
        total_loss = 0.0                                             # 总损失
        all_labels = []                                              # 所有标签
        all_predicts = []                                            # 所有预测
        
        bar = tqdm(iterable=valid_loader, desc="[ evaluate} ]", colour="red", ncols=80, leave=False)
        for batch in bar:
            inputs = { k: v.to(self.device) for k, v in batch.items() }
            outputs = self.model.forward(**inputs)                   # 获取模型输出
            loss = outputs.loss                                      # 获取损失
            total_loss += loss.item()                                # 累加损失
            logits = outputs.logits                                  # 预测分类结果
            predicts = argmax(logits, dim=-1)                        # 获取预测结果
            all_predicts.extend(predicts.tolist())                   # 保存预测结果
            labels = inputs[self.target_field]                       # 获取标签
            all_labels.extend(labels.tolist())                       # 保存标签
        
        # 遍历完验证集，计算平均损失和其它评估指标
        average_loss = total_loss / len(valid_loader)                # 平均损失
        metrics = Utils.compute_metrics(predicts=all_predicts, labels=all_labels)
        metrics.update({ self.metric_loss: average_loss })
        return metrics
        
    # 判断是否需要早停
    def __is_stop(self, metrics: dict) -> bool:
        metric = metrics.get(self.stop_metric, self.metric_loss)     # 获取当前指标
        score = -metric if metric == self.metric_loss else metric    # 转换评分
        
        is_stop = False                                              # 是否需要早停
        # 判断是否需要早停
        if score > self.best_score:
            self.best_score = score                                  # 更新最佳分数
            self.stop_counter = 0                                    # 重置计数器
            
            self.product_model.model = self.model                    # 保存模型
            self.product_model.save_model()
        else:
            self.stop_counter += 1                                   # 计数器加一
            if self.stop_counter >= self.stop_patience:              # 判断是否需要早停
                is_stop = True
        return is_stop
    
    # 加载检查点
    def __load_checkpoint(self):
        # 判断是否有检查点
        if exists(path=self.check_point_path):
            checkpoint = load(f=self.check_point_path)
            self.model.load_state_dict(checkpoint[self.check_model_key])
            self.optimizer.load_state_dict(checkpoint[self.check_optimizer_key])
            self.scaler.load_state_dict(checkpoint[self.check_scale_factor_key])
            self.step = checkpoint[self.check_step_key]
            self.best_score = checkpoint[self.check_best_score_key]
            self.stop_counter = checkpoint[self.check_stop_counter_key]
            tqdm.write(f"{ strftime('%Y-%m-%d %H:%M:%S') }：Load Checkpoint from {self.check_point_path}")
        else:
            tqdm.write(f"{ strftime('%Y-%m-%d %H:%M:%S') }：No Checkpoint")
            
    # 保存检查点
    def __save_checkpoint(self):
        checkpoint = \
            {
                self.check_model_key       : self.model.state_dict(),
                self.check_optimizer_key   : self.optimizer.state_dict(),
                self.check_scale_factor_key: self.scaler.state_dict(),
                self.check_step_key        : self.step,
                self.check_best_score_key  : self.best_score,
                self.check_stop_counter_key: self.stop_counter,
            }
        
        save(obj=checkpoint, f=self.check_point_path)                # 保存检查点
        tqdm.write(f"{ strftime('%Y-%m-%d %H:%M:%S') }：Save Checkpoint in {self.check_point_path}")
        
        
class ProductPredictor:
    def __init__(self, config: Config) -> None:
        self.bert_model = config.BERT_MODEL                          # BERT 模型路径
        self.model_path = config.MODEL_PATH                          # 模型保存路径
        self.label_path = config.LABELS_PATH                         # 标签保存路径
        self.device = config.DEVICE                                  # 设备
        
        self.is_padding = config.IS_PADDING                          # 是否填充
        self.is_truncation = config.IS_TRUNCATION                    # 是否截断
        self.return_tensors = config.RETURN_TENSORS                  # 是否返回张量
        
        self.model: Optional[AutoModelForSequenceClassification] = None  # 模型
        self.tokenizer: Optional[AutoTokenizer] = None               # 分词器
        self.label2id: Optional[dict] = None                         # 标签映射
        self.id2label: Optional[dict] = None                         # 标签映射
        
    # 预测模型
    def predict(self, texts: Union[str, list[str]]) -> Union[str, list[str]]:
        self.__load_model()                                          # 加载模型
        if isinstance(texts, str):                                   # 如果是字符串，则转为列表
            texts = [texts]
        
        # 创建输入
        encoded = self.tokenizer(text=texts, padding=self.is_padding, truncation=self.is_truncation,
                                 return_tensors=self.return_tensors)
        
        inputs = {k: v.to(self.device) for k, v in encoded.items()}  # 移动数据到 GPU
        with no_grad():
            outputs = self.model.forward(**inputs)                   # 前向传播
        
        predicts = argmax(outputs.logits, dim=-1).tolist()           # 获取预测结果
        id2label = self.model.config.id2label                        # 获取标签映射
        labels = [id2label[predict] for predict in predicts]         # 获取标签
        
        if isinstance(texts, str):                                   # 如果是字符串，则返回标签
            labels = labels[0]
            
        return labels
        
    # 加载模型
    def __load_model(self):
        if not self.model:
            self.model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=self.model_path)
            self.model.to(device=self.device)
            self.model.eval()
        
        if not self.tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(self.bert_model)
        
        if not self.label2id or not self.id2label:
            labels = Utils.load_labels(label_path=self.label_path)   # 加载标签
            self.label2id, self.id2label = Utils.get_label_map(labels=labels)  # 获取标签映射关系
            
            
# 工具类
class Utils:
    # 加载标签
    @staticmethod
    def load_labels(label_path: str) -> list:
        with open(file=label_path, mode="r", encoding="utf-8") as fr:
            labels = fr.read().splitlines()
        return labels
    
    # 保存标签
    @staticmethod
    def save_labels(labels: list[str], label_path: str) -> list[str]:
        remove_duplicates = set(labels)                              # 去重
        sorted_labels = sorted(remove_duplicates)                    # 排序
        contents = "\n".join(sorted_labels)                          # 拼接成字符串
        
        # 保存标签：保存类别 id → label 映射关系
        with open(file=label_path, mode="w", encoding="utf-8") as fw:
            fw.write(contents)
        
        return sorted_labels
        
    # 转换 ID 和 标签映射字典
    @staticmethod
    def get_label_map(labels: list[str]) -> tuple[dict, dict]:
        label2id = {label: id for id, label in enumerate(labels)}
        id2label = {id: label for id, label in enumerate(labels)}
        return label2id, id2label
    
    # 评估函数：根据实际预测结果和真实标签，返回评估指标
    @staticmethod
    def compute_metrics(predicts: list, labels: list) -> dict:
        accuracy = accuracy_score(y_true=labels, y_pred=predicts)
        f1 = f1_score(y_true=labels, y_pred=predicts, average=Config.METRICS_F1_TYPE)
        recall = recall_score(y_true=labels, y_pred=predicts, average=Config.METRICS_RECALL_TYPE)
        precision = precision_score(y_true=labels, y_pred=predicts, average=Config.METRICS_PRECISION_TYPE)
        metrics = \
            {
                Config.METRICS_ACCURACY : accuracy,
                Config.METRICS_F1       : f1,
                Config.METRICS_RECALL   : recall,
                Config.METRICS_PRECISION: precision
            }
        return metrics
