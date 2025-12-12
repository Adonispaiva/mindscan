#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BACKEND MINDSCAN — FULL ORCHESTRATOR (Enterprise v3)
----------------------------------------------------
Backend autossuficiente, resiliente e integrado ao MindScan DevOps Engine.
Inclui:
- Kernel de logs estruturados
- API + Worker supervisionados
- Heartbeat de componentes
- Self-healing automático
- Watchdog inteligente
- Runtime Dashboard (JSON)
- Integração com Auditor/Orchestrator
- Execução idempotente
"""

import threading
import time
import json
import traceback
from datetime import datetime
from pathlib import Path

from backend.pysettings import settings
from backend.app import app

# ============================================================
# 1) PATHS E LOG
# ============================================================
ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)

LOG = RUNTIME / "backend_orchestrator.log"
DASHBOARD = RUNTIME / "runtime_dashboard.json"


def log_event(event, data):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "data": data,
    }
    LOG.write_text(
        (LOG.read_text() if LOG.exists() else "") +
        json.dumps(entry, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"[Backend {entry['timestamp']}] {event}: {data}")


# ============================================================
# 2) HEARTBEAT
# ============================================================
HEARTBEAT = {
    "worker": None,
    "api": None,
    "main": None,
}


def update_dashboard():
    DASHBOARD.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "heartbeat": HEARTBEAT,
        "settings": {
            "API": settings.API_ENABLED,
            "WORKER": settings.WORKER_ENABLED,
            "interval": settings.WORKER_INTERVAL,
        },
    }, indent=4, ensure_ascii=False))


# ============================================================
# 3) WORKER COM SELF-HEALING
# ============================================================

def worker_loop():
    try:
        while True:
            HEARTBEAT["worker"] = datetime.now().isoformat()
            log_event("worker_tick", {"interval": settings.WORKER_INTERVAL})
            time.sleep(settings.WORKER_INTERVAL)
    except Exception as e:
        log_event("worker_crash", str(e))
        raise


def start_worker():
    th = threading.Thread(target=worker_loop, daemon=True)
    th.start()
    log_event("worker_started", {})
    return th


# ============================================================
# 4) API FASTAPI + SELF-HEALING
# ============================================================

def api_thread():
    try:
        import uvicorn
        log_event("api_boot", {"host": settings.API_HOST, "port": settings.API_PORT})
        while True:
            HEARTBEAT["api"] = datetime.now().isoformat()
            uvicorn.run(
                app,
                host=settings.API_HOST,
                port=settings.API_PORT,
                log_level="warning"
            )
    except Exception:
        log_event("api_crash", traceback.format_exc())
        raise


def start_api():
    th = threading.Thread(target=api_thread, daemon=True)
    th.start()
    log_event("api_thread_started", {})
    return th


# ============================================================
# 5) WATCHDOG INTELIGENTE
# ============================================================

def watchdog(worker_th, api_th):
    while True:
        HEARTBEAT["main"] = datetime.now().isoformat()

        if settings.WORKER_ENABLED and worker_th and not worker_th.is_alive():
            log_event("worker_recover", {})
            worker_th = start_worker()

        if settings.API_ENABLED and api_th and not api_th.is_alive():
            log_event("api_recover", {})
            api_th = start_api()

        update_dashboard()
        time.sleep(3)


# ============================================================
# 6) BOOT GERAL DO BACKEND
# ============================================================

def start_backend():
    log_event("backend_start", {})

    worker_th = None
    api_th = None

    if settings.WORKER_ENABLED:
        worker_th = start_worker()
    else:
        log_event("worker_disabled", {})

    if settings.API_ENABLED:
        api_th = start_api()
    else:
        log_event("api_disabled", {})

    wd = threading.Thread(
        target=watchdog,
        args=(worker_th, api_th),
        daemon=True
    )
    wd.start()
    log_event("watchdog_started", {})


# ============================================================
# 7) EXECUÇÃO DIRETA
# ============================================================
if __name__ == "__main__":
    log_event("direct_execution", {})
    start_backend()

    while True:
        time.sleep(1)
