import asyncio
import httpx
import pytest
import json
import os
import statistics
from datetime import datetime

# =============================
# CONFIGURAÇÃO DO TESTE
# =============================
DOCKER_API_HOST = os.getenv("MINDSCAN_API_HOST", "http://mindscan_backend:8000")
ENDPOINTS = [
    ("/api/v3/matcher/analyze", {"sample_id": "test01", "profile": "analytic"}),
    ("/api/v3/profile/get", {"user_id": "123"}),
    ("/api/v3/report/generate", {"report_type": "summary", "user_id": "123"}),
]
CONCURRENCY_LEVEL = 20
REQUESTS_PER_ENDPOINT = 50
TIMEOUT = 10.0

REPORT_DIR = "/reports"
HISTORY_DIR = "/data/perf_history"

# =============================
# UTILITÁRIOS
# =============================
class MetricsCollector:
    def __init__(self):
        self.results = []

    def record(self, endpoint: str, duration: float, status: int):
        self.results.append({
            "endpoint": endpoint,
            "duration": duration,
            "status": status
        })

    def summary(self):
        durations = [r["duration"] for r in self.results]
        success = len([r for r in self.results if 200 <= r["status"] < 300])
        errors = len(self.results) - success
        avg = statistics.mean(durations) if durations else 0
        p95 = statistics.quantiles(durations, n=100)[94] if len(durations) > 5 else avg
        throughput = len(durations) / sum(durations) if sum(durations) > 0 else 0
        return {
            "requests": len(durations),
            "success": success,
            "errors": errors,
            "avg_latency_ms": round(avg * 1000, 2),
            "p95_latency_ms": round(p95 * 1000, 2),
            "throughput_rps": round(throughput, 2)
        }

    def export(self):
        os.makedirs(REPORT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(REPORT_DIR, f"performance_results_{timestamp}.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        return report_path


async def run_request(client: httpx.AsyncClient, endpoint: str, payload: dict, metrics: MetricsCollector):
    start = asyncio.get_event_loop().time()
    try:
        response = await client.post(endpoint, json=payload, timeout=TIMEOUT)
        duration = asyncio.get_event_loop().time() - start
        metrics.record(endpoint, duration, response.status_code)
    except Exception:
        duration = asyncio.get_event_loop().time() - start
        metrics.record(endpoint, duration, 500)


# =============================
# TESTE PRINCIPAL
# =============================
@pytest.mark.performance
@pytest.mark.asyncio
async def test_performance_full_cycle():
    metrics = MetricsCollector()
    async with httpx.AsyncClient(base_url=DOCKER_API_HOST) as client:
        tasks = []
        for endpoint, payload in ENDPOINTS:
            for _ in range(REQUESTS_PER_ENDPOINT):
                tasks.append(run_request(client, endpoint, payload, metrics))
                if len(tasks) >= CONCURRENCY_LEVEL:
                    await asyncio.gather(*tasks)
                    tasks.clear()
        if tasks:
            await asyncio.gather(*tasks)

    summary = metrics.summary()
    report_path = metrics.export()

    # Histórico
    os.makedirs(HISTORY_DIR, exist_ok=True)
    history_file = os.path.join(HISTORY_DIR, "history.json")
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except Exception:
                history = []

    history.append({
        "timestamp": datetime.now().isoformat(),
        **summary
    })

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"\n📊 Relatório salvo em: {report_path}")
    print(json.dumps(summary, indent=2))

    # Validação mínima de performance
    assert summary["avg_latency_ms"] < 1500, "Latência média acima do limite institucional"
    assert summary["errors"] == 0, "Falhas detectadas nas requisições"
