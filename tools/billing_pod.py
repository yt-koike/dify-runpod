from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.runpod_client import RunpodClient


class CreatePod(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials.get("runpod_api_key")
        runpod = RunpodClient(api_key)
        billing = runpod.get_billing_pod()
        yield self.create_variable_message("amount", [x.amount for x in billing])
        yield self.create_variable_message(
            "endpointId", [x.endpointId for x in billing]
        )
        yield self.create_variable_message("gpuTypeId", [x.gpuTypeId for x in billing])
        yield self.create_variable_message("podId", [x.podId for x in billing])
        yield self.create_variable_message("time", [x.time for x in billing])
        yield self.create_variable_message(
            "timeBilledMs", [int(x.timeBilledMs) for x in billing]
        )
