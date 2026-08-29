#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  tool 
    CreateTime     ：  2026-08-09 16:05:50 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Annotated, Optional, Union
from langchain_core.tools import tool

from context import context
from connect import mysql_connect, tavily_connect, rag_flow_connect
from logger import logger
from monitor import monitor_service
from util import FileUtil, TransformUtil


# =================================== tavily ===================================
# 根据用户问题，进行网络信息搜索
@tool
def internet_search(query: str):
    """
    根据用户问题，检索互联网上的公开信息。
        
        本工具仅用于收集公开的网络资讯（如行业动态、背景知识、外部数据）。
        当用户问题指定查询数据库或 RAGFlow 内部知识库时，请使用对应的专用工具，
        切勿使用本工具进行检索。
    
    Args:
        query: 用户的查询问题，应包含具体、明确的关键词，如"2025年空调行业市场规模"。
        
    Returns:
        dict: 网络搜索结果，包含每条结果的标题、链接、摘要等信息.
    """
    
    topic = tavily_connect.topic
    max_results = tavily_connect.max_results
    include_raw_content = tavily_connect.include_raw_content
    args = \
        {
            "query"              : query,
            "topic"              : topic,
            "max_results"        : max_results,
            "include_raw_content": include_raw_content
        }
    
    # 每次调用工具，都会向前端推进调用进度：参数1： 工具的名字  参数2： 调用工具的参数信息
    monitor_service.report_tool(tool_name="网络搜索工具", args=args)
    response = tavily_connect.search(query=query)
    return response
    

# ================================== ragflow ===================================
# 1. 查询现在知识库中有哪些聊天助手和对应知识库的信息
@tool
def get_assistant_list() -> str:
    """
    查询 ragflow 服务器中可用的聊天助手及其关联的知识库信息。
        
        用途：为模型提供 ragflow 内部可用的助手清单（助手名称、功能介绍及关联知识库），
        供模型判断应从哪个助手获取对应的内部文档信息。
        
        使用边界：
            - 在调用 create_ask_delete 向某个助手提问之前，必须先调用本工具确认助手的准确名称；
            - 本工具仅用于查询助手与知识库的列表信息，不回答具体问题。

    Returns:
        str: 查询结果，格式说明如下：
            - 有可用助手 -> "助手名称:<名称>;功能介绍:<描述>; 关联的知识库：<知识库1>、<知识库2>..."
            - 没有可用助手 -> "没有任何可用助手"
            - 查询异常 -> "查询助手信息异常，无可用助手,异常信息:<异常信息>"
    """
    
    monitor_service.report_tool(tool_name="ragflow 聊天助手列表查询工具：get_assistant_list")
    
    response = rag_flow_connect.get_assistant_knowledge()
    if response:
        name_list = [name for _, name in response.items()]
        assistant = rag_flow_connect.get_assistant()
        
        result = f"助手名称:{assistant.name};功能介绍：{assistant.description};关联的知识库：{'、'.join(name_list)} \n"
        return result
    else:
        return "没有任何可用助手"

    
# 2. 对某个助手进行提问
@tool
def create_ask_delete(assistant_name: str, question: str) -> str:
    """
    向 ragflow 中的指定助手发起单次会话提问，提问结束后自动关闭会话。
        
        用途：用于查询 ragflow 内部知识库中与用户问题相关的信息。
        
        使用边界：
            - 调用本工具之前，必须先调用 get_assistant_list 确认助手的准确名称及可用性；
            - 本工具仅用于 ragflow 内部知识库的检索，不得用于网络信息搜索或数据库查询。
            
    Args:
        assistant_name: 助手的名称，必须与 get_assistant_list 返回结果中的助手名称完全一致。
        question: 本次要向该助手提出的问题。
        
    Returns:
        str: 助手对该问题的回答内容；提问失败时返回"提问失败，错误原因：<异常信息>"。
    """
    
    monitor_service.report_tool(tool_name="ragflow 提问助手工具：create_ask_delete",
                                args={"assistant_name": assistant_name, "question": question})
    
    response = rag_flow_connect.session_chat(assistant_name=assistant_name, question=question)
    if response:
        return response
    else:
        return "提问失败，错误原因：无返回结果"
    

