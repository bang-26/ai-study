#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  smart-dinner  
    FileName       ：  dao 
    CreateTime     ：  2026-07-18 10:36:03 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DataDict, BaiLianConfig, AmapConfig
from connect import MysqlConnection, PineConeConnection, BailianConnect, AmapMap, CloudModelConnect
from utils import SqlParser

bailian = BailianConnect(conf=BaiLianConfig())


# 点餐数据处理
class DinnerDao:
    # 获取所有菜品信息
    @staticmethod
    def get_all_menu(mysql_connect: MysqlConnection, sql_name: str, sql_parser: SqlParser) -> list[dict]:
        query = sql_parser.get_sql(key=sql_name)
        menu_list = mysql_connect.query_data(query=query)
        return menu_list
        
    # 拼接菜单信息
    @staticmethod
    def format_menu_string(menu_list: list, data_dict: DataDict) -> str:
        menu_string_list = []
        for menu in menu_list:
            # 1. 格式化辣度级别
            spice_level = menu.get("spice_level")
            spice_format = data_dict.SPICE_LEVEL.get(spice_level, data_dict.SPICE_LEVEL_DEFAULT)
            
            # 2. 格式化是否是素食
            is_vegetarian = menu.get("is_vegetarian")
            vegetarian_format = data_dict.IS_VEGETARIAN.get(is_vegetarian, data_dict.VEGETARIAN_DEFAULT)
            
            # 3. 格式化菜品描述
            description_format = menu.get("description", data_dict.DESCRIPTION_DEFAULT).strip()
            
            # 4. 格式化主要食材
            main_ingredients_format = menu.get("main_ingredients", data_dict.MAIN_INGREDIENTS_DEFAULT).strip()
            
            # 5. 格式化过敏原
            allergies_format = menu.get("allergens", data_dict.ALLERGIES_DEFAULT).strip()
            
            # 6. 拼接菜品结构为字符串
            result = (f"菜品ID:{menu.get('id')}|菜品名称:{menu.get('dish_name')}|价格:￥{menu.get('price'):.2f}|"
                      f"菜品描述:{description_format}|分类:{menu.get('category')}|辣度:{spice_format}|"
                      f"口味:{menu.get('flavor')}|主要食材:{main_ingredients_format}|烹饪方法:{menu.get('cooking_method')}|"
                      f"素食:{vegetarian_format}|过敏源:{allergies_format}")
            menu_string_list.append(result)
        menu_string = "\n".join(menu_string_list)
        return menu_string
    
    # 获取前端菜品展示信息
    @staticmethod
    def format_menu_list(menu_list: list, data_dict: DataDict) -> list[dict]:
        menu_dict_list = []
        if not menu_list:
            return menu_dict_list
        
        for menu in menu_list:
            item = \
                {
                    "id"              : menu['id'],
                    "dish_name"       : menu['dish_name'],
                    "price"           : float(menu['price']),
                    "formatted_price" : f"¥{menu['price']:.2f}",
                    "description"     : menu['description'] or "暂无描述",
                    "category"        : menu['category'],
                    "spice_level"     : menu['spice_level'],
                    "spice_text"      : data_dict.SPICE_LEVEL.get(menu['spice_level'], data_dict.SPICE_LEVEL_DEFAULT),
                    "flavor"          : menu['flavor'] or "暂无口味",
                    "main_ingredients": menu['main_ingredients'] or "暂无主要食材",
                    "cooking_method"  : menu['cooking_method'] or "暂无烹饪方法",
                    "is_vegetarian"   : bool(menu['is_vegetarian']),
                    "vegetarian_text" : "是" if menu['is_vegetarian'] else "否",
                    "allergens"       : menu['allergens'] if menu['allergens'] and menu['allergens'].strip() else "暂无过敏原",
                    "is_available"    : bool(menu['is_available'])
                }
            menu_dict_list.append(item)
        return menu_dict_list


