#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  image-process  
    FileName       ：  common 
    CreateTime     ：  2026-09-15 14:58:51 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from os import environ
from os.path import abspath, dirname, join, exists
from random import seed as random_seed
from re import split as re_split

import matplotlib.pyplot as plt
from numpy import random as np_random
from torch import manual_seed as torch_manual_seed, device, cuda, Tensor, rand_like, no_grad, save, load
from torch.backends import cudnn
from torch.cuda import manual_seed as cuda_manual_seed
from torch.nn import MSELoss, Module
from torch.optim import Optimizer
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.transforms import Compose, Resize, ToTensor
from tqdm import tqdm


# 工具类
class Utils:
    # 对所有库设置相同的随机数种子，保证训练过程可复现
    @staticmethod
    def seed_everything(seed: int=42) -> None:
        environ['PYTHONHASHSEED'] = str(seed)                  # 设置系统环境变量的哈希种子
        
        random_seed(a=seed)                                    # 设置 Python 内置随机数种子
        np_random.seed(seed=seed)                              # 设置 Numpy随机数种子
        torch_manual_seed(seed=seed)                           # 设置 PyTorch随机数种子
        cuda_manual_seed(seed=seed)                            # 设置 GPU 随机数种子
        cudnn.deterministic = True                             # 保证 CuDN N操作确定性
        cudnn.benchmark = False                                # 禁用自动选择优化算法
        
        print(f"将随机数种子设置为：{seed}")
        
        
    # 将文件名的列表，按照字母和数字进行排序
    @staticmethod
    def sorted_alphanum(file_names: list[str]) -> list[str]:
        # 定义转换函数：将数字转为int，非数字转为小写形式
        convert = lambda string: int(string) if string.isdigit() else string.lower()
        
        # 获取排序键函数：列表表达式，将原文件名切分开，并转换
        alphanum_key = lambda name: [convert(string) for string in re_split(pattern='([0-9]+)', string=name)]
        
        # 将原文件名列表，按键排序，并返回
        sorted_file_names = sorted(file_names, key=alphanum_key)
        
        return sorted_file_names


class BaseConfig:
    # =================================== 基本路径配置 ===================================
    PYTHON_PATH = abspath(path=__file__)                             # 执行脚本路径
    PYTHON_DIR = dirname(p=f"{PYTHON_PATH}")                         # 执行脚本目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/..")                   # 项目目录
    IMAGE_DIR = join(PROJECT_DIR, "data/dataset")                    # 图片数据集目录
    LABEL_PATH = join(PROJECT_DIR, "data/fashion-labels.csv")        # 标签数据集路径
    MODEL_PATH = join(PROJECT_DIR, "data/model.pth")                 # 模型保存路径
    
    # =================================== 随机种子配置 ===================================
    SEED = 42                                                        # 全局随机种子（确保实验可复现性）
    
    # =================================== 图片转换配置 ===================================
    IMAGE_HEIGHT = 68                                                # 原始图像高度（注意：实际训练时会被Resize为68x68）
    IMAGE_WIDTH = 68                                                 # 原始图像宽度（需检查与数据预处理的一致性）
    NOISE_FACTOR = 0.5                                               # 噪声因子
    TRAIN_RATIO = 0.75                                               # 训练集划分比例（75%训练，25%验证）
    VALID_RATIO = 1 - TRAIN_RATIO                                    # 验证集比例（自动计算，无需修改）
    IS_TRAIN_SHUFFLE = True                                          # 是否在训练时打乱数据
    IS_TRAIN_DROP_LAST = True                                        # 是否在训练时丢弃最后一个批次
    IS_VALID_SHUFFLE = False                                         # 是否在验证时打乱数据
    IS_VALID_DROP_LAST = False                                       # 是否在验证时丢弃最后一个批次
    IS_TEST_SHUFFLE = False                                          # 是否在测试时打乱数据
    IS_TEST_DROP_LAST = False                                        # 是否在测试时丢弃最后一个批次
    
    # =================================== 模型参数配置 ===================================
    LEARNING_RATE = 1e-3                                             # 初始学习率（AdamW 优化器使用）
    EPOCHS = 50                                                      # 总训练轮次（需平衡过拟合与欠拟合）
    TRAIN_BATCH_SIZE = 32                                            # 训练批次大小（GPU显存不足时可调小）
    VALID_BATCH_SIZE = 32                                            # 验证批次大小（建议与训练批次一致）
    TEST_BATCH_SIZE = 32                                             # 验证/测试批次大小（建议与训练批次一致）
    MIN_LOSS = float('inf')                                          # 最小损失值（用于早停法）
    DEVICE = device("cuda" if cuda.is_available() else "cpu")        # 设备（GPU 或 CPU）
    

