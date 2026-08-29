#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  graph 
    CreateTime     ：  2026-08-12 17:07:51 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""

from langgraph.graph import StateGraph, START, END

from query_node import node_item_name_confirm, node_search_embedding, node_search_embedding_hyde
from query_node import node_web_search_mcp, node_rrf, node_rerank, node_answer_output
from state import ImportGraphState, QueryGraphState
from import_node import node_entry, node_pdf_to_md, node_md_img, node_document_split, route_after_entry
from import_node import node_item_name_recognition, node_bge_embedding, node_import_milvus


# 生成导入知识图谱的流程图
def generate_import_graph(state: ImportGraphState):
    # 1. 初始化 Langgraph 状态图
    work_flow = StateGraph(state_schema=state)
    
    # 2. 注册所有的子节点
    work_flow.add_node(node="node_entry", action=node_entry)
    work_flow.add_node(node="node_pdf_to_md", action=node_pdf_to_md)
    work_flow.add_node(node="node_md_img", action=node_md_img)
    work_flow.add_node(node="node_document_split", action=node_document_split)
    work_flow.add_node(node="node_item_name_recognition", action=node_item_name_recognition)
    work_flow.add_node(node="node_bge_embedding", action=node_bge_embedding)
    work_flow.add_node(node="node_import_milvus", action=node_import_milvus)
    
    # 3. 设置入口节点
    work_flow.set_entry_point(key="node_entry")
    
    # 添加条件边
    path_map = \
        {
            "node_pdf_to_md": "node_pdf_to_md",
            "node_md_img"   : "node_md_img",
            END             : END
        }
    work_flow.add_conditional_edges(source="node_entry", path=route_after_entry, path_map=path_map)
    
    # 5. 定义静态边
    work_flow.add_edge(start_key="node_pdf_to_md", end_key="node_md_img")
    work_flow.add_edge(start_key="node_md_img", end_key="node_document_split")
    work_flow.add_edge(start_key="node_document_split", end_key="node_item_name_recognition")
    work_flow.add_edge(start_key="node_item_name_recognition", end_key="node_bge_embedding")
    work_flow.add_edge(start_key="node_bge_embedding", end_key="node_import_milvus")
    work_flow.add_edge(start_key="node_import_milvus", end_key=END)
    
    # 6. 编译图节点对象即可
    file_import_graph = work_flow.compile()
    
    return file_import_graph


# 生成查询知识图谱的流程图
def generate_query_graph(state: QueryGraphState):
    query_flow = StateGraph(state_schema=state)
    
    query_flow.add_node(node="node_item_name_confirm", action=node_item_name_confirm)
    query_flow.add_node(node="node_search_embedding", action=node_search_embedding)
    query_flow.add_node(node="node_search_embedding_hyde", action=node_search_embedding_hyde)
    query_flow.add_node(node="node_web_search_mcp", action=node_web_search_mcp)
    query_flow.add_node(node="node_rrf", action=node_rrf)
    query_flow.add_node(node="node_rerank", action=node_rerank)
    query_flow.add_node(node="node_answer_output", action=node_answer_output)
    
    query_flow.set_entry_point("node_item_name_confirm")
    
    path_map = \
        {
            "node_answer_output"        : "node_answer_output",
            "node_search_embedding"     : "node_search_embedding",
            "node_search_embedding_hyde": "node_search_embedding_hyde",
            "node_web_search_mcp"       : "node_web_search_mcp"
        }
    query_flow.add_conditional_edges(source="node_item_name_confirm", path=__route_to_item_confirm,
                                     path_map=path_map)
    
    query_flow.add_edge(start_key="node_search_embedding", end_key="node_rrf")
    query_flow.add_edge(start_key="node_search_embedding_hyde", end_key="node_rrf")
    query_flow.add_edge(start_key="node_web_search_mcp", end_key="node_rrf")
    query_flow.add_edge(start_key="node_rrf", end_key="node_rerank")
    query_flow.add_edge(start_key="node_rerank", end_key="node_answer_output")
    query_flow.add_edge(start_key="node_answer_output", end_key=END)
    
    query_graph = query_flow.compile()
    return query_graph


def __route_to_item_confirm(state: QueryGraphState):
    if state.get('answer'):
        return "node_answer_output"
    return "node_search_embedding", "node_search_embedding_hyde", "node_web_search_mcp"
    
    
file_import_graph = generate_import_graph(state=ImportGraphState)
query_graph = generate_query_graph(state=QueryGraphState)


if __name__ == '__main__':
    from os.path import join, dirname, abspath
    from config import PathConfig
    from logger import logger
    from state import create_default_state
    
    logger.info("===== 开始执行知识图谱导入全流程测试 =====")
    pdf_name = "B3-211H.pdf"
    pdf_path = abspath(path=f"{PathConfig.UPDATE_DIR}/{pdf_name}")
    out_path = PathConfig.OUTPUT_DIR
    logger.info(f"pdf_path：{pdf_path}，out_path：{out_path}")
    
    test_state = create_default_state(task_id="test-import-1", local_file_path=pdf_path,
                                      local_dir=out_path, is_pdf_read_enabled=False,
                                      user_id="test_user", is_md_read_enabled=False)
    
    state = ImportGraphState(test_state)
    
    logger.info("entry ==> pdf2md ==> md_img ==> split ==> item_name ==> embedding ==> milvus ==> kg")
    file_import_graph = generate_import_graph(state=state)
    results = file_import_graph.stream(input=test_state, stream_mode="values")
    
    final_state = None
    for step in results:
        current_node = list(step.keys())[-1] if step else "未知节点"
        logger.info(f"✅ 节点执行完成：{current_node}")
        final_state = step
    
    if final_state:
        logger.info("=" * 100)
        chunks = final_state.get("chunks", [])
        chunk_count = len(chunks)
        md_content = final_state.get("md_content", "")[:150]  # MD内容前150字符
        has_embedding = all("dense_vector" in c and "sparse_vector" in c for c in chunks) if chunks else False
        has_chunk_id = all("chunk_id" in c for c in chunks) if chunks else False
        kg_id = final_state.get("kg_id", "未生成")  # KG导入生成的ID（按实际业务字段调整）
        
        logger.info(f"📄 PDF 转 MD 内容预览（前 150 字符）：{md_content}...")
        logger.info(f"📝 文档切分总切片数：{chunk_count}")
        logger.info(f"🔍 所有切片是否完成向量化：{'是' if has_embedding else '否'}")
        logger.info(f"🗄️  所有切片是否完成 Milvus 入 库（含 chunk_id）：{'是' if has_chunk_id else '否'}")
        logger.info(f"🧠 知识图谱导入 ID：{kg_id}")
        logger.info(f"📂 最终状态包含的核心键：{list(final_state.keys())}")
        
    logger.info("===== 知识图谱导入全流程测试结束 =====")
    
