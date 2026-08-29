#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  product-classify  
    FileName       ：  web 
    CreateTime     ：  2026-06-24 21:33:01 
    Author         ：  issac  
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import uvicorn
from os.path import abspath, dirname
from time import strftime, time_ns
from fastapi import FastAPI
from product_classify import ProductModel
from pydantic import BaseModel


# 标题类
class Title(BaseModel):
    text: str


# 分类类
class Category(BaseModel):
    category: str
    

# 配置类
class Config:
    # ============================== 参数路径 ==============================
    PYTHON_PATH = abspath(path=__file__)                             # 脚本路径
    PYTHON_DIR = dirname(p=PYTHON_PATH)                              # Python 文件所在目录
    PROJECT_DIR = abspath(path=f"{PYTHON_DIR}/../")                  # 项目路径
    
    VOCAB_PATH = "google-bert/bert-base-chinese"                     # 词表路径
    LABELS_PATH = abspath(path=f"{PROJECT_DIR}/data/labels.txt")     # 标签保存路径
    MODEL_PATH = f"{PROJECT_DIR}/models/couplet"                     # 模型保存路径


# 创建服务
app = FastAPI(module_name="web", description="产品分类接", version="1.0", title="产品分类接口")

# 创建模型
model = ProductModel(model_path=Config.VOCAB_PATH,         # 词表路径
                     saved_model_path=Config.MODEL_PATH,   # 模型保存路径
                     label_path=Config.LABELS_PATH)        # 标签保存路径


# 获取预测结果
def get_predict(title: Title) -> Category:
    start = time_ns()                                      # 开始时间
    texts = title.text                                     # 获取待预测文本
    predicts = model.predict(texts=texts)                  # 模型预测
    category = Category(category=predicts[0])              # 封装返回结果
    end = time_ns()                                        # 结束时间
    cost = round((end - start) / 1e6, 2)                   # 耗时
    print(f"{strftime('%Y-%m-%d %H:%M:%S')}-|-cost={cost}-|-title={title}ms-|-category={category}")
    return category


# 预测接口
@app.post("/predict")
def predict(title: Title) -> Category:
    category = get_predict(title=title)                    # 获取预测结果
    return category
    

if __name__ == '__main__':
    uvicorn.run(app="web:app", host="0.0.0.0", port=8080)