# 图像数据集类
class BaseDataset(Dataset):
    def __init__(self) -> None:
        super().__init__()
    
    # 数据处理变换
    def _transform(self, height: int, width: int) -> Compose:
        resize = Resize(size=(height, width))                        # 调整图片大小
        transforms = [resize, ToTensor()]                            # 定义转换操作
        image_transform = Compose(transforms=transforms)             # 创建转换操作
        return image_transform
    
    # 添加噪声
    def _add_noise(self, image_tensor: Tensor, noisy_factor: float = 0.5) -> Tensor:
        noisy_tensor = noisy_factor * rand_like(image_tensor)        # 生成噪声张量（噪声因子乘以随机张量）
        noisy_image = image_tensor + noisy_tensor                    # 将噪声张量添加到图像张量中，生成噪声图像
        return noisy_image


# 模型操作类
class BaseModelOperation:
    def __init__(self, config: BaseConfig) -> None:
        self.learning_rate = config.LEARNING_RATE                    # 学习率
        self.epochs = config.EPOCHS                                  # 总训练轮次（需平衡过拟合与欠拟合
        self.device = config.DEVICE                                  # 设备（GPU 或 CPU）
        self.model_path = config.MODEL_PATH                          # 模型保存路径
        
        self.loss_fn = MSELoss()                                     # 损失函数
        self.optimizer = Optimizer                                   # 优化器
        self.min_train_loss = config.MIN_LOSS                        # 最小损失值（用于早停法）
        self.min_valid_loss = config.MIN_LOSS                        # 最小损失值（用于早停法）
    
    # 生成数据加载器
    @classmethod
    def split_dataset(cls, dataset: BaseDataset, config: BaseConfig) -> tuple[DataLoader, DataLoader]:
        length_list = [config.TRAIN_RATIO, 1 - config.TRAIN_RATIO]
        train_dataset, valid_dataset = random_split(dataset=dataset, lengths=length_list)
        
        # 训练数据加载器（自动打乱数据）
        train_loader = DataLoader(dataset=train_dataset, batch_size=config.TRAIN_BATCH_SIZE,
                                  shuffle=config.IS_TRAIN_SHUFFLE, drop_last=config.IS_TRAIN_DROP_LAST)
        
        # 验证数据加载器（不打乱数据）
        valid_loader = DataLoader(dataset=valid_dataset, batch_size=config.TEST_BATCH_SIZE,
                                  shuffle=config.IS_VALID_SHUFFLE, drop_last=config.IS_VALID_DROP_LAST)
        
        return train_loader, valid_loader
        
    # 训练一个 epoch
    def train_one_epoch(self, model: Module, train_loader: DataLoader, optimizer: Optimizer) -> float:
        model.train()                                                # 设置模型为训练模式
        
        train_loss = 0.0                                             # 训练损失
        for input_tensor, target_tensor in train_loader:
            input_tensor = input_tensor.to(device=self.device)       # 将噪声图像移动到指定设备
            target_tensor = target_tensor.to(device=self.device)     # 将目标图像移动到指定设备
            
            predict_tensor = model.forward(input_tensor)             # 前向传播，获取预测图像
            loss_value = self.loss_fn(predict_tensor, target_tensor) # 计算损失值
            loss_value.backward()                                    # 反向传播，计算梯度
            optimizer.step()                                         # 更新模型参数
            optimizer.zero_grad()                                    # 清空梯度
            train_loss += loss_value.item()                          # 累加损失值
        
        average_loss = train_loss / len(train_loader)                # 计算平均训练损失
        print(f"training loss: {average_loss:.4f}")
        
        return average_loss
    
    # 训练模型
    def train_model(self, model: Module, train_loader: DataLoader,
                    valid_loader: DataLoader) -> tuple[list[float], list[float]]:
        model.to(device=self.device)                                 # 将模型移动到指定设备
        optimizer = self.optimizer(params=model.parameters(), lr=self.learning_rate)  # 创建优化器
        
        train_loss_list = []                                         # 训练损失列表
        valid_loss_list = []                                         # 验证损失列表
        bar = tqdm(iterable=range(self.epochs), desc="Training", unit="epoch", colour="yellow")
        for epoch in bar:
            train_loss = self.train_one_epoch(model=model, train_loader=train_loader, optimizer=optimizer)
            train_loss_list.append(train_loss)                       # 将平均训练损失添加到列表中
            
            valid_loss = self.evaluate_model(model=model, valid_loader=valid_loader)
            valid_loss_list.append(valid_loss)                       # 将平均验证损失添加到列表中

            bar.set_description(f"training loss: {epoch} = {train_loss:.5f}")
            
            if valid_loss > self.min_valid_loss and train_loss > self.min_train_loss:
                break                                                # 跳出循环
            else:
                self.min_valid_loss = valid_loss                     # 更新最小损失
                self.min_train_loss = train_loss                     # 更新最小损失
        
        save(obj=model.state_dict(), f=self.model_path)              # 保存模型参数
        print(f"Model saved to '{self.model_path}'")
        
        return train_loss_list, valid_loss_list
    
    # 评估模型
    def evaluate_model(self, model: Module, valid_loader: DataLoader, is_progress: bool = False) -> float:
        model.eval()                                                 # 设置模型为评估模式
        
        valid_loss = 0.0                                             # 验证损失
        with no_grad():                                              # 禁用梯度计算
            if is_progress:
                bar = tqdm(iterable=valid_loader, desc="Validating", unit="batch", colour="green")
            else:
                bar = valid_loader
                
            for valid_tensor, target_tensor in bar:
                valid_tensor = valid_tensor.to(device=self.device)   # 将噪声图像移动到指定设备
                target_tensor = target_tensor.to(device=self.device) # 将目标图像移动到指定设备
                
                predict_image = model.forward(valid_tensor)          # 前向传播，获取预测图像
                loss_value = self.loss_fn(predict_image, target_tensor)    # 计算损失值
                valid_loss += loss_value.item()                      # 累加损失值
                
                # bar.set_description(f"validation loss: {valid_loss:.4f}")
                
        average_loss = valid_loss / len(valid_loader)                # 计算平均验证损失
        return average_loss
    
    # 测试模型
    def test_model(self, model: Module, test_loader: DataLoader) -> list[float]:
        if not exists(path = self.model_path):
            raise ValueError("进行测试之前，必须先训练模型......")
        
        state_dict = load(f=self.model_path, map_location=self.device)
        model.load_state_dict(state_dict=state_dict)                 # 加载模型参数
        model.eval()                                                 # 设置模型为评估模式
        
        accuracy_list = []                                           # 准确率
        with no_grad():                                              # 禁用梯度计算
            bar = tqdm(iterable=test_loader, desc="testing", unit="batch", colour="orange")
            for test_tensor, target_tensor in bar:
                test_tensor = test_tensor.to(device=self.device)     # 将测试移动到指定设备
                target_tensor = target_tensor.to(device=self.device) # 将目标移动到指定设备
                
                predict_tensor = model.forward(test_tensor)           # 前向传播，获取预测
                accuracy = (predict_tensor == target_tensor).sum().item() # 计算目标和预测相等的数量
                accuracy_list.append(accuracy)                        # 将准确率添加到列表中
                
        return accuracy_list
    
    # 预测图像
    def predict_data(self, model: Module, input_tensor: Tensor) -> Tensor:
        if not exists(self.model_path):
            raise ValueError("进行推理预测之前，必须先训练模型......")
        
        state_dict = load(f=self.model_path, map_location=self.device)    # 加载模型
        model.load_state_dict(state_dict=state_dict)                 # 加载模型参数
        model.eval()                                                 # 设置模型为评估模式
        
        with no_grad():
            predict_tensor = model.forward(input_tensor)                   # 前向传播，获取预测图像
        
        return predict_tensor
    

# 绘制图像
class BaseFigure:
    # 绘制损失曲线
    @staticmethod
    def plot_line(data_list: list[float]) -> None:
        plt.figure(figsize=(10, 6))
        plt.plot(data_list, label="loss", color="red", linestyle="-", marker="o")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.legend(loc="upper right")
        plt.show()
