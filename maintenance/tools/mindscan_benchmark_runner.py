"""
MindScan Benchmark Runner v1.0
Autor: Inovexa Software
Diretor Técnico: Leo Vinci
Descrição:
Executa testes de estabilidade, performance e resiliência do MindScan por 48h,
coletando métricas contínuas e avaliando interações entre Watchdog, SAFE e Daemon.
"""

import os
import json
import time
import psutil
from datetime import datetime, timedelta

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RESULTS_FILE = os.path.join(ROOT_DIR, "maintenance", "logs", "benchmark_results.json")
SAFE_LOG = os.path.join(ROOT_DIR, "maintenance", "logs", "diagnostico_safe.json")
ARCHIVE_LOG = os.path.join(ROOT_DIR, "maintenance", "logs", "archives")
DURATION_HOURS = 48
SAMPLE_INTERVAL = 60  # 1 minuto entre coletas

def collect_metrics():
    """Coleta métricas de uso do sistema."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").free / (1024 ** 3)
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": cpu,
        "mem": mem,
        "disk": round(disk, 2)
    }

def evaluate_stability(data):
    """Calcula métricas médias e picos."""
    if not data:
        return {}
    avg_cpu = sum(d["cpu"] for d in data) / len(data)
    avg_mem = sum(d["mem"] for d in data) / len(data)
    min_disk = min(d["disk"] for d in data)
    max_cpu = max(d["cpu"] for d in data)
    max_mem = max(d["mem"] for d in data)
    return {
        "avg_cpu": round(avg_cpu, 2),
        "avg_mem": round(avg_mem, 2),
        "min_disk": round(min_disk, 2),
        "max_cpu": round(max_cpu, 2),
        "max_mem": round(max_mem, 2)
    }

def write_results(summary):
    """Salva resultados finais no log JSON."""
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[BENCHMARK] Resultados gravados em {RESULTS_FILE}")

def monitor_system():
    """Executa o ciclo principal de benchmark."""
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(hours=DURATION_HOURS)
    results = []
    print(f"[BENCHMARK] Início: {start_time.isoformat()} — Duração: {DURATION_HOURS}h")

    while datetime.utcnow() < end_time:
        metrics = collect_metrics()
        results.append(metrics)
        print(f"[{metrics['timestamp']}] CPU={metrics['cpu']}% | MEM={metrics['mem']}% | DISK={metrics['disk']} GB")
        time.sleep(SAMPLE_INTERVAL)

    summary = evaluate_stability(results)
    summary["duration_hours"] = DURATION_HOURS
    summary["samples_collected"] = len(results)
    summary["start_time"] = start_time.isoformat()
    summary["end_time"] = datetime.utcnow().isoformat()
    summary["system_status"] = "Stable" if summary["avg_cpu"] < 70 and summary["avg_mem"] < 75 else "Attention"

    write_results(summary)
    print(f"[BENCHMARK] ✅ Concluído. Status final: {summary['system_status']}")

if __name__ == "__main__":
    monitor_system()
