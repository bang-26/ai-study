#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search  
    FileName       ：  util 
    CreateTime     ：  2026-08-09 14:53:27 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import makedirs, walk, remove
from os.path import exists, join, dirname, isfile, basename, abspath, isdir
# from pythoncom import CoInitialize, CoUninitialize
import pythoncom
from win32com.client import Dispatch
from shutil import copyfileobj, copy2
from typing import BinaryIO, Dict, Optional, Any
from docx import Document
from pandas import read_excel
from pypdf import PdfReader
from yaml import safe_load
from markdown import markdown
from logger import logger


class FileUtil:
    # 获取文件名
    @staticmethod
    def get_file_name(file_path: str) -> str:
        file_path = file_path.lower()
        return basename(p=file_path)
        
    # 获取文件目录
    @staticmethod
    def get_file_dir(file_path: str) -> str:
        file_path = file_path.lower()
        is_exist = FileUtil.judge_file_exists(file_path=file_path)
        
        if is_exist:
            file_path = abspath(path=file_path)
            return dirname(p=file_path)
        else:
            return ""
    
    # 获取文件后缀
    @staticmethod
    def get_file_suffix(file_path: str) -> str:
        file_path = file_path.lower()
        is_exist = FileUtil.judge_file_exists(file_path=file_path)
        
        if is_exist:
            suffix = file_path.split(".")[-1]
            return suffix
        else:
            return ""
    
    # 确保目录存在，如果不存在则创建
    @staticmethod
    def ensure_dir_exists(file_path: str) -> None:
        if not isdir(file_path):
            try:
                makedirs(file_path, exist_ok=True)
            except Exception as e:
                logger.error(f"创建目录失败: {file_path}, 错误信息: {e}")
    
    # 判断文件是否存在
    @staticmethod
    def judge_dir_exists(dir_path: str) -> bool:
        result = False
        
        if dir_path:
            if isdir(s=dir_path):
                result = True
        
        return result
    
    # 判断文件是否存在
    @staticmethod
    def judge_file_exists(file_path: str) -> bool:
        result = False
        
        if file_path:
            file_path = file_path.lower()
            if isfile(path=file_path):
                result = True
        
        return result
    
    # 获取目录中所有的文件
    @staticmethod
    def get_all_files(dir_path: str) -> list[str]:
        file_list = []
        
        try:
            is_exist = FileUtil.judge_dir_exists(dir_path=dir_path)
            if is_exist:
                for root, dirs, files in walk(top=dir_path):
                    for file in files:
                        file_path = join(root, file)
                        file_list.append(file_path)
        except Exception as e:
            logger.error(f"获取目录中所有文件失败: {dir_path}, 错误信息: {e}")
        finally:
            return file_list
    
    # 删除文件
    @staticmethod
    def delete_link(file_path: str) -> None:
        try:
            if FileUtil.judge_file_exists(file_path=file_path):
                remove(path=file_path)
                logger.info(f"删除文件: {file_path}")
        except Exception as e:
            logger.error(f"删除文件失败: {file_path}, 错误信息: {e}")
        
    # 复制文件
    @staticmethod
    def copy_file(src_path: str, dst_path: str) -> None:
        FileUtil.ensure_dir_exists(file_path=dirname(p=dst_path))
        
        try:
            copy2(src=src_path, dst=dst_path)
            logger.info(f"复制文件: {src_path} -> {dst_path}")
        except Exception as e:
            logger.error(f"复制文件失败: {src_path} -> {dst_path}, 错误信息: {e}")
            
    # 保存 IO 流到文件
    @staticmethod
    def save_io(file_path: str, file_io: BinaryIO) -> None:
        FileUtil.ensure_dir_exists(file_path=dirname(p=file_path))
        
        try:
            with open(file=file_path, mode="wb") as buffer:
                copyfileobj(fsrc=file_io, fdst=buffer)
            logger.info(f"保存文件: {file_path}")
        except Exception as e:
            logger.error(f"保存文件失败: {file_path}, 错误信息: {e}")
        
    # 读取文件的 IO 流
    @staticmethod
    def read_io(file_path: str) -> Optional[bytes]:
        buffer = None
        
        try:
            if not FileUtil.judge_file_exists(file_path=file_path):
                return buffer
            
            with open(file=file_path, mode="rb") as fr:
                buffer = fr.read()
                return buffer
            
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return buffer
    
    # 读取文本文件内容
    @staticmethod
    def read_text(file_path: str) -> Optional[str]:
        content = None
        
        if not FileUtil.judge_file_exists(file_path=file_path):
            return content
        
        try:
            with open(file=file_path, mode="r", encoding="utf-8") as fr:
                content = fr.read()
                return content
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return content
    
    # 读取 docx 文件内容
    @staticmethod
    def read_docx(file_path: str) -> Optional[str]:
        docx_content = None
        
        if not FileUtil.judge_file_exists(file_path=file_path):
            return docx_content
        
        try:
            docx = Document(file_path)
            docx_content = [para.text for para in docx.paragraphs]
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return docx_content
    
    # 读取 excel 文件内容
    @staticmethod
    def read_excel(file_path: str) -> str:
        excel_content = ""
        
        if not FileUtil.judge_file_exists(file_path=file_path):
            return excel_content
        
        try:
            excel_content += f"文件: {file_path}\n"
            
            df = read_excel(io=file_path)
            row = len(df.columns)
            excel_content += f"行数: {row}\n"
            
            column_names = df.columns.astype(str)
            excel_content += f"列名: {', '.join(column_names)}\n"
            
            head = df.head().to_string(index=False)
            excel_content += f"[前5行数据预览]:{head}\n"
            
            describe = df.describe().to_string()
            excel_content += f"[统计描述]:{describe}\n"
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return excel_content
    
    # 读取 pdf 文件内容
    @staticmethod
    def read_pdf(file_path: str) -> Optional[str]:
        pdf_content = None
        
        if not FileUtil.judge_file_exists(file_path=file_path):
            return pdf_content
        
        try:
            pdf = PdfReader(file_path)
            content_list = [page.extract_text() or "" for page in pdf.pages]
            pdf_content = "\n".join(content_list)
        except Exception as e:
            logger.error(f"加载文件失败: {file_path}, 错误信息: {e}")
        finally:
            return pdf_content
    
    @staticmethod
    def write_text(file_path: str, content: str) -> None:
        try:
            with open(file=file_path, mode="w", encoding="utf-8") as fw:
                fw.write(content)
            logger.info(f"写入文件: {file_path}")
        except Exception as e:
            logger.error(f"写入文件失败: {file_path}, 错误信息: {e}")
        

