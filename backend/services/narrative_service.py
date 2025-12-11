# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\narrative_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
narrative_service.py
--------------------

Serviço responsável por gerar a narrativa textual do MindScan.
Converte insights, padrões, riscos e forças em texto profissional,
estruturado, consistente e adequado ao estilo corporativo.

Este módulo é crucial, pois alimenta:
- renderers
- seções PDF
- resumo estratégico
- narrativa final
"""

from typing import Dict, Any, List


class NarrativeService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.insights: List[str] = payload.get("insights", [])
        self.context: Dict[str, Any] = payload.get("context", {})

    # --------------------------------------------------------------
    # Construção de parágrafos baseados nos insights
    # --------------------------------------------------------------
    def build_strengths_paragraph(self) -> str:
        strengths = [i for i in self.insights if "boa" in i.lower() or "alta" in i.lower()]
        if not strengths:
            return "O perfil apresenta estabilidade geral, sem destaques expressivos nos fatores avaliados."
        body = "O MindScan identificou pontos fortes relevantes, incluindo: "
        body += "; ".join(strengths) + "."
        return body

    def build_risks_paragraph(self) -> str:
        risks = [i for i in self.insights if "risco" in i.lower() or "atenção" in i.lower()]
        if not risks:
            return "Não foram observados riscos significativos que possam comprometer o desempenho atual."
        body = "Alguns pontos exigem atenção e monitoramento contínuo, tais como: "
        body += "; ".join(risks) + "."
        return body

    def build_behavior_paragraph(self) -> str:
        name = self.context.get("name", "O indivíduo")
        return (
            f"{name} demonstra um conjunto de características comportamentais derivadas de padrões emocionais, "
            f"cognitivos e interpessoais identificados pelo MindScan. Esses elementos contribuem para o "
            f"posicionamento profissional e social, influenciando a forma como desafios e oportunidades são enfrentados."
        )

    # --------------------------------------------------------------
    # Montagem final da narrativa
    # --------------------------------------------------------------
    def build(self) -> Dict[str, str]:
        return {
            "narrativa_forcas": self.build_strengths_paragraph(),
            "narrativa_riscos": self.build_risks_paragraph(),
            "narrativa_comportamento": self.build_behavior_paragraph(),
        }
