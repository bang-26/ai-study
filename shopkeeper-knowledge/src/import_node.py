#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName    ：  shopkeeper-knowledge  
    FileName       ：  node 
    CreateTime     ：  2026-08-12 17:07:40 
    Author         ：  lihuashiyu 
    Email          ：  lihuashiyu@github.com 
    PythonCompiler ：  3.12.10 
    IDE            ：  PyCharm 2024.3.6  
    Version        ：  1.0 
    Description    ：  文件描述 
====================================================================================================
"""


from os import environ
from os.path import abspath

environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from pathlib import Path
from sys import _getframe
from langgraph.graph import StateGraph, END, START

from config import PathConfig, app_config, DataDict
from process import ImageProcess, MineruProcess, DocumentProcess, RecognitionProcess, ContentProcess
from logger import logger
from state import ImportGraphState, create_default_state
from util import task_util, FileUtil, CompressionUtil


# 入口节点
def node_entry(state: ImportGraphState) -> ImportGraphState:
    """
    入口节点（node_entry）：解析入口参数，判定文件类型并初始化流程状态。
    
        本节点是工作流的 Entry Point，负责接收外部输入（local_file_path）、校验参数、
        识别文件类型（md / pdf）、设置后续分支所需的状态字段，并上报任务开始/结束埋点。
        
    Args:
        state (ImportGraphState): 当前图状态，核心字段：
            - local_file_path (str): 待解析文件的绝对路径，必传；
            - md_path / pdf_path (str): 按文件类型写入的解析路径；
            - is_md_read_enabled / is_pdf_read_enabled (bool): 路由分支开关；
            - file_title (str): 去掉后缀的文件名，用于主体识别失败的兜底。
            
    Returns:
        ImportGraphState: 更新后的状态，供条件边 route_after_entry 进行路由。
        
    Notes:
        1. 进入/结束节点时输出日志，并通过 add_running_task / add_done_task 上报任务埋点；
        2. 若 local_file_path 为空或不是 md / pdf，直接返回 state（由路由节点判定走向 END）；
        3. 文件名统一使用 Path(...).stem 提取，兼容多后缀文件（如 aa.bb.tar.gz）。
    """
    # 1. 进入节点的日志输出 【节点 + 核心参数】 记录任务状态（给前端推送信息）
    function_name = _getframe().f_code.co_name
    logger.info(f">>> [{function_name}]开始执行了！")
    task_util.add_running_task(state['task_id'], function_name)
    
    # 2. 进行必要的非空校验判定
    local_file_path = state['local_file_path']
    if not local_file_path:
        logger.error(f"[{function_name}]检查发现没有输入文件，无法继续解析！！")
        return state
    
    # 3. 判定并且完成 state 属性赋值
    if local_file_path.endswith(".md"):
        state['is_md_read_enabled'] = True
        state['md_path'] = local_file_path
    elif local_file_path.endswith(".pdf"):
        state['is_pdf_read_enabled'] = True
        state['pdf_path'] = local_file_path
    else:
        logger.error(f"[{function_name}]文件格式不是md,pdf，无法继续解析！！")
    
    file_title = FileUtil.get_file_name_without_suffix(file_path=local_file_path)
    state['file_title'] = file_title
    
    # 4. 结束节点的日志输出 【节点 + 核心参数】 记录任务状态（给前端推送信息）
    logger.info(f">>> [{function_name}] 执行结束了！")
    task_util.add_done_task(state['task_id'], function_name)
    
    return state
    

# PDF 转 MD 节点
def node_pdf_to_md(state: ImportGraphState) -> ImportGraphState:
    """PDF 转 Markdown 节点（node_pdf_to_md）：将 PDF 非结构化数据转为 Markdown 文本。

    本节点是 md 流程的核心转换节点，负责参数校验、调用 MinerU 解析、下载解压产物、
    读取 Markdown 内容并写入 state，全程包含日志与任务埋点，并通过 try/except 保证容错。

    Args:
        state (ImportGraphState): 当前图状态，需包含：
            - local_file_path (str): PDF 文件路径；
            - local_dir (str): 输出目录，可为空（自动使用默认值）。

    Returns:
        ImportGraphState: 更新后的状态，新增 md_path（解析出的 Markdown 路径）
            与 md_content（Markdown 文本内容）。

    Raises:
        Exception: 任意步骤失败时向上抛出，终止整个工作流。

    Notes:
        1. 进入/结束节点输出日志并上报任务埋点（add_running_task / add_done_task）；
        2. 复用 step_1_validate_paths、step_2_upload_and_poll、step_3_download_and_extract；
        3. 整体使用 try/except 包裹，异常时记录日志并重新抛出。
    """
    
    function_name = _getframe().f_code.co_name                       # 获取当前函数名
    logger.info(f">>> [{function_name}] 开始执行了！")  # 记录任务状态（给前端推送信息）
    task_util.add_running_task(state['task_id'], function_name)      # 记录任务状态（给前端推送信息）
    
    try:
        pdf_path, local_dir = __validate_path(state=state)           # 进行参数校验
        state['local_dir'] = local_dir                               # 主要处理下！是str类型
        
        mineru_process = MineruProcess(conf=app_config.mineru_config)
        url_info = mineru_process.get_parse_url(pdf_path_list=[pdf_path])    # 获取下载文件的地址
        
        # 下载文件 ==> 保存 zip 文件 ==> 解压文件 ==> 重命名文件 ==> 读取文件内容 ==> 返回文件内容
        for file_name, url in url_info.items():
            name = FileUtil.get_file_name_without_suffix(file_path=file_name)
            zip_path = f"{local_dir}/{name}.zip"                     # 创建 zip 文件路径
            mineru_process.save_zip_file(zip_url=url, file_path=zip_path)    # 保存 zip 文件
            
            # 解压文件
            extract_path = abspath(path=f"{local_dir}/{name}")
            CompressionUtil.unzip_file(zip_path=zip_path, extract_path=extract_path)
            
            # 将 full.md 重命名为 name.md
            md_path = abspath(path=f"{extract_path}/{name}.md")
            FileUtil.rename_path(src_path=f"{extract_path}/full.md", dst_path=md_path)
            
            # 给 md_path 地址进行赋值
            if FileUtil.judge_file_exists(file_path=md_path):
                state["md_path"] = md_path
            else:
                raise Exception(f"文件 {file_name} 解压后不存在 md 文件")
            
            content = FileUtil.read_text(file_path=md_path)          # 读取 md 文件内容
            state["md_content"] = content                            # 给 md_content 内容进行赋值
            
            logger.info(f"[{function_name}] 解析完成，结果为：{state}")
    except Exception as e:
        logger.error(f">>> [{function_name}] 使用 minerU 解析发生了异常，异常信息：{e}")
        raise                                                        # 终止工作流
    finally:
        task_id = state.get('task_id')                               # 获取任务ID
        task_util.add_done_task(task_id=task_id, node_name=function_name)  # 记录任务状态（给前端推送信息）
        logger.info(f">>> [{function_name}] 执行结束了！")
        
        return state


# 进行参数校验 （local_dir -》 给与默认值 | local_file_path完成字面意思的校验 -》 深入校验校验的文件是否真的存在）
def __validate_path(state: ImportGraphState) -> tuple[str, str]:
    """
    校验 PDF 路径与输出目录（PDF 转 MD 流程的第一步）。
        
        校验 pdf_path 是否有效，缺失时直接抛出异常；local_dir 未赋值时使用默认输出目录；
        同时校验路径是否存在，目录不存在时自动创建。
        
    Args:
        state (dict): 工作流状态，需包含：
            - pdf_path (str): 待转换 PDF 的路径；
            - local_dir (str): 输出目录，可为空（此时使用默认值 PROJECT_ROOT / "output"）。
            
    Returns:
        tuple[Path, Path]: 校验通过后的 (pdf_path, local_dir) 的 Path 对象。
        
    Raises:
        ValueError: pdf_path 为空或缺失时抛出。
        FileNotFoundError: pdf_path 指向的文件不存在时抛出。
    """
    
    logger.info(f">>> [validate_path] 在 md 转 pdf 下，开始进行文件格式校验！！")
    
    # 判断 pdf 文件的路径是否存在
    pdf_path = state.get('pdf_path')
    
    if not pdf_path:
        error_message = f"validate_path：检查发现 {pdf_path} 没有输入文件，无法继续解析！！"
        logger.error(error_message)
        raise ValueError(error_message)
    elif not FileUtil.judge_file_exists(pdf_path):
        error_message = f"validate_path：检查发现 {pdf_path} 不存在，请检查输入文件路径是否正确！！"
        logger.error(error_message)
        raise FileNotFoundError(error_message)
        
    local_dir = state.get('local_dir')
    if not local_dir:
        local_dir = PathConfig.OUTPUT_DIR
        logger.warning(f"validate_path：检查发现 local_dir 没有赋值，给与默认值：{local_dir}！")
        
    FileUtil.ensure_dir_exists(dir_path=local_dir)                   # 确保目录存在
    
    pdf_path = FileUtil.get_absolute_path(path=pdf_path)             # 获取绝对路径
    local_dir = FileUtil.get_absolute_path(path=local_dir)           # 获取绝对路径
    return pdf_path, local_dir

 
# 图片处理节点
def node_md_img(state: ImportGraphState) -> ImportGraphState:
    """
    图片处理节点（node_md_img）：处理 Markdown 中的图片资源并替换链接。
        
        扫描 Markdown 中的图片链接，将图片上传至 MinIO 对象存储，
        可选调用多模态模型生成图片描述，最后将 Markdown 中的图片链接替换为 MinIO URL。
        
    Args:
        state (ImportGraphState): 当前图状态，需包含 md_path 及 Markdown 文本内容。
        
    Returns:
        ImportGraphState: 更新后的状态，Markdown 中图片链接已替换为 MinIO URL。
        
    Notes:
        1. 扫描 Markdown 中的图片链接（本地相对路径或 Base64）；
        2. 上传图片到 MinIO，生成可访问的 URL；
        3.（可选）调用多模态模型为图片生成描述并追加到文本；
        4. 将原图片链接替换为 MinIO URL，保证渲染与检索效果。
    """
    
    function_name = _getframe().f_code.co_name
    logger.info(f">>> [{function_name}] 执行节点: {function_name} 开始执行了！")
    
    task_util.add_running_task(state.get('task_id'), function_name)
    
    # 1. 校验并且获取本次操作的数据
    md_path = state.get("md_path")                              # 获取 md 文件路径
    is_exist = FileUtil.judge_file_exists(file_path=md_path)    # 判断 md 文件是否存在
    
    if not is_exist:
        raise FileNotFoundError(f"md_path:{md_path} 文件不存在！")
    
    # 要读取 md_content
    if not state.get('md_content'):
        state['md_content'] = FileUtil.read_text(file_path=md_path)
        
    images_dir = FileUtil.get_file_dir(file_path=md_path) + "/images"
    if not FileUtil.judge_dir_exists(dir_path=images_dir):
        raise FileNotFoundError(f"{images_dir} 文件夹不存在！")
    
    # 2. 识别 md 中使用过的图片，采取做下一步（进行图片总结）
    image_path_list = ImageProcess.scan_images(dir_path=images_dir)
    usage_path_list = ImageProcess.query_image_context(image_list=image_path_list, content=state.get('md_content'))
    
    # 3. 进行图片内容的总结和处理 （视觉模型）
    image_summary_dict = ImageProcess.get_image_summary(image_info_list=usage_path_list)
    
    # 4. 上传图片到 minio 同时替换 md 中的图片 （描述 + url地址）
    md_file_name = FileUtil.get_file_name_without_suffix(file_path=md_path)
    upload_dir = f"{app_config.minio_config.image_folder}/{md_file_name}"
    content = ImageProcess.transform_images(content=state.get('md_content'), image_summary_dict=image_summary_dict,
                                            upload_dir=upload_dir)
    
    state['md_content'] = content
    
    # 5. 新的 md 内容替换和保存修改装
    md_dir = FileUtil.get_file_dir(file_path=md_path)
    new_md_path = f"{md_dir}/{md_file_name}_new.md"
    FileUtil.write_text(file_path=new_md_path, content=content)
    
    state['md_path'] = new_md_path
    
    task_util.add_done_task(state.get('task_id'), function_name)
    logger.info(f">>> [{function_name}] 执行结束！")
    
    return state


# 文档切割
def node_document_split(state: ImportGraphState) -> ImportGraphState:
    """文档切分节点（node_document_split）：将长文档递归切分为带元数据的 Chunk 列表。

    依据 Markdown 标题层级对文档进行递归切分，保证切块结构完整、语义连续，
    并对超长段落做二次切分，最终生成包含标题路径等元信息的 Chunk 列表。

    Args:
        state (ImportGraphState): 当前图状态，需包含 md_content（Markdown 文本）。

    Returns:
        ImportGraphState: 更新后的状态，新增切分后的 Chunk 列表。

    Notes:
        1. 优先基于 Markdown 标题层级（H1-H6）递归切分；
        2. 对超过阈值的段落进行二次切分，避免 Chunk 过长；
        3. 每个 Chunk 需携带 Metadata（如标题路径），供检索阶段使用。
    """
    
    function_name = _getframe().f_code.co_name
    logger.info(f">>> [{function_name}] 执行节点: {function_name} 开始执行了！")
    
    # 1. 参数校验 （材料是否完整）
    md_content = state['md_content']
    if not md_content:
        logger.error(f"没有有效的 md 内容，直接抛出异常！！！！")
        raise Exception("请检查输入文件路径是否正确！！")
    
    md_content = md_content.replace('\r\n', '\n').replace('\r', '\n')
    
    file_name = FileUtil.get_file_name_without_suffix(file_path=state.get('md_path'))
    file_title = state.get("file_title", file_name)
    
    # 2. 粗粒度切割（md）语义完善 -》 使用标题切割  （保证语义）
    file_title, title_count, section_list = DocumentProcess.split_by_title(md_content=md_content,
                                                                           file_title=file_title)
    
    # 3. 特殊场景，一个文档没有标题，我们给他一个默认标题 （兜底 文档 -》 没有标题 ）
    if title_count == 0:
        section_list = [{"title": "没有标题", "file_title": file_title, "content": md_content}]
    
    # 4. 细粒度切割（md）大小和重叠合适 -> 大 -》（设置重叠） 小 || 小 -》 合并  （大 -》 小 || 小 -》 合并）
    result_list = DocumentProcess.refine_chunks(section_list=section_list, min=DataDict.MIN_CONTENT_LENGTH,
                                                max=DataDict.MAX_CONTENT_LENGTH, overlap=DataDict.OVERLAP_SIZE)
    state['chunks'] = result_list
    
    # 5. 数据本地备份
    md_path = state.get('md_path')
    file_path = md_path.replace(".md", "_chunks.json")
    FileUtil.write_json(file_path=file_path, content=result_list)
    
    task_util.add_done_task(state.get('task_id'), function_name)
    logger.info(f">>> [{function_name}]执行结束！")
    
    return state


# 识别文档核心描述
def node_item_name_recognition(state: ImportGraphState) -> ImportGraphState:
    """
    主体识别节点（node_item_name_recognition）：识别文档核心描述的物品/商品名称。
        
        截取文档前几段作为输入，调用 LLM 识别文档描述的主体对象（如 "Fluke 17B+ 万用表"），
        将识别结果写入 state["item_name"]，用于向量库幂等清理。
        
    Args:
        state (ImportGraphState): 当前图状态，需包含 md_content 或文档前几段文本。
        
    Returns:
        ImportGraphState: 更新后的状态，新增 item_name 字段。
        
    Notes:
        1. 取文档前几段作为识别依据，控制 token 成本；
        2. LLM 未识别出结果时，使用 state["file_title"] 兜底；
        3. item_name 供 node_import_milvus 做幂等清理使用。
    """
    function_name = _getframe().f_code.co_name
    logger.info(f">>> [{function_name}] 执行节点: {function_name} 开始执行了！")
    
    # 1. 验和取值 （file_title, chunks）
    file_title = state.get("file_title")
    if not file_title:
        file_title = FileUtil.get_file_name_without_suffix(file_path=state.get('md_path'))
        state['file_title'] = file_title
    
    chunks = state.get("chunks")
    if not chunks:
        logger.error(f"没有有效的文件标题或 chunks 数据")
        raise Exception("请检查输入文件路径是否正确！！")
    
    # 2. 构建上下文环境  chunks -> top 5 -> 拼接成 context 文本
    context = RecognitionProcess.build_context(chunk_list=chunks[: DataDict.CHUNK_TOP])
    
    # 3. 调用模型，拼接提示词，识别 chunks 对应 item_name
    item_name = RecognitionProcess.call_llm(context=context, file_title=file_title)
    
    # 4. 修改 state chunks -> item_name -> chunks
    state["item_name"] = item_name
    for chunk in chunks:
        chunk["item_name"] = item_name
    state["chunks"] = chunks
    
    # 5. item_name 生成向量（稠密/稀疏）
    dense, sparse = RecognitionProcess.generate_vector(text=item_name)
    
    # 6. 将向量存储到向量数据库 kb_item_name (id / file_title / item_name / 稠密 和 稀疏)
    RecognitionProcess.save_item_vector(file_title=file_title, item_name=item_name,
                                        dense_vector=dense, sparse_vector=sparse)
    # state["item_name_vector"] = [dense, sparse]
    
    task_util.add_done_task(task_id=state.get('task_id'), node_name=function_name)
    logger.info(f">>> [{function_name}] 执行结束！")
    
    return state


# BGE 向量化
def node_bge_embedding(state: ImportGraphState) -> ImportGraphState:
    """
    向量化节点（node_bge_embedding）：使用 BGE-M3 模型将文本 Chunk 转换为向量。
        
        对切分后的文本块进行 Dense（稠密）与 Sparse（稀疏）双通道向量化，
        并组装为写入 Milvus 所需的向量数据结构。
        
    Args:
        state (ImportGraphState): 当前图状态，需包含已切分的 Chunk 列表及文本内容。
        
    Returns:
        ImportGraphState: 更新后的状态，携带每条 Chunk 对应的稠密/稀疏向量。
        
    Notes:
        1. 加载 BGE-M3 模型，建议全局加载避免重复初始化；
        2. 对每个 Chunk 的文本分别生成 Dense 和 Sparse 向量；
        3. 输出数据格式需与 node_import_milvus 的写入逻辑对齐。
    """
    
    function_name = _getframe().f_code.co_name
    logger.info(f">>> [{function_name}] 执行节点: {function_name} 开始执行了！")
    
    # 1.获取要生成向量的chunks
    chunks = state.get("chunks")
    if not chunks or not isinstance(chunks, list):
        logger.error(">>> chunks数据无效，请检查数据格式")
        raise ValueError(">>> chunks数据无效，请检查数据格式")
    
    # 2. 保存向量数据
    chunks = ContentProcess.get_chunk_vector(chunk_list=chunks, batch_size=5)
    state["chunks"] = chunks
    
    task_util.add_done_task(task_id=state.get('task_id'), node_name=function_name)
    logger.info(f">>> [{function_name}] 执行结束！")
    
    return state


def node_import_milvus(state: ImportGraphState) -> ImportGraphState:
    """导入向量库节点（node_import_milvus）：将向量数据批量写入 Milvus。

    连接 Milvus，依据 item_name 清理旧数据以保证幂等，随后批量写入新的向量数据。

    Args:
        state (ImportGraphState): 当前图状态，需包含 item_name 及待写入的向量数据。

    Returns:
        ImportGraphState: 更新后的状态（可标记导入结果）。

    Notes:
        1. 写入前连接 Milvus，复用连接池避免频繁建连；
        2. 依据 item_name 先删后插，保证幂等性；
        3. 使用批量插入提升吞吐，注意分批大小与超时控制。
    """
    function_name = _getframe().f_code.co_name
    logger.info(f">>> [{function_name}] 执行节点: {function_name} 开始执行了！")
    
    # 1. 获取要写入的向量数据
    chunks = state.get("chunks")
    if not chunks or not isinstance(chunks, list):
        logger.error(">>> chunks 数据无效，请检查数据格式")
        raise ValueError(">>> chunks 数据无效，请检查数据格式")
    
    # 2. 写入向量数据
    chunks = ContentProcess.save_chunk_vector(chunk_list=chunks)
    state["chunks"] = chunks
    
    task_util.add_done_task(task_id=state.get('task_id'), node_name=function_name)
    logger.info(f">>> [{function_name}] 执行结束！")
    return state


# 4. 定义条件边的路由函数(state = is_md_read_enabled: bool   # 是否启用 Markdown 读取路径
#                             is_pdf_read_enabled: bool  # 是否启用 PDF 读取路径)
def route_after_entry(state: ImportGraphState) -> str:
    """
    条件路由节点（route_after_entry）：根据文件类型决定 entry 之后的下一个节点。

    依据 state 中的 is_pdf_read_enabled / is_md_read_enabled 标志位判定走向：
    PDF 文件走 node_pdf_to_md，Markdown 文件走 node_md_img，均不满足则结束流程（END）。

    Args:
        state (ImportGraphState): 当前图状态，需包含：
            - is_pdf_read_enabled (bool): 是否为 PDF 文件；
            - is_md_read_enabled (bool): 是否为 Markdown 文件。

    Returns:
        str: 下一节点的名称，取值为 "node_pdf_to_md" | "node_md_img" | END。
    """
    if state["is_pdf_read_enabled"]:
        return "node_pdf_to_md"
    elif state["is_md_read_enabled"]:
        return "node_md_img"
    else:
        return END
    
    

if __name__ == '__main__':
    from json import dumps
    
    # pdf_name = "B3-211H.pdf"
    # pdf_path = f"{PathConfig.UPDATE_DIR}/{pdf_name}"
    #
    # state = create_default_state(task_id="test-pdf-1", pdf_path=pdf_path,
    #                              local_dir=f"{PathConfig.OUTPUT_DIR}")
    # node_pdf_to_md(state)
    #
    # state = create_default_state(task_id="test-image-1",
    #                              md_path=f"{PathConfig.OUTPUT_DIR}/B3-211H/B3-211H.md")
    # state = node_md_img(state=state)
    # print(state)
    #
    # md_path = f"{PathConfig.OUTPUT_DIR}/B3-211H/B3-211H_new.md"
    # content = FileUtil.read_text(file_path=md_path)
    # state = create_default_state(md_content=content, md_path=md_path)
    #
    # state = node_document_split(state=state)
    # string = dumps(obj=state.get("chunks"), indent=4, ensure_ascii=False, default=str)
    # print(string)
    #
    # md_path = f"{PathConfig.OUTPUT_DIR}/B3-211H/B3-211H_new_chunks.json"
    # chunks = FileUtil.read_json(file_path=md_path)
    # state = create_default_state(chunks=chunks, file_title="B3-211H")
    #
    # state = node_item_name_recognition(state=state)
    # string = dumps(obj=state.get("chunks"), indent=4, ensure_ascii=False, default=str)
    # print(string)
    #
    # chunks = \
    #     [
    #         {
    #             "title"     : "## 设置显示器菜单：",
    #             "file_title": "B3-211H",
    #             "content"   : "## 设置显示器菜单：\n\n1 显示器开机后，短按任意功能键，即可打开显示器设置菜单。\n\n2 在设置菜单界面，根据界面提示按 1\\~5 键，调节显示器的设置。\n\n<table><tr><td rowspan=\"2\">物理按键</td><td colspan=\"2\">快捷菜单</td><td colspan=\"2\">主菜单</td></tr><tr><td>图示</td><td>说明</td><td>图示</td><td>说明</td></tr><tr><td>按键1</td><td><img src=\"images/cd5fb4d5418a55e727b79241c4baa0b40ede5a01c427769e7cb3a3a930181069.jpg\"/></td><td>退出快捷菜单</td><td><img src=\"images/bc3cb60d2fc0b04368fe98393d1c5c0fbcece9166249221e2b022ad93caf7b3b.jpg\"/></td><td>左移</td></tr><tr><td>按键2</td><td></td><td>快捷键功能快速进入亮度设置菜单界面</td><td>↑</td><td>上移</td></tr><tr><td>按键3</td><td></td><td>快捷键功能快速进入情景模式设置菜单界面</td><td>[ DYD]</td><td>下移</td></tr><tr><td>按键4</td><td></td><td>进入主菜单</td><td>→</td><td>右移</td></tr><tr><td>按键5</td><td></td><td>关机</td><td>√</td><td>确认</td></tr></table>\n",
    #             "item_name" : "B3-211H显示器",
    #             "part"      : 1
    #         },
    #         {
    #             "title"     : "## 显示器菜单选项",
    #             "file_title": "B3-211H",
    #             "content"   : "## 显示器菜单选项\n\ni 不同型号、不同版本的显示器、菜单选项存在差异，请以实际为准。<table><tr><td>一级菜单</td><td>二级菜单</td><td>描述</td></tr><tr><td rowspan=\"6\">情景模式</td><td>P3色彩</td><td>浏览P3广色域图片或喜好鲜艳色彩的人士,建议选择P3色彩。</td></tr><tr><td>sRGB色彩</td><td>浏览计算机中的图片时,建议选择sRGB色彩。</td></tr><tr><td>HDR色彩</td><td>调色模拟HDR视频色彩效果,建议观赏影视场景使用。</td></tr><tr><td>游戏</td><td>游戏效果增强,建议游戏场景使用。</td></tr><tr><td>电子书</td><td>模拟纸质书籍效果,建议阅读场景使用。</td></tr><tr><td>用户</td><td>用户自定义显示效果。</td></tr><tr><td rowspan=\"7\">显示</td><td>亮度</td><td>设置范围为0-100。</td></tr><tr><td>对比度</td><td>设置范围为0-100。i 此功能仅在用户/sRGB色彩/P3色彩模式下且关闭护眼模式,才可使用。</td></tr><tr><td>锐利度</td><td>设置范围为0-100。</td></tr><tr><td>六色</td><td>可单独设置红色、绿色、蓝色、青色、品红色、黄色的色调与饱和度,设置范围为0-100。i 此功能仅在用户模式,才可使用。</td></tr><tr><td>护眼</td><td>可开启或关闭护眼模式。i 长期阅读时,建议开启护眼模式,预防用眼疲劳,使眼睛更加舒服。开启护眼模式后,屏幕显示偏黄为正常现象。此功能仅在用户/sRGB色彩/P3色彩模式下才可使用,其余的情景模式下护眼模式默认为关。</td></tr><tr><td>色温</td><td>可设置为冷色、中性色、标准色、暖色模式的一种。或者在用户自定义选项中,对红、绿、蓝颜色分别设置,设置数值为0-100。i 此功能仅在用户/sRGB色彩/P3色彩模式下且关闭护眼模式,才可使用。</td></tr><tr><td>缩放VGA 设置</td><td>可选择满屏或等比缩放。可设置 VGA 信号的水平位置、垂直位置、时钟、相位,设置数值为 0-100。或者可使用自动调整功能,自动设置 VGA 信号的水平位置、垂直位置、时钟、相位数值。i 此功能仅在连接 VGA 信号时,才可使用。</td></tr><tr><td rowspan=\"2\"><img src=\"images/e48bf1ea592e3df42e59fe14cde2301cdc81ca7637fd27d480587a658a2b04e6.jpg\"/>输入源</td><td>HDMI</td><td rowspan=\"2\">连接其他设备时,根据连接线缆,选择对应的输入源。</td></tr><tr><td>VGA</td></tr><tr><td rowspan=\"3\"><img src=\"images/a8277890bbf6b5ff329644066aebb5f390cbca18d97a549da53b8f4fa7b6bfa7.jpg\"/>游戏辅助</td><td>刷新率</td><td>在游戏场景中,可以在此菜单中进行一些辅助设置。开启后,可选择在屏幕左上角或右上角显示刷新率。</td></tr><tr><td>游戏准星</td><td>开启后,在屏幕上显示准星。并可将准星颜色设置为红色或绿色,也可对准星位置重置。</td></tr><tr><td>响应时间</td><td>可开启或关闭响应时间。开启时,可选择标准、快、极快等响应时间。</td></tr><tr><td rowspan=\"2\"><img src=\"images/a00657378ff23010838f537d0c904b5c6ad342fe8af303a0fad32479596c1cd3.jpg\"/>快捷键</td><td>上</td><td>OSD 快捷菜单上方的设置选项,默认为亮度,可设置为情景模式、响应时间、输入源、对比度等选项。</td></tr><tr><td>下</td><td>OSD 快捷菜单下方的设置选项,默认为情景模式,可设置为亮度、响应时间、输入源、对比度等选项。</td></tr><tr><td rowspan=\"9\"><img src=\"images/3307b6d548a42ebc9d1931502ad1024b46fea4a333fcc1703c17ba020ad966ad.jpg\"/>设置</td><td>音量</td><td>可设置音量大小设置数值为 0-100。i 此功能仅在连接 HDMI",
    #             "part"      : 1,
    #             "item_name" : "B3-211H显示器"
    #         },
    #         {
    #             "title"     : "## 显示器菜单选项",
    #             "file_title": "B3-211H",
    #             "content"   : "0-100。i 此功能仅在连接 HDMI 信号时,才可使用。</td></tr><tr><td>语言</td><td>可设置为简体中文、英语。</td></tr><tr><td rowspan=\"2\">菜单显示设置</td><td>菜单透明度:可设置菜单的显示透明度,设置数值为 1-8,数字越大透明度越高。</td></tr><tr><td>菜单显示时间:可将菜单显示时间设置为 10-100 秒。</td></tr><tr><td rowspan=\"2\">LED 电源按钮</td><td>待机模式时开:待机状态下,显示器的指示灯白色闪烁。</td></tr><tr><td>待机模式时关:待机状态下,显示器的指示灯熄灭。</td></tr><tr><td>信息</td><td>可查看显示器的 SN 号、固件版本号、情景模式、分辨率、刷新率、输入源等信息。</td></tr><tr><td>ECO Mode</td><td>选择开启或关闭节能模式。i 此功能默认关闭,打开后会减少能耗。开启节能模式后,亮度等选项将无法设置。</td></tr><tr><td>恢复出厂设置</td><td>选择是否将显示器菜单恢复出厂设置。</td></tr></table>",
    #             "part"      : 2,
    #             "item_name" : "B3-211H显示器"
    #         },
    #     ]
    # state = create_default_state(chunks=chunks)
    #
    # state = node_bge_embedding(state=state)
    # state = node_import_milvus(state=state)
    # string = dumps(obj=state.get("chunks"), indent=4, ensure_ascii=False, default=str)
    # print(string)
    #
    
