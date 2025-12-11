# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_strengths.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Esquemas Strengths
Identifica forças psicodinâmicas (lado adaptativo) associadas aos esquemas.
"""

from typing import Dict


class EsquemasStrengths:
    """
    Mesmo esquemas elevados podem ter aspectos funcionais.
    Este módulo identifica essas forças.
    """

    def __init__(self):
        self.version = "1.0"

        self.strength_map = {
            "abandono": "Sensibilidade emocional e busca por vínculos profundos.",
            "desconfianca": "Capacidade de cautela e proteção pessoal.",
            "privacao_emocional": "Alta percepção das necessidades afetivas.",
            "defectividade": "Autocrítica que pode sustentar desenvolvimento.",
            "isolamento": "Independência emocional.",
            "dependencia": "Capacidade de pedir ajuda.",
            "vulnerabilidade": "Atenção aos riscos reais.",
            "emaranhamento": "Forte senso de vínculo e empatia.",
            "fracasso": "Humildade e realismo.",
            "submissao": "Diplomacia e harmonia relacional.",
            "autossacrificio": "Altruísmo genuíno.",
            "busca_aprovacao": "Habilidade social e sensibilidade interpessoal.",
            "negatividade": "Capacidade de antecipar problemas.",
            "inibicao_emocional": "Autocontrole elevado.",
            "hipercriticismo": "Disciplina e busca de excelência.",
            "direitos_especiais": "Autoconfiança e iniciativa.",
            "autocontrole_insuficiente": "Espontaneidade.",
            "padrões_inflexíveis": "Organização e consistência.",
        }

    def extract(self, classified: Dict[str, float]) -> Dict[str, str]:
        """
        Forças são listadas para esquemas >40 (predisposição funcional).
        """
        strengths = {}

        for schema, value in classified.items():
            if value >= 40:
                strengths[schema] = self.strength_map.get(
                    schema,
                    "Aspecto funcional associado ao esquema."
                )

        return strengths
