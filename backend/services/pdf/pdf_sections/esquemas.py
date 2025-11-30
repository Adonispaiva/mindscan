#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
esquemas.py — Seção de Esquemas (MindScan PDF Premium)
-------------------------------------------------------

Exibe:
- Intensidade dos esquemas identificados
- Impacto no funcionamento profissional
- Sínteses MI (se disponíveis)
- Orientações de desenvolvimento
"""

class EsquemasSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        esquemas_mi = mi.get("esquemas", {})

        esquemas = resultados.get("esquemas", {})

        texto_mi = esquemas_mi.get(
            "texto",
            "Os esquemas identificados representam padrões cognitivo-emocionais "
            "que influenciam comportamentos, decisões e relações profissionais."
        )

        # Monta tabela de esquemas
        linhas = []
        for nome, intensidade in esquemas.items():
            linhas.append(f"<tr><td>{nome}</td><td>{intensidade}</td></tr>")

        tabela = "".join(linhas) if linhas else "<tr><td colspan='2'>Nenhum esquema identificado</td></tr>"

        return f"""
<section class="esquemas">

    <h2 class="secao-titulo">Esquemas — Padrões Cognitivo-Emocionais</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-esquemas">
        <thead>
            <tr>
                <th>Esquema</th>
                <th>Intensidade</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""
