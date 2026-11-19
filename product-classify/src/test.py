#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  product-classify  
    FileName       ：  test 
    CreateTime     ：  2026-06-24 23:34:07 
    Author         ：  Administrator
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from multiprocess.pool import Pool
from requests import get, post
from product_classify import Config, ProductDataProcess, ProductModel, ProductTrainer
from web import Title


config = Config()


class DataProcessTest(TestCase):
    process = ProductDataProcess(config=config)
    
    def test_process(self):
        self.process.process_data(ratio=0.01)
        
    def test_loader(self):
        train_path = f"{config.DATA_DIR}/{config.TEST_FLAG}"
        loader = self.process.get_dataloader(dataset_path=train_path)
        
        print(f"size = {len(loader)}")
        for batch in loader:
            for k, v in batch.items():
                print(f"{k} = {v}")
            break


class TrainerTest(TestCase):
    process = ProductDataProcess(config=config)
    product = ProductModel(config=config)
    trainer = ProductTrainer(config=config, product_model=product)
    
    def test_trainer(self):
        config.LEARNING_RATE = 0.001
        
        train_loader = self.process.get_dataloader(dataset_path=f"{config.DATA_DIR}/{config.TRAIN_FLAG}")
        valid_loader = self.process.get_dataloader(dataset_path=f"{config.DATA_DIR}/{config.VALID_FLAG}")
        
        self.trainer.train(train_loader=train_loader, valid_loader=valid_loader)
        

class WebTest(TestCase):
    BASE_URL = "http://127.0.0.1:8080"
    
    def test_hello(self):
        response = get(url=f"{self.BASE_URL}/")
        print(response.json())
        
    def test_predict(self):
        text_list = [
            "好奇心钻装纸尿裤L40片9-14kg",
            "240ML*15养元2430六个核桃",
            "911-267遥控车",
            "潘婷丝质顺滑洗发露750ml",
            "640G正航牛奶早餐饼干",
            "小萨牛牛奥尔良鸡肉芝士船披萨90g*1袋",
            "美的电热水壶304不锈钢MK-SP50Colour201",
            "24色彩猴彩泥",
            "红妮丝光棉男圆短袖87207",
            "弟弟妹妹袜768",
            "吉曼贝德蒸蛋糕系列",
            "富帛莫代尔男秋裤",
        ]
        
        with Pool(processes=2) as pool:
            pool.map(func=self.__call_predict, iterable=text_list)
    
    @staticmethod
    def __call_predict(text: str):
        uri = "/predict"
        title = Title(text=text)
        response = post(url=f"{WebTest.BASE_URL}{uri}", json=dict(title))
        
        # 根据你的需求处理响应
        if response.status_code == 200:
            category = response.json().get("category")
            print(f"{text} ==> {category}")
        else:
            print(f"请求失败，状态码 {response.status_code}")
