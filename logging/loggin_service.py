# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\logging\loggin_service.py
# Última atualização: 2025-12-11T09:59:27.683474

# ============================================================
# MindScan — Logging Service (auditoria + registros de MI)
# ============================================================

import json
import os
from datetime import datetime
from typing import Dict, Any, List

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "mindscan_reports.log")


class LoggingService:

    def __init__(self):
        self.file = LOG_FILE

    def record(self, entry: Dict[str, Any]) -> None:
        """
        Salva uma linha de log JSONL com todos os detalhes do MI.
        """
        entry["timestamp"] = datetime.utcnow().isoformat()
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def list_entries(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retorna as entradas mais recentes.
        """
        if not os.path.exists(self.file):
            return []

        with open(self.file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines = lines[-limit:]
        return [json.loads(line) for line in lines]
