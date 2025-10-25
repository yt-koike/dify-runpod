import json
import os
import requests
from dataclasses import dataclass, asdict, field


@dataclass
class CreatePodRequest:
    allowedCudaVersions: list[str] = field(default_factory=list[str])
    cloudType: str = "SECURE"
    computeType: str = "GPU"
    containerDiskInGb: int = 50
    countryCodes: list[str] = field(default_factory=list[str])
    dockerEntrypoint: list[str] = field(default_factory=list[str])
    dockerStartCmd: list[str] = field(default_factory=list[str])
    env: dict = field(default_factory=dict)
    gpuCount: int = 1
    gpuTypeIds: list[str] = field(default_factory=list[str])
    imageName: str = ""
    interruptible: bool = False
    locked: bool = False
    name: str = "my pod"
    ports: list[str] = field(default_factory=list[str])
    templateId: str = "null"
    volumeInGb: int = 20
    volumeMountPath: str = "/workspace"


@dataclass
class BillingPod:
    amount: float
    time: str
    diskSpaceBilledGb: int = 0
    timeBilledMs: int = 0
    endpointId: str = ""
    gpuTypeId: str = ""
    podId: str = ""


class RunpodClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.schema = json.loads(open(os.path.join(current_dir, "openapi.json")).read())

    def request_get(self, relative_path: str) -> requests.Response:
        return requests.get(
            "https://rest.runpod.io/v1" + relative_path,
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )

    def request_post(self, relative_path: str, data: dict = {}) -> requests.Response:
        return requests.post(
            "https://rest.runpod.io/v1" + relative_path,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
        )

    def request_delete(self, relative_path: str) -> requests.Response:
        return requests.delete(
            "https://rest.runpod.io/v1" + relative_path,
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )

    def create_pod(self, create_pod_input: CreatePodRequest) -> str:
        # Returns Pod ID
        schema = self.schema["components"]["schemas"]["PodCreateInput"]
        validGpuTypes = schema["properties"]["gpuTypeIds"]["items"]["enum"]
        for gpuType in create_pod_input.gpuTypeIds:
            if gpuType not in validGpuTypes:
                raise Exception(
                    f"GPU Type {gpuType} is not supported. Valid GPU Types are {', '.join(validGpuTypes)}"
                )
        response = self.request_post("/pods", data=asdict(create_pod_input))
        if response.status_code != 201:
            raise Exception("Pod Create Failed.")
        return response.json()["id"]

    def list_pods(self) -> dict:
        # Returns Pods
        response = self.request_get("/pods")
        if response.status_code != 200:
            raise Exception("List Pod Failed.")
        return response.json()

    def find_pod(self, pod_id: str) -> dict:
        # Returns Pod with pod_id
        response = self.request_get(f"/pods/{pod_id}")
        if response.status_code != 200:
            raise Exception("Find Pod Failed.")
        return response.json()

    def delete_pod(self, pod_id: str) -> None:
        response = self.request_delete(f"/pods/{pod_id}")
        if response.status_code != 204:
            raise Exception("Delete Pod Failed.")

    def start_pod(self, pod_id: str) -> None:
        response = self.request_post(f"/pods/{pod_id}/start")
        if response.status_code != 200:
            raise Exception("Start Pod Failed.")

    def stop_pod(self, pod_id: str) -> None:
        response = self.request_post(f"/pods/{pod_id}/stop")
        if response.status_code != 200:
            raise Exception("Stop Pod Failed.")

    def reset_pod(self, pod_id: str) -> None:
        response = self.request_post(f"/pods/{pod_id}/reset")
        if response.status_code != 200:
            raise Exception("Reset Pod Failed.")

    def restart_pod(self, pod_id: str) -> None:
        response = self.request_post(f"/pods/{pod_id}/restart")
        if response.status_code != 200:
            raise Exception("Restart Pod Failed.")

    def get_billing_pod(self) -> list[BillingPod]:
        response = self.request_get("/billing/pods")
        if response.status_code != 200:
            raise Exception("Billing Pod Failed.")
        result: list[BillingPod] = []
        for pod in response.json():
            tmp = BillingPod(
                amount=pod["amount"],
                time=pod["time"],
            )
            if pod.get("diskSpaceBilledGb") is not None:
                tmp.diskSpaceBilledGb = pod.get("diskSpaceBilledGb")
            if pod.get("timeBilledMs") is not None:
                tmp.timeBilledMs = pod.get("timeBilledMs")
            if pod.get("endpointId") is not None:
                tmp.endpointId = pod.get("endpointId")
            if pod.get("gpuTypeId") is not None:
                tmp.gpuTypeId = pod.get("gpuTypeId")
            if pod.get("podId") is not None:
                tmp.podId = pod.get("podId")
            result.append(tmp)
        return result
