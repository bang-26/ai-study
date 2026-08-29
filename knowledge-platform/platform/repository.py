#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  repository 
    CreateTime     ：  2026-07-20 20:47:27 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from os import makedirs
from os.path import isdir, exists, join, getctime
from glob import glob
from datetime import datetime
from json import load, dump
from typing import Optional, List, Dict, Any, Tuple, Union

from config import PathConfig
from logger import logger


# 会话数据仓储类
class SessionRepository:
    def __init__(self, storage_path: str = PathConfig.STORAGE_PATH, file_suffix: str = "json"):
        self.storage_path = storage_path
        self.file_suffix = file_suffix
        
    # 从文件加载会话数据
    def load_session(self, user_id: str = "", session_id: str = "", path: str = "") -> Optional[List[Dict[str, Any]]]:
        if user_id and session_id:
            path = self.__get_session_path(user_id=user_id, session_id=session_id)
        
        session_data = []
        if not exists(path):
            logger.warning(f"文件 {path} 不存在")
            return session_data
        
        try:
            with open(file=path, mode="r", encoding="utf-8") as f:
                session_data = load(fp=f)
                logger.info(f"加载会话数据 {path} 成功")
        except Exception as e:
            logger.error(f"加载会话数据 {path} 失败：{e}")
        finally:
            return session_data
    
    # 保存会话数据到文件
    def save_session(self, user_id: str, session_id: str, data: List[Dict[str, Any]]) -> None:
        session_id = session_id or "default"                         # 修复：处理 None 值
        file_path = self.__get_session_path(user_id=user_id, session_id=session_id)
        self.__create_dir()
        logger.info(f"保存会话数据 {data} 开始")
        try:
            with open(file=file_path, mode="w", encoding="utf-8") as f:
                dump(obj=data, fp=f, ensure_ascii=False, indent=4)
                logger.info(f"保存会话数据 {file_path} 成功")
        except Exception as e:
            logger.error(f"保存会话数据 {file_path} 失败：{e}")
        
    # 获取用户所有会话的元数据和内容
    def get_all_session(self, user_id: str) -> List[Tuple[str, str, List]]:
        path_list = self.__get_session_path(user_id=user_id)
        
        result_list = []
        for path in path_list:
            session_data = self.load_session(path=path)
            create_time = getctime(path)
            format_time = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
            session_id = path.split("-")[-1].split(".")[0]
            result_list.append((session_id, format_time, session_data))
            
        logger.info(f"获取用户 {user_id} 所有会话数据成功")
        return result_list
    
    # 获取用户指定会话的元数据和内容
    def get_epoch_session(self, user_id: str, session_id: str = "",
                          epoch: int = 10) -> list[tuple[str, str, list]]:
        if epoch < 1:                                                # 限制 epoch 的取值范围
            epoch = 1
        elif epoch > 10:
            epoch = 10
            
        all_list = self.get_all_session(user_id=user_id)             # 获取所有会话
        
        if session_id and all_list:
            session_list = [x for x in all_list if x[0] == session_id]    # 筛选指定会话
        
        if all_list:
            all_list.sort(key=lambda x: x[1])                        # 根据创建时间排序
        
        session_list = all_list[-epoch:]
        logger.info(f"获取用户 {user_id} 的 {epoch} 轮话数据成功")
        return session_list
    
    # 获取用户提问的记录
    def get_role_session(self, user_id: str, role: str = "user", session_id: str = "", epoch: int = 5,
                         limit: int = 100) -> List[Dict[str, str]]:
        if limit < 1:                                                # 限制 limit 的取值范围
            limit = 1
        elif limit > 100:
            limit = 100
        
        if epoch < 1:                                                # 限制 epoch 的取值范围
            epoch = 1
        elif epoch > 10:
            epoch = 10
            
        all_list = self.get_all_session(user_id=user_id)             # 获取所有会话
        
        if session_id and all_list:
            all_list = [x for x in all_list if x[0] == session_id]   # 筛选指定会话
        
        if all_list:
            all_list.sort(key=lambda x: x[1])                        # 根据创建时间排序
        
        total = epoch * limit
        user_list = []
        for _, _, session_data in all_list[-epoch:]:
            for data in session_data:
                if data["role"] == role:
                    user_list.append(data)
        
        return user_list[-total:]
        
    # 创建用户目录
    def __create_dir(self) -> None:
        if not isdir(s=self.storage_path) and not exists(path=self.storage_path):
            makedirs(name=self.storage_path, exist_ok=True)
            logger.info(f"创建用户目录: {self.storage_path}")
        else:
            logger.warning(f"用户目录已存在: {self.storage_path}")
    
    # 获取文件路径
    def __get_session_path(self, user_id: str = "", session_id: str = "") -> Union[str, list[str]]:
        if user_id and session_id:
            path_list = f"{self.storage_path}/{user_id}-{session_id}.{self.file_suffix}"
        elif user_id:
            path_name = join(self.storage_path, f"{user_id}*.{self.file_suffix}")
            path_list = glob(pathname=path_name)
        elif session_id:
            path_name = join(self.storage_path, f"*-{session_id}.{self.file_suffix}")
            path_list = glob(pathname=path_name)
        else:
            path_list = ""
            logger.warning(f"user_id 和 session_id 不能全部为空")
        return path_list
    
    