class YamlUtil:
    @staticmethod
    def load_yaml(file_path: str) -> dict:
        with open(file=file_path, mode="r", encoding="utf-8") as fr:
            content = safe_load(fr)
        return content
    

class TransformUtil:
    # 使用 Microsoft Word COM 接口将 Markdown 转换为 PDF
    @staticmethod
    def md_transform_word(md_path: str, pdf_path: str) -> str:
        
        temp_html_path = f"{md_path}.temp.html"
        word_app = None
        
        try:
            content = FileUtil.read_text(file_path=md_path)
            
            html_body = markdown(text=content, extensions=['tables', 'fenced_code'])
            html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: "Microsoft YaHei", "SimHei", sans-serif; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid black; padding: 8px; }}
                    pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 4px; }}
                    code {{ font-family: "Consolas", "Monaco", monospace; }}
                </style>
            </head>
            <body>
                {html_body}
            </body>
            </html>
            """
            FileUtil.write_text(file_path=temp_html_path, content=html_content)
            
            # 2. 调用 Word COM
            pythoncom.CoInitialize()
            word_app = Dispatch('Word.Application')
            word_app.Visible = False
            word_app.DisplayAlerts = False
            
            doc = word_app.Documents.Open(temp_html_path)
            
            doc.SaveAs(pdf_path, FileFormat=17)   # wdFormatPDF = 17
            doc.Close(SaveChanges=0)
        except ImportError:
            logger.error("缺少依赖库，请安装: pip install pywin32 markdown")
        except Exception as e:
            logger.error(f"Word 转换 pdf 失败: {e}", exc_info=True)
        finally:
            if word_app:
                try:
                    word_app.Quit()
                except:
                    logger.error("Word 转换 pdf 失败: 无法关闭 Word 应用程序")
            
            if FileUtil.judge_file_exists(file_path=temp_html_path):
                try:
                    FileUtil.delete_link(file_path=temp_html_path)
                except:
                    logger.error("Word 转换 pdf 失败: 无法删除临时 HTML 文件")
            
            try:
                pythoncom.CoUninitialize()
            except:
                logger.error("Word 转换 pdf 失败: 无法释放 COM 对象")
            
            is_exist = FileUtil.judge_file_exists(file_path=pdf_path)
            if is_exist:
                return f"成功转换: {pdf_path} (Word引擎)"
            else:
                return f"转换完成但未生成文件: {pdf_path}"
            

if __name__ == '__main__':
    # from config import PathConfig
    # content = YamlUtil.load_yaml(file_path=PathConfig.PROMPT_PATH)
    # print(content)
    
    path = r"a\b\c\d"
    dir = FileUtil.get_file_name(file_path=path)
    print(dir)
