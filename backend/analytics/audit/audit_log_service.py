# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\analytics\audit\audit_log_service.py
# Última atualização: 2025-12-11T09:59:20.730228

import json
import os
from datetime import datetime

class AuditLogService:
    """
    Sistema de auditoria avançado:
    Registra ações críticas do usuário e do sistema.
    """

    LOG_FILE = "logs/audit/audit_log.jsonl"

    @staticmethod
    def log(event: str, data: dict):
        os.makedirs(os.path.dirname(AuditLogService.LOG_FILE), exist_ok=True)

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data
        }

        with open(AuditLogService.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return True
