#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  data-structure  
    FileName       ：  06-tree 
    CreateTime     ：  2026-08-31 10:40:44 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from collections import deque


class Node:
    """二叉树节点"""
    
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """二叉搜索树"""
    
    def __init__(self):
        """初始化二叉树"""
        self.__root = None
        self.__size = 0
    
    def print_tree(self):
        """打印树的结构"""
        
        # 先得到树的层数
        def get_layer(node):
            """递归计算树的层数"""
            if node is None:
                return 0
            else:
                left_depth = get_layer(node.left)
                right_depth = get_layer(node.right)
                return max(left_depth, right_depth) + 1
        
        layer = get_layer(self.__root)
        # 层序遍历并打印
        queue = deque([(self.__root, 1)])
        current_level = 1
        while queue:
            node, level = queue.popleft()
            if level > current_level:
                print()
                current_level += 1
            if node:
                print(f"{node.data:^{20 * layer // 2 ** (level - 1)}}", end="")
            else:
                print(f"{"N":^{20 * layer // 2 ** (level - 1)}}", end="")
            if level < layer:
                if node:
                    queue.append((node.left, level + 1))
                    queue.append((node.right, level + 1))
                else:
                    queue.append((None, level + 1))
                    queue.append((None, level + 1))
        print()
    
    @property
    def size(self):
        """返回树中节点的个数"""
        return self.__size
    
    def is_empty(self):
        """判断树是否为空"""
        return self.__size == 0
    
    def search(self, item):
        """查找节点是否存在"""
        return self.__search_pos(item)[0] is not None
    
    def __search_pos(self, item):
        """查找节点，返回(节点,父节点)。如果节点不存在则为None，此时父节点为一个叶节点"""
        parent = None
        current = self.__root
        while current:
            if item == current.data:
                break
            parent = current
            current = current.left if item < current.data else current.right
        return current, parent
    
    def add(self, item):
        """插入节点"""
        node = Node(item)
        if self.is_empty():
            self.__root = node
        else:
            current, parent = self.__search_pos(item)
            # 如果节点之前已存在则返回
            if current:
                return
            # 如果节点之前不存在，则插入父节点的左节点或右节点
            if parent.data > item:
                parent.left = node
            else:
                parent.right = node
        self.__size += 1
    
    def remove(self, item):
        """删除节点"""
        current, parent = self.__search_pos(item)
        if not current:
            return
        
        # 如果删除的是叶节点（没有子节点）
        if not current.left and not current.right:
            if parent:
                if parent.left == current:
                    parent.left = None
                else:
                    parent.right = None
            else:
                # 如果没有父节点，说明是根节点
                self.__root = None
        
        # 如果删除的节点只有一个子节点
        elif not current.left or not current.right:
            child = current.left if current.left else current.right
            if parent:
                if parent.left == current:
                    parent.left = child
                else:
                    parent.right = child
            else:
                # 如果没有父节点，说明是根节点
                self.__root = child
        
        # 如果删除的节点有两个子节点
        else:
            # 找到中序后继（右子树中最小的节点）
            successor = self.__get_min(current.right)
            successor_data = successor.data
            # 删除中序后继节点
            self.remove(successor_data)
            # 因为current知识把值替换，没有删除
            self.__size += 1
            # 用中序后继的值替代当前节点
            current.data = successor_data
        
        self.__size -= 1
    
    def __get_min(self, node):
        """找到当前子树的最小节点"""
        current = node
        while current.left:
            current = current.left
        return current
    
    def for_each(self, func, order="inorder"):
        """遍历树，默认中序遍历"""
        match order:
            case "inorder":
                self.__inorder_traversal(func)
            case "preorder":
                self.__preorder_traversal(func)
            case "postorder":
                self.__postorder_traversal(func)
            case "levelorder":
                self.__levelorder_traversal(func)
    
    def __inorder_traversal(self, func):
        """深度优先搜索：中序遍历"""
        
        def inorder(node):
            if node:
                inorder(node.left)
                func(node.data)
                inorder(node.right)
        
        inorder(self.__root)
    
    def __preorder_traversal(self, func):
        """深度优先搜索：前序遍历"""
        
        def preorder(node):
            if node:
                func(node.data)
                preorder(node.left)
                preorder(node.right)
        
        preorder(self.__root)
    
    def __postorder_traversal(self, func):
        """深度优先搜索：后序遍历"""
        
        def postorder(node):
            if node:
                postorder(node.left)
                postorder(node.right)
                func(node.data)
        
        postorder(self.__root)
    
    def __levelorder_traversal(self, func):
        """广度优先搜索：层序遍历"""
        queue = deque()
        queue.append(self.__root)
        while queue:
            node = queue.popleft()
            func(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


def front(node):
    """前序遍历"""
    if node is None:
        return
    print(node)  # 访问当前节点
    front(node.left)  # 访问节点的左子树
    front(node.right)  # 访问节点的右子树


def middle(node):
    """中序遍历"""
    if node is None:
        return
    front(node.left)  # 访问节点的左子树
    print(node)  # 访问当前节点
    front(node.right)  # 访问节点的右子树


def back(node):
    """后序遍历"""
    if node is None:
        return
    back(node.left)  # 访问节点的左子树
    back(node.right)  # 访问节点的右子树
    print(node)  # 访问当前节点
