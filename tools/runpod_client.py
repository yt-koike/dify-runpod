import json
import requests
from dataclasses import dataclass, asdict, field


@dataclass
class CreatePodInput:
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


class RunpodClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def create_pod(self, create_pod_input: CreatePodInput) -> str:
        # Returns Pod ID
        response = requests.post(
            "https://rest.runpod.io/v1/pods",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(asdict(create_pod_input)),
        )
        if response.status_code != 201:
            raise Exception("Pod Create Failed.")
        return response.json()["id"]

    def list_pods(self) -> dict:
        # Returns Pods
        response = requests.get(
            "https://rest.runpod.io/v1/pods",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("List Pod Failed.")
        return response.json()

    def find_pod(self, pod_id: str) -> dict:
        # Returns Pod with pod_id
        response = requests.get(
            f"https://rest.runpod.io/v1/pods/{pod_id}",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("Find Pod Failed.")
        return response.json()

    def delete_pod(self, pod_id: str) -> None:
        response = requests.delete(
            f"https://rest.runpod.io/v1/pods/{pod_id}",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 204:
            raise Exception("Find Pod Failed.")

    def start_pod(self, pod_id: str) -> None:
        response = requests.post(
            f"https://rest.runpod.io/v1/pods/{pod_id}/start",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("Start Pod Failed.")

    def stop_pod(self, pod_id: str) -> None:
        response = requests.post(
            f"https://rest.runpod.io/v1/pods/{pod_id}/stop",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("Stop Pod Failed.")

    def reset_pod(self, pod_id: str) -> None:
        response = requests.post(
            f"https://rest.runpod.io/v1/pods/{pod_id}/reset",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("Reset Pod Failed.")

    def restart_pod(self, pod_id: str) -> None:
        response = requests.post(
            f"https://rest.runpod.io/v1/pods/{pod_id}/restart",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("Restart Pod Failed.")

    def get_billing_pod(self) -> dict:
        response = requests.get(
            "https://rest.runpod.io/v1/billing/pods",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        if response.status_code != 200:
            raise Exception("Billing Pod Failed.")
        return response.json()
