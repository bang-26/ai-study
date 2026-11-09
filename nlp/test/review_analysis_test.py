#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp 
    FileName       ：  review_analysis_test 
    CreateTime     ：  2026-10-13 09:36:31 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6 
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from torch import randint
from review_analysis import ReviewAnalysisConfig, ReviewAnalysisProcess, ReviewAnalysisTokenizer, ReviewAnalysisModel
from review_analysis import ReviewAnalysisTrainer, ReviewAnalysisPredictor


config = ReviewAnalysisConfig()


class TokenizerTest(TestCase):
    tokenizer = ReviewAnalysisTokenizer(config=config)
    tokenizer.load_vocab()

    def test_tokenizer(self):
        text = "商品质量很好，服务很好"
        tokens = self.tokenizer.encode(text=text)
        print(tokens)


class ProcessTest(TestCase):
    tokenizer = ReviewAnalysisTokenizer(config=config)
    process = ReviewAnalysisProcess(config=config, tokenizer=tokenizer)
    
    def test_load_data(self):
        train_df, test_df = self.process.load_data()
        
        print(f"Train DataFrame Shape: {train_df.shape}")
        # print(train_df.head())
        print(f"Test DataFrame Shape: {test_df.shape}")
        # print(test_df.head())
        
        return train_df, test_df
        
    def test_build_vocab(self):
        train_df, _ = self.test_load_data()
        self.process.build_vocab(data_df=train_df)
        
    def test_build_dataset(self):
        train_df, test_df = self.test_load_data()
        
        self.process.build_dataset(data_df=train_df, save_path=config.TRAIN_PATH)
        self.process.build_dataset(data_df=test_df, save_path=config.TEST_PATH)
        
    def test_build_dataloader(self):
        dataloader = self.process.build_dataloader(data_path=config.TRAIN_PATH)
        
        for label, review in dataloader:
            print(label.shape, review.shape)
            print(label, review)
            break
    
    
class ModelTest(TestCase):
    vocab_size = 128
    model = ReviewAnalysisModel(config=config, vocab_size=vocab_size)
    
    def test_model(self):
        input_tensor = randint(self.vocab_size, (1024, 10))
        output_tensor = self.model.forward(input_tensor)
        print(output_tensor.shape)


class TrainerTest(TestCase):
    tokenizer = ReviewAnalysisTokenizer(config=config)
    tokenizer.load_vocab()
    
    process = ReviewAnalysisProcess(config=config, tokenizer=tokenizer)
    model = ReviewAnalysisModel(config=config, vocab_size=tokenizer.vocab_length)
    trainer = ReviewAnalysisTrainer(config=config, model=model)
    
    def test_param(self):
        f = self.trainer.loss_function
        print(f)
        
    def test_trainer(self):
        train_loader = self.process.build_dataloader(data_path=config.TRAIN_PATH)
        loss_list = self.trainer.train(train_loader=train_loader)
        print(loss_list)
        
        
class PredictorTest(TestCase):
    tokenizer = ReviewAnalysisTokenizer(config=config)
    tokenizer.load_vocab()

    process = ReviewAnalysisProcess(config=config, tokenizer=tokenizer)
    model = ReviewAnalysisModel(config=config, vocab_size=tokenizer.vocab_length)
    model.load_model()
    
    predictor = ReviewAnalysisPredictor(model=model, tokenizer=tokenizer)
    
    def test_predict(self):
        review_list = ["商品质量很好，服务很好", "商品质量很差，服务也不好", "商品质量很差，但服务很好", "商品质量很好，但服务一般"]
        
        label_list = self.predictor.predict(text_list=review_list)
        for review, label in zip(review_list, label_list):
            print(f"{review} ==> {label}")

    def test_input(self):
        self.predictor.input_predict()
