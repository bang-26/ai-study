#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  test 
    CreateTime     ：  2026-08-31 10:54:17 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from unittest import TestCase


class FloorTest(TestCase):
    def climb1(self, n):
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return self.climb1(n - 1) + self.climb1(n - 2)
    
    def climb2(self, n):
        pre = 1
        cur = 1
        for _ in range(1, n):
            pre, cur = cur, pre + cur
        return cur
    
    def test_(self):
        self.assertEqual(self.climb1(1), 1)
        self.assertEqual(self.climb1(2), 2)
        self.assertEqual(self.climb1(3), 3)
        self.assertEqual(self.climb1(4), 5)
        self.assertEqual(self.climb1(5), 8)
        self.assertEqual(self.climb2(1), 1)
        self.assertEqual(self.climb2(2), 2)
        self.assertEqual(self.climb2(3), 3)
        self.assertEqual(self.climb2(4), 5)
        self.assertEqual(self.climb2(5), 8)


class MaxSubArrayTest(TestCase):
    def max_subarray(self, nums):
        result, f = nums[0], 0
        for i in nums:
            # 连续子数组之和若小于0，则中断连续
            if f < 0:
                f = 0
            # 累加连续子数组之和
            f += i
            # 更新最大值
            if result < f:
                result = f
        return result
    
    def test_(self):
        self.assertEqual(self.max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(self.max_subarray([1]), 1)
        self.assertEqual(self.max_subarray([5, 4, -1, 7, 8]), 23)


class ZeroOneTest(TestCase):
    def knapsack1(self, weights, values, W):
        n = len(weights)
        # 初始化二维数组dp，dp[i][j]表示前i个物品中，背包容量为j时的最大价值
        dp = [[0] * (W + 1) for _ in range(n)]
        
        # 每次增加一个可选物品，增加物品后遍历一次背包重量
        for i in range(n):
            for j in range(1, W + 1):
                # 如果当前物品放的进背包，进行比较
                if weights[i] <= j:
                    dp[i][j] = max(dp[i - 1][j], values[i] + dp[i - 1][j - weights[i]])
                # 如果当前物品放不进背包，使用上轮相同j的状态
                else:
                    dp[i][j] = dp[i - 1][j]
                
                print(f"前{i + 1}个物品，背包容量为{j}时")
                for row in range(len(dp)):
                    print(dp[row])
        
        return dp[n - 1][W]
    
    def knapsack2(self, weights, values, W):
        n = len(weights)
        dp = [0] * (W + 1)
        for i in range(n):
            for j in range(W, weights[i] - 1, -1):  # 从后往前遍历
                dp[j] = max(dp[j], values[i] + dp[j - weights[i]])
        return dp[W]
    
    def test_(self):
        self.assertEqual(self.knapsack1([1, 2, 3], [3, 2, 6], 3), 9)
        self.assertEqual(self.knapsack2([1, 2, 3], [3, 2, 6], 3), 9)


class FullTestBackpackTest(TestCase):
    def knapsack1(self, weights, values, W):
        n = len(weights)
        # 初始化二维数组dp，dp[i][j]表示前i个物品中，背包容量为j时的最大价值
        dp = [[0] * (W + 1) for _ in range(n)]
        
        # 每次增加一个可选物品，增加物品后遍历一次背包重量
        for i in range(n):
            for j in range(1, W + 1):
                # 如果当前物品放的进背包，进行比较
                if weights[i] <= j:
                    dp[i][j] = max(dp[i - 1][j], values[i] + dp[i][j - weights[i]])
                # 如果当前物品放不进背包，使用上轮相同j的状态
                else:
                    dp[i][j] = dp[i - 1][j]
                
                print(f"前{i + 1}个物品，背包容量为{j}时")
                for row in range(len(dp)):
                    print(dp[row])
        
        return dp[n - 1][W]
    
    def knapsack2(self, weights, values, W):
        n = len(weights)
        dp = [0] * (W + 1)
        
        for i in range(n):
            for j in range(weights[i], W + 1):
                dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
        
        return dp[W]
    
    def test_(self):
        self.assertEqual(self.knapsack1([1, 2, 3], [3, 7, 11], 3), 9)
        self.assertEqual(self.knapsack2([1, 2, 3], [3, 7, 11], 3), 9)
