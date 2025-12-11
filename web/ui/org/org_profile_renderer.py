# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\org\org_profile_renderer.py
# Última atualização: 2025-12-11T09:59:27.886588

class OrgProfileRenderer:
    """
    Renderizador de perfis organizacionais para o Dashboard.
    """

    @staticmethod
    def render(profile: dict):
        return {
            "organization": profile.get("name", "N/A"),
            "employees": profile.get("employees", 0),
            "culture_map": profile.get("culture_map", {})
        }
