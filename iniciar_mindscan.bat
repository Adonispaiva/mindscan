:: Arquivo: D:\projetos-inovexa\mindscan\iniciar_mindscan.bat
:: Status: Atualizado com Pipeline de Saneamento
@echo off
title MINDSCAN - Full Orchestrator
color 0B

:: Forçar o terminal a usar UTF-8 para evitar erros de charmap
chcp 65001 > nul

echo ===========================================
echo       INICIANDO PIPELINE MINDSCAN
echo ===========================================

:: Passo 1: Garantir que o ambiente Python está correto
set PYTHONPATH=.

:: Passo 2: Saneamento preventivo de caracteres especiais
echo [1/3] Sanear Encoding...
python revisor_encoding_global.py

:: Passo 3: Executar Auditoria e Sincronização
echo [2/3] Executar Auditoria e Push...
python sincronizar_github.py

echo [3/3] Processo Concluido.
echo ===========================================
pause