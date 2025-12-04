"""
pdf_engine/core/pipeline.py
Pipeline principal do PDF Engine do MindScan

Responsabilidade:
- Orquestra o fluxo completo para gerar um PDF
- Carrega dados via DataLoader
- Inicializa seções
- Transfere dados ao Builder
- Controla a ordem de montagem
- Não realiza renderização direta (isso é trabalho do renderer)
"""

from typing import Dict, Any, List

from .loader import load_data
from .builder import PDFBuilder


class PipelineError(Exception):
    """Erros do pipeline PDF."""
    pass


class PDFPipeline:
    """
    Pipeline completo do PDF Engine.
    Responsável por coordenar etapas e entregar um pacote pronto
    para o builder renderizar.
    """

    def __init__(self, raw_data: Dict[str, Any]):
        """
        :param raw_data: dicionário contendo todas as saídas dos algoritmos MindScan
        """
        if not isinstance(raw_data, dict):
            raise PipelineError("Pipeline exige um dicionário como entrada.")

        self.raw_data = raw_data
        self.cleaned_data: Dict[str, Any] = {}
        self.sections: List[Any] = []

    # ---------------------------------------------------------------------
    # Etapa 1 — Carregamento e normalização dos dados
    # ---------------------------------------------------------------------

    def load(self):
        """
        Executa o DataLoader para normalizar todos os dados.
        """
        self.cleaned_data = load_data(self.raw_data)
        return self.cleaned_data

    # ---------------------------------------------------------------------
    # Etapa 2 — Registro de seções
    # ---------------------------------------------------------------------

    def add_section(self, section):
        """
        Registra uma seção do PDF.

        Cada seção deve implementar um método:
        - build(cleaned_data) → retorna conteúdo estruturado daquela seção
        """
        if not hasattr(section, "build"):
            raise PipelineError(
                f"Seção inválida: {section.__class__.__name__} não possui método build()."
            )
        self.sections.append(section)

    # ---------------------------------------------------------------------
    # Etapa 3 — Execução das seções
    # ---------------------------------------------------------------------

    def run_sections(self) -> List[Dict[str, Any]]:
        """
        Executa todas as seções registradas e retorna a lista de outputs.
        """
        outputs = []

        for section in self.sections:
            result = section.build(self.cleaned_data)

            if not isinstance(result, dict):
                raise PipelineError(
                    f"A seção {section.__class__.__name__} retornou um "
                    "formato inválido: deve ser dict."
                )

            outputs.append(
                {
                    "section": section.__class__.__name__,
                    "content": result
                }
            )

        return outputs

    # ---------------------------------------------------------------------
    # Etapa 4 — Construção final via Builder
    # ---------------------------------------------------------------------

    def build_pdf(self, output_path: str):
        """
        Coordena todo o fluxo e invoca o Builder para gerar o PDF final.
        """

        # 1. Carregar dados
        self.load()

        # 2. Executar seções
        sections_output = self.run_sections()

        # 3. Enviar ao Builder
        builder = PDFBuilder()
        builder.load_sections(sections_output)
        builder.build(output_path)

        return output_path


# -------------------------------------------------------------------------
# Função auxiliar
# -------------------------------------------------------------------------

def generate_pdf(data: Dict[str, Any], sections: List[Any], output_path: str):
    """
    Gera um PDF completo usando pipeline + builder.
    API simplificada para chamadas externas.
    """
    pipe = PDFPipeline(data)

    for sec in sections:
        pipe.add_section(sec)

    return pipe.build_pdf(output_path)
