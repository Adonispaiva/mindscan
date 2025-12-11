# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\pdf_engine\sections\performance.py
# Última atualização: 2025-12-11T09:59:27.761619

"""
pdf_engine/sections/performance.py
Seção de Performance do relatório MindScan

Responsabilidades:
- Integrar resultados do módulo de performance consolidado
- Exibir histórico de desempenho, indicadores e tendências
- Organizar bloco textual + dados prontos para o PDFBuilder
- Não executa cálculos brutos (apenas apresenta)
"""

from typing import Dict, Any


class PerformanceSection:
    """
    Seção de Performance do MindScan.
    Baseada nos dados normalizados entregues pelo DataLoader.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.performance = data.get("performance", {})

    # -------------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Retorna uma estrutura padronizada que o PDFBuilder converte em PDF.
        Inclui:
        - título
        - subtítulo
        - texto contextual
        - indicadores numéricos
        - histórico (se existir)
        """
        return {
            "title": "Performance e Produtividade",
            "subtitle": "Histórico, Indicadores e Tendências",
            "body": self._build_body_text(),
            "scores": self._extract_indicators(),
            "history": self.performance.get("historico", []),
        }

    # -------------------------------------------------------------------------
    # TEXTO PRINCIPAL
    # -------------------------------------------------------------------------

    def _build_body_text(self) -> str:
        indicadores = self._extract_indicators()
        hist = self.performance.get("historico", [])

        txt_ind = "\n".join([f"- {k.capitalize()}: {v}" for k, v in indicadores.items()]) or "Nenhum indicador disponível."
        txt_hist = f"Foram identificados {len(hist)} períodos de histórico de performance." if hist else "Não há registros históricos disponíveis."

        return (
            "Esta seção apresenta os indicadores gerais de performance, bem como o "
            "histórico de evolução comportamental e produtiva do participante. "
            "As informações abaixo ajudam a compor uma visão objetiva e contextual "
            "sobre sua consistência, desempenho e eficiência ao longo do tempo.\n\n"
            f"📊 **Indicadores de Performance:**\n{txt_ind}\n\n"
            f"📈 **Histórico:**\n{txt_hist}"
        )

    # -------------------------------------------------------------------------
    # INDICADORES DE PERFORMANCE
    # -------------------------------------------------------------------------

    def _extract_indicators(self) -> Dict[str, Any]:
        """
        Extrai indicadores principais do bloco de performance.
        Ex.: consistência, entregas, evolução, produtividade.
        """
        if not isinstance(self.performance, dict):
            return {}

        # Campos comuns — adaptáveis conforme o dado real
        indicadores = {
            "consistencia": self.performance.get("consistencia", "N/D"),
            "producao": self.performance.get("producao", "N/D"),
            "entregas": self.performance.get("entregas", "N/D"),
            "evolucao": self.performance.get("evolucao", "N/D"),
        }

        return indicadores


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def build_performance_section(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interface simples para uso pelo PDFBuilder.
    """
    return PerformanceSection(data).render()
