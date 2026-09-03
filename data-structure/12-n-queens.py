#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  12-n-queens 
    CreateTime     ：  2026-08-31 12:33:31 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


def n_queens(n):
    result = []
    cols = set()  # 记录哪些列有皇后
    diag1 = set()  # 记录哪些主对角线上有皇后
    diag2 = set()  # 记录哪些副对角线上有皇后
    
    # 初始化棋盘
    board = [["." for _ in range(n)] for _ in range(n)]
    
    def backtrack(row):
        # 如果已经放置了n个皇后，说明找到一个解
        if row == n:
            result.append(["".join(row) for row in board])
            return
        
        for col in range(n):
            # 检查当前列和对角线是否有皇后
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue  # 如果有冲突，跳过当前列
            
            # 放置皇后
            board[row][col] = "Q"
            # 标记当前列和对角线
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # 递归处理下一行
            backtrack(row + 1)
            
            # 回溯，删除当前位置的皇后，并清理列和对角线的标记
            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return result
