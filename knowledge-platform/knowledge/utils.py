#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  utils 
    CreateTime     ：  2026-07-20 20:37:42 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import listdir
from os.path import exists, splitext, join, basename
from typing import List, Dict, Any
from re import sub, compile
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify
from config import DataDict


class FileReaderWriter:
    @staticmethod
    def read(self, path: str) -> str:
        with open(file=self.file_path, mode='r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write(file_path: str, content: str) -> None:
        with open(file=file_path, mode='w', encoding='utf-8') as f:
            f.write(content)
    
    # 清洗文件名中的非法字符
    @staticmethod
    def clean_filename(filename: str) -> str:
        if not filename:
            return "untitled"
        
        pattern = r'[\\/:*?"<>|]'
        result = sub(pattern=pattern, repl='-', string=filename)
        return result.strip()


# Html 格式解析器
class ParseHtmlUtil:
    def __init__(self, data_dict: DataDict):
        self.data_dict = data_dict
    
    # 解析 HTML
    def parse_html(self, html: dict[str, Any], knowledge_no: int = 1) -> str:
        # 1. 判断内容是否有
        if not html:
            return ""
        
        # 2.从 html 中取知识库编号
        items = [f"# 知识库 {knowledge_no}\n"]                          # 知识库的项
        
        # 3. 提取知识库的标题（必须要有）
        html_title = html.get('title', self.data_dict.HTML_TITLE)
        items.append(f"## 标题\n{html_title.strip()}\n")
        
        # 4. 提取摘要：比标题还具有代表性
        html_digest = html.get("digest", self.data_dict.HTML_DIGEST).strip()
        if html_digest:
            items.append(f"## 问题描述\n{html_digest.strip()}\n")
        
        # 5. 提取知识库的分类：主分类、子分类、问题分类
        first_topic_name = html.get("firstTopicName", self.data_dict.HTML_FIRST_TOPIC_NAME)
        sub_topic_name = html.get("subTopicName", self.data_dict.HTML_SUB_TOPIC_NAME)
        question_category_name = html.get("questionCategoryName", self.data_dict.HTML_QUESTION_CATEGORY_NAME)
        
        category_list = []
        if first_topic_name:
            category_list.append(f"主类别: {first_topic_name.strip()}")
        
        if sub_topic_name:
            category_list.append(f"子类别: {sub_topic_name.strip()}")
        
        if question_category_name:
            category_list.append(f"问题类别: {question_category_name}")
        
        if category_list:
            items.append(f"## 分类\n" + "\n".join(category_list) + "\n")
        
        # 6. 提取知识库关键词：打散 清洗 在组合（1.相似检索【原数据】可以根据关键词检索 2.提高召回率）
        html_key_words = html.get("keyWords", self.data_dict.HTML_KEY_WORDS)
        key_words_list = []
        if html_key_words:
            for key_world in html_key_words:
                key_world = key_world.strip()
                if key_world and isinstance(key_world, str):
                    temps = key_world.split(",")
                    key_words_list.extend([temp.strip() for temp in temps])
            
            if key_words_list:
                keywords = ", ".join(key_words_list)
                items.append(f"## 关键词\n{keywords}\n")
        
        # 7. 构建元信息（时效性、版本）
        create_time = html.get("createTime", "")
        version_no = html.get("versionNo", "")
        
        medata_data = []
        if create_time:
            medata_data.append(f"创建时间:{create_time.strip()}")
        
        if version_no:
            medata_data.append(f"版本:{version_no.strip()}")
        
        if medata_data:
            items.append(f"## 元信息\n" + "|".join(medata_data) + "\n")
        
        # 8. 构建内容（解决方案）
        html_content = html.get("content", self.data_dict.HTML_CONTENT)
        md_content = self.parse_content(content=html_content)
        items.append(f"## 解决方案\n{md_content}\n")
        
        # 2.8 构建标题作为知识库的注释（防止切块之后导致文档上下文丢失）
        items.append(f"<!-- 文档主题：{html_title} (知识库库编号: {knowledge_no}) -->")
        
        return "\n".join(items)
    
    # 转换为 markdown
    @staticmethod
    def parse_content(content: str) -> str:
        if not content:
            return ""
        
        # 1. 使用 BeautifulSoup 进行结构化清洗
        soup = BeautifulSoup(content, 'html.parser')
        
        # 2. 移除 script, style 标签
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        
        # 3. 移除特定广告或无用元素（扩展）
        for ad in soup.select('.mceNonEditable'):
            ad.decompose()
        
        # 4. 查找所有的加粗标签
        bold_tags = soup.find_all(['strong', 'b'])
        for tag in bold_tags:
            # 4.1 安全检查：如果标签在之前的循环中已经被合并（删除）了，跳过
            if not tag.parent:
                continue
                
            # 4.2 判断并获取下一个节点
            next_sibling = tag.next_sibling
            if next_sibling and isinstance(next_sibling, Tag) and next_sibling.name == tag.name:
                tag.extend(next_sibling.contents)                    # 将下一个标签的内容添加到当前标签中
                next_sibling.decompose()                             # 销毁下一个标签
        
        # 5. 将清洗后的 HTML 转为字符串
        cleaned_html = str(soup)
        
        # 6. 使用 markdownify 转换
        mark_down = markdownify(cleaned_html)
        return mark_down


# Markdown 文件工具
class MarkDownUtil:
    # 收集 Markdown 文件元数据
    @staticmethod
    def collect_metadata(folder_path: str) -> List[Dict[str, Any]]:
        metadata_list = []
        if not exists(path=folder_path):
            return metadata_list
        
        # 正则匹配文件名格式：编号-标题.md
        filename_pattern = compile(pattern=r'^(.+?)-(.*?)\.md$')
        
        for filename in listdir(folder_path):
            if filename.endswith('.md'):
                match = filename_pattern.match(filename)
                if match:
                    title = match.group(2).strip()
                else:
                    title = splitext(filename)[0].strip()
                
                metadata = { "path" : join(folder_path, filename), "title": title }
                metadata_list.append(metadata)
        return metadata_list
    
    # 提取标题
    @staticmethod
    def extract_title(file_path: str) -> str:
        filename = basename(p=file_path)
        filename_pattern = compile(pattern=r'^(.+?)-(.*?)\.md$')
        match = filename_pattern.match(filename)
        
        if match:
            return match.group(2).strip()                            # 提取正则分组的第2部分作为标题
        else:
            return splitext(filename)[0].strip()                     # 匹配失败则使用文件名（去后缀）
    
    # 将 ![描述](url) 替换为纯 url，每张图单独一行
    @staticmethod
    def clean_markdown_image(text: str) -> str:
        # 1. 匹配 Markdown 图片语法: ![任意文字](任意URL)
        pattern = r'!\$$[^$$]*\]\((https?://[^\s\)]+)\)'
        cleaned = sub(pattern=pattern, repl=MarkDownUtil.replace_function, string=text)
        
        # 清理多余空行
        result = sub(pattern=r'\n{3,}', repl='\n\n', string=cleaned).strip()
        return result
    
    @staticmethod
    def replace_function(match):
        url = match.group(1)
        return f"\n{url}\n"  # 每个链接前后加换行，保证独立一行


# 提示语解析器
class PromptParser:
    def __init__(self, path: str):
        self.path = path
        self.prompt_dict = None
    
    def reader(self, sep: str = "%%"):
        self.prompt_dict = {}
        with open(file=self.path, mode="r", encoding="utf-8") as fr:
            content_list = fr.readlines()
        
        key = ""
        value = ""
        for content in content_list:
            if content.strip().startswith(sep):
                if key:
                    self.prompt_dict[key] = value
                    value = ""
                key = content.split(sep)[1].strip().split()[0]
            else:
                value = value + content
        
        if value:
            self.prompt_dict[key] = value
    
    def get_prompt(self, key: str):
        if self.prompt_dict is None:
            self.reader()
        
        prompt = self.prompt_dict.get(key, "")
        return prompt


if __name__ == '__main__':
    parser = PromptParser(path="../data/prompt.txt")
    prompt = parser.get_prompt(key="knowledge")
    print(f"prompt = {prompt}")
