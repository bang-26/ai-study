#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-platform  
    FileName       ：  tools 
    CreateTime     ：  2026-07-23 16:06:01 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""
from contextlib import AsyncExitStack
from json import dumps, loads
from typing import Optional

from agents import function_tool, Runner, Agent, ModelSettings
from agents.run import RunConfig
from httpx import AsyncClient, HTTPError

from config import BaseAgentConfig, BaiLianConfig, BaiDuConfig, OrchestratorAgentConfig
from config import PathConfig, DataDict, MysqlConfig, MainModelConfig, ModelConfig
from config import TechnicalAgentConfig, SubModelConfig, ComprehensiveAgentConfig
from connect import CloudModel, MysqlPool
from entry import KnowledgeAnswer, KnowledgeError
from logger import logger
from mcps import BaiLianMcp, BaiDuMcp
from utils import PromptParser, MercatorLatitudeLongitude, SqlParser


# 创建技术智能体
def create_agent(agent_conf: BaseAgentConfig, model_conf: ModelConfig, tool_list: list = None, mcp_list: list = None):
    if mcp_list is None:
        mcp_list = []
    
    model = CloudModel(conf=model_conf).create_model()
    model_setting = ModelSettings(temperature=agent_conf.TEMPERATURE, max_tokens=agent_conf.MAX_TOKEN)
    
    parser = PromptParser(path=agent_conf.PROMPT_PATH)
    instruction = parser.get_prompt(key=agent_conf.PROMPT_KEY)
    
    agent = Agent(name=agent_conf.NAME, instructions=instruction, model=model,
                  model_settings=model_setting, tools=tool_list, mcp_servers=mcp_list)
    return agent


# 创建技术专家智能体工具
@function_tool
async def query_knowledge(question: Optional[str]) -> dict[str, str]:
    """
        查询电脑问题知识库服务，用于检索与用户问题相关的技术文档或解决方案
         
        Args:
            question (Optional[str]): 需要查询的问题文本
            
        Returns:
            dict: 包含查询结果的字典，包含查询结果的字典，结构为：
            {
                "answer": "具体解答内容",    # 知识库返回的答案
                "source": "知识库",         # 答案来源标识
                "confidence": 0.95          # 答案置信度（可选）
            }
            或错误时返回：
            {
                "error": "错误描述",
                "fallback": "建议用户重新提问或联系人工客服"
            }
    """
    url = f"{DataDict.KNOWLEDGE_BASE_URL}/query"
    request_data = {"question": question}
    async with AsyncClient() as client:
        try:
            # 发送请求到知识库服务
            response = await client.post(url=url, json=request_data, timeout=120.0)
            response.raise_for_status()                              # 检查 HTTP 状态码
            response_data = response.json()                          # 解析并返回结果
            
            answer = response_data.get("answer", "")                 # 获取答案
            confidence = response_data.get("confidence", 0.9)        # 获取答案置信度
            result = KnowledgeAnswer(answer=answer, confidence=confidence)
        except HTTPError as e:
            # HTTP错误处理
            logger.error(f"知识库工具 HTTP 错误: {str(e)}")
            result = KnowledgeError(error=str(f"知识库工具 HTTP 错误: {str(e)}"))
        except Exception as e:
            # 其他异常处理
            logger.error(f"知识库工具未知错误: {str(e)}")
            result = KnowledgeError(error=f"知识库查询失败: {str(e)}")
        finally:
            return dict(result)


