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

from typing import Dict, Union
from datasets import load_from_disk
from transformers import AutoTokenizer, Trainer, TrainingArguments, DataCollatorForTokenClassification
from transformers import AutoModelForTokenClassification, EvalPrediction, EarlyStoppingCallback
from torch import cuda, no_grad, argmax, device
from evaluate import load as load_metric
from config import PathConfig, FieldConfig, TrainConfig, PredictConfig


# 数据处理类
class GraphModel:
    def __init__(self):
        self.train_path = PathConfig.TRAIN_PATH                      # 训练数据路径
        self.test_path = PathConfig.TEST_PATH                        # 测试数据路径
        self.valid_path = PathConfig.VALID_PATH                      # 验证数据路径
        self.model_path = PathConfig.SAVED_MODEL_PATH                # 模型保存路径
        
        self.label2id = None                                          # 标签映射
        self.id2label = None                                          # 标签映射
        self.tokenizer = None                                         # 分词器
        self.model = None                                             # 模型
        self.data_collator = None                                     # 数据整理器
        self.trainer = None                                           # 训练器
        
        self.get_parameters()                                         # 获取参数
        
    # 获取参数
    def get_parameters(self) -> None:
        # 1. 加载预训练的 BERT 分词器
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=PathConfig.BERT_MODEL)
        
        # 2. 标签映射
        self.id2label = {index: label for index, label in enumerate(FieldConfig.LABELS)}
        self.label2id = {label: index for index, label in enumerate(FieldConfig.LABELS)}
        
        # 3. 加载预训练的 BERT 模型
        self.model = AutoModelForTokenClassification.from_pretrained(
                pretrained_model_name_or_path=PathConfig.BERT_MODEL,
                id2label=self.id2label,
                label2id=self.label2id,
                num_labels=len(FieldConfig.LABELS))
        
        # 4. 数据整理器
        self.data_collator = DataCollatorForTokenClassification(tokenizer=self.tokenizer,
                                                                padding=TrainConfig.IS_PADDING,
                                                                max_length=TrainConfig.MAX_LENGTH,
                                                                return_tensors=TrainConfig.RETURN_TENSORS,
                                                                label_pad_token_id=FieldConfig.MARK_LABEL)
        
    # 训练模型
    def train(self) -> None:
        # 1. 加载数据集
        train_dataset = load_from_disk(dataset_path=self.train_path)
        valid_dataset = load_from_disk(dataset_path=self.valid_path)
        
        # 2. 创建训练参数
        train_args = TrainingArguments(
                output_dir=PathConfig.SAVED_MODEL_PATH,              # 模型保存路径
                logging_dir=PathConfig.LOG_DIR,                      # 日志保存位置
                num_train_epochs=TrainConfig.EPOCHS,                 # 训练总轮次
                per_device_train_batch_size=TrainConfig.BATCH_SIZE,  # 批大小
                save_strategy=TrainConfig.SAVE_STRATEGY,             # 保存策略
                save_steps=TrainConfig.SAVE_STEP,                    # 保存一次的迭代批次
                save_total_limit=TrainConfig.CHECK_POINT_COUNT,      # 最多保存3个检查点
                fp16=TrainConfig.IS_FP16,                            # 开启混合精度训练
                logging_strategy=TrainConfig.SAVE_STRATEGY,          # 日志写入策略
                logging_steps=TrainConfig.SAVE_STEP,                 # 日志写入一次的迭代批次
                eval_strategy=TrainConfig.SAVE_STRATEGY,             # 评估策略
                eval_steps=TrainConfig.SAVE_STEP,                    # 评估一次的迭代批次
                metric_for_best_model=TrainConfig.EVAL_METRIC,       # 模型评估指标
                greater_is_better=TrainConfig.GREATER_IS_BETTER,     # 模型评估指标是否越
                load_best_model_at_end=TrainConfig.IS_BEST_MODEL     # 训练结束加载最佳模型
        )
        
        # 3. 早停回调
        early_stop = EarlyStoppingCallback(early_stopping_patience=TrainConfig.EARLY_STOPPING_PATIENCE)
        
        # 4. 创建训练器
        self.trainer = Trainer(model=self.model, train_dataset=train_dataset, eval_dataset=valid_dataset,
                               args=train_args, data_collator=self.data_collator, callbacks=[early_stop],
                               compute_metrics=self.compute_metrics)
                
        # 5. 训练
        results = self.trainer.train()
        
        # 6. 保存模型
        self.__save_model()
        
        return results
        
    # 验证模型
    def eval(self):
        # 1. 加载模型
        model = AutoModelForTokenClassification.from_pretrained(PathConfig.SAVED_MODEL_PATH)
        
        # 2. 加载数据集（测试集）
        test_dataset = load_from_disk(dataset_path=self.test_path)
        
        # 3. 定义训练器
        trainer = Trainer(model=model, eval_dataset=test_dataset, data_collator=self.data_collator,
                          compute_metrics=self.compute_metrics)
        
        # 4. 验证评估
        result = trainer.evaluate()
        return  result
    
    # 预测数据
    def predict(self, text: Union[str, list[str]]):
        is_string = isinstance(text, str)
        
        # 1. 判断输入参数类型
        if is_string:
            text = [text]
        
        # 2. 预分词，得到字符列表
        token_list = [list(char) for char in text]
        
        # 3. 数据编码
        encoding = self.tokenizer(text=token_list, is_split_into_words=PredictConfig.IS_SPLIT_WORDS,
                                  truncation=PredictConfig.IS_TRUNCATION, padding=PredictConfig.IS_PADDING,
                                  return_tensors=PredictConfig.RETURN_TENSORS)
        
        # 2. 加载模型
        model = AutoModelForTokenClassification.from_pretrained(pretrained_model_name_or_path=PathConfig.SAVED_MODEL_PATH)
        
        # 3. 将模型和数据加载到设备
        dev = device("cuda" if cuda.is_available() else "cpu")
        inputs = {key: value.to(device=dev) for key, value in encoding.items()}
        model.to(device=dev)
        
        # 4. 前向传播
        with no_grad():
            outputs = model(**inputs)                                # 前向传播
            logits = outputs.logits                                  # 预测结果
            predict_list = argmax(input=logits, dim=-1).tolist()     # 预测标签
        
        # 5. 将 id 转换为真正的标签
        results = []
        for tokens, predict in zip(token_list, predict_list):
            predict = predict[1:len(tokens) + 1]                     # 去掉填充对应的 id
            predicts = [self.id2label[index] for index in predict]   # 预测标签
            result = self.__extract_label(inputs=predicts, contents=tokens)    # 抽取标签
            results.append(result)                                   # 添加结果
        
        if is_string:
            return results[0]
        
        return results
        
    # 评估模型
    def compute_metrics(self, predict: EvalPrediction) -> Dict[str, float]:
        seqeval_eval = load_metric(TrainConfig.SEQEVAL)              # 评估指标
        logits = predict.predictions                                 # 模型预测输出
        predict_list = logits.argmax(axis=-1)                        # 预测标签
        label_list = predict.label_ids                               # 真实标签
        
        # 将标签 id 转换为真正的标注标签 BIO
        unpad_label_list = []
        unpad_predict_list = []
        for pred, label in zip(predict_list, label_list):
            # 使用标签的 mask 同时对标签和预测进行过滤，确保长度一致
            mask = label != FieldConfig.MARK_LABEL
            unpad_label = label[mask]
            unpad_predict = pred[mask]
            
            # 映射为真正的标签
            unpad_label = [self.id2label[l] for l in unpad_label]
            unpad_predict = [self.id2label[p] for p in unpad_predict]
            
            # 保存
            unpad_label_list.append(unpad_label)
            unpad_predict_list.append(unpad_predict)
            
        results = seqeval_eval.compute(predictions=unpad_predict_list, references=unpad_label_list)
        return results
    
    # 保存模型
    def __save_model(self, model_path: str = PathConfig.SAVED_MODEL_PATH) -> None:
        self.trainer.save_model(output_dir=model_path)
        print(f"模型保存成功：{model_path}")
    
    # 抽取标签
    def __extract_label(self, inputs: list[str], contents: list[str]) -> list[str]:
        label_list = []
        label = ""
        for index, input in enumerate(inputs):
            if input == FieldConfig.START_FLAG:
                if label and label not in label_list:
                    label_list.append(label)
                    
                label = contents[index]
            elif input == FieldConfig.MIDDLE_FLAG:
                label += contents[index]
            else:
                if label and label not in label_list:
                    label_list.append(label)
        
        if label and label not in label_list:
            label_list.append(label)
            
        return label_list
    

if __name__ == '__main__':
    TrainConfig.BATCH_SIZE = 16
    TrainConfig.EPOCHS = 2
    model = GraphModel()
    trains = model.train()
    print(f"trains = {trains}")
    
    pre = model.predict(text="曼妮芬性感轻透舒适提托文胸女士性感蕾丝单层围薄款调整型内衣")
    print(f"predict = {pre}")

    evals = model.eval()
    print(f"evals = {evals}")
