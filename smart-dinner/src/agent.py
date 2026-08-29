#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  mcp 
    CreateTime     ：  2026-07-19 16:19:13 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from typing import Dict, Any
from time import sleep
from langchain_core.tools import tool, ToolException
from json import loads, JSONDecodeError
from config import AmapConfig
from dao import VectorQueryDao, AmapDao, CloudModelDao
from init import cloud_model, amap_map, pinecone_connect, prompt_parser, data_dict


class SmartRestaurantAssistant:
    def __init__(self):
        self.tool_dict = \
            {
                "general_inquiry": general_inquiry,
                "menu_inquiry"   : menu_inquiry,
                "delivery_check" : delivery_check_tool,
            }
        
        self.prompt = prompt_parser.get_prompt(key=data_dict.ADAPT_PARSER)
        self.max_retries = 3                                         # 最大重试次数  (包括第一次)
        self.backoff = 1                                             # 重试的间隔
    
    # 智能问答
    def invoke(self, user_query: str) -> str | dict[str, str]:
        # 1. 分析用户的意图（找工具），构建重试策略
        tool = self.retry_policy(user_query=user_query)
        
        # 2. 获取工具的名字
        tool_name = tool.get("tool_name", data_dict.MENU_INQUIRY)
        
        # 3. 获取工具的参数
        tool_param = tool.get("format_query", "")
        print(f"工具信息->名字:{tool_name}:参数:{tool_param}")
        
        # 4.调用工具
        tool_result = self.__execute_tool(tool_name=tool_name, tool_param=tool_param)
        
        # 5.返回工具结果
        return tool_result
    
    # 重试机制
    def retry_policy(self, user_query: str) -> dict[str, str]:
        last_error = None
        
        # 1.重试
        for i in range(self.max_retries):
            try:
                response_dict = self.__analyze_intention(user_query=user_query, last_error=last_error)
                return response_dict
            except(ValueError, JSONDecodeError) as e:
                last_error = str(e)
                if i < self.max_retries - 1:
                    sleep(self.backoff)
        # 2. 走降级处理
        return self.__analyse_fallback(user_query=user_query)
        
    # 意图分析
    def __analyze_intention(self, user_query: str, last_error: str = "") -> dict[str, str]:
        instruction = self.prompt
        # 1.是否有错误
        if last_error:
            instruction += f"\n\n上次解析失败，错误信息：{last_error}\n请根据错误信息修正JSON格式，确保返回正确的JSON。"
        
        # 2.调用模型
        model_response = CloudModelDao.get_assistant_answer(cloud_model=cloud_model, query=user_query,
                                                          instruction=instruction)
        content = model_response.get("content", "")
        
        # 3.清洗模型的结果
        clean_content = self.__process_model_response(content=content)
        
        # 4.解析模型的结果(反序列化)
        content_dict = loads(s=clean_content)
        
        # 5.校验字典的key是否有效
        if not all(key in content_dict for key in ["tool_name", "format_query"]):
            raise ValueError(f"无效的工具结构信息：{content_dict}")
        
        # 6.校验工具名是否在工具集中
        if content_dict['tool_name'] not in self.tool_dict:
            raise ValueError(f"无效的工具结构信息：{content_dict}")
        
        # 7.返回模型的结果(工具结构信息)
        return content_dict
    
    # 执行工具
    def __execute_tool(self, tool_name: str, tool_param: str) -> str | dict[str, str]:
        # 1.判断工具是否在工具集中
        tool_function = self.tool_dict.get(tool_name)
        if tool_function is None:
            raise ValueError(f"工具：{tool_name}不可用")
        
        # 2. 构建工具参数
        input_param = {"query": tool_param}
        if tool_name != data_dict.GENERAL_INQUIRY and tool_name != data_dict.MENU_INQUIRY:
                input_param["transport"] = 2
        
        # 3.执行工具
        tool_result = ""
        try:
            tool_result = tool_function.invoke(input=input_param)
        except Exception as e:
            raise Exception(f"查询功能不可用,{str(e)}")
        finally:
            return tool_result
    
    # 清洗LLM的字符串内容
    def __process_model_response(self, content: str):
        # 1.处理 markdown 格式的 json
        text = content = content.strip()
        if text.startswith("```json"):
            content = content[7:]
        if text.endswith("```"):
            content = content[:-3]
        
        # 2.处理 json 的嵌套(有效的json)的位置
        star_index = content.find("{")                               # 左边找打第一个
        end_index = content.rfind("}")                               # 右边找到第一个
        
        # 3.获取有效的json
        if star_index != -1 and end_index != -1 and end_index > star_index:
            clean_response = content[star_index:end_index + 1]
            return clean_response
        else:
            raise ValueError(f"{content}不是有效的 json 格式字符串")
    
    # 降级回落处理
    def __analyse_fallback(self, user_query: str) -> dict[str, str]:
        
        return {}
    