# 智能解析用户当前位置
@function_tool
async def resolve_location(user_input: str, user_ip: str = "****************") -> str:
    """
        智能解析用户当前位置（起点），用于导航或服务站查询。
            ✅ 适用场景：
                - 用户说“我在武汉”、“从当前位置出发”等；
                - 无明确位置时，通过 user_ip 地址兜底定位。
            ⚠️ 注意：
                - 返回坐标为 BD09LL（百度经纬度）；
                - 仅用于获取**起点**，不可作为终点使用。
                - 最终兜底返回北京坐标 (39.9042, 116.4074)。
        
        Args:
            user_input (str): 用户输入的位置描述（可选）
            user_ip (str): 用户 IP 地址（用于兜底定位）
        
        返回 JSON 字符串：
            {
                "ok": bool,
                "lat": float,
                "lng": float,
                "source": "geocode" | "ip" | "fallback",
                "original_input": str,
                "error": str?  # 仅当 ok=False 时存在
            }
    """
    original_input = user_input
    user_input = user_input.strip() if user_input else ""
    
    baidu = BaiDuMcp(conf=BaiDuConfig())
    await baidu.get_connect()
    baidu_map_mcp = baidu.mcp
    
    # === Step 1: 尝试 Geocode ===
    if user_input:
        try:
            logger.debug(f"[Location] Trying geocode for: '{user_input}'")
            geo_result = await baidu_map_mcp.call_tool(tool_name="map_geocode", arguments={"address": user_input})
            text = geo_result.content[0].text
            result = loads(text).get('result')
            
            if isinstance(result, dict) and "lat" in result['location'] and "lng" in result['location']:
                lat = float(result['location']['lat'])
                lng = float(result['location']['lng'])
                
                logger.info(f"[Location] Geocode success: '{user_input}' → ({lat}, {lng})")
                return dumps(obj={
                    "ok"            : True,
                    "lat"           : lat,
                    "lng"           : lng,
                    "source"        : "geocode",
                    "original_input": original_input
                }, ensure_ascii=False)
            else:
                logger.warning(f"[Location] Geocode returned invalid result: {geo_result}")
        except Exception as e:
            logger.warning(f"[Location] Geocode failed for '{user_input}': {e}")
        finally:
            await baidu.close()
            
    # === Step 2: 尝试 IP 定位 ===
    if user_ip and user_ip not in ("127.0.0.1", "localhost", "::1"):
        try:
            logger.debug(f"[Location] Trying IP location for: {user_ip}")
            ip_result = await baidu_map_mcp.call_tool("map_ip_location", {"ip": user_ip})
            
            text = ip_result.content[0].text
            data = loads(text)
            
            if data.get("status") != 0:
                logger.warning(f"[Location] IP location API error: {data.get('message', 'unknown')}")
                raise ValueError("IP location API returned non-zero status")
            
            point = data.get("content", {}).get("point", {})
            x_str = point.get("x")
            y_str = point.get("y")
            
            if not x_str or not y_str:
                logger.warning(f"[Location] Missing x/y in IP location result: {data}")
                raise ValueError("Missing x/y coordinates")
            
            # 转换墨卡托 → 经纬度
            x = float(x_str)
            y = float(y_str)
            lng, lat = MercatorLatitudeLongitude.mercator_to_latitude_longitude(x, y)
            
            logger.info(f"[Location] IP location success: {user_ip} → ({lat:.6f}, {lng:.6f})")
            return dumps(obj={
                "ok"            : True,
                "lat"           : lat,
                "lng"           : lng,
                "source"        : "ip",
                "original_input": original_input
            }, ensure_ascii=False)
        
        except Exception as e:
            logger.warning(f"[Location] IP location failed for {user_ip}: {e}")
        
    # === Step 3: 兜底 ===
    fallback_lat, fallback_lng = 39.9042, 116.4074
    logger.info("[Location] Using fallback coordinates (Beijing)")
    return dumps({
        "ok"            : False,
        "error"         : "无法解析用户位置，使用默认坐标",
        "lat"           : fallback_lat,
        "lng"           : fallback_lng,
        "source"        : "fallback",
        "original_input": original_input
    }, ensure_ascii=False)


# 查询附近维修站
@function_tool
async def query_nearest_repair(lat: float, lng: float, limit: int = 5) -> str:
    """
    根据给定的经纬度坐标，查询数据库中最近的维修站/服务站。
    注意：此工具仅用于查询官方授权服务站，不得用于普通POI查询。
    
    Args:
        lat (float): 纬度 (BD09LL坐标系)
        lng (float): 经度 (BD09LL坐标系)
        limit (int): 返回结果数量限制，默认为5
        
    Returns:
        str: JSON格式的查询结果，包含最近的维修站列表。
        成功时返回：
            {
                "ok": true,
                "count": 3,
                "data": [
                    {
                        "service_station_name": "小米之家(光谷店)",
                        "address": "武汉市洪山区光谷广场",
                        "phone": "027-88888888",
                        "distance_km": 1.5,
                        "latitude": 30.505,
                        "longitude": 114.404
                    }
                ]
            }
        失败时返回：
            {
                "ok": false,
                "error": "错误描述"
            }
    """
    parser = SqlParser(path=PathConfig.SQL_PATH)
    sql = parser.get_sql(key=DataDict.SQL_KEY)
    
    data = (lat, lng, lat, limit)
    with MysqlPool(conf=MysqlConfig()) as pool:
        rows = pool.query_data(query=sql, args=data)
    
    result = {"ok": False, "query": {"lat": lat, "lng": lng, "limit": limit}}
    
    if rows:
        result["ok"] = True
        result["data"] = rows
        result["count"] = len(rows)
    else:
        result["error"] = "未找到任何结果"
        
    return dumps(obj=result, ensure_ascii=False)
        

