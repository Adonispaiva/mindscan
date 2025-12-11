# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\user_management_service.py
# Última atualização: 2025-12-11T09:59:27.870966

class UserManagementService:
    """
    Serviço de gerenciamento de usuários do portal MindScan.
    """

    @staticmethod
    def list_users():
        return [{"id": 1, "name": "Admin"}, {"id": 2, "name": "Operador"}]
