#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  product-classify  
    FileName       ：  test 
    CreateTime     ：  2026-06-24 23:34:07 
    Author         ：  issac  
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from multiprocess.pool import Pool
from requests import post
from product_classify import ProductDataProcess, ProductModel, Config
from web import Title


class ProductTest(TestCase):
    Config.BATCH_SIZE = 8
    Config.TRAIN_SELECT_NUMBER = 1000
    Config.VALID_SELECT_NUMBER = 100
    Config.TEST_SELECT_NUMBER = 1000
    Config.EPOCHS = 5
    Config.SAVE_STEP = 10
    Config.STOP_PATIENCE = 2
    
    def test_process(self):
        process = ProductDataProcess(data_path=Config.DATASET_PATH, label_path=Config.LABELS_PATH)
        process.process_data()
    
    def test_loader(self):
        process = ProductDataProcess(data_path=Config.DATASET_PATH, label_path=Config.LABELS_PATH)
        train_path = f"{Config.DATASET_PATH}/{Config.TRAIN_FLAG}"
        loader = process.get_dataloader(dataset_path=train_path)
        
        for batch in loader:
            for k, v in batch.items():
                print(f"{k} = {v}")
            break
    
    def test_trainer(self):
        model = ProductModel(data_path=Config.DATASET_PATH, model_path=Config.BERT_MODEL,
                               saved_model_path=Config.SAVED_MODEL_PATH, label_path=Config.LABELS_PATH,
                               check_point_path=Config.CHECK_POINT_DIR)
        model.train()
    
    def test_evaluator(self):
        model = ProductModel(data_path=Config.DATASET_PATH, model_path=Config.BERT_MODEL,
                               saved_model_path=Config.SAVED_MODEL_PATH, label_path=Config.LABELS_PATH,
                               check_point_path=Config.CHECK_POINT_DIR)
        metrics = model.test()
        print(f"metrics = {metrics}")
    
    def test_predict(self):
        model = ProductModel(data_path=Config.DATASET_PATH, model_path=Config.BERT_MODEL,
                               saved_model_path=Config.SAVED_MODEL_PATH, label_path=Config.LABELS_PATH,
                               check_point_path=Config.CHECK_POINT_DIR)
        content = "好奇心钻装纸尿裤L40片9-14kg"
        label = model.predict(texts=content)
        print(f"label = {label}")
    
        contents = ["240ML*15养元2430六个核桃", "911-267遥控车", "潘婷丝质顺滑洗发露750ml"]
        labels = model.predict(texts=contents)
        print(f"labels = {labels}")


def call_predict(text: str):
    uri = "/predict"
    title = Title(text=text)
    response = post(url=f"{WebTest.BASE_URL}{uri}", json=dict(title))
    # 根据你的需求处理响应
    if response.status_code == 200:
        category = response.json().get("category")
        print(f"{text} ==> {category}")
    else:
        print(f"{text} 请求失败，状态码 {response.status_code}")
        
        
class WebTest(TestCase):
    BASE_URL = "http://127.0.0.1:8080"
    
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
            pool.map(func=call_predict, iterable=text_list)