@tool
def general_inquiry(query: str, context: str = "") -> str:
    """
        常规问询工具

        处理用户的一般性问题，包括但不限于：
        - 餐厅介绍和服务信息
        - 营业时间和联系方式
        - 优惠活动和会员服务
        - 其他非菜品相关的咨询

        Args:
            query: 用户的问询内容
            context: 可选的上下文信息，用于提供更精准的回复

        Returns:
            str: 针对用户问询的智能回复

        Raises:
            ToolException: 当处理查询时发生错误
    """
    try:
        # 1.加载常规问题的提示词
        instruction = prompt_parser.get_prompt(key=data_dict.GENERAL_INQUIRY)
        
        # 从记忆组件读取QA TODO(可扩展)
        if context:
            full_query = f"当前历史对话的内容:\n{context}\n\n当前用户问题:\n{query}\n\n,请基于以上的上下文信息来回答用户问题"
        else:
            full_query = f"当前没有历史对话，当前用户问题:\n{query}\n\n,请基于一般信息来回答用户问题"
        
        # 2.调用LLM
        response = CloudModelDao.get_assistant_answer(cloud_model=cloud_model, query=full_query,
                                                      instruction=instruction)
        # 3.直接返回
        content = response.get("content")
        return content
    except Exception as e:
        raise ToolException(f"常规问询失败{e}")
        

@tool
def menu_inquiry(query: str) -> Dict[str, Any]:
    """
        智能菜品咨询工具
    
        专门处理与菜品相关的所有查询，包括：
        - 菜品介绍和详细信息
        - 价格和营养信息
        - 菜品推荐和搭配建议
        - 过敏原和饮食限制相关问题
        - 菜品可用性和特色介绍
    
        该工具会自动通过语义搜索找到最相关的菜品信息，然后基于这些信息回答用户问题。
    
        Args:
            query: 用户关于菜品的具体问题
    
        Returns:
            Dict[str, Any]: 包含推荐建议和菜品ID的字典
            {
                "recommendation": "基于菜品信息的推荐建议",
                "menu_ids": ["菜品ID1", "菜品ID2"]
            }
    
        Raises:
            ToolException: 当处理菜品查询时发生错误
    """
    
    try:
        # 1.加载菜品推荐问题的提示词
        instruction = prompt_parser.get_prompt(key=data_dict.MENU_INQUIRY)
        
        # 2. 利用文本嵌入模型（作用:利用语义从向量数据库找相似性菜品）
        similar_list = VectorQueryDao.similarity_search(pinecone_connect=pinecone_connect, query=query,
                                                          top_k=data_dict.MAX_MATCH_COUNT)
        # 3. 获取菜品信息
        content_list = []
        id_list = []
        for similar in similar_list:
            content = similar.get("content")
            index = similar.get("id")
            
            content_list.append(content)
            id_list.append(index)
        
        # 4. 构建完整查询
        if content_list:
            context = "\n".join(content_list)
            full_query = (f"当前从向量数据库中检索到的菜品信息:\n{context}\n\n"
                          f"当前用户问题:\n{query}\n\n,请基于以上检索到的菜品信息，回答来用户提出的相关问题")
        else:
            full_query = f"暂无相关菜品信息:\n\n当前用户问题:\n{query}\n\n,请基于一般的菜品知识信息，回答来用户提出的相关问题"
        
        # 5.调用模型(分析总结：context：宫爆鸡丁 麻婆豆腐 query：推荐宫爆鸡丁  instruction：“”)
        response = CloudModelDao.get_assistant_answer(cloud_model=cloud_model, query=full_query,
                                                      instruction=instruction)
        # 6. 封装字典结构返回
        result = { "recommendation": response.get("content"), "menu_ids": id_list }
        return result
    except Exception as e:
        raise ToolException(f"菜品咨询处理失败:{e}")


@tool
def delivery_check_tool(address: str, transport: int) -> str:
    """
        配送范围检查工具
    
        检查指定地址是否在配送范围内，并提供距离信息。
    
        Args:
            address  : 配送地址
            transport: 距离计算方式 (1=步行距离, 2=骑行距离, 3=驾车距离)
        
        Returns:
            str: 配送检查结果的格式化信息
    
        Raises:
            ToolException: 当配送检查失败时
    """
    
    try:
        # 1. 获取配送地点的坐标
        url = AmapConfig.GEO_URL
        coordinates_info = AmapDao.geocode_address(amap_map=amap_map, url=url, address=address)
        location = coordinates_info.get("location")
        
        # 2. 获取距离
        path_type = data_dict.PATH_MODE.get(transport, 0)
        path_url = AmapConfig.PATH_URL.get(path_type)
        params = {"origin": data_dict.DINNER_COORDINATES, "destination": location}
        
        distance_info = AmapDao.calculate_distance(amap_map=amap_map, url=path_url, params=params)
        
        if distance_info["success"]:
            distance = distance_info.get("distance")
            in_range = distance < data_dict.MAX_DISTANCE
            
            status_text = "✅ 可以配送" if in_range else "❌ 超出配送范围"
            
            response = (f"配送信息查询结果：\n配送地址：{coordinates_info.get('format_address')}\n"
                        f"配送距离：{round(distance / 1000, 2)}公里 (骑电车)\n配送状态：{status_text}")
        else:
            response = f"❌ 配送查询失败"
        return response
    except Exception as e:
        raise ToolException(f"配送范围检查失败:{e}")


smart_restaurant_assistant = SmartRestaurantAssistant()


if __name__ == '__main__':
    # ass = general_inquiry.invoke({"query": "请问您们餐厅的营业时间是什么时候"})
    # print(f"general_inquiry = {ass}")
    #
    # menu = menu_inquiry.invoke({"query": "请给我推荐一些素食的菜品"})
    # print(f"menu_inquiry = {menu}")
    #
    # delivery = delivery_check_tool.invoke({"address": "请问海淀区清华大学能配送到嘛?", "transport": 2})
    # print(f"delivery_check_tool = {delivery}")
    
    assistant = SmartRestaurantAssistant()
    response = assistant.invoke(user_query="请问您们餐厅的营业时间是什么时候")
    print(f"response = {response}")
