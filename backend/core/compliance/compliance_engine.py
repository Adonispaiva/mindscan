# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\compliance\compliance_engine.py
# Última atualização: 2025-12-11T09:59:20.777102

class ComplianceEngine:
    """
    Classe responsável por garantir que o diagnóstico
    siga critérios de conformidade ética, LGPD e normas internas.
    """

    @staticmethod
    def validate_data_structure(data: dict):
        if not isinstance(data, dict):
            return False

        required = ["big5", "teique", "global_score"]
        return all(key in data for key in required)

    @staticmethod
    def sanitize(data: dict) -> dict:
        """
        Remove dados sensíveis antes de exportações ou integrações.
        """
        sanitized = dict(data)
        sanitized.pop("cpf", None)
        sanitized.pop("email", None)
        sanitized.pop("telefone", None)
        return sanitized
