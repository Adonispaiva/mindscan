"""
pdf_engine/core/renderer.py
Módulo: Renderização das seções do PDF do MindScan

Responsabilidades:
- Receber o conteúdo das seções
- Unificar e montar o documento intermediário
- Aplicar templates
- Preparar a estrutura final que será enviada ao PDFBuilder
"""

from typing import Dict, Any, List


class RendererError(Exception):
    """Erro específico do Renderer."""
    pass


class Renderer:
    """
    Classe responsável por montar o documento intermediário
    antes da exportação em PDF.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        :param data: dados estruturados carregados pelo DataLoader
        """
        if not isinstance(data, dict):
            raise RendererError("Renderer recebeu dados inválidos.")

        self.data = data
        self.sections: List[Dict[str, Any]] = []
        self.document: Dict[str, Any] = {}

    # -------------------------------------------------------------------------
    # CONTROLE DE SEÇÕES
    # -------------------------------------------------------------------------

    def add_section(self, section_name: str, content: Dict[str, Any]):
        """
        Adiciona uma seção renderizada ao documento.
        """
        if not isinstance(content, dict):
            raise RendererError(f"Seção '{section_name}' deve retornar um dicionário.")

        self.sections.append({
            "name": section_name,
            "content": content
        })

    # -------------------------------------------------------------------------
    # TEMPLATE
    # -------------------------------------------------------------------------

    def apply_template(self):
        """
        Cria a estrutura final do documento intermediário.
        Este método pode ser estendido para aplicar temas/estilos.
        """
        return {
            "title": "Relatório MindScan",
            "theme": "default",
            "sections": self.sections
        }

    # -------------------------------------------------------------------------
    # EXECUÇÃO
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Renderiza o documento completo e retorna a estrutura
        que será passada ao PDFBuilder.
        """
        if not self.sections:
            raise RendererError("Nenhuma seção foi adicionada ao Renderer.")

        try:
            self.document = self.apply_template()
            return self.document
        except Exception as e:
            raise RendererError(f"Erro ao renderizar documento: {e}")


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def render_document(sections: List[Dict[str, Any]], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Renderização simples via função direta.
    """
    renderer = Renderer(data)

    for sec in sections:
        renderer.add_section(sec["name"], sec["content"])

    return renderer.render()
