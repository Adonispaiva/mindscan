# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\events\event_dispatcher.py
# Última atualização: 2025-12-11T09:59:20.856706

from datetime import datetime

class EventDispatcher:
    """
    Dispara eventos internos do MindScan.
    """

    listeners = {}

    @staticmethod
    def subscribe(event_name: str, handler):
        if event_name not in EventDispatcher.listeners:
            EventDispatcher.listeners[event_name] = []
        EventDispatcher.listeners[event_name].append(handler)

    @staticmethod
    def emit(event_name: str, data: dict):
        handlers = EventDispatcher.listeners.get(event_name, [])
        event_context = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_name,
            "data": data
        }
        for h in handlers:
            h(event_context)
