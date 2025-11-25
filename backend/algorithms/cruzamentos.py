# cruzamentos.py
# MindScan Rebuild – Cross Insights (Cruzamentos Psicométricos)
# Versão Final e Definitiva — Inovexa / MindScan
# Autor: Leo Vinci – IA Supervisora Inovexa
# Última atualização: 23/11/2025
# -------------------------------------------------------------------------
# Este módulo gera cruzamentos inteligentes entre todos os modelos do MindScan:
#
#   - Big Five (OCEAN)
#   - TEIQue (Inteligência Emocional Traço)
#   - DASS-21 (Clínico: Depressão, Ansiedade, Estresse)
#   - Esquemas (18 Esquemas Desadaptativos – Young)
#   - Performance MindScan
#   - Bússola de Competências
#   - OCAI (Perfil Cultural Organizacional)
#
# Objetivos:
#   - Identificar padrões combinados
#   - Gerar alertas e insights
#   - Detectar riscos psicossociais
#   - Encontrar coerências ou contradições de perfil
#   - Criar indicadores avançados
#   - Entregar estrutura final ao Diagnostic Engine
# -------------------------------------------------------------------------

from typing import Dict, Any, List


class CrossInsights:
    """
    Módulo definitivo de cruzamentos psicométricos.
    Recebe *todos* os resultados brutos do MindScan e gera insights agregados.
    """

    # Limiares gerais para alertas
    HIGH = 75
    LOW = 25

    def __init__(self, data: Dict[str, Any]):
        """
        data deve conter:
        {
            "big5": {...},
            "teique": {...},
            "dass21": {...},
            "esquemas": {...},
            "performance": {...},
            "bussola": {...},
            "ocai": {...}
        }
        """
        self.data = data

    # -------------------------------------------------------------
    # Funções auxiliares
    # -------------------------------------------------------------

    def _is_high(self, value: float) -> bool:
        return value >= self.HIGH

    def _is_low(self, value: float) -> bool:
        return value <= self.LOW

    # -------------------------------------------------------------
    # CRUZAMENTO 1: Big Five × TEIQue
    # -------------------------------------------------------------

    def _cross_big5_teique(self) -> List[str]:
        insights = []

        big5 = self.data["big5"]["results"]
        tei = self.data["teique"]["results"]

        # Extroversão + Sociabilidade emocional
        if self._is_high(big5["E"]) and self._is_high(tei["S"]):
            insights.append("Alto potencial de engajamento social e comunicação emocional.")

        # Neuroticismo alto × Baixa regulação emocional
        if self._is_high(big5["N"]) and self._is_low(tei["RE"]):
            insights.append("Interação crítica: alta sensibilidade emocional com baixa regulação.")

        # Conscienciosidade × Autocontrole emocional
        if self._is_high(big5["C"]) and self._is_high(tei["AR"]):
            insights.append("Padrão de responsabilidade com maturidade emocional.")

        return insights

    # -------------------------------------------------------------
    # CRUZAMENTO 2: DASS-21 × Esquemas
    # -------------------------------------------------------------

    def _cross_dass_esquemas(self) -> List[str]:
        insights = []
        dass = self.data["dass21"]["results"]
        esquemas = self.data["esquemas"]["results"]

        # Depressão alta × Esquemas de Defectividade
        if self._is_high(dass["D"]) and self._is_high(esquemas.get("DV", 0)):
            insights.append("Sinal clínico: depressão elevada associada ao esquema de defectividade.")

        # Ansiedade alta × Vulnerabilidade
        if self._is_high(dass["A"]) and self._is_high(esquemas.get("VU", 0)):
            insights.append("Alta ansiedade combinada ao esquema de vulnerabilidade.")

        # Estresse alto × Padrões inflexíveis
        if self._is_high(dass["E"]) and self._is_high(esquemas.get("PI", 0)):
            insights.append("Estresse alto reforçado por padrões inflexíveis e autoexigência.")

        return insights

    # -------------------------------------------------------------
    # CRUZAMENTO 3: Performance × Bússola
    # -------------------------------------------------------------

    def _cross_performance_bussola(self) -> List[str]:
        insights = []

        perf = self.data["performance"]["results"]
        bus = self.data["bussola"]["results"]

        # Alta execução com baixa aprendizagem
        if self._is_high(bus["X"]) and self._is_low(bus["A"]):
            insights.append("Boa execução, mas baixa adaptabilidade e aprendizagem contínua.")

        # Estratégia alta + Propósito alto
        if self._is_high(bus["E"]) and self._is_high(bus["P"]):
            insights.append("Perfil estratégico sustentado por forte senso de propósito.")

        # Alta liderança + Alta performance global
        if self._is_high(bus["L"]) and perf["overall"] >= self.HIGH:
            insights.append("Indicador de liderança sólida com suporte de alta performance geral.")

        return insights

    # -------------------------------------------------------------
    # CRUZAMENTO 4: OCAI × Perfil Psicológico
    # -------------------------------------------------------------

    def _cross_ocai_profile(self) -> List[str]:
        insights = []
        ocai = self.data["ocai"]["profiles"]
        big5 = self.data["big5"]["results"]

        # Cultura Clan + Alta Amabilidade
        if ocai["C"] >= self.HIGH and self._is_high(big5["A"]):
            insights.append("Cultura colaborativa alinhada ao perfil altamente cooperativo.")

        # Cultura Mercado + Alta Conscienciosidade
        if ocai["M"] >= self.HIGH and self._is_high(big5["C"]):
            insights.append("Cultura orientada a resultados combinada com disciplina individual.")

        # Cultura Hierarquia + Neuroticismo alto → alerta
        if ocai["H"] >= self.HIGH and self._is_high(big5["N"]):
            insights.append("Ambiente rígido pode aumentar riscos emocionais em perfis sensíveis.")

        return insights

    # -------------------------------------------------------------
    # CRUZAMENTO 5: Padrões Compostos Avançados
    # -------------------------------------------------------------

    def _cross_advanced_patterns(self) -> List[str]:
        insights = []
        big5 = self.data["big5"]["results"]
        dass = self.data["dass21"]["results"]

        # Combo crítico: Neuroticismo muito alto + Estresse muito alto
        if big5["N"] >= 85 and dass["E"] >= 85:
            insights.append("Padrão crítico: alta reatividade emocional combinada com sobrecarga.")

        # Combo de excelência
        if big5["C"] >= 80 and big5["A"] >= 80:
            insights.append("Padrão de excelência pessoal: combinação rara de empatia e disciplina.")

        return insights

    # -------------------------------------------------------------
    # EXECUÇÃO FINAL
    # -------------------------------------------------------------

    def compute(self) -> Dict[str, Any]:
        insights = []

        insights.extend(self._cross_big5_teique())
        insights.extend(self._cross_dass_esquemas())
        insights.extend(self._cross_performance_bussola())
        insights.extend(self._cross_ocai_profile())
        insights.extend(self._cross_advanced_patterns())

        return {
            "model": "MindScan – Cross Insights",
            "insights": insights,
            "count": len(insights)
        }
