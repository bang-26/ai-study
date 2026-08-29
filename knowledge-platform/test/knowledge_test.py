#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  knowledge 
    CreateTime     ：  2026-07-22 13:29:11 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from unittest import TestCase
from requests import post


class KnowledgeTest(TestCase):
    base_url = "http://127.0.0.1:8001"
    
    def test_crawler(self):
        url = f"{self.base_url}/crawler"
        params = {"max_no": 1}
        response = post(url=url, json=params)
        
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.text
        print(f"data = {data}")
    
    def test_query(self):
        url = f"{self.base_url}/query"
        params = {"question": "我的电脑蓝屏死机了"}
        response = post(url=url, json=params)
        
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.text
        print(f"data = {data}")
