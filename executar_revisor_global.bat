@echo off
setlocal enabledelayedexpansion

:: ----------------------------------------------------------
::  MindScan - Executor do Revisor Global
::  Autor: Leo Vinci (GPT Inovexa)
::  Data: 26/11/2025
:: ----------------------------------------------------------

echo ================================================
echo     EXECUTANDO REVISOR GLOBAL DO MINDSCAN
echo ================================================
echo.

:: Pasta raiz do MindScan
set PROJECT_ROOT=%~dp0

:: Caminho para o Python
set PYTHON=python

:: Caminho do script
set SCRIPT=%PROJECT_ROOT%tools\revisor_global.py

if not exist "%SCRIPT%" (
    echo ERRO: O arquivo revisor_global.py nao foi encontrado.
    echo Verifique em:
    echo %SCRIPT%
    pause
    exit /b
)

echo Rodando revisor_global.py...
%PYTHON% "%SCRIPT%"

echo.
echo ================================================
echo     REVISAO GLOBAL CONCLUIDA
echo     Relatorios gerados em: mindscan/logs/
echo ================================================
echo.

pause
exit /b
