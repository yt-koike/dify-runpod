from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.runpod_client import RunpodClient


class ListPods(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials.get("runpod_api_key")
        runpod = RunpodClient(api_key)
        podIds = [pod["id"] for pod in runpod.list_pods()]
        yield self.create_variable_message("podIds", podIds)
