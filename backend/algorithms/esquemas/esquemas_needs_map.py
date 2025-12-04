"""
Esquemas Needs Map
Mapeia cada um dos 18 Esquemas de Young para suas necessidades emocionais
não atendidas, segundo o modelo original.
"""

from typing import Dict


class EsquemasNeedsMap:
    """
    Fornece mapeamento fundamental para narrativa psicodinâmica.
    """

    def __init__(self):
        self.version = "1.0"

        self.needs = {
            "abandono": "Necessidade de segurança emocional e estabilidade nas relações.",
            "desconfianca": "Necessidade de previsibilidade, transparência e proteção.",
            "privacao_emocional": "Necessidade de validação afetiva consistente.",
            "defectividade": "Necessidade de aceitação, valor pessoal e reconhecimento.",
            "isolamento": "Necessidade de pertencimento e conexão social.",
            "dependencia": "Necessidade de autonomia e autoeficácia.",
            "vulnerabilidade": "Necessidade de proteção e competência diante de ameaças.",
            "emaranhamento": "Necessidade de identidade própria e autodeterminação.",
            "fracasso": "Necessidade de competência e senso de capacidade.",
            "submissao": "Necessidade de assertividade e autodireção.",
            "autossacrificio": "Necessidade de autocuidado e limites saudáveis.",
            "busca_aprovacao": "Necessidade de autoestima interna e autonomia.",
            "negatividade": "Necessidade de autorregulação e flexibilidade cognitiva.",
            "inibicao_emocional": "Necessidade de expressão emocional segura.",
            "hipercriticismo": "Necessidade de equilíbrio e autocompaixão.",
            "direitos_especiais": "Necessidade de reciprocidade e responsabilidade.",
            "autocontrole_insuficiente": "Necessidade de disciplina emocional.",
            "padrões_inflexíveis": "Necessidade de flexibilidade e adaptabilidade.",
        }

    def map(self, classified_schemas: Dict[str, float]) -> Dict[str, str]:
        """
        Retorna necessidades emocionais relevantes apenas para esquemas elevados (>50).
        """
        results = {}

        for schema, value in classified_schemas.items():
            if value >= 50:
                results[schema] = self.needs.get(
                    schema,
                    "Necessidade emocional associada ao esquema."
                )

        return {
            "module": "Esquemas",
            "version": self.version,
            "needs_map": results,
        }
