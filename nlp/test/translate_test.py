#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  translate_test 
    CreateTime     ：  2026-10-14 15:34:06 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from translate import TranslateConfig, EnglishTokenizer, ChineseTokenizer, TranslateDataProcess
from translate import TranslateModel, TranslateTransformer, TranslateTrainer, TranslatePredictor, TranslateTransformerTrainer


config = TranslateConfig()


class TokenizerTest(TestCase):
    en_tokenizer = EnglishTokenizer(config=config)
    cn_tokenizer = ChineseTokenizer(config=config)
    
    def test_tokenizer(self):
        print("中文词表大小：", self.cn_tokenizer.vocab_length)
        print("英文词表大小：", self.en_tokenizer.vocab_length)
        print("特殊符号UNK：", self.cn_tokenizer.unknown_token)
        print("特殊符号PAD ID：", self.en_tokenizer.pad_id)
        print("特殊符号START：", self.en_tokenizer.start_token)
        print("特殊符号END ID：", self.cn_tokenizer.end_id)
    
    def test_encode(self):
        print("中文编码：", self.cn_tokenizer.encode("自然语言处理"))
        print("英文编码：", self.en_tokenizer.encode("hello world!", mark=True))
    
    
class DataProcessTest(TestCase):
    process = TranslateDataProcess(config=config)
    en_tokenizer = EnglishTokenizer(config=config)
    zh_tokenizer = ChineseTokenizer(config=config)
    
    def test_load_data(self):
        train_df, test_df = self.process.load_data()
        print(train_df.head())
        print(test_df.head())
        
        return train_df, test_df
        
    def test_build_vocab(self):
        train_df, _ = self.test_load_data()
        self.process.build_vocab(data_frame=train_df, tokenizer=self.zh_tokenizer, is_zh=True)
        self.process.build_vocab(data_frame=train_df, tokenizer=self.en_tokenizer, is_zh=False)
        
    def test_build_dataset(self):
        train_df, test_df = self.test_load_data()
        
        self.process.build_dataset(data_frame=train_df, zh_tokenizer=self.zh_tokenizer,
                                   en_tokenizer=self.en_tokenizer, is_train=True)
        self.process.build_dataset(data_frame=test_df, zh_tokenizer=self.zh_tokenizer,
                                   en_tokenizer=self.en_tokenizer, is_train=False)
    
    def test_build_loader(self):
        train_loader = self.process.build_loader(data_path=config.TRAIN_PATH)
        for idx, batch_data in enumerate(train_loader):
            print(idx, batch_data)
            break
        
        test_loader = self.process.build_loader(data_path=config.TEST_PATH)
        for idx, batch_data in enumerate(test_loader):
            print(idx, batch_data)
            break


class ModelTest(TestCase):
    model = TranslateModel(config=config, en_vocab_size=7412, zh_vocab_size=2749)
    transform = TranslateTransformer(config=config, en_vocab_size=7412, zh_vocab_size=2749)
    
    def test_model(self):
        print(f"模型的编码器结构：{self.model.encoder}")
        print(f"模型的解码器结构：{self.model.decoder}")
    
    def test_transformer(self):
        print(f"Transformer 结构：{self.transform}")
    
        
class TrainerTest(TestCase):
    process = TranslateDataProcess(config=config)
    
    en_tokenizer = EnglishTokenizer(config=config)
    en_tokenizer.load_vocab(vocab_path=config.EN_VOCAB_PATH)
    
    zh_tokenizer = ChineseTokenizer(config=config)
    zh_tokenizer.load_vocab(vocab_path=config.ZH_VOCAB_PATH)
    
    model = TranslateModel(config=config, en_vocab_size=en_tokenizer.vocab_length, zh_vocab_size=zh_tokenizer.vocab_length)
    transform = TranslateTransformer(config=config, en_vocab_size=en_tokenizer.vocab_length, zh_vocab_size=zh_tokenizer.vocab_length)
    
    def test_model_train(self):
        train_loader = self.process.build_loader(data_path=config.TRAIN_PATH)
        
        trainer = TranslateTrainer(config=config, model=self.model)
        trainer.train(train_loader=train_loader)
    
    def test_transform_train(self):
        train_loader = self.process.build_loader(data_path=config.TRAIN_PATH)
        
        trainer = TranslateTransformerTrainer(config=config, model=self.transform)
        trainer.train(train_loader=train_loader)
        
        
class PredictorTest(TestCase):
    en_tokenizer = EnglishTokenizer(config=config)
    en_tokenizer.load_vocab(vocab_path=config.EN_VOCAB_PATH)
    
    zh_tokenizer = ChineseTokenizer(config=config)
    zh_tokenizer.load_vocab(vocab_path=config.ZH_VOCAB_PATH)
    
    model = TranslateModel(config=config, en_vocab_size=en_tokenizer.vocab_length, zh_vocab_size=zh_tokenizer.vocab_length)
    transform = TranslateTransformer(config=config, en_vocab_size=en_tokenizer.vocab_length,
                                     zh_vocab_size=zh_tokenizer.vocab_length)
    
    def test_predict(self):
        predictor = TranslatePredictor(model=self.model, config=config, en_tokenizer=self.en_tokenizer,
                                       zh_tokenizer=self.zh_tokenizer)
        print("预测结果：", predictor.predict(zh_text="你好，世界！"))
        
    def test_transform_predict(self):
        predictor = TranslatePredictor(model=self.transform, config=config, en_tokenizer=self.en_tokenizer,
                                       zh_tokenizer=self.zh_tokenizer)
        print("预测结果：", predictor.transform_predict(zh_text="我喜欢编程"))
