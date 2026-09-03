#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  03-stack 
    CreateTime     ：  2026-08-31 10:36:30 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


class Stack:
    def __init__(self):
        """初始化栈"""
        self.__size = 0
        self.__items = []
    
    @property
    def size(self):
        """获取栈元素个数"""
        return self.__size
    
    def is_empty(self):
        """判断栈是否为空"""
        return self.__size == 0
    
    def push(self, item):
        """入栈"""
        self.__items.append(item)
        self.__size += 1
    
    def pop(self):
        """出栈"""
        if self.is_empty():
            raise Exception("栈为空")
        item = self.__items[self.__size - 1]
        del self.__items[self.__size - 1]
        self.__size -= 1
        return item
    
    def peek(self):
        """访问栈顶元素"""
        if self.is_empty():
            raise Exception("栈为空")
        return self.__items[self.__size - 1]
