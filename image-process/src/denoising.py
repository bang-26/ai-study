#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  image-process  
    FileName       ：  denoising 
    CreateTime     ：  2026-09-13 00:10:14 
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

import matplotlib.pyplot as plt
from PIL.Image import open as pil_open
from torch import Tensor
from torch.nn import Module, Conv2d, MaxPool2d, ConvTranspose2d, MSELoss, Sequential, ReLU
from torch.optim import Adam

from common import Utils, BaseConfig, BaseDataset, BaseModelOperation, BaseFigure


class Config(BaseConfig):
    # =================================== 基本路径配置 ===================================
    MODEL_PATH = abspath(path=f"{BaseConfig.PROJECT_DIR}/data/denoiser.pth")   # 模型保存路径
    
    # ================================= 数据划分配置 =================================
    SHUFFLE_BUFFER_SIZE = 100                                        # 数据混洗缓冲区大小（影响数据加载顺序随机性）
    IS_TRAIN_SHUFFLE = True                                          # 是否在训练时打乱数据
    IS_VALID_SHUFFLE = False                                         # 是否在验证时打乱数据
    IS_TRAIN_DROP_LAST = True                                        # 是否在训练时丢弃最后一个批次
    IS_VALID_DROP_LAST = False                                       # 是否在验证时丢弃最后一个批次
    
    # =================================== 模型配置 ===================================
    EPOCHS = 50                                                      # 训练轮数


# 图像数据集类
class ImageDataset(BaseDataset):
    def __init__(self, image_config: Config) -> None:
        super().__init__()
        
        self.image_dir = abspath(path=image_config.IMAGE_DIR)        # 图像目录
        self.image_height = image_config.IMAGE_HEIGHT                # 图像高度
        self.image_width = image_config.IMAGE_WIDTH                  # 图像宽度
        self.noisy_factor = image_config.NOISE_FACTOR                # 噪声因子
        
        name_list = listdir(path=f"{self.image_dir}")                # 图像文件名列表
        self.name_list = Utils.sorted_alphanum(file_names=name_list) # 图像文件名列表
    
    def __len__(self) -> int:
        length = len(self.name_list)                                 # 图像文件名列表长度
        return length
    
    def __getitem__(self, index) -> tuple[Tensor, Tensor]:
        image_path = join(f"{self.image_dir}", self.name_list[index])     # 获取图像路径
        
        image = pil_open(fp=image_path).convert(mode="RGB")          # 打开图像并转换为 RGB 模式
        
        # 应用数据处理变换，转换图像
        image_tensor = self._transform(height=self.image_height, width=self.image_width)(img=image)
        
        # 添加噪声
        noisy_tensor = self._add_noise(image_tensor=image_tensor, noisy_factor=self.noisy_factor)
        processed_tensor = noisy_tensor.clamp(min=0.0, max=1.0)      # 将噪声图像的像素值限制在 0 到 1 之间
        
        return processed_tensor, image_tensor
        

# 自定义神经网络
class DeNoisyConv(Module):
    
    def __init__(self, in_channels: int=3, out_channels: int=3):
        super().__init__()
        
        # 定义三个编码器卷积层
        encoder_conv1 = Conv2d(in_channels=in_channels, out_channels=32, kernel_size=3, stride=1, padding=1)
        encoder_conv2 = Conv2d(in_channels=32, out_channels=16, kernel_size=3, stride=1, padding=1)
        encoder_conv3 = Conv2d(in_channels=16, out_channels=8, kernel_size=3, stride=1, padding=1)
        
        # 定义编码器池化层
        encoder_pool = MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        # 定义编码器激活层
        encoder_relu = ReLU()
        
        # 定义编码器
        self.encoder = Sequential(encoder_conv1, encoder_relu, encoder_pool, encoder_conv2, encoder_relu,
                                  encoder_pool, encoder_conv3, encoder_relu, encoder_pool)
        
        # 定义三个转置卷积层
        decoder_conv1 = ConvTranspose2d(in_channels=8, out_channels=8, kernel_size=3, stride=2)
        decoder_conv2 = ConvTranspose2d(in_channels=8, out_channels=16, kernel_size=2, stride=2)
        decoder_conv3 = ConvTranspose2d(in_channels=16, out_channels=32, kernel_size=2, stride=2)
        
        # 定义解码器输出卷积层
        decoder_conv_out = Conv2d(in_channels=32, out_channels=out_channels, kernel_size=3, stride=1, padding=1)
        
        # 定义编码器激活层
        decoder_relu = ReLU()
        
        self.decoder = Sequential(decoder_conv1, decoder_relu, decoder_conv2, decoder_relu,
                                  decoder_conv3, decoder_relu, decoder_conv_out)
    
    # 前向传播
    def forward(self, input: Tensor):
        encoded = self.encoder(input=input)                          # 编码阶段
        decoded = self.decoder(input=encoded)                        # 解码阶段
        return decoded


class ModelOperation(BaseModelOperation):
    def __init__(self, config: Config) -> None:
        super().__init__(config=config)
        
        self.loss_fn = MSELoss()                                     # 损失函数
        self.optimizer = Adam                                        # 优化器
        self.min_loss = config.MIN_LOSS                              # 最小损失初始化为模型配置中的值
        

# 绘制图像
class Figure(BaseFigure):
    @staticmethod
    def plot_image(images: Tensor, noisies: Tensor, predicts: Tensor) -> None:
        noisy_array = noisies.permute(0, 2, 3, 1).cpu().numpy()
        origin_array = images.permute(0, 2, 3, 1).cpu().numpy()
        predict_array = predicts.permute(0, 2, 3, 1).detach().cpu().numpy()
        
        fig, axes = plt.subplots(nrows=3, ncols=10, figsize=(25, 4), sharex=True, sharey=True)
        
        for images, row in zip([noisy_array, predict_array, origin_array], axes):
            for image, ax in zip(images, row):
                ax.imshow(image)
                ax.axis("off")
        
        plt.show()
    

if __name__ == '__main__':
    Utils.seed_everything(seed=Config.SEED)                          # 设置随机数种子
    config = Config()                                                # 实例化配置类
    
    dataset = ImageDataset(image_config=config)
    
    model_operate = ModelOperation(config=config)
    train_loader, valid_loader = model_operate.split_dataset(dataset=dataset, config=config)
    
    model = DeNoisyConv()
    train_loss_list, valid_loss_list = model_operate.train_model(model=model, train_loader=train_loader,
                                                                 valid_loader=valid_loader)
    Figure.plot_line(data_list=train_loss_list)
    Figure.plot_line(data_list=valid_loss_list)
    
    data_iter = iter(valid_loader)
    noisy_images, images = next(data_iter)
    predict_images = model_operate.predict_data(model=model, input_tensor=images)
    Figure.plot_image(images=images, noisies=noisy_images, predicts=predict_images)
