from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.runpod_client import CreatePodInput, RunpodClient


class CreatePod(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials.get("runpod_api_key")
        runpod = RunpodClient(api_key)
        create_pod_input = CreatePodInput(templateId=tool_parameters.get("templateId"))
        yield self.create_json_message(runpod.create_pod(create_pod_input))
