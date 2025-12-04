"""
DASS21 Forms — Versão ULTRA SUPERIOR
--------------------------------------------------------------

Representa e valida o formulário completo do DASS21.

Útil em:
- validação de payloads
- criação de instâncias padrão
- APIs de entrada
"""

from typing import Dict, Any


class DASS21Forms:
    def __init__(self):
        self.version = "2.0-ultra"

    def template(self) -> Dict[str, int]:
        return {
            "depressao": 0,
            "ansiedade": 0,
            "stress": 0,
        }

    def validate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        required = ["depressao", "ansiedade", "stress"]

        for r in required:
            if r not in payload:
                raise ValueError(f"Campo obrigatório ausente: {r}")
            if not isinstance(payload[r], (int, float)):
                raise TypeError(f"Campo {r} deve ser numérico.")

        return payload
