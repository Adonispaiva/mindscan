"""
predictive_analyzer.py
Módulo de manutenção preditiva — MindScan v3.1
"""

import os
import json
import statistics
from datetime import datetime

PERF_HISTORY_DIR = os.path.join("data", "perf_history")
AUDIT_PATH = os.path.join("data", "auditoria_mindscan", "predictive_report.json")


def ensure_dirs():
    """Garante a existência dos diretórios necessários."""
    os.makedirs(PERF_HISTORY_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)


def load_history():
    """Carrega métricas históricas."""
    history = []
    for file in os.listdir(PERF_HISTORY_DIR):
        if file.endswith(".json"):
            try:
                with open(os.path.join(PERF_HISTORY_DIR, file), "r", encoding="utf-8") as f:
                    history.extend(json.load(f))
            except Exception:
                continue
    return history


def analyze_metrics(metrics):
    """Analisa tendências e anomalias simples."""
    results = {}
    for key in ("latency_ms", "cpu", "memory"):
        values = [m.get(key, 0) for m in metrics if key in m]
        if not values:
            continue
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0
        last = values[-1]
        trend = (last - mean) / (stdev or 1)
        if trend > 2:
            status = "critical"
        elif trend > 1:
            status = "warning"
        else:
            status = "normal"
        results[key] = {
            "mean": round(mean, 2),
            "stdev": round(stdev, 2),
            "last": round(last, 2),
            "trend": round(trend, 2),
            "status": status,
        }
    return results


def generate_report(results):
    """Salva relatório preditivo."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }
    with open(AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("✅ Relatório preditivo salvo em:", AUDIT_PATH)


def main():
    ensure_dirs()
    history = load_history()
    if not history:
        print("⚠️ Nenhum histórico de performance encontrado em", PERF_HISTORY_DIR)
        return
    results = analyze_metrics(history)
    generate_report(results)


if __name__ == "__main__":
    main()
