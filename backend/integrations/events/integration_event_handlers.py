# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\events\integration_event_handlers.py
# Última atualização: 2025-12-11T09:59:20.856706

from backend.integrations.webhooks.webhook_engine import WebhookEngine

class IntegrationEventHandlers:
    """
    Handlers que são disparados quando certos eventos ocorrem no MindScan.
    """

    @staticmethod
    def on_report_generated(event):
        report = event["data"]
        url = report.get("webhook_url")

        if url:
            WebhookEngine.trigger(url, {
                "event": "report_generated",
                "test_id": report.get("test_id"),
                "timestamp": event.get("timestamp")
            })

    @staticmethod
    def on_diagnostic_completed(event):
        # Envia informações básicas quando um diagnóstico é concluído
        url = event["data"].get("webhook_url")
        if url:
            WebhookEngine.trigger(url, {
                "event": "diagnostic_completed",
                "test_id": event["data"].get("test_id"),
                "results": event["data"].get("results")
            })
