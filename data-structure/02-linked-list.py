#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  02-linked-list 
    CreateTime     ：  2026-08-31 10:34:41 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        """初始化链表"""
        self.__head = None
        self.__size = 0
    
    def __str__(self):
        """打印链表"""
        result = []
        current = self.__head
        while current:
            result.append(str(current.data))
            current = current.next
        return " -> ".join(result)
    
    @property
    def size(self):
        """获取链表元素个数"""
        return self.__size
    
    def is_empty(self):
        """判断链表是否为空"""
        return self.__size == 0
    
    def insert(self, index, item):
        """插入元素"""
        if index < 0 or index > self.__size:
            raise IndexError
        if index == 0:
            # 插入到头部，需要新建一个节点，然后让新节点的next指向原来的head，然后让head指向新节点
            self.__head = Node(item, self.__head)
        else:
            # 插入到中间，先找到index-1位置的节点
            node = self.__head
            for i in range(index - 1):
                node = node.next
            # 新节点的next指向index位置的节点，然后让index-1位置的节点的next指向新节点
            node.next = Node(item, node.next)
        self.__size += 1
    
    def append(self, item):
        """末尾插入元素"""
        self.insert(self.__size, item)
    
    def remove(self, index):
        """删除元素"""
        if index < 0 or index >= self.__size:
            raise IndexError
        if index == 0:
            self.__head = self.__head.next
        else:
            # 找到index-1位置的节点，然后让index-1位置的节点的next指向index位置的节点的next
            node = self.__head
            for i in range(index - 1):
                node = node.next
            node.next = node.next.next
        self.__size -= 1
    
    def set(self, index, item):
        """修改元素"""
        if index < 0 or index >= self.__size:
            raise IndexError
        node = self.__head
        for i in range(index):
            node = node.next
        node.data = item
    
    def get(self, index):
        """访问元素"""
        if index < 0 or index >= self.__size:
            raise IndexError
        node = self.__head
        for i in range(index):
            node = node.next
        return node.data
    
    def find(self, item):
        """查找元素"""
        node = self.__head
        while node:
            if node.data == item:
                return True
            node = node.next
        return False
    
    def for_each(self, func):
        """遍历链表"""
        node = self.__head
        while node:
            func(node)
            node = node.next
