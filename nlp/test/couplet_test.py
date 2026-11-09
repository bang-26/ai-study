#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  couplet_test 
    CreateTime     ：  2026-06-24 16:57:10 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from couplet import CoupletConfig, CoupletDataProcessor, CoupletTrainer, CoupletPredictor


config = CoupletConfig()


class ProcessorTest(TestCase):
    processor = CoupletDataProcessor(config=config)
    
    def test_read(self):
        input_data = self.processor.read_data(text_path=self.processor.in_path)
        print(f"上联数据集前5条: {input_data[:5]}")
        print(f"上联数据集长度: {len(input_data)}")
        
        output_data = self.processor.read_data(text_path=self.processor.out_path)
        print(f"下联数据集前5条: {output_data[:5]}")
        print(f"下联数据集长度: {len(output_data)}")
        
    def test_process(self):
        self.processor.process()
        
    def test_loader(self):
        loader = self.processor.build_loader()
        
        for batch in loader:
            for key, value in batch.items():
                print(f"{key} = {value}")
            break
            
            
class TrainerTest(TestCase):
    processor = CoupletDataProcessor(config=config)
    trainer = CoupletTrainer(config=config)
    
    def test_train(self):
        loader = self.processor.build_loader()
        self.trainer.train(train_loader=loader)
        
        
class PredictorTest(TestCase):
    predictor = CoupletPredictor(config=config)
    
    def test_predict(self):
        out = self.predictor.predict(input_text="春风又绿江南岸")
        print(f"预测结果: {out}")
        
    def test_batch(self):
        self.predictor.predict_batch()
    
