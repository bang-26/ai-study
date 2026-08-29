#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  agent 
    CreateTime     ：  2026-07-20 20:46:35 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from json import loads
from typing import Any

from agents.mcp import MCPServerSse, MCPServerStreamableHttp

from config import BaiDuConfig, BaiLianConfig
from logger import logger


# search_mcp_client = None
# baidu_mcp_client = None


class BaiLianMcp:
    def __init__(self, conf: BaiLianConfig):
        self.name = conf.NAME
        self.url = conf.URL
        self.headers = conf.HEADERS
        self.tool_name= conf.TOOL_NAME
        self.timeout = conf.TIMEOUT
        self.cache_tool_list = conf.CACHE_TOOL_LIST
        
        self.mcp = None
    
    # 连接
    async def get_connect(self) -> None:
        params = \
            {
                "url"             : self.url,
                "headers"         : self.headers,
                "timeout"         : self.timeout,
                "sse_read_timeout": self.timeout * 10
            }
        
        self.mcp = MCPServerStreamableHttp(name=self.name, params=params, cache_tools_list=self.cache_tool_list,
                                           client_session_timeout_seconds=self.timeout * 10)
        try:
            await self.mcp.connect()
            logger.info(f"连接 MCP==<{self.name}>==成功")
        except Exception as e:
            logger.error(f"连接 MCP==<{self.name}>==失败: {e}")
    
    # 查询
    async def query(self, query: str, tool_name: str = None) -> list[str]:
        tool_name = tool_name or self.tool_name
        
        if self.mcp is None:
            await self.get_connect()
        
        arguments = {"query": query}
        result_list = []
        try:
            response = await self.mcp.call_tool(tool_name=tool_name, arguments=arguments)
            for content in response.content:
                if hasattr(content, "text"):
                    text = loads(content.text)
                    result = text.get("pages", [])
                    result_list.extend(result)
            logger.info(f" 调用 MCP==<{self.name}>==成功")
        except Exception as e:
            logger.error(f"调用 MCP==<{self.name}>==异常: {e}")
        finally:
            await self.close()
            return result_list
            
    # 关闭
    async def close(self):
        if self.mcp is not None:
            await self.mcp.cleanup()
        

# 百度地图
class BaiDuMcp:
    def __init__(self, conf: BaiDuConfig):
        self.name = conf.NAME
        self.url = f"{conf.URL}?ak={conf.API_KEY}"
        self.tool_name_list = conf.TOOL_NAME_LIST
        self.timeout = conf.TIMEOUT
        self.cache_tool_list = conf.CACHE_TOOL_LIST
        self.mcp = None
    
    async def get_connect(self) -> None:
        params = \
            {
                "url"             : self.url,
                "timeout"         : self.timeout,
                "sse_read_timeout": self.timeout * 10
            }
        try:
            self.mcp = MCPServerSse(name=self.name, params=params, cache_tools_list=self.cache_tool_list,
                                    client_session_timeout_seconds=self.timeout * 10)
            await self.mcp.connect()
            logger.info(f"连接 MCP==<{self.name}>==成功")
        except Exception as e:
            logger.error(f"连接 MCP==<{self.name}>==失败: {e}")
    
    async def query(self, arguments: dict, tool_name: str = None) -> list[Any]:
        tool_name = tool_name or self.tool_name_list
        
        if self.mcp is None:
            await self.get_connect()
            
        result_list = []
        try:
            response = await self.mcp.call_tool(tool_name=tool_name, arguments=arguments)
            for content in response.content:
                if hasattr(content, "text"):
                    try:
                        text = loads(content.text)
                    except Exception as e:
                        logger.error(f"解析 MCP==<{self.name}>==返回数据异常: {e}")
                        text = content.text
                    result_list.append(text)
            logger.info(f" 调用 MCP==<{self.name}>==成功")
        except Exception as e:
            logger.error(f"调用 MCP==<{self.name}>==异常: {e}")
        finally:
            # await self.close()
            return result_list
    
    async def  query_coordinate_by_address(self, address: str) -> list[dict]:
        arguments = {"address": address}
        data_list = await self.query(arguments= arguments, tool_name=self.tool_name_list[0])
        
        result_list = []
        for  data in data_list:
            result = data.get("result", {})
            result_list.append(result)
            
        return result_list
    
    async def query_coordinate_by_ip(self, ip: str) -> list[dict]:
        arguments = {"address": ip}
        data_list = await self.query(arguments= arguments, tool_name=self.tool_name_list[1])
        
        result_list = []
        for  data in data_list:
            result = data.get("content", {}).get("point", {})
            result_list.append(result)
        return result_list
    
    async def query_uri(self, service: str = "direction") -> list[str]:
        arguments = {"service": service}
        data_list = await self.query(arguments= arguments, tool_name=self.tool_name_list[2])
        return data_list
    
    async def close(self):
        if self.mcp is not None:
            await self.mcp.cleanup()
    
    
if __name__ == '__main__':
    import asyncio
    from json import dumps
    #
    # async def bailian_test():
    #     bailian = BaiLianMcp(conf=BaiLianConfig())
    #     resp = await bailian.query(query="我的电脑不开机了")
    #
    #     await bailian.close()
    #     dp = dumps(resp, indent=4, ensure_ascii=False)
    #     print(dp)
    # asyncio.run(bailian_test())
    #
    async def baidu_test():
        baidu = BaiDuMcp(conf=BaiDuConfig())
        
        resp1 = await baidu.query_coordinate_by_address(address="北京清华大学")
        dp1 = dumps(obj=resp1, indent=4, ensure_ascii=False)
        print(dp1)
        
        resp2 = await baidu.query_coordinate_by_ip(ip="****************")
        dp2 = dumps(obj=resp2, indent=4, ensure_ascii=False)
        print(dp2)
        
        resp3 = await baidu.query_uri(service="direction")
        dp3 = dumps(obj=resp3, indent=4, ensure_ascii=False)
        print(dp3)
        
        await baidu.close()
    asyncio.run(baidu_test())
