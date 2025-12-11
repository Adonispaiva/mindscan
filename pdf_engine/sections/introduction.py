# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\pdf_engine\sections\introduction.py
# Última atualização: 2025-12-11T09:59:27.761619

"""
pdf_engine/sections/introduction.py
Seção de Introdução do relatório MindScan

Responsabilidades:
- Criar a abertura do PDF
- Renderizar informações gerais do participante
- Exibir contextualização do MindScan
- Não faz cálculos psicométricos
"""

from typing import Dict, Any


class IntroductionSection:
    """
    Seção inicial do PDF MindScan.
    Recebe os dados já normalizados pelo DataLoader e monta o texto/estrutura
    que será consumido pelo PDFBuilder.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    # -------------------------------------------------------------------------
    # BLOCO PRINCIPAL DA SEÇÃO
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Gera uma estrutura padronizada contendo:
        - título
        - subtítulo
        - texto introdutório
        - informações iniciais do relatório
        """
        return {
            "title": "Relatório MindScan",
            "subtitle": "Análise Integrada de Perfil Psicológico, Comportamental e Organizacional",
            "body": self._build_body_text(),
            "metadata": self._extract_metadata(),
        }

    # -------------------------------------------------------------------------
    # CONSTRUÇÃO DO TEXTO
    # -------------------------------------------------------------------------

    def _build_body_text(self) -> str:
        """
        Texto introdutório padrão do relatório.
        Pode ser expandido conforme necessidade.
        """

        return (
            "Este relatório reúne uma análise integrada composta pelos principais "
            "fatores psicológicos, emocionais, comportamentais e organizacionais que "
            "formam o MindScan. Todos os dados foram processados por algoritmos "
            "especializados e consolidados em uma visão única e objetiva."
        )

    # -------------------------------------------------------------------------
    # METADADOS INICIAIS
    # -------------------------------------------------------------------------

    def _extract_metadata(self) -> Dict[str, Any]:
        """
        Pode extrair dados do participante quando disponíveis.
        """
        participant = self.data.get("participant", {})

        return {
            "name": participant.get("name", "Participante"),
            "role": participant.get("role", "Função não informada"),
            "date": participant.get("date", "Data não informada"),
            "version": "MindScan v3 – PDF Engine",
        }


# -------------------------------------------------------------------------
# Função utilitária da seção
# -------------------------------------------------------------------------

def build_introduction_section(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interface simples para uso pelo PDFBuilder.
    """
    return IntroductionSection(data).render()
