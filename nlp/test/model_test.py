#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  nlp  
    FileName       ：  model_test 
    CreateTime     ：  2026-06-21 00:33:50 
    Author         ：  lihuashiyu
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
print(os.environ["HF_ENDPOINT"])

from transformers import AutoModel
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained("google-bert/bert-base-chinese")

if __name__ == '__main__':
    pass
