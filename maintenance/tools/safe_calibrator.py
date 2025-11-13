"""
MindScan SAFE Calibrator v1.0
Autor: Inovexa Software
Diretor Técnico: Leo Vinci
Descrição:
Coleta métricas reais de uso do sistema (CPU, memória, disco) em execução
contínua e recalibra automaticamente os thresholds do supervisor_rules.json.
"""

import os
import json
import time
import psutil
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "maintenance", "configs", "supervisor_rules.json")
LOG_PATH = os.path.join(ROOT_DIR, "maintenance", "logs", "safe_calibration.json")

SAMPLE_INTERVAL = 60       # segundos entre amostras
CALIBRATION_PERIOD = 24*60 # minutos (24 horas)
TARGET_SAMPLES = CALIBRATION_PERIOD

def load_policies():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_policies(policies):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(policies, f, indent=2)

def log_sample(data):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

def collect_metrics():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").free / (1024**3)
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": cpu,
        "mem": mem,
        "disk": round(disk, 2)
    }

def main():
    policies = load_policies()
    print(f"[SAFE-Calibrator] Iniciado às {datetime.now().strftime('%H:%M:%S')} — coleta contínua por 24h.")

    samples = []

    for i in range(TARGET_SAMPLES):
        metrics = collect_metrics()
        samples.append(metrics)
        log_sample(metrics)
        print(f"[{i+1}/{TARGET_SAMPLES}] CPU={metrics['cpu']}% | MEM={metrics['mem']}% | DISK={metrics['disk']} GB")
        time.sleep(SAMPLE_INTERVAL)

    # cálculo das médias reais
    avg_cpu = sum(s["cpu"] for s in samples) / len(samples)
    avg_mem = sum(s["mem"] for s in samples) / len(samples)
    min_disk = min(s["disk"] for s in samples)

    # margem de segurança de 25%
    cpu_threshold = round(avg_cpu * 1.25, 2)
    mem_threshold = round(avg_mem * 1.25, 2)
    disk_threshold = round(min_disk * 0.8, 2)

    recovery = policies.get("recovery_policies", {})
    self_check = recovery.get("self_check_rules", {})
    self_check.update({
        "cpu_threshold_percent": cpu_threshold,
        "memory_threshold_percent": mem_threshold,
        "disk_space_min_gb": disk_threshold
    })
    recovery["self_check_rules"] = self_check
    policies["recovery_policies"] = recovery
    save_policies(policies)

    print("\n[SAFE-Calibrator] ✅ Calibração concluída com sucesso:")
    print(f"→ CPU limite ajustado para {cpu_threshold}%")
    print(f"→ Memória limite ajustada para {mem_threshold}%")
    print(f"→ Espaço mínimo ajustado para {disk_threshold} GB")
    print(f"Políticas atualizadas em {CONFIG_PATH}")

if __name__ == "__main__":
    main()
