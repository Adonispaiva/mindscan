#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_validator.py — Validador Oficial de Dados do MindScan PDF Engine
---------------------------------------------------------------------

Este módulo valida todos os dados necessários antes da geração do PDF,
garantindo integridade, consistência e proteção contra relatórios corrompidos.

Ele valida três blocos:
- dados_usuario (identidade)
- resultados (algoritmos)
- mi (textos interpretativos)

Se algo estiver incorreto, o validador levanta um erro claro e bloqueia o PDF.
"""

from typing import Dict, Any


class MindScanDataValidator:

    # ============================================================
    # ENTRADA PRINCIPAL
    # ============================================================
    def validar(self, usuario: Dict[str, Any], resultados: Dict[str, Any], mi: Dict[str, Any]):
        """
        Valida todos os blocos de informação.
        Lança ValueError se algo estiver inválido.
        """
        self._validar_usuario(usuario)
        self._validar_resultados(resultados)
        self._validar_mi(mi)

        return True  # Se passou sem erro, está válido.

    # ============================================================
    # VALIDAR USUÁRIO
    # ============================================================
    def _validar_usuario(self, usuario: Dict[str, Any]):
        obrigatorios = ["nome", "cargo"]

        for campo in obrigatorios:
            if campo not in usuario or not usuario[campo]:
                raise ValueError(f"[MindScan Validator] Campo obrigatório ausente em 'usuario': {campo}")

        if "idade" in usuario:
            if not isinstance(usuario["idade"], int):
                raise ValueError("[MindScan Validator] 'idade' deve ser um número inteiro.")

    # ============================================================
    # VALIDAR RESULTADOS DOS ALGORITMOS
    # ============================================================
    def _validar_resultados(self, resultados: Dict[str, Any]):
        obrigatorios = ["big_five", "dass", "esquemas"]

        for campo in obrigatorios:
            if campo not in resultados:
                raise ValueError(f"[MindScan Validator] Campo obrigatório ausente em 'resultados': {campo}")

        # Big Five deve conter 5 dimensões
        if "big_five" in resultados:
            bf = resultados["big_five"]
            dimensoes = ["abertura", "conscienciosidade", "extroversao", "agradabilidade", "neuroticismo"]

            for d in dimensoes:
                if d not in bf:
                    raise ValueError(f"[MindScan Validator] Dimensão Big Five ausente: {d}")

    # ============================================================
    # VALIDAR MI (MIND INTELLIGENCE)
    # ============================================================
    def _validar_mi(self, mi: Dict[str, Any]):
        """
        MI não exige campos obrigatórios.
        Porém, se presentes, devem ser strings ou listas válidas.
        """
        for chave, item in mi.items():

            # Caso seja texto simples
            if isinstance(item, dict) and "texto" in item:
                if not isinstance(item["texto"], str):
                    raise ValueError(f"[MindScan Validator] Texto MI inválido em '{chave}'. Deve ser string.")

            # Caso tenha listas
            if isinstance(item, dict):
                for campo, valor in item.items():
                    if isinstance(valor, list):
                        for elemento in valor:
                            if not isinstance(elemento, (str, int, float)):
                                raise ValueError(
                                    f"[MindScan Validator] Elemento inválido na lista '{campo}' em MI[{chave}]"
                                )


# ========================================================================
# AUTOTESTE RÁPIDO (opcional)
# ========================================================================
if __name__ == "__main__":
    validator = MindScanDataValidator()

    usuario = {"nome": "Teste", "cargo": "Dev", "idade": 30}
    resultados = {
        "big_five": {
            "abertura": 50,
            "conscienciosidade": 60,
            "extroversao": 40,
            "agradabilidade": 70,
            "neuroticismo": 30,
        },
        "dass": {"depressao": "Normal", "ansiedade": "Leve", "estresse": "Moderado"},
        "esquemas": {"Autoexigência": "Moderado"},
    }
    mi = {"resumo_executivo": {"texto": "Tudo ok."}}

    validator.validar(usuario, resultados, mi)
    print("✔ Dados válidos.")
