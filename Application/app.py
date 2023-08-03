from flask import Flask, render_template
from kubernetes import client, config
import os

app = Flask(__name__)

# Load configuration from file
config.load_incluster_config()

# Create Kubernetes API client
v1 = client.CoreV1Api()

@app.route('/')
def index():
    pod_name = get_pod_name()
    pod_ip = get_pod_ip()
    return render_template('index.html', pod_name=pod_name, pod_ip=pod_ip)

def get_pod_name():
    # Obtém o nome do pod atual
    pod_name = os.environ['HOSTNAME']

    # Obtém o nome do namespace atual
    namespace = open('/var/run/secrets/kubernetes.io/serviceaccount/namespace').read()

    # Obtém informações do pod atual
    pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)

    # Retorna o nome do pod
    return pod.metadata.name

def get_pod_ip():
    # Obtém o nome do pod atual
    pod_name = os.environ['HOSTNAME']

    # Obtém o nome do namespace atual
    namespace = open('/var/run/secrets/kubernetes.io/serviceaccount/namespace').read()

    # Obtém informações do pod atual
    pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)

    # Retorna o IP do pod
    return pod.status.pod_ip

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')