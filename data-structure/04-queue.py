#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  04-queue 
    CreateTime     ：  2026-08-31 10:38:28 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        """初始化队列"""
        self.__head = None
        self.__tail = None
        self.__size = 0
    
    @property
    def size(self):
        """获取队列元素个数"""
        return self.__size
    
    def is_empty(self):
        """判断队列是否为空"""
        return self.__size == 0
    
    def push(self, data):
        """入队"""
        node = Node(data)
        if self.is_empty():
            self.__head = node
            self.__tail = node
        else:
            self.__tail.next = node
            self.__tail = node
        self.__size += 1
    
    def pop(self):
        """ "出队"""
        if self.is_empty():
            raise Exception("队列为空")
        data = self.__head.data
        self.__head = self.__head.next
        self.__size -= 1
        return data
    
    def peek(self):
        """访问队首元素"""
        if self.is_empty():
            raise Exception("队列为空")
        return self.__head.data
