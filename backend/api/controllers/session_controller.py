# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\controllers\session_controller.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import HTTPException
from backend.api.services.session_gateway import SessionGateway

class SessionController:

    @staticmethod
    def start():
        session_id = SessionGateway.start_session()
        return {
            "status": "success",
            "session_id": session_id
        }

    @staticmethod
    def store(session_id: str, key: str, value):
        try:
            SessionGateway.store(session_id, key, value)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def load(session_id: str, key: str):
        try:
            value = SessionGateway.load(session_id, key)
            return {"status": "success", "value": value}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
