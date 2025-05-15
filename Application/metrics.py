from typing import Tuple
from app.utils import parse_cpu, parse_memory
from kubernetes import client, config

try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

custom_api = client.CustomObjectsApi()

def get_usage_from_metrics(pod_name: str, namespace: str) -> Tuple[float, float]:
    try:
        metrics_data = custom_api.get_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods",
            name=pod_name
        )
        container = metrics_data["containers"][0]
        cpu = parse_cpu(container["usage"]["cpu"])
        mem = parse_memory(container["usage"]["memory"])
        return cpu, mem
    except Exception as e:
        print(f"[ERROR] Metrics fetch failed: {e}")
        return 0.0, 0.0