# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\utils\error_response_builder.py
# Última atualização: 2025-12-11T09:59:20.777102

class ErrorResponseBuilder:

    @staticmethod
    def build(status: str, message: str, detail: str = None):
        base = {
            "status": status,
            "message": message
        }
        if detail:
            base["detail"] = detail
        return base
