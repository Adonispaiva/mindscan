# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\profiles\expv4_export_profile.py
# Última atualização: 2025-12-11T09:59:27.620971

class EXPV4ExportProfile:
    """
    Perfil configurável de exportação (executivo, técnico, clínico, corporativo).
    """

    @staticmethod
    def build(profile: str):
        return {
            "profile": profile,
            "metadata": f"Profile-{profile}-v4"
        }
