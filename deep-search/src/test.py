#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  test 
    CreateTime     ：  2026-08-09 20:23:13 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from unittest import TestCase
from requests import get


class WebTest(TestCase):
    BASE_URL = "http://127.0.0.1:8000"
    
    def test_websocket(self):
        url = f"{self.BASE_URL}/ws"
        response = get(url=url)
        print(f"response = {response}")
