def parse_cpu(cpu_str: str) -> float:
    if cpu_str.endswith("n"):
        return int(cpu_str[:-1]) / 1e6
    if cpu_str.endswith("u"):
        return int(cpu_str[:-1]) / 1e3
    if cpu_str.endswith("m"):
        return float(cpu_str[:-1])
    return float(cpu_str) * 1000

def parse_memory(mem_str: str) -> float:
    if mem_str.endswith("Ki"):
        return int(mem_str[:-2]) / 1024
    if mem_str.endswith("Mi"):
        return float(mem_str[:-2])
    if mem_str.endswith("Gi"):
        return float(mem_str[:-2]) * 1024
    return float(mem_str) / (1024 * 1024)