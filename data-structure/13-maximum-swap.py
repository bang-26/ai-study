#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  13-maximum-swap 
    CreateTime     ：  2026-08-31 12:34:14 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

def maximum_swap(num):
    result = num
    num_list = list(str(num))
    max_index = -1  # 最大值的索引
    for i in range(len(num_list) - 1, -1, -1):
        # 当前值大于最大值时，更新最大值的索引
        if num_list[i] > num_list[max_index]:
            max_index = i
        # 当前值小于最大值时，交换，更新result，再交换回来
        else:
            num_list[i], num_list[max_index] = num_list[max_index], num_list[i]
            result = max(result, int("".join(num_list)))
            num_list[i], num_list[max_index] = num_list[max_index], num_list[i]
    return result
