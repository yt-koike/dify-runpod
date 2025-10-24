from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.runpod_client import RunpodClient


class StopPod(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials.get("runpod_api_key")
        runpod = RunpodClient(api_key)
        runpod.stop_pod(pod_id=tool_parameters.get("pod_id"))
        yield self.create_text_message("Successfully stopped the pod.")
