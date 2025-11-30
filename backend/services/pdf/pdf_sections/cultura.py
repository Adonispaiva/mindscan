#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cultura.py — Seção de Cultura Organizacional (OCAI) — MindScan PDF Premium
--------------------------------------------------------------------------

Esta seção apresenta:
- Perfil cultural atual do avaliado
- Compatibilidade com culturas organizacionais (OCAI)
- Direções de desenvolvimento
- Análise MI (se disponível)
"""

class CulturaSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        cultura_mi = mi.get("cultura", {})

        ocai = resultados.get("ocai", {})

        texto_mi = cultura_mi.get(
            "texto",
            "A análise cultural identifica as inclinações naturais do avaliado em termos "
            "de estrutura, flexibilidade, colaboração e orientação a resultados."
        )

        def linha(nome, valor):
            return f"<tr><td>{nome}</td><td>{valor}</td></tr>"

        tabela = "".join([
            linha("Cultura Clã", ocai.get("cla", "—")),
            linha("Cultura Adhocracia", ocai.get("adhocracia", "—")),
            linha("Cultura Mercado", ocai.get("mercado", "—")),
            linha("Cultura Hierarquia", ocai.get("hierarquia", "—")),
        ])

        return f"""
<section class="cultura">

    <h2 class="secao-titulo">Cultura Organizacional (OCAI)</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-cultura">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Percentil</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""
