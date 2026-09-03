#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  11-permutations 
    CreateTime     ：  2026-08-31 12:32:59 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


def permute(nums):
    result = []
    
    def backtrack(start):
        # 到达末尾，将此时排列结果添加到最终结果中
        if start == len(nums):
            result.append(nums[:])
            return
        
        for i in range(start, len(nums)):
            # 选取当前位置的元素：将要选取的元素与此位置的元素互换
            if start != i:
                nums[start], nums[i] = nums[i], nums[start]
            # 递归处理下一个位置的元素
            backtrack(start + 1)
            # 回溯，恢复原始数组
            if start != i:
                nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result
