#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  05-hash-table 
    CreateTime     ：  2026-08-31 10:39:03 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    
    def __init__(self):
        """初始化哈希表"""
        self.__capacity = 8  # 数组长度
        self.__size = 0  # 键值对个数
        self.__load_factor = 0.7  # 负载因子
        self.__table = [None] * self.__capacity
    
    def display(self):
        """显示哈希表内容"""
        for i, node in enumerate(self.__table):
            print(f"Index {i}: ", end="")
            current = node
            while current:
                print(f"({current.key}, {current.value}) -> ", end="")
                current = current.next
            print("None")
        print()
    
    def __hash(self, key):
        """哈希函数，根据key计算索引"""
        return hash(key) % self.__capacity
    
    def __grow(self):
        """哈希表负载因子超过阈值时进行扩容"""
        self.__capacity = self.__capacity * 2
        self.__table, old_table = [None] * self.__capacity, self.__table
        self.__size = 0
        
        # 将旧哈希表中的元素重新插入到新的哈希表中
        for node in old_table:
            current = node
            while current:
                self.put(current.key, current.value)
                current = current.next
    
    @property
    def size(self):
        """获取哈希表键值对个数"""
        return self.__size
    
    def is_empty(self):
        """判断哈希表是否为空"""
        return self.__size == 0
    
    def put(self, key, value):
        """插入键值对，处理哈希冲突"""
        # 如果负载因子超过阈值则进行扩容
        if self.__size / self.__capacity > self.__load_factor:
            self.__grow()
        
        index = self.__hash(key)
        new_node = Node(key, value)
        # 如果当前位置为空，直接插入
        if self.__table[index] is None:
            self.__table[index] = new_node
        else:
            # 否则，发生哈希冲突，链式存储
            current = self.__table[index]
            while current:
                # 如果键已经存在，更新值
                if current.key == key:
                    current.value = value
                    return
                if not current.next:
                    break
                current = current.next
            # 如果键不存在，插入到链表尾部
            current.next = new_node
        self.__size += 1
    
    def remove(self, key):
        """删除键值对"""
        index = self.__hash(key)
        current = self.__table[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    # 删除非头节点
                    prev.next = current.next
                else:
                    # 删除头节点
                    self.__table[index] = current.next
                self.__size -= 1
                return True
            prev = current
            current = current.next
        return False
    
    def get(self, key):
        """访问键值对"""
        index = self.__hash(key)
        current = self.__table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None
    
    def for_each(self, func):
        """遍历哈希表"""
        for node in self.__table:
            current = node
            while current:
                func(current.key, current.value)
                current = current.next
