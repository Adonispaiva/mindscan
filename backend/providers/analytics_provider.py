# ============================================================
# MindScan — Analytics Provider
# ============================================================
# Provedor unificado de telemetria e métricas internas.
#
# Responsável por:
# - registrar eventos do sistema
# - registrar uso de serviços internos
# - consolidar métricas de execução do pipeline
# - integrar com futuros serviços externos de analytics
#
# Versão: Final — SynMind 2025
# ============================================================

from datetime import datetime
from typing import List, Dict


class AnalyticsProvider:
    """
    Registro avançado de telemetria e eventos de sistema.
    """

    def __init__(self):
        # Lista de eventos registrados
        self.events: List[Dict] = []

    # ------------------------------------------------------------
    # Registrar evento
    # ------------------------------------------------------------
    def track(self, event_name: str, metadata: Dict = None):
        metadata = metadata or {}

        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "metadata": metadata
        }

        self.events.append(entry)

    # ------------------------------------------------------------
    # Recuperar todos os eventos
    # ------------------------------------------------------------
    def all_events(self) -> List[Dict]:
        return self.events

    # ------------------------------------------------------------
    # Filtrar por evento específico
    # ------------------------------------------------------------
    def filter(self, event_name: str) -> List[Dict]:
        return [e for e in self.events if e["event"] == event_name]

    # ------------------------------------------------------------
    # Estatísticas simples
    # ------------------------------------------------------------
    def count(self, event_name: str) -> int:
        return len(self.filter(event_name))

    # ------------------------------------------------------------
    # Limpar eventos
    # ------------------------------------------------------------
    def clear(self):
        self.events = []
