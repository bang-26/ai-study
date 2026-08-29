#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  json_test 
    CreateTime     ：  2026-07-25 16:46:21 
    Author         ：  issac  
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""


from unittest import TestCase
from json import loads, dumps


class TestJson(TestCase):
    def test_json(self):
        with open(file="test.json", mode="r", encoding="utf-8") as f:
            content = loads(s=f.read())
        
        data_string = dumps(obj=content, indent=4, ensure_ascii=False)
        print(data_string)
