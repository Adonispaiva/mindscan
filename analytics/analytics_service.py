# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\analytics\analytics_service.py
# Última atualização: 2025-12-11T09:59:20.542656

# ============================================================
# MindScan — Analytics Service
# ============================================================
# Consolida informações dos logs para gerar:
# - Distribuição de modos MI
# - Distribuição de tipos de relatório
# - Média dos scores
# - Volume de relatórios por dia
# ============================================================

import json
import os
from datetime import datetime
from typing import Dict, Any, List

LOG_FILE = "logs/mindscan_reports.log"


class AnalyticsService:

    def __init__(self):
        self.file = LOG_FILE

    def _load(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file):
            return []
        with open(self.file, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f.readlines()]

    def summary(self) -> Dict[str, Any]:
        entries = self._load()

        if not entries:
            return {
                "total_reports": 0,
                "modes": {},
                "report_types": {},
                "avg_score": 0,
                "per_day": {}
            }

        total = len(entries)
        modes = {}
        types = {}
        scores = []
        per_day = {}

        for e in entries:
            m = e.get("mi_mode")
            t = e.get("report_type")
            s = e.get("mi_score")
            ts = e.get("timestamp", "")

            modes[m] = modes.get(m, 0) + 1
            types[t] = types.get(t, 0) + 1

            if s is not None:
                scores.append(float(s))

            if ts:
                day = ts.split("T")[0]
                per_day[day] = per_day.get(day, 0) + 1

        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            "total_reports": total,
            "modes": modes,
            "report_types": types,
            "avg_score": avg_score,
            "per_day": per_day
        }
