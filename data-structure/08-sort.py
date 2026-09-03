#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  08-sort 
    CreateTime     ：  2026-08-31 10:47:28 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


# 冒泡排序
def bubble_sort(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]


# 选择排序
def select_sort(nums):
    for i in range(len(nums) - 1):
        min_index = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_index]:
                min_index = j
        nums[i], nums[min_index] = nums[min_index], nums[i]


# 插入排序
def insert_sort(nums):
    for i in range(1, len(nums)):
        for j in range(i, 0, -1):
            if nums[j] >= nums[j - 1]:
                break
            nums[j], nums[j - 1] = nums[j - 1], nums[j]


def __merge(left, right):
    """合并两个已排序的数组"""
    merged = []
    i = j = 0
    # 比较两个子数组的元素，按升序放入 merged 数组
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    # 将数组中剩余元素加入 merged
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# 归并排序
def merge_sort(arr):
    """归并排序"""
    # 数组长度为1时，不再分割
    if len(arr) <= 1:
        return arr
    # 分割数组
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # 合并已排序的子数组
    return __merge(left, right)


def __partition(nums, left, right):
    """选择基准并按基准划分"""
    pivot = nums[left]
    while left < right:
        while left < right and nums[right] >= pivot:
            right -= 1
        nums[left] = nums[right]
        while left < right and nums[left] <= pivot:
            left += 1
        nums[right] = nums[left]
    nums[left] = pivot
    return left


# 快速排序
def quick_sort(nums, left, right):
    """快速排序"""
    if left < right:
        mid = __partition(nums, left, right)
        quick_sort(nums, left, mid - 1)
        quick_sort(nums, mid + 1, right)


def __heapify(arr, n, i):
    """堆化"""
    largest = i  # 最大节点指向父节点
    left = 2 * i + 1  # 左子节点
    right = 2 * i + 2  # 右子节点
    
    # 如果左子节点大于父节点,最大节点指向左子节点
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # 如果右子节点大于当前最大节点，最大节点指向右子节点
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # 如果最大节点不是父节点，则交换并递归堆化
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        __heapify(arr, n, largest)


# 堆排序
def heap_sort(arr):
    """堆排序"""
    n = len(arr)
    # 构建大顶堆
    # n//2–1获取最后一个非叶子节点的索引
    # stop为不包含，所以意味着循环会一直执行到索引为 0 的节点
    for i in range(n // 2 - 1, -1, -1):
        __heapify(arr, n, i)
    # 依次将堆顶元素放在末尾，并重新堆化
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        __heapify(arr, i, 0)
    return arr

# arr = [12, 11, 13, 5, 6, 7]
# sorted_arr = heap_sort(arr)
# print("排序后的数组:", sorted_arr)