# ===================================== db =====================================
# 查询当前库中所有可用的表
@tool
def list_sql_tables(query: str) -> str:
    """
    列出当前数据库中所有可用的表。

        作用：让模型识别数据库中有哪些表，为后续自定义 SQL 查询提供表名校验依据。
        在执行自定义 SQL 查询（execute_sql_query）之前，必须先调用本工具确认表名。

        Returns:
            str: 可用的表名列表，以逗号分隔，如"可用的表有：表1,表2,表3"；
                 无可用表时返回"没有可用的表"；
                 查询异常时返回"查询出现异常：<异常信息>"。
    """
    
    # 埋点,调用工具了告诉前端哪个工具被调用了！！
    monitor_service.report_tool(tool_name="数据库表数据查询工具：execute_sql_query", args={"query": query})
    sql = "show tables"
    table_dict_list = mysql_connect.query_data(query=sql)
    
    if table_dict_list:
        table_list = []
        for table_dict in table_dict_list:
            for table in table_dict.values():
                table_list.append(table)
            
        result = "可用的表有：" + ",".join(table_list)
        logger.info(f"查询结果：{result}")
    else:
        result = "没有可用的表"
    
    return result


# 查询指定表名的数据
@tool
def get_table_data(table_name: str) -> Union[list[dict[str, any]], str]:
    """
    查询指定表名的数据。
        
        本工具的作用：1. 完成单表数据的查询；2. 为多表查询提供表结构信息（列名与数据格式）。
        调用本工具之前，必须先调用 list_sql_tables 完成表名的校验。
        
    Args:
        table_name: 需要查询数据的表名。
         
    Returns:
        Union[list[dict[str, any]], str]: 查询到结果，以 JSON 列表格式返回的表数据，否则返回查询为空的信息；格式说明如下：
            - [ {字段1:值1, 字段2:값2, ...}, {字段1:값1, 字段2:값2, ...} ]；
            - 最多返回 100 条数据；
            - 没有数据时返回"数据表：表名 为空没有数据！"；
        示例：
            - [{"id": 1, "name": "张三", "age": 18}], [{"id": 2, "name": "李四", "age": 20}]；
            - 数据表：aaa 为空没有数据！；
    """

    sql = "select * from %s limit 100 " % table_name
    result = mysql_connect.query_data(query=sql)
    logger.info(f"获取表数据：{table_name}")
    
    if result:
        return result
    else:
        return f"数据表：{table_name}为空没有数据！"
    

# 执行自定义 SQL 查询语句
@tool
def execute_sql_query(query) -> Union[list[dict[str, any]], str]:
    """
    执行自定义 SQL 查询语句
        - 重要：执行之前，必须先调用 list_sql_tables 明确表名，再调用 get_table_data
        - 明确表结构和数据格式，确保 SQL 语句准确无误。
    
    Args:
        query: 要执行的自定义 SQL 语句。

    Returns:
        Union[list[dict[str, any]], str]: 查询到结果，以 JSON 列表格式返回的表数据，否则返回查询为信息；格式说明如下：
            - [ {字段1: 值1, 字段2: 值2, ...}, {字段1: 值1, 字段2: 값2, ...} ]；
            - 最多返回 100 条数据；
            - 没有数据时返回"数据表：表名 为空没有数据！"；
        示例：
            - [{"id": 1, "name": "张三", "age": 18}], [{"id": 2, "name": "李四", "age": 20}]；
            - 执行自定义SQL语句查询没有结果，sql为：select * from aaa！
    """
    result = mysql_connect.query_data(query=query)
    logger.info(f"执行 SQL 查询：{query}")
    
    if result:
        return result
    else:
        return f"执行自定义SQL语句查询没有结果，sql为：{query}！"
    

# =================================== main ===================================
@tool
def read_file_content(filename: Annotated[str, "要读取的文件名或路径（支持 .md, .doc, .docx, .pdf, .xlsx, .xls）"],
                      instruction: Annotated[str, "对提取内容的具体指令（例如：'提取摘要', '统计数据'）"] = "提取全部内容") -> str:
    """
    读取指定文件的内容。
        
        用途：读取会话目录下用户上传或生成的文件，获取其中的文本信息用于后续处理。
        支持格式：Markdown(.md)、Word(.doc/.docx)、PDF(.pdf)、Excel(.xlsx/.xls)；
        对于 Excel 文件，会自动附带数据统计信息（前 5 行预览与 describe 统计描述）。
        
        使用边界：
            - 仅用于读取已存在的文件，不修改文件内容；
            - 当文件不存在或不支持的格式时，返回对应的错误提示。
            
    Args:
        filename: 要读取的文件名或路径，支持 .md、.docx、.pdf、.xlsx、.xls 格式。
        instruction: 对提取内容的具体指令，如"提取摘要"、"统计数据"（默认"提取全部内容"）。
        
    Returns:
        str: 文件的文本内容；Excel 文件额外返回数据统计信息；
             文件不存在或读取失败时返回"错误：不支持的文件格式，且无法作为文本读取"。
    """
    
    monitor_service.report_tool(tool_name="文件内容读取工具", args={"filename": filename, "instruction": instruction})
    
    session_dir = context.get_session_context()
    FileUtil.ensure_dir_exists(file_path=session_dir)
    suffix = FileUtil.get_file_suffix(file_path=filename)
    
    if suffix in ['.doc', '.docx']:
        file_data = FileUtil.read_docx(file_path=filename)
    elif suffix in ['.xlsx', '.xls']:
        file_data = FileUtil.read_excel(file_path=filename)
    elif suffix == '.pdf':
        file_data = FileUtil.read_pdf(file_path=filename)
    else:
        file_data = FileUtil.read_text(file_path=filename)
    
    if file_data:
        return file_data
    else:
        return f"错误：不支持的文件格式，且无法作为文本读取"


