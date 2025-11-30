#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capa.py — Seção de Capa (MindScan PDF Premium)
----------------------------------------------
Gera a capa executiva do relatório MindScan.
Inclui:
- Logo
- Identidade
- Nome do avaliado
- Data
- Título oficial
"""

from datetime import datetime

class CapaSection:
    def render(self, context: dict) -> str:
        usuario = context.get("usuario", {})
        nome = usuario.get("nome", "Avaliado")
        cargo = usuario.get("cargo", "Profissional")
        data = datetime.now().strftime("%d/%m/%Y")

        return f"""
<section class='capa'>
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