if __name__ == '__main__':
    user_id = "tom"
    session_id = "default"
    session = SessionRepository(storage_path=PathConfig.STORAGE_PATH)
    
    # data = session.load_session(path=f"{PathConfig.STORAGE_PATH}/{user_id}-{session_id}.json")
    # print(data)

    # data_dict_list = \
    #     [
    #         {'role': 'system', 'content': '你是一个有记忆的智能体助手，请基于上下文历史会话用户问题 (会话ID default_session)'},
    #         {'role': 'assistant', 'content': '\n根据查询结果，昌平区温都水城附近有以下商场：\n1. **宏福水城广场**\n   - 地址：北京市昌平区宏福大道温都水城文化广场\n   - 距离：约395米\n2. **小站公园STATIONPARK**\n   - 地址：北京市昌平区回南北路公园悦府\n   - 距离：约2.28公里\n   - 营业时间：10:00-22:00\n3. **禧乐汇生活主题广场(马连店)**\n   - 地址：北京市昌平区文华路89号院1号\n   - 距离：约2.95公里\n   - 联系电话：(010)60789871\n   - 营业时间：09:00-21:30\n您可以点击以下链接导航至最近的宏福水城广场：\n[导航至宏福水城广场](https://api.map.baidu.com/direction?origin=40.1102640888901,116.3770169663488&destination=40.11360103519952,116.37861648913986&mode=driving&output=html)'},
    #         {'role': 'user', 'content': '我们刚刚都聊了些什么'}
    #     ]
    data_dict_list = [{'role': 'system', 'content': '你是一个有记忆的智能助手，请基于上下文历史会话用户问题 (会话ID default)'}, {'role': 'user', 'content': '我的电脑蓝屏了'}, {'role': 'assistant', 'content': '> 以下信息来自网络搜索，仅供参考，不构成官方建议。\n电脑蓝屏是常见的系统故障，通常由硬件或软件问题引起。以下是常见原因及解决方法：\n---\n## 🔍 常见原因\n| 类型 | 具体原因 |\n|------|----------|\n| **硬件问题** | 内存条接触不良/损坏、硬盘坏道、显卡驱动不兼容、散热不良导致过热 |\n| **软件问题** | 驱动冲突、系统文件损坏、病毒/恶意软件感染、Windows更新失败 |\n---\n## 🛠️ 解决方法（由简到繁）\n### 方法一：重启电脑（最简单）\n- 长按电源键 5-10 秒强制关机\n- 等待几秒后重新开机\n- 如果是偶发性蓝屏，重启后通常可恢复正常\n### 方法二：检查硬件连接\n1. **检查内存条**：关机断电后，取出内存条用橡皮擦擦拭金手指，重新插紧\n2. **检查显卡**：重新插拔显卡，确保接触良好\n3. **检查散热**：清理机箱内部灰尘，特别是CPU散热器和风扇\n### 方法三：进入安全模式排查\n1. 重启时连续按 **F8** 或 **Shift+F8**\n2. 选择"疑难解答" → "高级选项" → "启动设置" → "启用安全模式"\n3. 在安全模式下卸载最近安装的软件或驱动\n### 方法四：更新或回滚驱动程序\n1. 按 **Win+X** → 选择"设备管理器"\n2. 查找带黄色感叹号的设备\n3. 右键选择"更新驱动程序"或"回滚驱动程序"\n### 方法五：修复系统文件\n以管理员身份运行命令提示符，输入以下命令：\n```\nsfc /scannow\n```\n等待扫描修复完成后重启电脑。\n### 方法六：重装系统\n如果以上方法均无效，可考虑重装系统。\n---\n## 💡 温馨提示\n- 如果蓝屏时显示了**错误代码**（如 `0x0000007B`），可以记录下来，有助于精准定位问题\n- 如果是在安装某软件/驱动后出现蓝屏，优先卸载该软件\n- 如果不确定如何操作硬件，建议寻求专业人士帮助，避免造成更大损害\n如果您能提供更多细节（如蓝屏错误代码、何时出现蓝屏等），我可以帮您进一步分析问题原因。'}]
    session.save_session(session_id="", user_id=user_id, data=data_dict_list)

    # session.get_session_list(user_id=user_id)
    # print("=" * 100)
    # session.get_session_list(user_id=user_id, session_id=session_id)
    # print("=" * 100)
    # session.get_session_list(session_id=session_id)
    # print("=" * 100)
    # session.get_session_list()
    #
    # results = session.get_all_session(user_id=user_id)
    # for result in results:
    #     print(result)
    #
    # results = session.get_epoch_session(user_id="alice", epoch=3)
    # for result in results:
    #     print(result)
    #
    # print("=" * 100)
    #
    # results = session.get_role_session(user_id="alice", session_id=session_id, epoch=2, limit=3)
    # print(results)
    # print("=" * 100)
    # for result in results:
    #     print(result)

    
