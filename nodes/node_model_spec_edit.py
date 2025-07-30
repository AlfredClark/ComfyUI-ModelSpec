# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  node_model_spec_edit.py
@Time    :  2025-07-30 12:10:23
@Author  :  Alfred Clark
@Contact :  alfredclark@163.com
@Desc    :  
"""
import json
import os.path

from safetensors import safe_open
from safetensors.torch import save_file

from comfy.comfy_types import IO


class ModelSpecEditNode:
    NODE_NAME = "ModelSpecEditNode"
    DISPLAY_NAME = "Model Spec Editor"
    DESCRIPTION = "ModelSpec Edit Node"

    CATEGORY = "ModelSpec"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("MODEL_PATH",),
                "metadata": ("METADATA",),
                "use_title": (IO.BOOLEAN,)
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",  # 节点的唯一标识符
                "prompt": "PROMPT",  # 客户端发送到服务器的完整提示
                "extra_pnginfo": "EXTRA_PNGINFO",  # 额外PNG信息
                "dynprompt": "DYNPROMPT"  # 动态Prompt
            },  # 隐藏的输入节点
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "run"

    @classmethod
    def run(cls, model_path, metadata, use_title, **kwargs):
        metadata = json.loads(metadata)
        tensors = {}
        orig_metadata = None
        dtypes = []
        with safe_open(model_path, framework="pt") as f:
            orig_metadata = f.metadata()
            for key in f.keys():
                tensors[key] = f.get_tensor(key)
                dtypes.append(tensors[key].dtype)

        if orig_metadata is None or not isinstance(orig_metadata, dict):
            orig_metadata = {}

        # orig_metadata.update(metadata)
        for key, val in metadata.items():
            if val:
                orig_metadata[key] = val
        if not os.path.exists('./output/metadata'):
            os.makedirs('./output/metadata')
        if not os.path.exists('./output/modelspec'):
            os.makedirs('./output/modelspec')
        if use_title:
            json.dump(orig_metadata, open('./output/metadata/{}.json'.format(metadata["modelspec.title"]), 'w'),
                      indent=4)
            save_file(tensors, './output/modelspec/{}.safetensors'.format(metadata["modelspec.title"]),
                      metadata=orig_metadata)
        else:
            json.dump(orig_metadata, open('./output/metadata/{}.json'.format(os.path.basename(model_path)), 'w'),
                      indent=4)
            save_file(tensors, './output/modelspec/{}'.format(os.path.basename(model_path)),
                      metadata=orig_metadata)
        return ()
