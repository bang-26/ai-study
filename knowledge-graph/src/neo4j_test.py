#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  knowledge-graph  
    FileName       ：  neo4j_test 
    CreateTime     ：  2026-07-03 23:04:29 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(self, uri="bolt://****************:7687", user="****************", password="****************"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def query(self, cypher, params=None):
        with self.driver.session() as session:
            return session.run(cypher, params or {}).data()

    def get_all_nodes(self):
        return self.query("MATCH (n) RETURN n, labels(n) AS labels, id(n) AS node_id LIMIT 200")

    def get_all_relationships(self):
        return self.query("MATCH ()-[r]->() RETURN r, type(r) AS rel_type, id(r) AS rel_id LIMIT 200")

    def get_graph_summary(self):
        nodes = self.query("MATCH (n) RETURN count(n) AS total_nodes")
        rels = self.query("MATCH ()-[r]->() RETURN count(r) AS total_rels")
        labels = self.query("MATCH (n) RETURN DISTINCT labels(n) AS label")
        rel_types = self.query("MATCH ()-[r]->() RETURN DISTINCT type(r) AS rel_type")
        return {
            "total_nodes": nodes[0]["total_nodes"],
            "total_rels": rels[0]["total_rels"],
            "node_labels": [r["label"] for r in labels],
            "rel_types": [r["rel_type"] for r in rel_types],
        }


if __name__ == "__main__":
    client = Neo4jClient(uri="bolt://****************:7687", user="****************", password="****************")

    print("=" * 60)
    print("📊 图数据库概览")
    print("=" * 60)
    summary = client.get_graph_summary()
    print(f"节点总数: {summary['total_nodes']}")
    print(f"关系总数: {summary['total_rels']}")
    print(f"节点标签: {summary['node_labels']}")
    print(f"关系类型: {summary['rel_types']}")

    print("\n" + "=" * 60)
    print("🔵 所有节点")
    print("=" * 60)
    for record in client.get_all_nodes():
        node = record["n"]
        labels = record["labels"]
        node_id = record["node_id"]
        props = dict(node)
        print(f"[ID:{node_id}] 标签: {labels}  属性: {props}")
    client.close()
