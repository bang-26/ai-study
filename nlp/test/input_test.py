#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp 
    FileName       ：  input_test 
    CreateTime     ：  2026-10-08 16:27:38 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6 
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase
from torch import tensor, randint
from input_method import RawDataProcessor, InputMethodConfig, InputMethodDataset
from input_method import InputMethodModel, InputMethodTrainer, InputMethodPredictor, InputMethodTester


config = InputMethodConfig()


class RawDataTest(TestCase):
    raw_data_processor = RawDataProcessor(config=config)
    
    def test_load_data(self):
        train_data, test_data = self.raw_data_processor.load_data(sample_factor=0.1)
        print(f"Train data size: {len(train_data)}")
        print(train_data[0])
        print(f"Test data size: {len(test_data)}")
        print(test_data[0])
        return train_data, test_data
    
    def test_build_vocab(self):
        train_data, _ = self.test_load_data()
        self.raw_data_processor.build_vocab(sentence_list=train_data)
        print(f"Vocabulary size: {len(self.raw_data_processor.word_id_dict)}")
        print(f"Word ID mapping: {list(self.raw_data_processor.word_id_dict.items())[:10]}")
    
    def test_save_vocab(self):
        self.test_build_vocab()
        self.raw_data_processor.save_vocab()
    
    def test_load_vocab(self):
        self.raw_data_processor.load_vocab()
        print(f"Vocabulary size: {len(self.raw_data_processor.word_id_dict)}")
        
    def test_build_dataset(self):
        train_data, test_data = self.test_load_data()
        self.test_load_vocab()
        
        self.raw_data_processor.build_dataset(sentence_list=train_data, save_path=config.TRAIN_PATH)
        self.raw_data_processor.build_dataset(sentence_list=test_data, save_path=config.TEST_PATH)
        
    def test_dataloader(self):
        train_dataloader = self.raw_data_processor.build_dataloader(data_path=config.TRAIN_PATH)
        test_dataloader = self.raw_data_processor.build_dataloader(data_path=config.TEST_PATH)
        
        for batch in train_dataloader:
            print(f"Batch: {batch}")
            break
        
        for batch in test_dataloader:
            print(f"Batch: {batch}")
            break


class DatasetTest(TestCase):
    train_path = InputMethodConfig.TRAIN_PATH

    def test_dataset(self):
        dataset = InputMethodDataset(data_path=self.train_path)
        print(f"Dataset size: {len(dataset)}")
        print(dataset[0])


class InputMethodModelTest(TestCase):
    vocab_size = 100
    model = InputMethodModel(config=config, vocab_size=vocab_size)

    def test_model(self):
        inputs = randint(self.vocab_size, (config.BATCH_SIZE, config.VECTOR_LENGTH))
        outputs = self.model.forward(inputs)

        self.assertEqual(first=outputs.shape, second=(config.BATCH_SIZE, self.vocab_size))
        print(f"Outputs shape: {outputs[0]}")


class InputMethodTrainerTest(TestCase):
    data_processor = RawDataProcessor(config=config)
    
    def test_trainer(self):
        self.data_processor.load_vocab()
        model = InputMethodModel(config=config, vocab_size=self.data_processor.vocab_length)
        
        train_loader = self.data_processor.build_dataloader(data_path=config.TRAIN_PATH)

        trainer = InputMethodTrainer(model=model, config=config)
        
        loss_list = trainer.train(train_loader=train_loader)
        print(f"Loss list: {loss_list}")


class InputMethodPredictTest(TestCase):
    raw_data_processor = RawDataProcessor(config=config)
    raw_data_processor.load_vocab()
    
    model = InputMethodModel(config=config, vocab_size=raw_data_processor.vocab_length)
    predictor = InputMethodPredictor(model=model, tokenizer=raw_data_processor)
    
    def test_predict(self):
        text_list = ["今天天气", "我想吃苹果", "你喜欢看电", "明天有空", "请问最近的地铁站"]
        predicted_words_list = self.predictor.predict(text_list=text_list)
        
        for predicted_words in predicted_words_list:
            print(f"Predicted Words: {predicted_words}")
            
    def test_input(self):
        self.predictor.input_predict()


class InputMethodTesterTest(TestCase):
    raw_data_processor = RawDataProcessor(config=config)
    raw_data_processor.load_vocab()
    
    model = InputMethodModel(config=config, vocab_size=raw_data_processor.vocab_length)
    tester = InputMethodTester(config=config, model=model)
    
    def test_test(self):
        test_loader = self.raw_data_processor.build_dataloader(data_path=config.TEST_PATH)
        avg1, avg5 = self.tester.test(test_loader=test_loader, top_k=5)
        print(f"Average accuracy@1: {avg1}, Average accuracy@5: {avg5}")

