#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  image-process  
    FileName       ：  test 
    CreateTime     ：  2026-09-13 00:09:22 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from torch import randn, load
from denoising import Config as NC, DeNoisyConv, ModelOperation, ImageDataset, Figure


class NoisyTest(TestCase):
    config = NC()
    model = DeNoisyConv()
    model_operation = ModelOperation(config=config)
    image_dataset = ImageDataset(image_config=config)
    
    def test_model(self):
        x = randn(1, 3, 68, 68)
        print(f"输入图片形状：{x.shape}")
        
        y = self.model.forward(input=x)
        print(f"输出图片形状：{y.shape}")
        
        self.assertEqual(y.shape, x.shape)
    
    def test_vaild(self):
        _, vailds = self.model_operation.split_dataset(dataset=self.image_dataset, config=self.config)
        iterable = iter(vailds)
        noisy_images, origin_images = next(iterable)
        predict_images = self.model_operation.predict_data(model=self.model, input_tensor=noisy_images)
        
        Figure.plot_image(images=origin_images, noisies=noisy_images, predicts=predict_images)
        
