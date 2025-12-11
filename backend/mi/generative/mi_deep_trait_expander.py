# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_deep_trait_expander.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIDeepTraitExpander:
    """
    Expande traços psicométricos em subdimensões interpretativas.
    """

    SUBDIMENSIONS = {
        "extroversao": ["iniciativa social", "assertividade", "nível de energia"],
        "consciencia": ["disciplina", "organização", "consistência"],
        "amabilidade": ["cooperação", "paciência", "relacionalidade"],
        "abertura": ["criatividade", "curiosidade", "flexibilidade"],
    }

    @staticmethod
    def expand(big5: dict) -> dict:
        expansion = {}

        for trait, value in big5.items():
            dims = MIDeepTraitExpander.SUBDIMENSIONS.get(trait)
            if dims:
                expansion[trait] = {
                    dim: round(value * 0.95 + i * 0.5, 2)
                    for i, dim in enumerate(dims)
                }

        return expansion
