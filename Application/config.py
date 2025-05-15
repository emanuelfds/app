import os

def get_env_var(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória não definida: {name}")
    return value

APP_VERSION = get_env_var("APP_VERSION", "unknown")
APP_CONFIG = get_env_var("APP_CONFIG", "default")
CPU_THRESHOLD = float(get_env_var("CPU_THRESHOLD", "80"))
MEMORY_THRESHOLD = float(get_env_var("MEMORY_THRESHOLD", "80"))
# CPU_LIMIT_MILLICORES = float(get_env_var("CPU_LIMIT_MILLICORES", "200"))
# MEMORY_LIMIT_MIB = float(get_env_var("MEMORY_LIMIT_MIB", "128"))
THRESHOLD_DELAY = 300
