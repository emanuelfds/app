import threading, time, datetime
from prometheus_client import Gauge
import os
from kubernetes import client, config

try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

pod_uptime_seconds = Gauge('pod_uptime_seconds', 'Total uptime of the pod in seconds')
v1 = client.CoreV1Api()

def update_pod_uptime_metric():
    while True:
        try:
            pod_name = os.environ.get("HOSTNAME", "unknown")
            with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
                namespace = f.read().strip()

            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            start_time = pod.status.start_time.timestamp()
            uptime = datetime.datetime.now().timestamp() - start_time
            pod_uptime_seconds.set(uptime)
        except Exception as e:
            print(f"[ERROR] Uptime update failed: {e}")
        time.sleep(1)

def start_uptime_thread():
    thread = threading.Thread(target=update_pod_uptime_metric, daemon=True)
    thread.start()