@tool
def generate_markdown(content: Annotated[str, "要写入Markdown文档的文本内容"],
                      filename: Annotated[str, "Markdown文档的文件名（不包含扩展名或包含.md）"],
                      path: Annotated[str, "文件保存的绝对路径"] = "") -> None:
    """
    根据提供的文本内容，生成对应的 Markdown(.md) 文件。
        
        用途：将模型生成的报告、总结等内容保存为 Markdown 文件，便于后续阅读或转 PDF。
    
        使用边界：
            - 当用户要求输出文件并明确需要 Markdown 格式时，使用本工具；
            - 若需要 PDF 文件，应先用本工具生成 .md，再调用 convert_md_to_pdf 进行转换。
        
    Args:
        content: 要写入 Markdown 文档的文本内容，支持 Markdown 语法。
        filename: 文件名，可不含扩展名（自动补 .md），也可直接传入包含 .md 后缀的名称。
        path: 文件保存的绝对路径（可选，默认空时按默认目录规则解析）。

    Returns:
        str: 生成成功返回文件保存路径信息；生成失败返回"生成Markdown文件失败: <异常信息>"。
    """
    
    monitor_service.report_tool(tool_name="Markdown文档生成工具", args={"写入的文本内容": content})
    
    if not filename.endswith('.md'):
        filename += '.md'
    
    FileUtil.ensure_dir_exists(file_path=path)
    file_path = f"{path}/{filename}"
    
    logger.debug(f"[MarkdownTool] Debug: file_path = {file_path}")
    FileUtil.write_text(file_path=file_path, content=content)
    

@tool
def convert_md_to_pdf(md_filename: Annotated[str, "要转换的Markdown文档路径（包含.md后缀）"],
                      pdf_filename: Annotated[Optional[str], "输出的PDF文件路径（可选，默认与源文件同名）"] = None) -> str:
    """
     将 Markdown 文档转换为 PDF 文件（基于 Word 引擎）。

     用途：把已生成的 .md 文件转换为 PDF 格式，供最终交付或分享使用。

     使用边界：
         - 调用本工具之前，必须先通过 generate_markdown 生成源 .md 文件，并确保文件存在；
         - 本工具仅负责 Markdown 转 PDF，不做内容生成与编辑。

     Args:
         md_filename: 要转换的 Markdown 文档路径，需包含 .md 后缀。
         pdf_filename: 输出的 PDF 文件路径（可选，默认与源文件同名，仅后缀不同）。

     Returns:
         str: 转换成功返回 PDF 文件路径信息；失败返回"转换失败: <异常信息>"或对应的错误提示。
     """
    
    monitor_service.report_tool(tool_name="Markdown 转 PD F工具")
    
    session_dir = context.get_session_context()
    
    if not md_filename.endswith('.md'):
        md_filename += '.md'
    md_filename = f"{session_dir}/{md_filename}"
    
    if not pdf_filename.endswith('.pdf'):
        pdf_filename += '.pdf'
    pdf_filename = f"{session_dir}/{pdf_filename}"
    
    message = TransformUtil.md_transform_word(md_path=md_filename, pdf_path=pdf_filename)
    return message


if __name__ == '__main__':
    
    # tables= list_sql_tables(query="")
    # datas = get_table_data(table_name="sales_records")
    # datas = dumps(datas, indent=4, ensure_ascii=False, default=str)
    # print(datas)
    
    # desc = get_assistant_list()
    # print(f"desc = {desc}")
    
    res = create_ask_delete(assistant_name="空调安装助手", question="如何安装电脑")
    print(res)
