#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  product-classify  
    FileName       ：  product_classify 
    CreateTime     ：  2026-06-24 23:35:06 
    Author         ：  issac  
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from typing import Union
from os.path import dirname, abspath, exists
from time import strftime
from datasets import load_dataset, load_from_disk, ClassLabel
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from transformers import AutoTokenizer, DataCollatorWithPadding, BatchEncoding, AutoModelForSequenceClassification
from torch import device, cuda, no_grad, Tensor, argmax, float16, int32, autocast, GradScaler, save, load
from torch.optim import Adam
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
from tqdm import tqdm


# 数据预处理
class ProductDataProcess:
    def __init__(self, data_path: str = None, label_path: str = None) -> None:
        self.data_path = data_path
        self.label_path = label_path
        self.tokenizer = AutoTokenizer.from_pretrained(Config.BERT_MODEL)
        self.labels = None
        
    # 获取数据集
    def process_data(self) -> None:
        # 1. 数据集名称和对应的路径
        file_dict = \
            {
                Config.TRAIN_FLAG: Config.TRAIN_PATH,
                Config.TEST_FLAG : Config.TEST_PATH,
                Config.VALID_FLAG: Config.VALID_PATH,
            }
        
        # 2. 从文件中加载数据集
        dataset_dict = load_dataset(path=Config.RAW_SUFFIX, data_files=file_dict, delimiter=Config.RAW_DELIMITER)
        
        # 3. 获取所有分类的名称，并使用 set 去重
        labels = dataset_dict[Config.TRAIN_FLAG][Config.LABEL_FIELD]
        
        # 4. 保存标签
        self.labels = Utils.save_labels(labels=labels, label_path=self.label_path)
        
        # 5. 使用 map 将字符串标签转换为对应的整数 ID
        map_dict = dataset_dict.map(function=self.__map_label)
        
        # 6. 列转换编码
        feature = ClassLabel(names=self.labels)
        transform_dict = map_dict.cast_column(column=Config.LABEL_FIELD, feature=feature)
        
        # 7. 处理标题文本，得到模型输入
        input_dict = transform_dict.map(function=self.__batch_encode, batched=Config.IS_BATCHED,
                                        remove_columns=Config.REMOVE_COLUMNS)
        
        # 8. 保存数据集
        input_dict.save_to_disk(dataset_dict_path=self.data_path)
        print(f"input_dict = {input_dict[Config.TRAIN_FLAG][0: 3]}")
     
    # 获取数据加载器
    def get_dataloader(self, dataset_path: str, collate_fn: callable = None, select: int = 0) -> DataLoader:
        # 1. 加载数据集
        dataset = load_from_disk(dataset_path=dataset_path)
        
        # 2. 选取数据
        if select > 0:
            dataset = dataset.select(indices=range(select))
        
        # 3. 设置格式为 tensor
        dataset.set_format(type=Config.DATASET_FORMAT)
        
        # 4. 创建收集器
        if collate_fn is None:
            collate_fn = DataCollatorWithPadding(tokenizer=self.tokenizer, padding=Config.IS_PADDING,
                                                 return_tensors=Config.RETURN_TENSORS)
        # 5. 创建 DataLoader
        dataloader = DataLoader(dataset=dataset, batch_size=Config.BATCH_SIZE,
                                shuffle=Config.IS_SHUFFLE, collate_fn=collate_fn)
        return dataloader
    
    # 使用 map 将字符串标签转换为对应的整数 ID
    def __map_label(self, example: dict[str, Union[str, int]]) -> dict[str, int]:
        feature = ClassLabel(names=self.labels)
        label_index = feature.str2int(example[Config.LABEL_FIELD])
        example[Config.LABEL_FIELD] = label_index
        return example
    
    # 处理标题文本，得到模型输入
    def __batch_encode(self, examples: dict[str, str]) -> BatchEncoding:
        encoded = self.tokenizer(examples[Config.CONTENT_FIELD], truncation=Config.IS_TRUNCATION)
        encoded[Config.TARGET_FIELD] = examples[Config.LABEL_FIELD]
        return encoded
        
    
