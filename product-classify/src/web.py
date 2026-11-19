#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  product-classify  
    FileName       ：  web 
    CreateTime     ：  2026-06-24 21:33:01 
    Author         ：  Administrator
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

import uvicorn
from time import strftime, time_ns
from fastapi import FastAPI
from product_classify import Config, ProductPredictor
from pydantic import BaseModel


# 标题类
class Title(BaseModel):
    text: str


# 分类类
class Category(BaseModel):
    category: str
    

# 创建服务
app = FastAPI(description="产品分类接", version="1.0", title="产品分类接口")
model = ProductPredictor(config=Config())                  # 创建模型


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
@app.get(path="/", response_model=dict[str, str], summary="测试接口")
def hello() -> dict[str, str]:
    return {"hello": "world"}
    
    
# 预测接口
@app.post(path="/predict", response_model=Category, summary="预测接口")
def predict(title: Title) -> Category:
    category = get_predict(title=title)                    # 获取预测结果
    return category
    

if __name__ == '__main__':
    uvicorn.run(app="web:app", host="0.0.0.0", port=8080)
