#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  image-process  
    FileName       ：  similarity 
    CreateTime     ：  2026-09-13 00:10:34 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import matplotlib.pyplot as plt
from os import listdir
from os.path import abspath
from numpy import ndarray, save as np_save, load as np_load
from sklearn.neighbors import NearestNeighbors
from torch import Tensor, no_grad, empty, cat, save, load
from torch.nn import Module, Conv2d, ConvTranspose2d, MaxPool2d, Sequential, ReLU, Sigmoid, CrossEntropyLoss
from torch.optim import AdamW, Optimizer
from PIL.Image import open as pil_open
from torch.utils.data import DataLoader
from tqdm import tqdm
from common import BaseConfig, BaseDataset, BaseModelOperation, Utils, BaseFigure


class Config(BaseConfig):
    # =================================== 基本路径配置 ===================================
    IMAGE_DIR = abspath(path=f"{BaseConfig.PROJECT_DIR}/data/dataset")       # 数据集目录
    MODEL_PATH = abspath(path=f"{BaseConfig.PROJECT_DIR}/data")      # 模型保存路径
    
    # =================================== 图片转换配置 ===================================
    IMAGE_HEIGHT = 64                                                # 原始图像高度（注意：实际训练时会被Resize为68x68）
    IMAGE_WIDTH = 64                                                 # 原始图像宽度（需检查与数据预处理的一致性）
    
    # ================================= 数据划分配置 =================================
    SHUFFLE_BUFFER_SIZE = 100                                        # 数据混洗缓冲区大小（影响数据加载顺序随机性）
    IS_TRAIN_SHUFFLE = True                                          # 是否在训练时打乱数据
    IS_VALID_SHUFFLE = False                                         # 是否在验证时打乱数据
    IS_TEST_SHUFFLE = False                                          # 是否在测试时打乱数据
    IS_TRAIN_DROP_LAST = True                                        # 是否在训练时丢弃最后一个批次
    IS_VALID_DROP_LAST = False                                       # 是否在验证时丢弃最后一个批次
    IS_TEST_DROP_LAST = False                                        # 是否在测试时丢弃最后一个批次
    
    # =================================== 模型配置 ===================================
    LEARNING_RATE = 0.001                                            # 学习率
    BATCH_SIZE = 32                                                  # 批次大小
    EPOCHS = 10                                                      # 训练轮数


# 图像数据集
class ImageDataset(BaseDataset):
    def __init__(self, config: Config):
        super().__init__()
        
        self.image_dir = abspath(path=config.IMAGE_DIR)              # 图像目录
        self.image_height = config.IMAGE_HEIGHT                      # 图像高度
        self.image_width = config.IMAGE_WIDTH                        # 图像宽度
        self.noisy_factor = config.NOISE_FACTOR                      # 噪声因子
        
        name_list = listdir(path=f"{self.image_dir}")                # 图像文件名列表
        self.name_list = Utils.sorted_alphanum(file_names=name_list) # 图像文件名列表
    
    def __len__(self):
        length = len(self.name_list)                                 # 图像文件名列表长度
        return length

    def __getitem__(self, index: int) -> tuple[Tensor, Tensor]:
        image_path = abspath(path=f"{self.image_dir}/{self.name_list[index]}")
        image = pil_open(fp=image_path).convert(mode="RGB")          # 打开图像并转换为 RGB 模式
        
        # 应用数据处理变换，转换图像
        image_tensor = self._transform(height=self.image_height, width=self.image_width)(img=image)
        return image_tensor, image_tensor


# 编码器
class ConvEncoder(Module):
    def __init__(self, in_channels: int=3, out_channels: int=256, kernel_size: int = 3,
                 stride: int = 1, padding: int = 1):
        super().__init__()
        
        # 定义 5 个卷积层
        conv1 = Conv2d(in_channels=in_channels, out_channels=16, kernel_size=kernel_size, stride=stride, padding=padding)
        conv2 = Conv2d(in_channels=16, out_channels=32, kernel_size=kernel_size, stride=stride, padding=padding)
        conv3 = Conv2d(in_channels=32, out_channels=64, kernel_size=kernel_size, stride=stride, padding=padding)
        conv4 = Conv2d(in_channels=64, out_channels=128, kernel_size=kernel_size, stride=stride, padding=padding)
        conv5 = Conv2d(in_channels=128, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding)
        
        # 通用池化层
        pool = MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        # 通用激活层
        relu = ReLU()
        
        self.network = Sequential(conv1, relu, pool, conv2, relu, pool, conv3, relu, pool,
                                  conv4, relu, pool, conv5, relu, pool)
    
    def forward(self, input_tensor: Tensor) -> Tensor:
        output_tensor = self.network.forward(input_tensor)
        return output_tensor


