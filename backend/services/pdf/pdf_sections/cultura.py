# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\cultura.py
# Última atualização: 2025-12-11T09:59:21.215694

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cultura.py — Seção de Cultura Organizacional (OCAI) — MindScan PDF Premium
Versão consolidada — Leo Vinci v2.0
-----------------------------------------------------------
Apresenta:
- Perfil OCAI
- Interpretação MI cultural
- Estrutura premium padronizada
"""

from typing import Dict, Any


def build_cultura(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial de seção:
    {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    ocai = resultados.get("ocai", {})
    cultura_mi = mi.get("cultura", {})

    texto_mi = cultura_mi.get(
        "texto",
        "A análise cultural identifica as inclinações naturais do avaliado "
        "em termos de estrutura, flexibilidade, colaboração e orientação a resultados."
    )

    cla = ocai.get("cla", "—")
    adhoc = ocai.get("adhocracia", "—")
    mercado = ocai.get("mercado", "—")
    hier = ocai.get("hierarquia", "—")

    html = f"""
<section class="cultura page">

    <h2 class="secao-titulo">Cultura Organizacional (OCAI)</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Percentil</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Cultura Clã</td><td>{cla}</td></tr>
            <tr><td>Cultura Adhocracia</td><td>{adhoc}</td></tr>
            <tr><td>Cultura Mercado</td><td>{mercado}</td></tr>
            <tr><td>Cultura Hierarquia</td><td>{hier}</td></tr>
        </tbody>
    </table>

</section>
"""

    return {
        "id": "cultura",
        "titulo": "Cultura Organizacional (OCAI)",
        "html": html
    }
