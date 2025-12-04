#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdi.py — PDI (Plano de Desenvolvimento Individual) — MindScan PDF Premium
Versão consolidada — Leo Vinci v2.0
---------------------------------------------------------------------------
Inclui:
- Curto prazo
- Médio prazo
- Longo prazo
- MI integrada
- Estrutura premium uniforme
"""

from typing import Dict, Any


def build_pdi(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial para seções PDF:
    {id, titulo, html}
    """

    mi = context.get("mi", {})
    pdi_mi = mi.get("pdi", {}) or {}

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

    def blocos(titulo: str, lista: list) -> str:
        itens = "".join(f"<li>{item}</li>" for item in lista)
        return f"""
        <div class="bloco-pdi">
            <h3>{titulo}</h3>
            <ul>{itens}</ul>
        </div>
        """

    html = f"""
<section class="pdi page">

    <h2 class="secao-titulo">Plano de Desenvolvimento Individual (PDI)</h2>

    <p class="mi-texto">{texto_mi}</p>

    <div class="container-pdi">
        {blocos("Objetivos de Curto Prazo", curto)}
        {blocos("Objetivos de Médio Prazo", medio)}
        {blocos("Objetivos de Longo Prazo", longo)}
    </div>

</section>
"""

    return {
        "id": "pdi",
        "titulo": "Plano de Desenvolvimento Individual (PDI)",
        "html": html
    }
