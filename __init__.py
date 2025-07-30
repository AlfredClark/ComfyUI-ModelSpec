# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  __init__.py
@Time    :  2025-07-30 10:47:17
@Author  :  Alfred Clark
@Contact :  alfredclark@163.com
@Desc    :  
"""
from .nodes.node_select_model import SelectModelNode
from .nodes.node_model_metadata import ModelMetadataNode
from .nodes.node_model_spec_edit import ModelSpecEditNode

# 节点名称类型映射（包含要导出的所有节点及其名称的字典，注意名称需要全局唯一）
NODE_CLASS_MAPPINGS = {
    "SelectModelNode": SelectModelNode,
    "ModelMetadataNode": ModelMetadataNode,
    "ModelSpecEditNode": ModelSpecEditNode,
}

# 节点展示名称映射（包含节点的展示标题名称的字典）
NODE_DISPLAY_NAME_MAPPINGS = {
    "SelectModelNode": "Select Model",
    "ModelMetadataNode": "Model Metadata",
    "ModelSpecEditNode": "Model Spec Editor",
}

# 设置 Web 目录，该目录中的任何.js文件都会被前端作为前端扩展脚本加载
WEB_DIRECTORY = "js"

# 自定义节点元数据信息
__version__ = "1.0.0"  # 版本信息
__author__ = "Alfred Clark"  # 作者信息
__doc__ = "ComfyUI ModelSpec"  # 文本信息

# 需要导出的映射与目录（根据具体已添加的信息选择是否导出）
# __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
