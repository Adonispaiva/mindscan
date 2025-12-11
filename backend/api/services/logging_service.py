# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\logging_service.py
# Última atualização: 2025-12-11T09:59:20.761538

import json
import os
from datetime import datetime

class LoggingService:

    LOG_PATH = "logs/api_log.jsonl"

    @staticmethod
    def log(event_type: str, payload: dict):
        os.makedirs(os.path.dirname(LoggingService.LOG_PATH), exist_ok=True)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "payload": payload
        }

        with open(LoggingService.LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
