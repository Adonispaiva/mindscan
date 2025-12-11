# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\analytics\live_metrics_service.py
# Última atualização: 2025-12-11T09:59:20.542656

# ============================================================
# MindScan — Live Metrics Service (Observability Engine)
# ============================================================
# Gera fluxos contínuos de métricas para dashboards:
# - Relatórios/minuto
# - Score médio móvel
# - Modos MI mais recentes
# - Últimos sujeitos processados
# ============================================================

import json
import time
from typing import Dict, Any, Generator, List
from logging.logging_service import LoggingService


class LiveMetricsService:

    def __init__(self):
        self.log = LoggingService()

    def stream(self) -> Generator[str, None, None]:
        """
        Stream infinito de métricas via SSE.
        """
        while True:
            entries = self.log.list_entries(limit=80)

            total = len(entries)
            avg = (
                sum(float(e.get("mi_score", 0)) for e in entries) / total
                if total > 0 else 0
            )
            modes = {}
            recent = []

            for e in entries[-10:]:
                modes[e["mi_mode"]] = modes.get(e["mi_mode"], 0) + 1
                recent.append({
                    "subject_id": e["subject_id"],
                    "mode": e["mi_mode"],
                    "score": e["mi_score"],
                    "timestamp": e["timestamp"],
                })

            payload = {
                "total_recent": total,
                "avg_score_recent": avg,
                "mode_distribution": modes,
                "recent": recent,
                "timestamp": time.time(),
            }

            yield f"data: {json.dumps(payload)}\n\n"
            time.sleep(1)
