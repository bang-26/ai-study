#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill  
    FileName       ：  test 
    CreateTime     ：  2026-07-26 20:58:03 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from unittest import TestCase
from json import dumps
from requests import post


class BillTest(TestCase):
    BASE_URL = "http://127.0.0.1:8000"
    
    def test_query(self):
        url = f"{self.BASE_URL}/api/query"
        data = {"query": "查询 2023 年 1 月 1 日至 2023 年 1 月 31 日的账单"}
        
        response = post(url=url, json=data)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.text
            
        data_json = dumps(obj=data, indent=4, ensure_ascii=False)
        print(data_json)
        
