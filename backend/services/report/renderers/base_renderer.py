# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\renderers\base_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

class BaseRenderer:
    """
    Classe base para os renderizadores de relatório.
    Define interface padrão e métodos utilitários.
    """

    template_name = None

    @staticmethod
    def render_header(test_id: str, results: dict) -> dict:
        return {
            "test_id": test_id,
            "global_score": results.get("global_score", "—")
        }

    @staticmethod
    def render_footer() -> dict:
        return {
            "generated_by": "MindScan Enterprise v3.0",
            "version": "3.0"
        }

    def build(self, test_id: str, results: dict) -> dict:
        raise NotImplementedError("Subclasses devem implementar build().")
