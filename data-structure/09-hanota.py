#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  09-hanota
    CreateTime     ：  2026-08-31 10:51:49 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


def print_abc():
    """打印3个柱子"""
    print("a:", a)
    print("b:", b)
    print("c:", c)
    print()


def hanota(n, source, target, buffer):
    # 只有一个盘子时，直接从源柱子移动到目标柱子
    if n == 1:
        target.append(source.pop())
        return
    
    # 1. 将 n-1 个盘子从源柱子移动到缓冲柱子
    hanota(n - 1, source, buffer, target)
    print_abc()
    
    # 2. 将第 n 个盘子从源柱子移动到目标柱子
    hanota(1, source, target, buffer)
    print_abc()
    
    # 3. 将 n-1 个盘子从缓冲柱子移动到目标柱子
    hanota(n - 1, buffer, target, source)
    print_abc()


if __name__ == "__main__":
    n = 3
    a = list(range(n, 0, -1))
    b = []
    c = []
    hanota(n, a, c, b)
