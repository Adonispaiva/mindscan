#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dass.py — Seção DASS-21 (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-----------------------------------------------------------
Exibe:
- Depressão
- Ansiedade
- Estresse
"""

from typing import Dict, Any


def build_dass(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial: {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    dass = resultados.get("dass", {}) or {}
    dass_mi = mi.get("dass", {}) or {}

    texto_mi = dass_mi.get(
        "texto",
        "A avaliação DASS-21 identifica níveis emocionais relacionados a "
        "depressão, ansiedade e estresse, permitindo compreender como o "
        "avaliado responde às pressões do ambiente profissional."
    )

    depressao = dass.get("depressao", "—")
    ansiedade = dass.get("ansiedade", "—")
    estresse = dass.get("estresse", "—")

    html = f"""
<section class="dass page">

    <h2 class="secao-titulo">DASS-21 — Estresse, Ansiedade e Depressão</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Nível</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Depressão</td><td>{depressao}</td></tr>
            <tr><td>Ansiedade</td><td>{ansiedade}</td></tr>
            <tr><td>Estresse</td><td>{estresse}</td></tr>
        </tbody>
    </table>

</section>
"""

    return {
        "id": "dass",
        "titulo": "DASS-21 — Estresse, Ansiedade e Depressão",
        "html": html
    }
