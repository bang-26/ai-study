#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  image-process  
    FileName       ：  classification 
    CreateTime     ：  2026-09-13 00:09:56 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from os import listdir
from os.path import abspath, join
from typing import Any
from PIL.Image import open as pil_open
from pandas import read_csv
from torch import Tensor
from torch.nn import Module, Conv2d, MaxPool2d, Flatten, Sequential, ReLU, Linear, CrossEntropyLoss
from torch.optim import AdamW
from common import Utils, BaseConfig, BaseDataset, BaseModelOperation, BaseFigure


class Config(BaseConfig):
    # =================================== 基本路径配置 ===================================
    IMAGE_DIR = abspath(path=f"{BaseConfig.PROJECT_DIR}/data/dataset")       # 数据集目录
    MODEL_PATH = abspath(path=f"{BaseConfig.PROJECT_DIR}/data/classify.pth") # 模型保存路径
    
    # =================================== 图片转换配置 ===================================
    IMAGE_HEIGHT = 64                                                # 原始图像高度（注意：实际训练时会被Resize为68x68）
    IMAGE_WIDTH = 64                                                 # 原始图像宽度（需检查与数据预处理的一致性）
    
    # ================================= 数据划分配置 =================================
    SHUFFLE_BUFFER_SIZE = 100                                        # 数据混洗缓冲区大小（影响数据加载顺序随机性）
    IS_TRAIN_SHUFFLE = True                                          # 是否在训练时打乱数据
    IS_VALID_SHUFFLE = False                                         # 是否在验证时打乱数据
    IS_TRAIN_DROP_LAST = True                                        # 是否在训练时丢弃最后一个批次
    IS_VALID_DROP_LAST = False                                       # 是否在验证时丢弃最后一个批次
    
    # =================================== 模型配置 ===================================
    LEARNING_RATE = 0.001                                            # 学习率
    BATCH_SIZE = 32                                                  # 批次大小
    EPOCHS = 10                                                      # 训练轮数
    

# 图像标签数据集
class ImageLabelDataset(BaseDataset):
    def __init__(self, config: Config):
        super().__init__()
        
        self.image_dir = config.IMAGE_DIR                            # 图像目录
        self.label_path = config.LABEL_PATH                          # 标签路径
        self.image_height = config.IMAGE_HEIGHT                      # 图像高度
        self.image_width = config.IMAGE_WIDTH                        # 图像宽度
        self.noisy_factor = config.NOISE_FACTOR                      # 噪声因子
        
        name_list = listdir(path=self.image_dir)                     # 所有文件名
        self.image_files = Utils.sorted_alphanum(file_names=name_list)
        
        label_data = read_csv(self.label_path)                       # 读取标签数据
        self.label_dict = dict(zip(label_data["id"], label_data["target"]))
    
    # 数据集长度
    def __len__(self) -> int:
        length = len(self.image_files)                               # 数据集长度
        return length
    
    # 获取数据
    def __getitem__(self, index: int) -> tuple[Tensor, Any]:
        if index >= len(self):
            raise IndexError("index out of range")
        
        file_name = self.image_files[index]                          # 文件名
        image_path = join(self.image_dir, file_name)                 # 图像路径
        image_label = self.label_dict.get(index)                     # 图像标签
        
        image = pil_open(fp=image_path, mode='r').convert("RGB")     # 打开图像并转换为 RGB 模式
        
        # 应用数据处理变换，转换图像
        image_tensor = self._transform(height=self.image_height, width=self.image_width)(img=image)
        
        return image_tensor, image_label


# 分类模型
class ClassifyModel(Module):
    def __init__(self, in_channels: int = 3, out_features: int = 5, kernel_size: int = 3,
                 stride: int = 1, padding: int = 1):
        super().__init__()
        
        # 定义两个卷积层
        conv1 = Conv2d(in_channels=in_channels, out_channels=8, kernel_size=kernel_size, stride=stride, padding=padding)
        conv2 = Conv2d(in_channels=8, out_channels=16, kernel_size=kernel_size, stride=stride, padding=padding)
        
        # 定义池化层
        pool = MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        # 定义激活函数
        relu = ReLU()
        
        # 重置形状
        flatten = Flatten()
        
        # 定义全连接层
        full_connection = Linear(in_features=4096, out_features=out_features)
        
        self.sequential = Sequential(conv1, relu, pool, conv2, relu, pool, flatten, full_connection)
        
    # 前向传播
    def forward(self, input_tensor: Tensor) -> Tensor:
        output_tensor = self.sequential.forward(input_tensor)
        return output_tensor
    

# 模型操作
class ClassifyOperate(BaseModelOperation):
    def __init__(self, config: Config):
        super().__init__(config=config)
        
        self.model_path = config.MODEL_PATH                          # 模型保存路径
        self.loss_fn = CrossEntropyLoss()                            # 损失函数
        self.optimizer = AdamW                                       # 优化器
    

# 画图
class Figure(BaseFigure):
    def __init__(self):
        super().__init__()

        
if __name__ == '__main__':
    config = Config()
    dataset = ImageLabelDataset(config=config)
    model = ClassifyModel(in_channels=3, out_features=5, kernel_size=3, stride=1, padding=1)
    
    classify_operate = ClassifyOperate(config=config)
    train_loader, valid_loader = classify_operate.split_dataset(dataset=dataset, config=config)
    
    train_loss_list, valid_loss_list = classify_operate.train_model(model=model, train_loader=train_loader,
                                                                    valid_loader=valid_loader)
    Figure.plot_line(data_list=train_loss_list)
    Figure.plot_line(data_list=valid_loss_list)
