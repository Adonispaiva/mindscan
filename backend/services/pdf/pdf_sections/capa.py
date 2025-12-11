# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\capa.py
# Última atualização: 2025-12-11T09:59:21.215694

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capa.py — Seção de Capa (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
------------------------------------------------
Responsável por gerar a capa executiva do PDF,
seguindo o padrão visual oficial SynMind/Inovexa.
"""

from datetime import datetime
from typing import Dict, Any


def build_capa(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retorna estrutura de seção padronizada para o PDFEngine.
    O PDFEngine injeta o HTML final no template principal.
    """

    usuario = context.get("usuario", {})
    nome = usuario.get("nome", "Avaliado")
    cargo = usuario.get("cargo", "Profissional")
    data = datetime.now().strftime("%d/%m/%Y")

    html = f"""
<section class='capa page'>
    <div class='capa-container'>
        <div class='logo'>
            <h1>MIND<span>SCAN</span></h1>
            <p class='tagline'>Relatório PsicoProfissional Premium</p>
        </div>

        <div class='box-identidade'>
            <h2>{nome}</h2>
            <h3>{cargo}</h3>
            <p class='data'>Data: {data}</p>
        </div>

        <div class='footer'>
            <p>SynMind · Inovexa Software</p>
        </div>
    </div>
</section>
"""

    return {
        "id": "capa",
        "titulo": "Capa",
        "html": html
    }