# 技术专家智能体工具，依赖：query_knowledge
@function_tool
async def consult_technical(query: str) -> str:
    """
        【咨询与技术专家】处理技术咨询、设备故障、维修建议以及实时资讯（如股价、新闻、天气）。
            当用户询问：
                1. "怎么修"、"为什么坏了"、"如何操作"等技术问题。
                2. "今天股价"、"现在天气"等实时信息。
            请调用此工具。
        
        Args:
            query: 用户的原始问题或完整指令
        
        Returns:
            dict
    """
    logger.info(f"[Route] 转交技术专家: {query[:30]}...")
    
    bailian = BaiLianMcp(conf=BaiLianConfig())
    await bailian.get_connect()
    search_mcp = bailian.mcp
    
    # 创建资讯与技术专家智能体
    technical_agent = create_agent(agent_conf=TechnicalAgentConfig(), model_conf=SubModelConfig(),
                                   tool_list=[query_knowledge], mcp_list=[search_mcp])
    result = ""
    try:
        # 直接透传用户指令，不要做任何加工
        run_config = RunConfig(tracing_disabled=True)
        response = await Runner.run(starting_agent=technical_agent, input=query, run_config=run_config)
        result = response.final_output
        logger.info("技术专家的回答成功")
    except Exception as e:
        return f"技术专家暂时无法回答: {str(e)}"
    finally:
        await bailian.close()
        return result


# 定义全能业务智能体工具，依赖：resolve_location、query_nearest_repair
@function_tool
async def query_station_navigate(query: str) -> str:
    """
        【服务站专家】处理线下服务站查询、位置查找和地图导航需求。
            当用户询问：
                1. "附近的维修点"、"找小米之家"（服务站查询）。
                2. "怎么去XX"、"导航到XX"（路径规划）。
                3. 任何涉及地理位置和线下门店的请求。
            请调用此工具。
        Args:
            query: 用户的原始问题（包含隐含的位置信息）
        
        Returns:
            dict
    """
    
    baidu = BaiDuMcp(conf=BaiDuConfig())
    await baidu.get_connect()
    baidu_map_mcp = baidu.mcp
    
    try:
        logger.info(f"[Route] 转交业务专家: {query[:30]}...")
        # 创建资讯与技术专家智能体
        comprehensive_agent = create_agent(agent_conf=ComprehensiveAgentConfig(), model_conf=SubModelConfig(),
                                           tool_list=[resolve_location, query_nearest_repair],
                                           mcp_list=[baidu_map_mcp])
        
        run_config = RunConfig(tracing_disabled=True)
        result = await Runner.run(starting_agent=comprehensive_agent, input=query, run_config=run_config)
        logger.info("导航业务专家的回答成功")
        return result.final_output
    except Exception as e:
        return f"业务专家暂时无法回答: {e}"
    finally:
        await baidu.close()


# 创建资讯与技术专家智能体
comprehensive_agent = create_agent(agent_conf=OrchestratorAgentConfig(), model_conf=MainModelConfig(),
                                   tool_list=[consult_technical, query_station_navigate])

if __name__ == '__main__':
    import asyncio
    
    # query = "我的电脑不开机了"
    # resp = asyncio.run(consult_technical(query=query))
    # print(f"response = {resp}")

    # technical_agent = create_agent(agent_conf=TechnicalAgentConfig(), model_conf=SubModelConfig(),
    #                                tool_list=[query_knowledge], mcp_list=[search_mcp])
    
    # response = query_nearest_repair(lat=13200603.38, lng=3628686.64)
    # resp = loads(response)
    # for data in resp.get("data"):
    #     print("=" * 100)
    #     dj = dumps(data, ensure_ascii=False, indent=4)
    #     print(dj)
    
    # query = "我的位置在北京温都水城，怎样去最近的维修店"
    # resp = asyncio.run(query_station_navigate(query=query))
    # print(f"response = {resp}")
    
    async def test(input_text: str):
        # 使用 AsyncExitStack 同时管理多个连接
        async with AsyncExitStack() as stack:
            bailian = BaiLianMcp(conf=BaiLianConfig())
            await bailian.get_connect()
            search_mcp = bailian.mcp
            await stack.enter_async_context(search_mcp)
            
            baidu = BaiDuMcp(conf=BaiDuConfig())
            await baidu.get_connect()
            baidu_map_mcp = baidu.mcp
            await stack.enter_async_context(baidu_map_mcp)
            
            result = Runner.run_streamed(starting_agent=comprehensive_agent, input=input_text, )
            async for event in result.stream_events():
                if event.type == "run_item_stream_event":
                    if hasattr(event, "name") and event.name == "tool_called":
                        
                        from agents import ToolCallItem
                        if isinstance(event.item, ToolCallItem):
                            raw_item = event.item.raw_item
                            print(f"\n调用工具名:{raw_item.name}--->工具参数:{raw_item.arguments}")
                    elif hasattr(event, 'name') and event.name == "tool_output":
                        from agents import ToolCallOutputItem
                        if isinstance(event.item, ToolCallOutputItem):
                            print(f"调用工具结果:{event.item.output}")
            # 4. 打印最终结果（最后协调Agent的输出）
            print(f"\n最终输出（来自 {result.last_agent.name}）:")
            print(f"{result.final_output}")
            
    queries = ["我的电脑不开机了", "我的位置在北京温都水城，怎样去最近的维修店"]
    for query in queries:
        asyncio.run(test(query))
