#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
identidade.py — Seção de Identidade (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-----------------------------------------------------------
Apresenta:
- Informações pessoais essenciais
- Contexto profissional
- Identidade organizacional
"""

from datetime import datetime
from typing import Dict, Any


def build_identidade(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retorna estrutura padronizada para o PDFEngine.
    Padrão oficial: {id, titulo, html}
    """

    usuario = context.get("usuario", {})

    nome = usuario.get("nome", "Nome não informado")
    idade = usuario.get("idade", "—")
    genero = usuario.get("genero", "—")
    empresa = usuario.get("empresa", "—")
    cargo = usuario.get("cargo", "—")
    senioridade = usuario.get("senioridade", "—")
    data_geracao = datetime.now().strftime("%d/%m/%Y")

    html = f"""
<section class="identidade page">
    <h2 class="secao-titulo">Identidade Profissional</h2>

    <div class="identidade-container">

        <div class="identidade-bloco">
            <h3>Informações do Avaliado</h3>
            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Idade:</strong> {idade}</p>
            <p><strong>Gênero:</strong> {genero}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
        </div>

        <div class="identidade-bloco">
            <h3>Contexto Profissional</h3>
            <p><strong>Cargo Atual:</strong> {cargo}</p>
            <p><strong>Senioridade:</strong> {senioridade}</p>
            <p><strong>Data do Relatório:</strong> {data_geracao}</p>
        </div>

    </div>
</section>
"""

    return {
        "id": "identidade",
        "titulo": "Identidade Profissional",
        "html": html
    }
