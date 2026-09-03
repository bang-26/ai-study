#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  01-array 
    CreateTime     ：  2026-08-31 10:32:49 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


class Array:
    def __init__(self):
        """初始化数组"""
        self.__capacity = 8
        self.__size = 0
        self.__items = [0] * self.__capacity
    
    def __str__(self):
        """打印数组"""
        arr_str = "["
        for i in range(self.__size):
            arr_str += str(self.__items[i])
            if i < self.__size - 1:
                arr_str += ", "
        arr_str += "]"
        return arr_str
    
    @property
    def size(self):
        """获取数组元素个数"""
        return self.__size
    
    def is_empty(self):
        """判断数组是否为空"""
        return self.__size == 0
    
    def __grow(self):
        """数组扩容"""
        self.new___items = [0] * self.__capacity * 2
        for i in range(self.__size):
            self.new___items[i] = self.__items[i]
        self.__items = self.new___items
        self.__capacity *= 2
    
    def insert(self, index, item):
        """插入元素"""
        if index < 0 or index > self.__size:
            raise IndexError
        if self.__size == self.__capacity:
            self.__grow()
        for i in range(self.__size, index, -1):
            self.__items[i] = self.__items[i - 1]
        self.__items[index] = item
        self.__size += 1
    
    def append(self, item):
        """末尾插入元素"""
        self.insert(self.__size, item)
    
    def remove(self, index):
        """删除元素"""
        if index < 0 or index >= self.__size:
            raise IndexError
        for i in range(index, self.__size - 1):
            self.__items[i] = self.__items[i + 1]
        self.__size -= 1
    
    def set(self, index, item):
        """修改元素"""
        if index < 0 or index >= self.__size:
            raise IndexError
        self.__items[index] = item
    
    def get(self, index):
        """访问元素"""
        if index < 0 or index >= self.__size:
            raise IndexError
        return self.__items[index]
    
    def find(self, item):
        """查找元素"""
        for i in range(self.__size):
            if self.__items[i] == item:
                return i
        return -1
    
    def for_each(self, func):
        """遍历数组"""
        for i in range(self.__size):
            func(self.__items[i])


if __name__ == '__main__':
    array = Array()
    
    
