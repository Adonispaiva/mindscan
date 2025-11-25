from typing import Dict, Any, List
from backend.models.diagnostic_request import DiagnosticRequest


class DataService:
    """
    Serviço responsável por preparar, validar e transformar
    os dados psicométricos antes de entrar na engine MindScan.
    """

    @staticmethod
    def prepare_dataset(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converte o payload cru recebido do endpoint em um dataset
        padronizado que a MindScanEngine consegue processar.
        """

        # ------------------------------
        # 1. Validar estrutura do payload
        # ------------------------------
        try:
            request = DiagnosticRequest(**payload)
        except Exception as e:
            raise ValueError(f"Payload inválido para diagnóstico: {e}")

        # ------------------------------
        # 2. Padronizar instrumentos
        # ------------------------------
        instruments_data = []
        for section in request.instruments:
            instruments_data.append({
                "instrument": section.instrument,
                "answers": [
                    {"id": a.question_id, "value": a.value}
                    for a in section.answers
                ]
            })

        # ------------------------------
        # 3. Estrutura final entregue à engine
        # ------------------------------
        dataset = {
            "candidate": {
                "name": request.candidate.name,
                "email": request.candidate.email,
                "age": request.candidate.age,
                "gender": request.candidate.gender,
                "notes": request.candidate.notes,
            },
            "instruments": instruments_data,
            "metadata": request.metadata or {}
        }

        return dataset

    # =========================================================
    # Configurações avançadas do sistema (Painel da Milena)
    # =========================================================
    @staticmethod
    def get_system_settings() -> Dict[str, Any]:
        """
        Retorna parâmetros psicométricos globais, pesos, calibrações,
        versões dos instrumentos e outros ajustes administrativos.
        """

        settings = {
            "version": "2.0",
            "weights": {
                "BIG5": 1.0,
                "TEIQue": 1.0,
                "OCAI": 1.0,
                "DASS21": 1.0
            },
            "calibration": {
                "last_update": "2025-11-25",
                "engine_revision": 2
            }
        }

        return settings