# 解码器
class ConvDecoder(Module):
    def __init__(self, in_channels: int = 256, out_channels: int = 3, kernel_size: int = 2, stride: int = 2):
        super().__init__()
        
        # 定义 5 个反卷积层
        conv1 = ConvTranspose2d(in_channels=in_channels, out_channels=128, kernel_size=kernel_size, stride=stride)
        conv2 = ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=kernel_size, stride=stride)
        conv3 = ConvTranspose2d(in_channels=64, out_channels=32, kernel_size=kernel_size, stride=stride)
        conv4 = ConvTranspose2d(in_channels=32, out_channels=16, kernel_size=kernel_size, stride=stride)
        conv5 = ConvTranspose2d(in_channels=16, out_channels=out_channels, kernel_size=kernel_size, stride=stride)
        
        # 通用激活层
        relu = ReLU()
        sigmoid = Sigmoid()
        
        self.network = Sequential(conv1, relu, conv2, relu, conv3, relu, conv4, relu, conv5, sigmoid)
    
    def forward(self, input_tensor: Tensor) -> Tensor:
        output_tensor = self.network.forward(input_tensor)
        return output_tensor


# 相似度模型
class SimilarityModel(Module):
    def __init__(self, encode_model: ConvEncoder, decode_model: ConvDecoder):
        super().__init__()
        
        self.encode_model = encode_model
        self.decode_model = decode_model
    
    # 前向传播
    def forward(self, input_tensor: Tensor) -> Tensor:
        encoded = self.encode_model.forward(input_tensor=input_tensor)
        output_tensor = self.decode_model.forward(input_tensor=encoded)
        return output_tensor
        

