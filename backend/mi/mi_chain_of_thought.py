# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_chain_of_thought.py
# Última atualização: 2025-12-11T09:59:20.856706

"""
MI Chain of Thought — Gerador estruturado da cadeia de raciocínio interno
para uso exclusivo do motor MI do MindScan.
"""

from __future__ import annotations
from typing import List, Dict, Any
from pydantic import BaseModel


class ThoughtStep(BaseModel):
    step: int
    reasoning: str
    evidence: str
    conclusion: str


class MIChainOfThought:
    """
    Responsável por construir cadeias de raciocínio completas e estruturadas.
    """

    def __init__(self):
        self.steps: List[ThoughtStep] = []

    def add_step(self, reasoning: str, evidence: str, conclusion: str) -> ThoughtStep:
        step = ThoughtStep(
            step=len(self.steps) + 1,
            reasoning=reasoning,
            evidence=evidence,
            conclusion=conclusion,
        )
        self.steps.append(step)
        return step

    def generate(self) -> List[Dict[str, Any]]:
        """Retorna a cadeia estruturada."""
        return [s.dict() for s in self.steps]

    def summarize(self) -> str:
        """Resumo lógico da cadeia inteira."""
        return " → ".join([s.conclusion for s in self.steps])

    def reset(self):
        self.steps = []


if __name__ == "__main__":
    cot = MIChainOfThought()
    cot.add_step("Analisando perfil.", "Big5 alto em Abertura.", "Indivíduo criativo.")
    cot.add_step("Relacionando características.", "Aparece também alta Conscienciosidade.", "Equilíbrio ideal.")
    cot.add_step("Conclusão final.", "Dados consistentes.", "Perfil propício para inovação.")

    print(cot.generate())
    print("Resumo:", cot.summarize())
