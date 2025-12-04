"""
Esquemas Crosslinks
Gera cruzamentos entre esquemas predominantes e outros módulos,
como Big Five, TEIQue e DASS-21.
"""

from typing import Dict, Any


class EsquemasCrosslinks:
    """
    Produz relações intermodulares para uso em:
    - narrativa
    - recomendações
    - relatório psicodinâmico
    """

    def __init__(self):
        self.version = "1.0"

        # Relações principais entre esquemas e perfis emocionais
        self.cross_map = {
            "abandono": "Associa-se a instabilidade emocional e medo de perda.",
            "desconfianca": "Relaciona-se a hipervigilância e ansiedade social.",
            "privacao_emocional": "Conecta-se a TEIQue (empatia e vínculos).",
            "defectividade": "Impacta autoestima e autocrítica.",
            "isolamento": "Afeta engajamento social e vinculação.",
            "dependencia": "Relaciona-se à baixa autonomia no Big Five.",
            "vulnerabilidade": "Conecta-se a ansiedade e estresse (DASS-21).",
            "emaranhamento": "Impacta autonomia e identidade pessoal.",
            "fracasso": "Associado à percepção negativa de autoeficácia.",
            "submissao": "Relacionado a baixa assertividade.",
            "autossacrificio": "Conecta-se a empatia elevada e exaustão emocional.",
            "busca_aprovacao": "Relaciona-se a baixa autodeterminação.",
            "negatividade": "Forte relação com depressão no DASS-21.",
            "inibicao_emocional": "Relaciona-se ao controle emocional rígido.",
            "hipercriticismo": "Associado a perfeccionismo disfuncional.",
            "direitos_especiais": "Conecta-se a dominância e impulsividade.",
            "autocontrole_insuficiente": "Relacionado a impulsividade e frustração.",
            "padrões_inflexíveis": "Conecta-se a rigidez cognitiva.",
        }

    def generate(self, classified: Dict[str, float]) -> Dict[str, Any]:
        """
        Gera crosslinks apenas para esquemas com pontuação significativa (>50).
        """

        results = {}

        for schema, value in classified.items():
            if value >= 50:
                results[schema] = self.cross_map.get(
                    schema,
                    "Interação psicodinâmica relevante com outros módulos."
                )

        return {
            "module": "Esquemas",
            "version": self.version,
            "crosslinks": results,
        }
