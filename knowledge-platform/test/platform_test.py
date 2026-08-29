#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  platform_test 
    CreateTime     ：  2026-07-24 21:14:10 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from json import dumps
from unittest import TestCase
from requests import post


class PlatformTest(TestCase):
    base_url = "http://127.0.0.1:8000"
    
    def test_session(self):
        url = f"{self.base_url}/api/user_sessions"
        
        params = [{"user_id": "tom"}, {"user_id": "jerry"}]
        for param in params:
            response = post(url=url, json=param)
            
            if response.status_code == 200:
                data = response.json()
            else:
                data = response.text
                
            data_json = dumps(data, indent=4, ensure_ascii=False)
            print(f"==================== {param} ====================\n{data_json}")
    
