#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-bill
    FileName       ：  utils 
    CreateTime     ：  2026-07-20 20:47:09 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from configs import PathConfig
from logger import logger


# SQL 解析类
class SqlParser:
    def __init__(self, path: str):
        self.path = path
        self.sql_dict = None
    
    # 读取 SQL 文件
    def reader(self):
        self.sql_dict = {}
        try:
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
            logger.info(f"SQL 解析完成: {len(self.sql_dict)}")
        except Exception as e:
            logger.error(f"SQL 解析失败: {e}")
    
    # 获取 SQL
    def get_sql(self, key: str):
        if self.sql_dict is None:
            self.reader()
        
        sql = self.sql_dict.get(key, "")
        logger.debug(f"获取 SQL: {sql}")
        return sql


# 提示语解析器
class PromptParser:
    def __init__(self, path: str):
        self.path = path
        self.prompt_dict = None
    
    def reader(self, sep: str = "%%"):
        self.prompt_dict = {}
        try:
            with open(file=self.path, mode="r", encoding="utf-8") as fr:
                content_list = fr.readlines()
            
            key = ""
            value = ""
            for content in content_list:
                if content.strip().startswith(sep):
                    if key:
                        self.prompt_dict[key] = value
                        value = ""
                    key = content.split(sep)[1].strip().split()[0]
                else:
                    value = value + content
            
            if value:
                self.prompt_dict[key] = value
            
            logger.info(f"提示语解析完成: {len(self.prompt_dict)}")
        except Exception as e:
            logger.error(f"提示语解析失败: {e}")
            
    def get_prompt(self, key: str):
        if self.prompt_dict is None:
            self.reader()
        
        prompt = self.prompt_dict.get(key, "")
        logger.debug(f"获取提示语: {key}")
        return prompt


if __name__ == '__main__':
    prompt_parser = PromptParser(path=PathConfig.PROMPT_PATH)
    prompt_parser.reader()
    # for key, value in prompt_parser.prompt_dict.items():
    #     print(f"=================== {key} =================== \n{value}")
    
    prompt = prompt_parser.get_prompt(key="correct-sql")
    print(prompt)