# 相似度模型操作
class SimilarityModelOperation(BaseModelOperation):
    def __init__(self):
        super().__init__(config=config)
        
        self.encode_model_path = abspath(path=f"{config.MODEL_PATH}/encode-similarity.pth")
        self.decode_model_path = abspath(path=f"{config.MODEL_PATH}/decode-similarity.pth")
        
        self.loss_fn = CrossEntropyLoss()                            # 损失函数
        self.optimizer = AdamW                                       # 优化器
    
    def train_one_epoch(self, model: Module, train_loader: DataLoader, optimizer: Optimizer) -> float:
        encoder_model = model.encode_model                           # 获取编码器模型
        decoder_model = model.decode_model                           # 获取解码器模型
        encoder_model.train()                                        # 设置编码器为训练模式
        decoder_model.train()                                        # 设置解码器为训练模式
        
        train_loss = 0.0                                             # 训练损失
        for input_tensor, target_tensor in train_loader:
            input_tensor = input_tensor.to(device=self.device)       # 将噪声图像移动到指定设备
            target_tensor = target_tensor.to(device=self.device)     # 将目标图像移动到指定设备
            
            encoded = model.encode_model.forward(input_tensor)       # 编码
            decoded = model.decode_model.forward(encoded)            # 解码
            loss_value = self.loss_fn(decoded, target_tensor)        # 计算损失值
            
            loss_value.backward()                                    # 反向传播，计算梯度
            optimizer.step()                                         # 更新模型参数
            optimizer.zero_grad()                                    # 清空梯度
            train_loss += loss_value.item()                          # 累加损失值
        
        average_loss = train_loss / len(train_loader)                # 计算平均训练损失
        print(f"training loss: {average_loss:.4f}")
        
        return average_loss
    
    def train_model(self, model: Module, train_loader: DataLoader,
                    valid_loader: DataLoader) -> tuple[list[float], list[float]]:
        
        model.to(device=self.device)                                 # 将模型移动到指定设备
        params = list(model.encode_model.parameters()) + list(model.decode_model.parameters())
        optimizer = self.optimizer(params=params, lr=self.learning_rate)  # 创建优化器
        
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
        
        save(obj=model.encode_model.state_dict(), f=self.encode_model_path)     # 保存编码器模型参数
        save(obj=model.decode_model.state_dict(), f=self.decode_model_path)     # 保存解码器模型参数
        print(f"Model saved to '{self.encode_model_path}' and '{self.decode_model_path}'")
        
        return train_loss_list, valid_loss_list
    
    # 嵌入
    def embed(self, embed_model: ConvEncoder, data_loader: DataLoader, bedding_path: str = "embeddings.npy") -> ndarray:
        state_dict = load(f=self.encode_model_path, map_location=self.device)  # 加载编码器模型参数
        embed_model.load_state_dict(state_dict=state_dict)   # 加载编码器模型参数
        embed_model.eval()                                          # 设置模型为评估模式
        
        embedding_tensor = empty(size=(0,))                          # 初始化为空张量
        with no_grad():
            bar = tqdm(iterable=data_loader, desc="embedding ", dynamic_ncols=True, colour="red")
            for input_tensor, _ in bar:
                input_tensor = input_tensor.to(device=self.device)   # 将输入图像移动到指定设备
                predict_tensor = embed_model.forward(input_tensor)   # 前向传播，获取预测图像
                embedding_tensor = cat(tensors=(embedding_tensor, predict_tensor) , dim=0)
                
        vector_array = embedding_tensor.reshape(embedding_tensor.shape[0], -1).numpy()
        np_save(file=bedding_path, arr=vector_array)                 # 保存嵌入向量
        print(f"Embeddings saved to '{bedding_path}'")
        
    
    # 计算相似度
    def calculate_similarity(self, image_tensor: Tensor, image_count: int, bedding_path: str = "embeddings.npy") -> list:
        model = ConvEncoder()                                        # 创建编码器模型
        model.to(device=self.device)                                 # 将模型移动到指定设备
        model.eval()                                                 # 设置模型为评估模式
        image_tensor = image_tensor.to(device=self.device)           # 将数据张量移动到指定设备
        
        with no_grad():
            predict_tensor = model.forward(input_tensor=image_tensor)
        predict_array = predict_tensor.reshape(predict_tensor.shape[0], -1).numpy()
        
        vector_array = np_load(file=bedding_path)
        knn = NearestNeighbors(n_neighbors=image_count, metric='cosine')
        
        knn.fit(X=vector_array)
        indices = knn.kneighbors(X=predict_array, return_distance=False)
        
        if len(indices.tolist()) > 0:
            return indices.tolist()[0]
        else:
            return []
        

class Figure(BaseFigure):
    @staticmethod
    def plot_similarity(similarity_list: list, image_tensor: Tensor, image_count: int, dataset: ImageDataset) -> None:
        fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(25, 5))
        
        image_array = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
        axes[0, 2].imshow(image_array)
        
        for i in range(image_count):
            index = similarity_list[i]
            image, _ = dataset[index]
            image_array = image.squeeze(0).permute(1, 2, 0).cpu().numpy()
            axes[1, i].imshow(image_array)
        
        for ax in axes.flat:
            ax.axis('off')
        
        plt.show()


if __name__ == '__main__':
    config = Config()
    Utils.seed_everything(seed=Config.SEED)
    
    dataset = ImageDataset(config=config)
    # model = SimilarityModel(encode_model=ConvEncoder(), decode_model=ConvDecoder())
    #
    model_operation = SimilarityModelOperation()
    train_loader, valid_loader = model_operation.split_dataset(dataset=dataset, config=config)
    #
    # train_losses, valid_losses = model_operation.train_model(model=model, train_loader=train_loader,
    #                                                          valid_loader=valid_loader)
    # Figure.plot_line(data_list=train_losses)
    # Figure.plot_line(data_list=valid_losses)
    #
    # accuracies = model_operation.test_model(model=model, test_loader=valid_loader)
    # Figure.plot_line(data_list=accuracies)

    # model_operation.embed(embed_model=ConvEncoder(), data_loader=valid_loader, bedding_path="../data/embeddings.npy")
    
    image_tensor, _ = valid_loader.dataset[0]
    image_tensor = image_tensor.unsqueeze(0)
    similarity = model_operation.calculate_similarity(image_tensor=image_tensor, image_count=5, bedding_path="../data/embeddings.npy")
    Figure.plot_similarity(similarity_list=similarity, image_tensor=image_tensor, image_count=5, dataset=dataset)
