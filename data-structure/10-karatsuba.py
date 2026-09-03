#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  10-karatsuba 
    CreateTime     ：  2026-08-31 10:53:06 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


def karatsuba(x, y):
    """卡拉楚巴算法"""
    # 将 x 和 y 转换为字符串
    x_str, y_str = str(x), str(y)
    n = max(len(x_str), len(y_str))
    
    # 如果存在负数，将其转换为正数再调用 karatsuba
    if x_str[0] == "-":
        return -karatsuba(-x, y)
    if y_str[0] == "-":
        return -karatsuba(x, -y)
    
    # 如果只剩1位则返回乘积
    if n == 1:
        return x * y
    
    # 确保数字长度一致
    x_str = x_str.zfill(n)
    y_str = y_str.zfill(n)
    
    # 计算分割点
    m = n // 2
    
    # 将数字划分为高位部分和低位部分
    high1, low1 = int(x_str[:-m]), int(x_str[-m:])
    high2, low2 = int(y_str[:-m]), int(y_str[-m:])
    
    # 递归调用 karatsuba
    z0 = karatsuba(low1, low2)
    z1 = karatsuba(low1 + high1, low2 + high2)
    z2 = karatsuba(high1, high2)
    
    return pow(10, 2 * m) * z2 + pow(10, m) * (z1 - z2 - z0) + z0
