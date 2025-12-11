# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass\dass_validation.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS – VALIDATION ENGINE (Versão ULTRA SUPERIOR)
Valida entradas para o DASS clássico e assegura conformidade estrutural.
"""

from typing import Dict


class DASSValidation:

    REQUIRED_DOMAINS = {"stress", "anxiety", "depression"}

    @staticmethod
    def validate_scores(data: Dict[str, float]) -> Dict:
        """
        Valida estrutura e valores do DASS clássico.
        """
        missing = DASSValidation.REQUIRED_DOMAINS - set(data.keys())
        if missing:
            raise ValueError(f"Domínios faltando: {', '.join(missing)}")

        invalid = {k: v for k, v in data.items() if not isinstance(v, (int, float))}
        if invalid:
            raise TypeError(f"Valores inválidos: {invalid}")

        negative = {k: v for k, v in data.items() if v < 0}
        if negative:
            raise ValueError(f"Valores negativos detectados: {negative}")

        return {"status": "valid", "domains": list(data.keys())}
