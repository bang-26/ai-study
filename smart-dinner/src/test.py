#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner 
    FileName       ：  test 
    CreateTime     ：  2026-07-18 11:22:40 
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


class DinnerTest(TestCase):
    base_url = "127.0.0.1:8000"
    
    def test_healthy(self):
        response = post(url=f"{self.base_url}/chat", json={"query": "北京清华大学能到吗？"})
        print(response)
