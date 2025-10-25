from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.runpod_client import CreatePodRequest, RunpodClient


class CreatePod(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials.get("runpod_api_key")
        runpod = RunpodClient(api_key)
        create_pod_input = CreatePodRequest()
        create_pod_input.templateId = tool_parameters.get("templateId")
        create_pod_input.gpuTypeIds = [tool_parameters.get("gpuTypeId")]
        create_pod_input.gpuCount = int(tool_parameters.get("gpuCount"))
        create_pod_input.name = tool_parameters.get("name", "My Pod")
        podId = runpod.create_pod(create_pod_input)
        yield self.create_variable_message("podId", podId)
