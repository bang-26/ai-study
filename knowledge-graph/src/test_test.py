#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph 
    FileName       ：  teat 
    CreateTime     ：  2026-07-04 13:13:23 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6 
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from unittest import TestCase
from sentence_transformers import SentenceTransformer


class SentenceTransformersTest(TestCase):
    def test_sentence(self):
        sentences = ["This is an example sentence", "Each sentence is converted"]
        
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)
        print(embeddings)

