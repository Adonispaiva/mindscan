#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdi.py — Plano de Desenvolvimento Individual (MindScan PDF Premium)
-------------------------------------------------------------------

Inclui:
- Objetivos de curto, médio e longo prazo
- Plano de ação estratégico
- Reforços positivos
- Direcionadores de desenvolvimento
- Estrutura flexível alimentada por MI
"""

class PDISection:
    def render(self, context: dict) -> str:

        mi = context.get("mi", {})
        pdi_mi = mi.get("pdi", {})

        texto_mi = pdi_mi.get(
            "texto",
            "O Plano de Desenvolvimento Individual organiza ações estratégicas para "
            "fortalecer competências, reduzir vulnerabilidades e impulsionar crescimento profissional."
        )

        curto = pdi_mi.get("curto_prazo", [
            "Reforçar práticas de foco e organização.",
            "Implementar estratégias semanais de autorregulação emocional."
        ])

        medio = pdi_mi.get("medio_prazo", [
            "Desenvolver assertividade em ambientes de tomada de decisão.",
            "Expandir tolerância a incertezas em projetos complexos."
        ])

        longo = pdi_mi.get("longo_prazo", [
            "Consolidar liderança situacional.",
            "Aprimorar visão estratégica e influência macroorganizacional."
        ])

        def blocos(titulo, lista):
            itens = "".join([f"<li>{item}</li>" for item in lista])
            return f"""
            <div class="bloco-pdi">
                <h3>{titulo}</h3>
                <ul>{itens}</ul>
            </div>
            """

        return f"""
<section class="pdi">

    <h2 class="secao-titulo">Plano de Desenvolvimento Individual (PDI)</h2>

    <p class="mi-texto">{texto_mi}</p>

    <div class="container-pdi">
        {blocos("Objetivos de Curto Prazo", curto)}
        {blocos("Objetivos de Médio Prazo", medio)}
        {blocos("Objetivos de Longo Prazo", longo)}
    </div>

</section>
"""
