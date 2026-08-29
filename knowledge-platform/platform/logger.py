#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  looger 
    CreateTime     ：  2026-07-23 11:41:24 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from sys import stdout
from os import makedirs
from os.path import dirname, isfile, exists
from logging import getLogger, Formatter, LogRecord, StreamHandler, DEBUG, INFO, WARN, ERROR, CRITICAL
from logging.handlers import TimedRotatingFileHandler
from config import LogConfig


# ================= 彩色日志格式器 (仅用于控制台) =================
class ColorFormat(Formatter):
    def __init__(self, conf: LogConfig):
        grey = "\x1b[38;20m"                                         # 灰色
        green = "\x1b[32;20m"                                        # 绿色
        yellow = "\x1b[33;20m"                                       # 黄色
        red = "\x1b[31;20m"                                          # 红色
        bold_red = "\x1b[31;1m"                                      # 加粗红色
        reset = "\x1b[0m"                                            # 重置颜色
        
        console_format = conf.CONSOLE_FORMAT                         # 日志格式
        self.format_dict = \
            {
                DEBUG   : grey + console_format + reset,             # 调试用灰色
                INFO    : green + console_format + reset,            # 正常用绿色
                WARN    : yellow + console_format + reset,           # 警告用黄色
                ERROR   : red + console_format + reset,              # 错误用红色
                CRITICAL: bold_red + console_format + reset          # 严重用红色加粗
            }
        self.file_format = conf.FILE_FORMAT                          # 文件格式
        self.console_level = conf.CONSOLE_LEVEL                      # 控制台级别
        self.file_level = conf.FILE_LEVEL                            # 文件级别
        self.name = conf.LOG_NAME                                    # 日志名称
        self.debug_name = conf.LOG_DEBUG_NAME                        # 调试日志存储路径
        self.info_name = conf.LOG_INFO_NAME                          # 普通日志存储路径
        self.warn_name = conf.LOG_WARN_NAME                          # 警告日志存储路径
        self.error_name = conf.LOG_ERROR_NAME                        # 错误日志存储路径
        
        super().__init__(datefmt=conf.TIME_FORMAT)
    
    # 重写 format 方法
    def format(self, record: LogRecord) -> str:
        # 1. 根据当前日志的级别 (record.levelno)，去字典里查对应的颜色格式
        log_format = self.format_dict.get(record.levelno)
        # 2. 创建一个临时的标准 Formatter，使用配置中的时间格式（含日期）
        formatter = Formatter(log_format, datefmt=self.datefmt)
        # 3. 调用父类方法进行最终格式化
        format_string = formatter.format(record)
        return format_string
    
    # 获取配置好的 Logger 实例
    def get_logger(self) -> getLogger:
        for path in [self.debug_name, self.info_name, self.warn_name, self.error_name]:
            self.__create_dir(path=path)
        
        logger = getLogger(name=self.name)
        
        # 如果已经有 handler 说明初始化过了，直接返回，防止重复打印
        if logger.handlers:
            return logger
        
        logger.setLevel(level=DEBUG)                                 # 总开关设为最低，由 handler 决定具体过滤
        
        # 1. 控制台 Handler (带颜色)
        console_handler = StreamHandler(stream=stdout)               # 输出到标准输出(屏幕)
        console_handler.setLevel(level=self.console_level)           # 控制台级别
        console_handler.setFormatter(fmt=self)                       # 使用颜色格式
        logger.addHandler(hdlr=console_handler)                      # 添加 Handler
        
        # 2. 通用日志：每天轮转
        file_format = Formatter(fmt=self.file_format)                # 文件日志格式
        file_handler = TimedRotatingFileHandler(filename=self.info_name, when="midnight", interval=1,
                                                backupCount=30, encoding="utf-8")
        
        file_handler.setLevel(level=self.file_level)                 # 文件日志级别
        file_handler.setFormatter(fmt=file_format)                   # 使用详细的文件格式
        logger.addHandler(hdlr=file_handler)                         # 添加 Handler
        
        # 3. 错误错误日志
        error_handler = TimedRotatingFileHandler(filename=self.error_name, when="midnight", interval=1,
                                                 backupCount=60, encoding="utf-8")
        error_handler.setLevel(level=ERROR)                          # 只有 ERROR 及以上才写进来
        error_handler.setFormatter(fmt=file_format)                  # 使用详细的文件格式
        logger.addHandler(hdlr=error_handler)
        
        # 4. Agent/Debug 详细日志 (用于追踪 LLM 思考过程)
        agent_handler = TimedRotatingFileHandler(filename=self.debug_name, when="midnight", interval=1,
                                                 backupCount=7, encoding="utf-8")
        agent_handler.setLevel(level=DEBUG)
        agent_handler.setFormatter(fmt=file_format)
        logger.addHandler(hdlr=agent_handler)
        
        return logger
    
    # 创建日志文件夹
    def __create_dir(self, path: str) -> None:
        folder_path = dirname(p=path)
        if not isfile(path=path) and not exists(path=folder_path):
            makedirs(name=folder_path)
        

# 日志大小级别：DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
logger = ColorFormat(conf=LogConfig()).get_logger()
