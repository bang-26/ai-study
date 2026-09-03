#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  14-candy 
    CreateTime     ：  2026-08-31 12:34:45 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


def candy1(ratings):
    n = len(ratings)
    
    # 每个孩子先分发1个糖果
    candy_num = [1] * len(ratings)
    
    # 从左向右遍历，如果右边评分更高，则右边孩子的糖果数改为左边孩子的糖果数+1
    for pos in range(n - 1):
        if ratings[pos] < ratings[pos + 1]:
            candy_num[pos + 1] = candy_num[pos] + 1
    
    # 从右向左遍历，如果左边评分更高，则左边孩子的糖果数改为右边孩子的糖果数+1
    total_candies = candy_num[-1]
    for pos in range(n - 2, -1, -1):
        if ratings[pos] > ratings[pos + 1]:
            if candy_num[pos] <= candy_num[pos + 1]:
                candy_num[pos] = candy_num[pos + 1] + 1
        total_candies += candy_num[pos]
    return total_candies


def candy2(ratings):
    # 每个孩子分发一个糖果
    result = len(ratings)
    # 上升区长度
    up_length = 0
    # 上升区长度的记录
    up_num = 0
    # 下降区长度
    down_length = 0
    for i in range(1, len(ratings)):
        # 如果处于上升区
        if ratings[i] > ratings[i - 1]:
            # 上升区长度+1，清空下降区长度，并在result中累加糖果数
            up_length += 1
            up_num = up_length
            down_length = 0
            result += up_length
        # 如果处于下降区
        elif ratings[i] < ratings[i - 1]:
            # 如果上升区长度为0，说明前一个位置已经不在上升区内，下降区长度+1
            if up_length == 0:
                down_length += 1
            # 如果下降区长度已经等于之前上升区长度,说明峰值的糖果数由下降区决定，下降区长度+1
            if down_length == up_num:
                down_length += 1
            # 清空上升区长度
            up_length = 0
            result += down_length
        # 如果处于平缓区
        else:
            # 清空所有记录
            up_length = 0
            down_length = 0
            up_num = 0
    return result
