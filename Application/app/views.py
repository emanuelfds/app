from flask import Blueprint, jsonify, render_template
from kubernetes import client
from .metrics import get_usage_from_metrics
from . import config
import os, time
from .utils import parse_cpu, parse_memory

def get_pod_ip(pod_name: str, namespace: str) -> str:
    try:
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        return pod.status.pod_ip or "unknown"
    except Exception as e:
        print(f"[ERROR] Failed to get pod IP: {e}")
        return "unknown"

bp = Blueprint('views', __name__)
state = {"cpu_exceeded_since": None, "mem_exceeded_since": None, "cpu_normal_since": None, "mem_normal_since": None}

@bp.route("/")
def index():
    return render_template("index.html", **get_template_context())

@bp.route("/metrics-data")
def metrics_data():
    return jsonify(get_metric_payload())

@bp.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


# Novo
def get_pod_resource_limits(pod_name: str, namespace: str):
    try:
        v1 = client.CoreV1Api()
        # Obtém o pod com a API do Kubernetes
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        
        # Acessa os containers do pod para pegar os limites
        containers = pod.spec.containers
        limits = {}

        for container in containers:
            container_name = container.name
            resources = container.resources

            cpu_limit = resources.limits.get('cpu') if resources.limits else None
            memory_limit = resources.limits.get('memory') if resources.limits else None

            limits[container_name] = {
                'cpu_limit': cpu_limit,
                'memory_limit': memory_limit
            }

        return limits
    except Exception as e:
        print(f"[ERROR] Failed to get pod resource limits: {e}")
        return None
 
# def get_template_context():
#     pod_name = os.environ.get("HOSTNAME", "unknown")
#     namespace = _get_namespace()
#     cpu, mem = get_usage_from_metrics(pod_name, namespace)
#     cpu_pct = round((cpu / config.CPU_LIMIT_MILLICORES) * 100, 1)
#     mem_pct = round((mem / config.MEMORY_LIMIT_MIB) * 100, 1)
#     return {
#         "pod_name": pod_name,
#         "pod_ip": get_pod_ip(pod_name, namespace),
#         "namespace": namespace,
#         "cpu_metric": cpu_pct,
#         "mem_metric": mem_pct,
#         "messages": _check_thresholds(cpu_pct, mem_pct)
#     }

# def get_metric_payload():
#     pod_name = os.environ.get("HOSTNAME", "unknown")
#     namespace = _get_namespace()
#     cpu, mem = get_usage_from_metrics(pod_name, namespace)
#     cpu_pct = round((cpu / config.CPU_LIMIT_MILLICORES) * 100, 1)
#     mem_pct = round((mem / config.MEMORY_LIMIT_MIB) * 100, 1)
#     alerts = _check_thresholds(cpu_pct, mem_pct)
#     return {
#         "cpu": cpu_pct,
#         "memory": mem_pct,
#         "alerts": alerts,
#         "cpu_warning": cpu_pct > config.CPU_THRESHOLD,
#         "mem_warning": mem_pct > config.MEMORY_THRESHOLD
#     }

# Novo
def get_template_context():
    pod_name = os.environ.get("HOSTNAME", "unknown")
    namespace = _get_namespace()
    cpu, mem = get_usage_from_metrics(pod_name, namespace)

    limits = get_pod_resource_limits(pod_name, namespace)
    if not limits:
        return {"error": "Could not fetch pod limits"}

    # Assumindo um container (ou pegar o primeiro)
    first_container = list(limits.values())[0]
    cpu_limit_millicores = parse_cpu(first_container['cpu_limit'])
    memory_limit_mib = parse_memory(first_container['memory_limit'])

    cpu_pct = round((cpu / cpu_limit_millicores) * 100, 1)
    mem_pct = round((mem / memory_limit_mib) * 100, 1)

    return {
        "pod_name": pod_name,
        "pod_ip": get_pod_ip(pod_name, namespace),
        "namespace": namespace,
        "cpu_metric": cpu_pct,
        "mem_metric": mem_pct,
        "messages": _check_thresholds(cpu_pct, mem_pct)
    }

# Novo
def get_metric_payload():
    pod_name = os.environ.get("HOSTNAME", "unknown")
    namespace = _get_namespace()
    cpu, mem = get_usage_from_metrics(pod_name, namespace)

    limits = get_pod_resource_limits(pod_name, namespace)
    if not limits:
        return {"error": "Could not fetch pod limits"}

    first_container = list(limits.values())[0]
    cpu_limit_millicores = parse_cpu(first_container['cpu_limit'])
    memory_limit_mib = parse_memory(first_container['memory_limit'])

    cpu_pct = round((cpu / cpu_limit_millicores) * 100, 1)
    mem_pct = round((mem / memory_limit_mib) * 100, 1)

    alerts = _check_thresholds(cpu_pct, mem_pct)
    return {
        "cpu": cpu_pct,
        "memory": mem_pct,
        "alerts": alerts,
        "cpu_warning": cpu_pct > config.CPU_THRESHOLD,
        "mem_warning": mem_pct > config.MEMORY_THRESHOLD
    }


def _get_namespace() -> str:
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
            return f.read().strip()
    except:
        return "unknown"

def _check_thresholds(cpu: float, mem: float) -> list[str]:
    now = time.time()
    messages = []

    if cpu > config.CPU_THRESHOLD:
        if not state["cpu_exceeded_since"]:
            state["cpu_exceeded_since"] = now
        elif now - state["cpu_exceeded_since"] > config.THRESHOLD_DELAY:
            messages.append(f"CPU usage > {config.CPU_THRESHOLD}% for over {config.THRESHOLD_DELAY} minutes - consider scaling up")
        state["cpu_normal_since"] = None
    else:
        if not state["cpu_normal_since"]:
            state["cpu_normal_since"] = now
        if state["cpu_exceeded_since"] and now - state["cpu_normal_since"] > config.THRESHOLD_DELAY:
            state["cpu_exceeded_since"] = None

    if mem > config.MEMORY_THRESHOLD:
        if not state["mem_exceeded_since"]:
            state["mem_exceeded_since"] = now
        elif now - state["mem_exceeded_since"] > config.THRESHOLD_DELAY:
            messages.append(f"Memory usage > {config.MEMORY_THRESHOLD}% for over {config.THRESHOLD_DELAY}  minutes - consider scaling up")
        state["mem_normal_since"] = None
    else:
        if not state["mem_normal_since"]:
            state["mem_normal_since"] = now
        if state["mem_exceeded_since"] and now - state["mem_normal_since"] > config.THRESHOLD_DELAY:
            state["mem_exceeded_since"] = None

    return messages