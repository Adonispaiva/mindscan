import asyncio
import httpx
import json
import os
from datetime import datetime

# =============================
# CONFIGURAÇÃO
# =============================
SERVICES = {
    "backend": "http://mindscan_backend:8000/health",
    "frontend": "http://mindscan_frontend:3000/health",
    "synmind_adapter": "http://synmind_core:9000/health",
    "database": "http://postgres:5432"
}

TIMEOUT = 5.0
OUTPUT_PATH = "/data/auditoria_mindscan/health_log.json"

# =============================
# FUNÇÕES AUXILIARES
# =============================
async def check_service(name: str, url: str) -> dict:
    start = datetime.now()
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=TIMEOUT)
            status = resp.status_code
            healthy = status in [200, 204]
    except Exception as e:
        status = 0
        healthy = False
    duration = (datetime.now() - start).total_seconds()
    return {
        "service": name,
        "url": url,
        "status": status,
        "latency": round(duration * 1000, 2),
        "healthy": healthy,
        "timestamp": datetime.now().isoformat()
    }


async def run_healthcheck():
    results = await asyncio.gather(*[check_service(n, u) for n, u in SERVICES.items()])
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    total = len(results)
    ok = len([r for r in results if r["healthy"]])
    warning = len([r for r in results if not r["healthy"] and r["status"] != 0])
    critical = len([r for r in results if r["status"] == 0])

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "ok": ok,
        "warning": warning,
        "critical": critical
    }

    print("🩺 Healthcheck Summary:")
    print(json.dumps(summary, indent=2))

    # Código de saída institucional
    if critical > 0:
        exit(2)
    elif warning > 0:
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    asyncio.run(run_healthcheck())
