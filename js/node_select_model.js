import {app} from "../../scripts/app.js";
import {api} from "../../scripts/api.js";

app.registerExtension({
    name: "SelectModelExtension",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "SelectModelNode") {
            return;
        }
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const node = this;
            const r = onNodeCreated ? (
                onNodeCreated.apply(this, arguments)
            ) : void 0;
            const model_type = this.widgets.find(w => w.name === "model_type");
            const model_name = this.widgets.find(w => w.name === "model_name");
            if (model_type && model_name) {
                model_type.callback = (value) => {
                    node.setDirtyCanvas(true, true);
                    interact_with_server(node.id, value, model_name);
                };
                model_type.callback(model_type.value);
            }
            return r
        };

        // 配置加载后的初始化
        nodeType.prototype.onConfigure = function () {
            const node = this
            const model_type = this.widgets.find(w => w.name === "model_type");
            const model_name = this.widgets.find(w => w.name === "model_name");
            interact_with_server(node.id, model_type.value, model_name);
        };
    }
});

// 更新ModelName数据
function updateModelName(node, names) {
    console.log(node.value)
    console.log(node.options)
    // 更新选项列表
    node.options.values = names;
    node.value = names[0]
    // 通知ComfyUI更新widget状态
    if (node.callback) {
        node.callback(node.value);
    }
}

// 与服务器异步交互的方法
async function interact_with_server(node_id, value, node) {
    // 构建表单数据
    const body = new FormData();
    body.append('node_id', node_id);
    body.append('type', value);
    // 访问API
    let resp = await api.fetchApi("/select_model", {method: "POST", body,});
    // 请求成功则更新列表
    if (resp.status === 200) {
        const data = await resp.json()
        console.log(data)
        updateModelName(node, data.names);
    }
}