# 向量查询数据处理
class VectorQueryDao:
    # 批量更新索引
    @staticmethod
    def upsert_menu(pinecone_connect: PineConeConnection, menu_data: str, batch_size: int = 30,
                    clear_existing: bool = True) -> None:
        # 0. 清空索引
        if clear_existing:
            pinecone_connect.clear_data()
        
        # 1. 定义文本分词器
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=0, separators=["\n"],
                                                       length_function=len)
        # 2. 切分数据
        menu_data_chunks = text_splitter.split_text(text=menu_data)
        
        # 3. 进行向量化
        vector_list = bailian.query(text=menu_data_chunks)
        
        # 4. 插入向量数据
        data_list = []
        for line, chunk in enumerate(menu_data_chunks, 1):
            # 4.1 准备元数据
            menu_data_metadata = \
                {
                    "content"    : chunk,
                    "line_number": line,
                    "dash_id"    : f"菜品ID:{line}",
                    "type"       : "menu_item",
                }
            
            # 4.2 构造数据
            batch = (str(line), vector_list[line - 1], menu_data_metadata)
            data_list.append(batch)
            
            # 4.3 判断是否需要批量插入
            if len(data_list) >= batch_size:
                pinecone_connect.upsert_data(vector_list=data_list)
                data_list = []
            
        # 5. 批量插入向量数据
        if len(data_list) > 0:
            pinecone_connect.upsert_data(vector_list=data_list)
            
    # 相似性检索
    @staticmethod
    def similarity_search(pinecone_connect: PineConeConnection, query: str, top_k: int = 2) -> list[dict]:
        vector = bailian.query(text=query)
        similarity_list = pinecone_connect.similarity_search(vector=vector, top_k=top_k)
        
        result_list = []
        for similarity in similarity_list:
            result = \
                {
                    "id"         : similarity.id,
                    "score"      : similarity.score,
                    "content"    : similarity.metadata.get("content"),
                    "line_number": similarity.metadata.get("line_number"),
                }
            result_list.append(result)
        return result_list


class AmapDao:
    # 地址转换为经纬度
    @staticmethod
    def geocode_address(amap_map: AmapMap, url: str, address: str) -> dict:
        response = amap_map.multi_request(url=url, params={"address": address})
        
        result = {"success": False, "message": "请求失败"}
        if response.get("status") == "1":
            geocode = response.get("geocodes")[0]
            format_address = geocode.get("formatted_address")
            location = geocode.get("location")
            print(f"=============== 高德地图 地址转换成功 ===============")
            
            result = \
                {
                    "success"       : True,
                    "message"       : "请求成功",
                    "format_address": format_address,
                    "location"      : location
                }
        else:
            result["message"] = response.get("info")
        
        return result

    # 获取两点间的距离规划
    @staticmethod
    def calculate_distance(amap_map: AmapMap, url: str, params: dict) -> dict:
        response = amap_map.multi_request(url=url, params=params)
        
        if response.get("status") != "1":
            result = { "success": False, "message": response.get("info") }
        else:
            path = response.get("route").get("paths")[0]
            distance = path.get("distance")
            duration = path.get("duration")
            if not duration:
                duration = path.get("cost").get("duration")
            result = { "success": True, "distance": eval(distance), "duration": eval(duration) }
            print(f"=============== 高德地图 距离规划 ===============")
        return result
    

class CloudModelDao:
    @staticmethod
    def get_assistant_answer(cloud_model: CloudModelConnect, query: str, instruction: str) -> dict:
        result = {}
        try:
            response = cloud_model.query(query=query, instruction=instruction)
            content = response.content
            result = \
                {
                    "success": True,
                    "message": "请求成功",
                    "content": content
                }
            print(f"=============== 模型响应 ===============")
        except Exception as e:
            result = \
                {
                    "success": False,
                    "message": "请求失败",
                    "content": e
                }
        finally:
            return result
        
    
if __name__ == '__main__':
    from config import PathConfig, MysqlConfig, SQLConfig, PineConeConfig, CloudModelConfig
    sql_parser = SqlParser(path=PathConfig.SQL_PATH)
    sql_key = SQLConfig.GET_AVAILABLE_DISHES
    data_dict = DataDict()
    
    with MysqlConnection(conf=MysqlConfig()) as mysql:
        menus = DinnerDao.get_all_menu(mysql_connect=mysql, sql_name=sql_key, sql_parser=sql_parser)
    
    menu_string = DinnerDao.format_menu_string(menu_list=menus, data_dict=data_dict)
    # print(f"menu_string = {menu_string}")
    
    menu_list = DinnerDao.format_menu_list(menu_list=menus, data_dict=data_dict)
    # print(f"menu_list = {menu_list}")
    
    pine = PineConeConnection(conf=PineConeConfig())
    pine.connect()
    VectorQueryDao.upsert_menu(pinecone_connect=pine, menu_data=menu_string)
    results = VectorQueryDao.similarity_search(pinecone_connect=pine, query="湘菜", top_k=2)
    for result in results:
        print(f"result = {result}")
    pine.close()
