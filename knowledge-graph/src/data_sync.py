#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph  
    FileName       ：  data_sync 
    CreateTime     ：  2026-07-06 13:59:36 
    Author         ：  issac  
    PythonCompiler ：  3.13.9 
    IDE            ：  PyCharm-2025.3.4 
    Description    ：  文件描述 
====================================================================================================
"""

from commerce import GraphModel
from connnect import MysqlConnection, Neo4jConnection
from config import MysqlConfig, Neo4jConfig


# noinspection SqlDialectInspection
class TableSynchronizer:
    def __init__(self):
        self.mysql = MysqlConnection(host=MysqlConfig.HOST, port=MysqlConfig.PORT, user=MysqlConfig.USER,
                                     password=MysqlConfig.PASSWORD, database=MysqlConfig.DATABASE)
        self.neo4j = Neo4jConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                                     password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
    
    def sync_base_category1(self):
        sql = """
              select id, name
              from base_category1 \
              """
        
        self.neo4j.write_nodes(node_label="Category1", node_list=self.mysql.query_data(sql))
    
    def sync_base_category2(self):
        sql = """
              select id, name
              from base_category2 \
              """
        self.neo4j.write_nodes(node_label="Category2", node_list=self.mysql.query_data(sql))
    
    def sync_base_category3(self):
        sql = """
              select id, name
              from base_category3 \
              """
        self.neo4j.write_nodes(node_label="Category3", node_list=self.mysql.query_data(sql))
    
    def sync_category1_category2(self):
        sql = """
              select c2.id as start_id, c2.category1_id as end_id
              from base_category2 c2 \
              """
        
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="Category2",
                                   end="Category1",
                                   relation_list=relation_list,
                                   relation_type='Belong')
    
    def sync_category2_category3(self):
        sql = """
              select c3.id as start_id, c3.category2_id as end_id
              from base_category3 c3 \
              """
        
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="Category3",
                                   end="Category2",
                                   relation_list=relation_list,
                                   relation_type='Belong')
    
    def sync_base_attr(self):
        sql = """
              select id, attr_name as name
              from base_attr_info \
              """
        self.neo4j.write_nodes(node_label="BaseAttr", node_list=self.mysql.query_data(sql))
    
    def sync_base_attr_category(self):
        sql = """
              select id end_id, category_id start_id, category_level
              from base_attr_info \
              """
        relation_list = self.mysql.query_data(sql)
        base_attr_category3 = [
            {
                "start_id": r['start_id'],
                "end_id"  : r['end_id']
            } for r in relation_list if r['category_level'] == 3
        ]
        self.neo4j.write_relations(start="Category3",
                                   end="BaseAttr",
                                   relation_list=base_attr_category3,
                                   relation_type='Have')
        
        base_attr_category2 = [
            {
                "start_id": r['start_id'],
                "end_id"  : r['end_id']
            } for r in relation_list if r['category_level'] == 2
        ]
        self.neo4j.write_relations(start="Category2",
                                   end="BaseAttr",
                                   relation_list=base_attr_category2,
                                   relation_type='Have')
        
        base_attr_category1 = [
            {
                "start_id": r['start_id'],
                "end_id"  : r['end_id']
            } for r in relation_list if r['category_level'] == 1
        ]
        self.neo4j.write_relations(start="Category1",
                                   end="BaseAttr",
                                   relation_list=base_attr_category1,
                                   relation_type='Have')
    
    def sync_base_attr_value(self):
        sql = """
              select id, value_name name
              from base_attr_value \
              """
        self.neo4j.write_nodes(node_label="BaseAttrValue", node_list=self.mysql.query_data(sql))
    
    def sync_base_attr_value_attr(self):
        sql = """
              select id end_id, attr_id start_id
              from base_attr_value \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="BaseAttr",
                                   end="BaseAttrValue",
                                   relation_list=relation_list,
                                   relation_type='Have')
    
    def sync_spu(self):
        sql = """
              select id, spu_name name
              from spu_info \
              """
        self.neo4j.write_nodes(node_label="SPU", node_list=self.mysql.query_data(sql))
    
    def sync_spu_category3(self):
        sql = """
              select id start_id, category3_id end_id
              from spu_info \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SPU",
                                   end="Category3",
                                   relation_list=relation_list,
                                   relation_type='Belong')
    
    def sync_sale_attr(self):
        sql = """
              select id, sale_attr_name name
              from spu_sale_attr \
              """
        self.neo4j.write_nodes(node_label="SaleAttr", node_list=self.mysql.query_data(sql))
    
    def sync_sale_attr_spu(self):
        sql = """
              select id end_id, spu_id start_id
              from spu_sale_attr \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SPU",
                                   end="SaleAttr",
                                   relation_list=relation_list,
                                   relation_type='Have')
    
    def sync_sale_attr_value(self):
        sql = """
              select id, sale_attr_value_name name
              from spu_sale_attr_value \
              """
        self.neo4j.write_nodes(node_label="SaleAttrValue", node_list=self.mysql.query_data(sql))
    
    def sync_sale_attr_value_attr(self):
        sql = """
              select a.id start_id, v.id end_id
              from spu_sale_attr_value v
                       join spu_sale_attr a on v.spu_id = a.spu_id and v.base_sale_attr_id = a.base_sale_attr_id \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SaleAttr",
                                   end="SaleAttrValue",
                                   relation_list=relation_list,
                                   relation_type='Have')
    
    def sync_sku(self):
        sql = """
              select id, sku_name name
              from sku_info \
              """
        self.neo4j.write_nodes(node_label="SKU", node_list=self.mysql.query_data(sql))
    
    def sync_sku_base_attr_value(self):
        sql = """
              select sku_id start_id, value_id end_id
              from sku_attr_value \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SKU",
                                   end="BaseAttrValue",
                                   relation_list=relation_list,
                                   relation_type='Have')
    
    def sync_sku_sale_attr_value(self):
        sql = """
              select sku_id start_id, sale_attr_value_id end_id
              from sku_sale_attr_value \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SKU",
                                   end="SaleAttrValue",
                                   relation_list=relation_list,
                                   relation_type='Have')
    
    def sync_sku_spu(self):
        sql = """
              select id start_id, spu_id end_id
              from sku_info \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SKU",
                                   end="SPU",
                                   relation_list=relation_list,
                                   relation_type='Belong')
    
    def sync_base_trademark(self):
        sql = """
              select id, tm_name name
              from base_trademark \
              """
        self.neo4j.write_nodes(node_label="BaseTrademark", node_list=self.mysql.query_data(sql))
    
    def sync_base_trademark_spu(self):
        sql = """
              select id start_id, tm_id end_id
              from spu_info \
              """
        relation_list = self.mysql.query_data(sql)
        self.neo4j.write_relations(start="SPU",
                                   end="BaseTrademark",
                                   relation_list=relation_list,
                                   relation_type='Belong')


