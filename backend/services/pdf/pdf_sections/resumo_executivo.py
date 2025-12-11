# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\resumo_executivo.py
# Última atualização: 2025-12-11T09:59:21.231327

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resumo_executivo.py — Seção de Resumo Executivo (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-----------------------------------------------------------
Resumo estratégico do diagnóstico, unificando:
- síntese geral,
- destaques positivos,
- pontos de atenção,
- diretrizes de decisão.
"""

from typing import Dict, Any


def build_resumo_executivo(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial: {id, titulo, html}
    Compatível com PDFEngine e templates premium.
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})
    resumo = mi.get("resumo_executivo", {})

    # Texto MI (fallback seguro)
    texto_resumo = resumo.get(
        "texto",
        "O MindScan identificou padrões comportamentais, emocionais e "
        "cognitivos que explicam com precisão a atuação profissional do avaliado."
    )

    destaques = resumo.get(
        "destaques",
        [
            "Traços de personalidade bem estruturados.",
            "Boa estabilidade emocional em ambientes de pressão.",
            "Recursos cognitivos compatíveis com funções estratégicas."
        ]
    )

    alertas = resumo.get(
        "alertas",
        [
            "Algumas tendências emocionais requerem acompanhamento.",
            "Padrões esquemáticos podem influenciar decisões sob estresse."
        ]
    )

    html = f"""
<section class="resumo-executivo page">

    <h2 class="secao-titulo">Resumo Executivo</h2>

    <p class="resumo-texto">
        {texto_resumo}
    </p>

    <div class="resumo-blocos">

        <div class="bloco">
            <h3>Destaques Identificados</h3>
            <ul>
                {''.join(f'<li>{item}</li>' for item in destaques)}
            </ul>
        </div>

        <div class="bloco alerta-premium">
            <h3>Pontos de Atenção</h3>
            <ul>
                {''.join(f'<li>{item}</li>' for item in alertas)}
            </ul>
        </div>

    </div>

</section>
"""

    return {
        "id": "resumo_executivo",
        "titulo": "Resumo Executivo",
        "html": html
    }
