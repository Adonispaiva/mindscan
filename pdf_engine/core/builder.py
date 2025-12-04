"""
pdf_engine/core/builder.py
PDFBuilder — Núcleo de montagem estrutural do PDF MindScan

Responsabilidades:
- Orquestrar a construção completa do documento
- Integrar todas as seções (introduction, personality, emotional, culture, performance, final_report)
- Criar uma estrutura única (document dict) para entrega ao renderer
- Não renderiza PDF — apenas organiza conteúdo

Fluxo:
    loader → pipeline → PDFBuilder.build() → renderer.export()
"""

from typing import Dict, Any

# Importa todas as seções da camada sections/
from ..sections.introduction import build_introduction_section
from ..sections.emotional import build_emotional_section
from ..sections.culture import build_culture_section
from ..sections.performance import build_performance_section
from ..sections.final_report import build_final_report_section

# Personality (Big Five) ainda não gerado pelo usuário → placeholder seguro
# Para evitar quebra antes da geração do arquivo personality.py:
try:
    from ..sections.personality import build_personality_section
except Exception:
    def build_personality_section(data):
        return {
            "title": "Personalidade (Big Five)",
            "subtitle": "Seção ainda não implementada.",
            "body": "A seção de personalidade será incluída assim que o arquivo estiver disponível.",
            "scores": {},
        }


class PDFBuilderError(Exception):
    """Erro específico do PDFBuilder."""
    pass


class PDFBuilder:
    """
    Monta o documento de forma modular.
    Cada seção retorna um dict, e o builder agrega tudo em uma estrutura final.
    """

    def __init__(self, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise PDFBuilderError("PDFBuilder exige dados normalizados do DataLoader.")

        self.data = data
        self.document = {}

    # -------------------------------------------------------------------------
    # CONSTRUÇÃO DO DOCUMENTO COMPLETO
    # -------------------------------------------------------------------------

    def build(self) -> Dict[str, Any]:
        """
        Agrupa todas as seções de forma ordenada em um único documento.
        O renderer utiliza esse dict para gerar o PDF final.
        """

        try:
            self.document = {
                "title": "Relatório MindScan",
                "subtitle": "Análise Integrada",
                "sections": [
                    build_introduction_section(self.data),
                    build_personality_section(self.data),
                    build_emotional_section(self.data),
                    build_culture_section(self.data),
                    build_performance_section(self.data),
                    build_final_report_section(self.data),
                ],
            }
        except Exception as e:
            raise PDFBuilderError(f"Erro ao montar documento: {e}")

        return self.document

    # -------------------------------------------------------------------------
    # EXPORTAÇÃO (chama renderer externo)
    # -------------------------------------------------------------------------

    def export(self, document: Dict[str, Any], output_path: str) -> str:
        """
        O renderer real está no módulo renderer.py
        Aqui apenas chamamos a função apropriada.
        """

        try:
            from .renderer import PDFRenderer
        except Exception as e:
            raise PDFBuilderError(f"Renderer indisponível: {e}")

        renderer = PDFRenderer()
        return renderer.render(document, output_path)


# -------------------------------------------------------------------------
# Função utilitária simples
# -------------------------------------------------------------------------

def build_pdf(data: Dict[str, Any], output_path: str) -> str:
    """
    Interface direta:
    data → PDFBuilder → PDF final
    """
    builder = PDFBuilder(data)
    document = builder.build()

    from .renderer import PDFRenderer
    renderer = PDFRenderer()

    return renderer.render(document, output_path)
