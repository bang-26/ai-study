#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  deep-search
    FileName       ：  loger
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
from pathlib import Path
from loguru import logger as logging
from contextvars import ContextVar
from config import app_config
from config import PathConfig, LogConfig


# ================= 彩色日志格式器 (仅用于控制台) =================
class ColorFormat:
    def __init__(self, conf: LogConfig):
        self.log_format = conf.pattern                               # 日志格式
        self.console_enable = conf.console.enable                    # 控制台是否启用
        self.console_level = conf.console.level                      # 控制台级别
        self.file_enable = conf.file.enable                          # 文件是否启用
        self.file_level = conf.file.level                            # 文件级别
        self.log_name = f"{PathConfig.PROJECT_DIR}/{conf.file.path}/{conf.file.log_name}"
        self.file_rotation = conf.file.rotation                      # 日志文件轮转
        self.file_retention = conf.file.retention                    # 日志文件保存时长
    
    def profile(self):
        logging.remove()
        patched_logger = logging.patch(patcher=self.__inject_request_id)
        
        if self.console_enable:
            patched_logger.add(sink=stdout, level=self.console_level, format=self.log_format)
        
        if self.file_enable:
            self.__create_log_dir()
            
            patched_logger.add(sink=self.log_name, level=self.file_level, format=self.log_format,
                        rotation=self.file_rotation, retention=self.file_retention, encoding="utf-8")
        return patched_logger
        
    def __create_log_dir(self):
        path = Path(self.log_name).parent                            # 日志文件路径
        
        if path.exists() and path.is_dir():                          # 判断路径是否存在
            return
        
        path.mkdir(parents=True, exist_ok=True)                      # 创建路径
    
    @classmethod
    def __inject_request_id(cls, record: dict[str, dict[str, str]]):
        request_id = ContextVar("request_id", default="1").get()
        record["extra"]["request_id"] = request_id


# 日志大小级别：DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
logger = ColorFormat(conf=app_config.log_config).profile()



if __name__ == '__main__':
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
