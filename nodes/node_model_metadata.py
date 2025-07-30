# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  node_model_metadata.py
@Time    :  2025-07-30 11:31:24
@Author  :  Alfred Clark
@Contact :  alfredclark@163.com
@Desc    :  
"""
import json
import base64
import numpy as np
from PIL import Image
from io import BytesIO

from comfy.comfy_types import IO


class ModelMetadataNode:
    NODE_NAME = "ModelMetadataNode"
    DISPLAY_NAME = "Model Metadata"
    DESCRIPTION = "Model Metadata Node"

    CATEGORY = "ModelSpec"

    @classmethod
    def INPUT_TYPES(cls):
        architectures = [
            "",
            "pony",
            "pony/lora",
            "noobai",
            "noobai/lora",
            "flux.1-dev",
            "flux.1-dev/lora",
            "flux.1-schnell",
            "flux.1-schnell/lora",
            "illustrious",
            "illustrious/lora",
            "controlnet",
        ]
        return {
            "required": {
                "title": (IO.STRING,),  # COMBO下拉列表
                "architecture": (architectures, {"default": architectures[0]}),
                "author": (IO.STRING,),
                "description": (IO.STRING, {
                    "multiline": True,
                    "default": "This is a Model .",
                }),
                "usage_hint": (IO.STRING, {
                    "multiline": True,
                    "default": "CFG: 6(5-7); STEP: 25(20-30); SAMPLER: Euler a",
                }),
                "trigger_phrase": (IO.STRING, {
                    "multiline": True,
                    "default": "Positive Prompt: []; Negative Prompt: []",
                }),
            },
            "optional": {
                "thumbnail": (IO.IMAGE,),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",  # 节点的唯一标识符
                "prompt": "PROMPT",  # 客户端发送到服务器的完整提示
                "extra_pnginfo": "EXTRA_PNGINFO",  # 额外PNG信息
                "dynprompt": "DYNPROMPT"  # 动态Prompt
            },  # 隐藏的输入节点
        }

    RETURN_TYPES = ("METADATA",)
    RETURN_NAMES = ("metadata",)
    FUNCTION = "run"

    @classmethod
    def run(cls, title, architecture, author, description, usage_hint, trigger_phrase, thumbnail=None, **kwargs):
        """
        可选输入需要设置默认值，其余隐藏输入可以使用**kwargs接收
        """
        metadata = {
            "modelspec.title": title,
            "modelspec.architecture": architecture,
            "modelspec.author": author,
            "modelspec.thumbnail": "",
            "modelspec.description": description,
            "modelspec.usage_hint": usage_hint,
            "modelspec.trigger_phrase": trigger_phrase,
            "modelspec.sai_model_spec": "1.0.1"
        }
        if thumbnail is not None:
            thumbnail = 255. * thumbnail[0].cpu().numpy()
            img = Image.fromarray(np.clip(thumbnail, 0, 255).astype(np.uint8))
            metadata["modelspec.thumbnail"] = f"data:image/jpeg;base64,{cls.convert_to_base64(img)}"
        return (json.dumps(metadata, indent=4),)

    @classmethod
    def convert_to_base64(cls, image: Image.Image) -> str:
        image = image.resize((512, 512))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_b64
