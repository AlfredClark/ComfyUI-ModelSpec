# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  node_select_model.py
@Time    :  2025-07-30 11:04:42
@Author  :  Alfred Clark
@Contact :  alfredclark@163.com
@Desc    :  
"""
import os
from aiohttp import web
from server import PromptServer

types_filter = ("safetensors",)


class SelectModelNode:
    NODE_NAME = "SelectModelNode"
    DISPLAY_NAME = "Select Model"
    DESCRIPTION = "Select Model Node"

    CATEGORY = "ModelSpec"

    @classmethod
    def INPUT_TYPES(cls):
        model_type_list = os.listdir('models')
        model_name_list = []
        for model_type in model_type_list:
            models_list = os.listdir(os.path.join('models', model_type))
            models_list = [model for model in models_list if model.endswith(types_filter)]
            model_name_list.extend(models_list)
        return {
            "required": {
                "model_type": (model_type_list,),  # COMBO下拉列表
                "model_name": (model_name_list,),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",  # 节点的唯一标识符
                "prompt": "PROMPT",  # 客户端发送到服务器的完整提示
                "extra_pnginfo": "EXTRA_PNGINFO",  # 额外PNG信息
                "dynprompt": "DYNPROMPT"  # 动态Prompt
            },  # 隐藏的输入节点
        }

    RETURN_TYPES = ("MODEL_PATH",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "run"

    @classmethod
    def run(cls, model_type, model_name, **kwargs):
        """
        可选输入需要设置默认值，其余隐藏输入可以使用**kwargs接收
        """
        # 注意单值返回也需要使用元组
        return ("./models/{}".format(os.path.join(model_type, model_name)),)


# 获得ComfyUI路由
routes = PromptServer.instance.routes


# 定义需要使用的接口
@routes.post('/select_model')
async def interact_with_node(request):
    the_data = await request.post()  # 获得异步请求信息
    data = dict(the_data)  # 转换数据格式
    names = os.listdir(os.path.join('models', data['type']))  # 获得需要返回的数据
    names = [name for name in names if name.endswith(types_filter)]
    return web.json_response({
        "names": names
    })  # 返回响应数据
