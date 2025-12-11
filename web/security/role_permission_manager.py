# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\security\role_permission_manager.py
# Última atualização: 2025-12-11T09:59:27.855343

class RolePermissionManager:
    """
    Define permissões e papéis dentro do MindScan Web Enterprise.
    """

    ROLES = {
        "admin": ["view_all", "edit_all", "export_all"],
        "manager": ["view_team", "export_reports"],
        "operator": ["view_tests"]
    }

    @staticmethod
    def permissions(role: str):
        return RolePermissionManager.ROLES.get(role, [])