# 模型的训练
class ProductModel:
    def __init__(self, data_path: str = None, model_path: str = None, saved_model_path: str = None,
                 label_path: str = None, check_point_path: str = None) -> None:
        self.train_path = f"{data_path}/{Config.TRAIN_FLAG}"
        self.test_path = f"{data_path}/{Config.TEST_FLAG}"
        self.valid_path = f"{data_path}/{Config.VALID_FLAG}"
        self.model_path = model_path
        self.saved_model_path = saved_model_path
        self.label_path = label_path
        self.check_point_path = check_point_path
        
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.load_model()
        self.optimizer = Adam(params=self.model.parameters(), lr=Config.LEARNING_RATE)
        self.scaler = GradScaler()                                   # 创建自动混合精度缩放器
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)   # 创建分词器
        
        log_dir = f"{ Config.LOG_DIR }/{ strftime('%Y-%m-%d-%H-%M-%S') }"
        self.writer = SummaryWriter(log_dir=log_dir)                 # 创建 TensorBoard 日志
        
        self.stop_metric = Config.STOP_METRIC                        # 停止指标
        self.stop_patience = Config.STOP_PATIENCE                    # 停止容忍度
        
        self.min_loss = float("inf")                                 # 最小损失
        self.step = 1                                                # 全局迭代次数
        self.best_score = -float("inf")                              # 全局最佳评估得分
        self.stop_counter = 0                                        # 停止计数器
        
    # 加载模型
    def load_model(self, model_path: str = None) -> None:
        labels = Utils.load_labels(label_path=self.label_path)       # 加载标签
        label2id, id2label = Utils.get_label_map(labels=labels)      # 获取标签映射关系
        
        if model_path is None:
            model_path = self.model_path
        
        # 创建模型
        self.model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=model_path,
                                                                        num_labels=len(labels), id2label=id2label,
                                                                        label2id=label2id)
        self.model.to(self.device)                                   # 将模型移动到 GPU
    
    #  保存模型
    def save_model(self) -> None:
        self.model.save_pretrained(save_directory=self.saved_model_path)  # 保存模型
        tqdm.write(f"[ Time：{strftime('%Y-%m-%d %H:%M:%S')}：模型保存成功 ... ")
        
    # 训练模型
    def train(self) -> None:
        self.__load_checkpoint()                                     # 加载检查点
        self.model.train()                                           # 训练模式
        
        # 1. 创建训练集数据加载器
        dataloader = self.__get_dataloader(dataset_path=self.train_path, select=Config.TRAIN_SELECT_NUMBER)
        
        # 2. 双重 for 循环
        for epoch in range(Config.EPOCHS):
            
            # 内部 for 循环，遍历每个 epoch 中的所有批次
            bar = tqdm(iterable=dataloader, desc=f"[ Epoch：{epoch + 1} ]")
            for batch in bar:
                this_loss = self.__train_one_step(batch=batch)       # 训练一个批次
                
                # 如果达到步数，就记录训练损失
                if self.step % Config.SAVE_STEP == 0:
                    # 打印训练损失
                    tqdm.write(f"[ Epoch：{epoch + 1} ]-[ Step：{self.step} ]-[ Loss：{this_loss} ]")
                    self.writer.add_scalar(tag="train_loss", scalar_value=this_loss, global_step=self.step)
                    
                    valid_loader = self.__get_dataloader(dataset_path=self.valid_path, select=Config.VALID_SELECT_NUMBER)
                    valid_metrics = self.evaluate(dataloader=valid_loader)     # 得到验证指标
                    metrics_str = "-|-".join([f"{k}：{v:.4f}" for k, v in valid_metrics.items()])
                    tqdm.write(f"Evaluate：{metrics_str}")            # 输出验证指标
                    
                    self.__save_checkpoint()                         # 保存检查点
                    self.__is_stop(metrics=valid_metrics)            # 判断是否需要停止
                self.step += 1                                       # 步数加一
    
    # 评估模型
    def evaluate(self, dataloader: DataLoader = None) -> dict:
        self.model.eval()                                            # 验证模式
        total_loss = 0.0                                             # 总损失
        all_labels = []                                              # 所有标签
        all_predicts = []                                            # 所有预测
        bar = tqdm(iterable=dataloader, desc="[ Evaluate ]")         # 创建进度条
        for batch in bar:
            inputs = { k: v.to(self.device) for k, v in batch.items() }
            outputs = self.model(**inputs)                           # 获取模型输出
            loss = outputs.loss                                      # 获取损失
            total_loss += loss.item()                                # 累加损失
            logits = outputs.logits                                  # 预测分类结果
            predicts = argmax(logits, dim=-1)                        # 获取预测结果
            all_predicts.extend(predicts.tolist())                   # 保存预测结果
            labels = inputs[Config.TARGET_FIELD]                     # 获取标签
            all_labels.extend(labels.tolist())                       # 保存标签
        
        # 遍历完验证集，计算平均损失和其它评估指标
        average_loss = total_loss / len(dataloader)                  # 平均损失
        metrics = Utils.compute_metrics(predicts=all_predicts, labels=all_labels)
        metrics.update({ Config.METRICS_LOSS: average_loss })
        return metrics
    
    # 预测模型
    def predict(self, texts: Union[str, list[str]]) -> Union[str, list[str]]:
        self.load_model(model_path=self.saved_model_path)            # 加载模型
        self.model.eval()                                            # 验证模式
        if self.__is_input_str(input=texts):                         # 如果是字符串，则转为列表
            texts = [texts]
        
        # 创建输入
        encoded = self.tokenizer(text=texts, padding=Config.IS_PADDING,
                                truncation=Config.IS_TRUNCATION, return_tensors=Config.RETURN_TENSORS)
        
        inputs = { k: v.to(self.device) for k, v in encoded.items() }     # 移动数据到 GPU
        with no_grad():
            outputs = self.model(**inputs)                           # 前向传播
            
        predicts = argmax(outputs.logits, dim=-1).tolist()           # 获取预测结果
        id2label = self.model.config.id2label                        # 获取标签映射
        labels = [id2label[predict] for predict in predicts]         # 获取标签
        
        if self.__is_input_str(input=texts):                         # 如果是字符串，则返回标签
            labels = labels[0]
        return labels
        
    # 测试模型
    def test(self):
        self.load_model(model_path=self.saved_model_path)            # 加载模型
        # 创建测试集数据加载器
        test_loader = self.__get_dataloader(dataset_path=self.test_path, select=Config.TEST_SELECT_NUMBER)
        metrics = self.evaluate(dataloader=test_loader)              # 评估模型
        return metrics
    
    # 获取数据加载器
    def __get_dataloader(self, dataset_path: str, select: int = 0) -> DataLoader:
        process = ProductDataProcess()
        dataloader = process.get_dataloader(dataset_path=dataset_path, select=select)
        return dataloader
        
    # 训练一轮
    def __train_one_step(self, batch: dict[str, Tensor]) -> float:
        inputs = { k: v.to(self.device) for k, v in batch.items() }  # 移动数据到 GPU
        
        # 前向传播，使用自动混合精度训练
        with autocast(device_type=self.device.type, dtype=Config.TORCH_FLOAT_TYPE, enabled=Config.IS_AUTO_CAST):
            outputs = self.model(**inputs)                           # 获取模型输出
            loss = outputs.loss                                      # 获取损失
        
        # 反向传播，使用自动混合精度训练
        self.scaler.scale(loss).backward()                           # 缩放损失
        self.scaler.step(self.optimizer)                             # 更新参数
        self.scaler.update()                                         # 更新缩放因子
        self.optimizer.zero_grad()                                   # 清空梯度
        return loss.item()                                           # 返回损失
    
    # 判断是否需要早停
    def __is_stop(self, metrics: dict) -> bool:
        metric = metrics.get(self.stop_metric, Config.METRICS_LOSS)  # 获取当前指标
        score = -metric if metric == Config.METRICS_LOSS else metric # 转换评分
        
        is_stop = False                                              # 是否需要早停
        # 判断是否需要早停
        if score > self.best_score:
            self.best_score = score                                  # 更新最佳分数
            self.stop_counter = 0                                    # 重置计数器
            self.save_model()                                        # 保存模型
        else:
            self.stop_counter += 1                                   # 计数器加一
            if self.stop_counter >= self.stop_patience:              # 判断是否需要早停
                is_stop = True
        return is_stop
    
    # 加载模型
    def __load_checkpoint(self):
        # 判断是否有检查点
        if exists(path=self.check_point_path):
            checkpoint = load(f=self.check_point_path)
            self.model.load_state_dict(checkpoint[Config.CHECK_MODEL_KEY])
            self.optimizer.load_state_dict(checkpoint[Config.CHECK_OPTIMIZER_KEY])
            self.scaler.load_state_dict(checkpoint[Config.CHECK_SCALE_FACTOR_KEY])
            self.step = checkpoint[Config.CHECK_STEP_KEY]
            self.best_score = checkpoint[Config.CHECK_BEST_SCORE_KEY]
            self.stop_counter = checkpoint[Config.CHECK_STOP_COUNTER_KEY]
            tqdm.write(f"{ strftime('%Y-%m-%d %H:%M:%S') }：Load Checkpoint from {self.check_point_path}")
        else:
            tqdm.write(f"{ strftime('%Y-%m-%d %H:%M:%S') }：No Checkpoint")
            
    # 保存检查点
    def __save_checkpoint(self):
        checkpoint = \
            {
                Config.CHECK_MODEL_KEY       : self.model.state_dict(),
                Config.CHECK_OPTIMIZER_KEY   : self.optimizer.state_dict(),
                Config.CHECK_SCALE_FACTOR_KEY: self.scaler.state_dict(),
                Config.CHECK_STEP_KEY        : self.step,
                Config.CHECK_BEST_SCORE_KEY  : self.best_score,
                Config.CHECK_STOP_COUNTER_KEY: self.stop_counter,
            }
        save(obj=checkpoint, f=self.check_point_path)                # 保存检查点
        tqdm.write(f"{ strftime('%Y-%m-%d %H:%M:%S') }：Save Checkpoint in {self.check_point_path}")
    
    def __is_input_str(self, input: Union[str, list[str], Tensor, None]):
        return isinstance(input, str)


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
        
        
# 配置类
class Config:
    # ============================== 参数路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                              # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    
    TRAIN_PATH = abspath(path=f"{PROJECT_DIR}/data/train.txt")       # 训练数据路径
    TEST_PATH = abspath(path=f"{PROJECT_DIR}/data/test.txt")         # 测试数据路径
    VALID_PATH = abspath(path=f"{PROJECT_DIR}/data/valid.txt")       # 验证数据路径
    DATASET_PATH = abspath(path=f"{PROJECT_DIR}/data/product")       # 处理后的数据路径
    LABELS_PATH = abspath(path=f"{PROJECT_DIR}/data/labels.txt")     # 标签保存路径
    
    BERT_MODEL = "google-bert/bert-base-chinese"                     # BERT 模型名称
    SAVED_MODEL_PATH = abspath(path=f"{PROJECT_DIR}/models/couplet") # 模型保存路径
    LOG_DIR = abspath(path=f"{PROJECT_DIR}/logs")                    # 日志保存位置
    CHECK_POINT_DIR = abspath(path=f"{PROJECT_DIR}/data/check.pt")   # 检查点保存位置
    
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
    TRAIN_SELECT_NUMBER = 0                                          # 训练数据选择数量
    VALID_SELECT_NUMBER = 0                                          # 验证数据选择数量
    TEST_SELECT_NUMBER = 0                                           # 测试数据选择数量
    
    TORCH_FLOAT_TYPE  = float16                                      # 浮点类型
    TORCH_INT_TYPE = int32                                           # 整数类型
    IS_AUTO_CAST = True                                              # 是否自动转换类型
    
    IS_SHUFFLE = True                                                # 是否打乱数据
    SEQ_LEN = 128                                                    # 最大序列长度
    BATCH_SIZE = 256                                                 # 批处理大小
    LEARNING_RATE = 1e-5                                             # 学习率
    SAVE_STEP = 100                                                  # 每批次保存
    EPOCHS = 30                                                      # 训练轮数
    MAX_LENGTH = 32                                                  # 生成最大长度
    NUM_BEAMS = 5                                                    # 束搜索
    
    
if __name__ == '__main__':
    Config.BATCH_SIZE = 16
    # process = ProductDataProcess(data_path=Config.DATASET_PATH, label_path=Config.LABELS_PATH)
    # process.process_data()
    
    trainer = ProductModel(data_path=Config.DATASET_PATH, model_path=Config.BERT_MODEL,
                           saved_model_path=Config.SAVED_MODEL_PATH, label_path=Config.LABELS_PATH,
                           check_point_path=Config.CHECK_POINT_DIR)
    # trainer.train()
    metrics = trainer.test()
    print(f"metrics = {metrics}")
