#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  parser 
    CreateTime     ：  2026-07-17 22:43:39 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


# SQL 解析类
class SqlParser:
    def __init__(self, path: str):
        self.path = path
        self.sql_dict = None
    
    def reader(self):
        self.sql_dict = {}
        with open(file=self.path, mode="r", encoding="utf-8") as fr:
            content_list = fr.readlines()
            
        key = ""
        sql = ""
        for content in content_list:
            if content and not content.startswith("--"):
                if content.startswith("#"):
                    key = content.split("#")[-1].strip()
                else:
                    sql = sql + content
                    if content.strip().endswith(";"):
                        self.sql_dict[key] = sql.strip()
                        sql = ""
    
    def get_sql(self, key: str):
        if self.sql_dict is None:
            self.reader()
        
        sql = self.sql_dict.get(key, "")
        return sql
        

class PromptParser:
    def __init__(self, path: str):
        self.path = path
        self.prompt_dict = None
    
    def reader(self):
        self.prompt_dict = {}
        with open(file=self.path, mode="r", encoding="utf-8") as fr:
            content_list = fr.readlines()
        
        key = ""
        value = ""
        for content in content_list:
            if content.strip().startswith("--"):
                if key:
                    self.prompt_dict[key] = value
                    value = ""
                key = content.split("--")[-1].strip()
            else:
                value = value + content
        
        if value:
            self.prompt_dict[key] = value
    
    def get_prompt(self, key: str):
        if self.prompt_dict is None:
            self.reader()
        
        prompt = self.prompt_dict.get(key, "")
        return prompt


if __name__ == '__main__':
    # parser = SqlParser(path="../data/dinner.sql")
    # sql = parser.get_sql("get_menu_items")
    # print(sql)

    parser = PromptParser(path="../data/prompt.txt")
    
    for key in ["customer-service", "consultant", "test"]:
        prompt = parser.get_prompt(key=key)
        print(f"{key} {'=' * 100}> \n{prompt}")
    
    