# 文本同步
# noinspection SqlDialectInspection
class TextSynchronizer:
    def __init__(self):
        self.mysql = MysqlConnection(host=MysqlConfig.HOST, port=MysqlConfig.PORT, user=MysqlConfig.USER,
                                     password=MysqlConfig.PASSWORD, database=MysqlConfig.DATABASE)
        self.neo4j = Neo4jConnection(host=Neo4jConfig.HOST, port=Neo4jConfig.PORT, user=Neo4jConfig.USER,
                                     password=Neo4jConfig.PASSWORD, database=Neo4jConfig.DATABASE)
        
    def sync_spu_desc(self):
        sql = """
              select id, description
              from spu_info
              """
        spu_desc = self.mysql.query_data(query=sql)
        
        spu_id_list = [spu['id'] for spu in spu_desc]
        description_list = [spu['description'] for spu in spu_desc]
        
        spu_entry_list = GraphModel().predict(description_list)
        
        node_list = []
        relation_list = []
        for id, entities in zip(spu_id_list, spu_entry_list):
            for index, entity in enumerate(entities):
                node = {"id": f"{id}-{index}", "name": entity}
                node_list.append(node)
                relationship = {"start_id": id, "end_id": f"{id}-{index}"}
                relation_list.append(relationship)
        print(f"node_list = {node_list}")
        print(f"relation_list = {relation_list}")
        self.neo4j.write_nodes(node_list=node_list, node_label='Tag')
        self.neo4j.write_relations(start='SPU', end='Tag', relation_list=relation_list, relation_type='Have')
        
    def close(self):
        self.mysql.close()
        self.neo4j.close()
        
        
if __name__ == '__main__':
    # Neo4jConfig.HOST = '****************'
    # Neo4jConfig.PASSWORD = '****************'
    
    table_sync = TableSynchronizer()
    # 同步分类系统
    table_sync.sync_base_category1()
    table_sync.sync_base_category2()
    table_sync.sync_base_category3()
    table_sync.sync_category1_category2()
    table_sync.sync_category2_category3()
    
    # 同步属性系统
    table_sync.sync_base_attr()
    table_sync.sync_base_attr_category()
    table_sync.sync_base_attr_value()
    table_sync.sync_base_attr_value_attr()
    
    # 同步SPU
    table_sync.sync_spu()
    table_sync.sync_spu_category3()
    
    # 同步销售属性
    table_sync.sync_sale_attr()
    table_sync.sync_sale_attr_spu()
    
    # 同步销售属性值
    table_sync.sync_sale_attr_value()
    table_sync.sync_sale_attr_value_attr()
    
    # 同步SKU
    table_sync.sync_sku()
    table_sync.sync_sku_spu()
    table_sync.sync_sku_base_attr_value()
    table_sync.sync_sku_sale_attr_value()
    
    # 同步品牌
    table_sync.sync_base_trademark()
    table_sync.sync_base_trademark_spu()

    text_sync = TextSynchronizer()
    text_sync.sync_spu_desc()
    text_sync.close()
