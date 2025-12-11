# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\session_gateway.py
# Última atualização: 2025-12-11T09:59:20.777102

import uuid
from typing import Dict, Any

class SessionGateway:
    _sessions: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def start_session() -> str:
        session_id = str(uuid.uuid4())
        SessionGateway._sessions[session_id] = {}
        return session_id

    @staticmethod
    def store(session_id: str, key: str, value: Any):
        if session_id not in SessionGateway._sessions:
            SessionGateway._sessions[session_id] = {}
        SessionGateway._sessions[session_id][key] = value

    @staticmethod
    def load(session_id: str, key: str):
        return SessionGateway._sessions.get(session_id, {}).get(key)
