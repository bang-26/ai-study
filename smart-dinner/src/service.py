#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  service 
    CreateTime     ：  2026-07-18 10:35:41 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from re import match
from config import AmapConfig
from dao import DinnerDao, VectorQueryDao, AmapDao, CloudModelDao
from entry import DeliveryResponse, ChatResponse
from init import data_dict, sql_parser, prompt_parser, mysql_connect, pinecone_connect, amap_map, cloud_model
from agent import SmartRestaurantAssistant


# 点餐
class DinnerService:
    # 获取所有的菜单
    @staticmethod
    def get_menu_list():
        sql_name = data_dict.GET_AVAILABLE_DISHES
        menu_list = DinnerDao.get_all_menu(mysql_connect=mysql_connect, sql_name=sql_name, sql_parser=sql_parser)
        menu_info_list = DinnerDao.format_menu_list(menu_list=menu_list, data_dict=data_dict)
        return menu_info_list
    
    @staticmethod
    def get_menu_string():
        sql_name = data_dict.GET_AVAILABLE_DISHES
        menu_list = DinnerDao.get_all_menu(mysql_connect=mysql_connect, sql_name=sql_name, sql_parser=sql_parser)
        menu_string = DinnerDao.format_menu_string(menu_list=menu_list, data_dict=data_dict)
        return menu_string


# 向量查询处理
class VectorQueryService:
    @staticmethod
    def async_data():
        menu_string = DinnerService.get_menu_string()
        VectorQueryDao.upsert_menu(pinecone_connect=pinecone_connect, menu_data=menu_string)
    
    @staticmethod
    def similarity_search(query: str) -> list[dict]:
        top_k = data_dict.MAX_MATCH_COUNT
        similarity_list = VectorQueryDao.similarity_search(pinecone_connect=pinecone_connect, query=query, top_k=top_k)
        return similarity_list
    
    @staticmethod
    def search_with_ids(query: str) -> dict:
        similarity_list = VectorQueryService.similarity_search(query=query)
        
        content_list = []
        id_list = []
        score_list = []
        pattern = r"菜品ID(\d)"
        
        for similarity in similarity_list:
            content = similarity.get("content")
            content_list.append(content)
            
            score = similarity.get("score")
            score_list.append(score)
            
            is_match = match(pattern=pattern, string=content)
            if is_match:
                index = is_match.group(1)
            else:
                index = similarity.get("id")
            id_list.append(index)
            
        result_dict = \
            {
                "contents" : content_list,
                "ids": id_list,
                "scores" : score_list
            }
        
        return result_dict


# 距离查询
class AmapService:
    @staticmethod
    def get_geocode(address: str):
        url = AmapConfig.GEO_URL
        coordinates = AmapDao.geocode_address(amap_map=amap_map, url=url, address=address)
        return coordinates
    
    @staticmethod
    def calculate_distance(origin: str, destination: str, transport: int = 3):
        path_type = data_dict.PATH_MODE.get(transport, 0)
        path_url = AmapConfig.PATH_URL.get(path_type)
        
        params = { "origin": origin, "destination": destination }
        if transport == 3:
            params["show_fields"] = "cost"
        
        response = AmapDao.calculate_distance(amap_map=amap_map, url=path_url, params=params)
        return response
    
    @staticmethod
    def verify_range(address: str, transport: int = 3):
        result = DeliveryResponse(success=False, in_range=False, distance=0.0, formatted_address=address,
                                  duration=0.0, message="", travel_mode=transport, input_address=address)
                
        coord = AmapService.get_geocode(address=address)
        
        destination = coord.get("location")
        distance_info = AmapService.calculate_distance(origin=data_dict.DINNER_COORDINATES,
                                                       destination=destination, transport=transport)
        
        distance = distance_info.get("distance", None)
        if isinstance(distance, int):
            result.in_range = distance <= data_dict.MAX_DISTANCE
            result.distance = round(distance / 1000, 2)
            result.duration = distance_info.get("duration")
            result.formatted_address = coord.get("format_address")
            result.message = (f"配送地址：{result.formatted_address}\n配送距离：{result.distance}公里\n"
                              f"配送时间：{result.duration}min\n"
                              f"配送状态：{'在配送范围内' if result.in_range else '超出配送范围'}")
        else:
            result.message = "配送范围服务查询失败"
        return result
    

# 大语言模型使用
class ChatService:
    @staticmethod
    def get_assistant(prompt: str, instruction: str = None) -> ChatResponse:
        result = ChatResponse(success=False, query=prompt, response="")
        
        if instruction is None:
            instruction = prompt_parser.get_prompt(key=data_dict.ADAPT_PARSER)
        
        response = CloudModelDao.get_assistant_answer(cloud_model=cloud_model, query=prompt, instruction=instruction)
        
        if response.get("success"):
            result.success = True
            result.response = response.get("content")
        else:
            result.response = "查询失败"
        return result
    
    @staticmethod
    def chat(query: str) -> ChatResponse:
        answer = SmartRestaurantAssistant().invoke(user_query=query)
        recom = answer.get("recommendation", "")
        ids = answer.get("menu_ids", [])
        result = ChatResponse(success=False, query=query, response=str(answer), recommendation=recom, menu_ids=ids)
        return result
    

if __name__ == '__main__':
    from config import MysqlConfig, PineConeConfig, AmapConfig, CloudModelConfig
    
    # mysql = MysqlConnection(conf=MysqlConfig())
    # mysql.connect()
    
    # menus = DinnerService.get_menu_list(mysql_connect=mysql)
    # print(f"menu_list = {menus}")
    #
    # menu_str = DinnerService.get_menu_string(mysql_connect=mysql)
    # print(f"menu_string = {menu_str}")
    
    # pine = PineConeConnection(conf=PineConeConfig())
    # pine.connect()
    
    # VectorQueryService.async_data(mysql_connect=mysql, pinecone_connect=pine)
    
    # similarities = VectorQueryService.similarity_search(pinecone_connect=pine, query="湘菜")
    # for result in similarities:
    #     print(f"result = {result}")
    
    # similarities = VectorQueryService.search_with_ids(pinecone_connect=pine, query="湘菜")
    # for key, value in similarities.items():
    #     print(f"{key} =====> {value}")
    #
    # pine.close()
    # mysql.close()
    
    # amap = GaodeMap(conf=AmapConfig())
    # for adress in ["武汉大学", "清华大学", "北京大学", "安徽信息工程学院", "中原工学院", "河南理工大学"]:
    #     codes = AmapService.get_geocode(gaode_map=amap, address=adress)
    #     print(f"codes = {codes}")
    #
    # for o, d in [("114.364514,30.536243", "119.416425,32.203075"),("116.310918,39.992873", "117.019194,31.743191")]:
    #     res = AmapService.calculate_distance(gaode_map=amap, origin=o, destination=d, transport=3)
    #     print(f"res = {res}")
    # for adress in ["湖北省武汉市武昌区武汉大学", "北京市昌平区温都水城", "海淀区清华大学"]:
    #     for transport in [2, 3]:
    #         res = AmapService.verify_range(gaode_map=amap, address=adress, transport=transport)
    #         print(f"transport = {transport} =====> message = {res.get('message')}")
    
    res = ChatService.get_assistant(prompt="我想吃四川菜")
    print(f"response = {res}")
