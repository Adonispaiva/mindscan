# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\providers\user_activity_provider.py
# Última atualização: 2025-12-11T09:59:27.870966

class UserActivityProvider:
    """
    Fornece dados de atividades recentes de usuários do sistema.
    """

    @staticmethod
    def fetch():
        return [
            {"user": "Ana", "action": "Realizou diagnóstico", "timestamp": "2025-12-10"},
            {"user": "Carlos", "action": "Gerou relatório", "timestamp": "2025-12-10"},
        ]
