@echo off
title 🧠 Inovexa MindScan Web — Launcher Executivo v4.2
color 0B
setlocal enabledelayedexpansion

:: ============================================
:: Inovexa MindScan Web — Launcher Executivo
:: Autor: Leo Vinci (GPT Inovexa)
:: Versão: 4.2 — 12/11/2025
:: ============================================

echo.
echo ============================================
echo 🧠 Inovexa MindScan — Inicializando Serviços...
echo ============================================
echo.

set BASE_PATH=D:\MindScan\core
set LOG_PATH=D:\MindScan\logs\launcher_output.log
set PYTHON_EXE=python

:: -------------------------------------------------
:: Verificação inicial de rede local e dependências
:: -------------------------------------------------
echo [CHECK] Verificando conectividade local...
ping 127.0.0.1 -n 1 >nul
if %errorlevel% neq 0 (
    echo [ERRO] Falha na conectividade local. Abortando.
    pause
    exit /b
)
echo [OK] Rede local ativa.

:: -------------------------------------------------
:: Iniciar LogHandler
:: -------------------------------------------------
echo [INIT] Iniciando LogHandler...
start "LogHandler" %PYTHON_EXE% "%BASE_PATH%\log_handler.py"
timeout /t 3 >nul

:: -------------------------------------------------
:: Iniciar System Manager
:: -------------------------------------------------
echo [INIT] Iniciando System Manager...
start "SystemManager" %PYTHON_EXE% "%BASE_PATH%\system_manager.py"
timeout /t 3 >nul

:: -------------------------------------------------
:: Iniciar Supervisor AutoSync
:: -------------------------------------------------
echo [INIT] Iniciando Supervisor AutoSync...
start "AutoSync" %PYTHON_EXE% "%BASE_PATH%\supervisao_diretor_auto_sync.py"
timeout /t 2 >nul

:: -------------------------------------------------
:: Iniciar Command Center Integration
:: -------------------------------------------------
echo [INIT] Iniciando Command Center Integration...
start "CommandCenter" %PYTHON_EXE% "%BASE_PATH%\command_center_integration.py"
timeout /t 2 >nul

:: -------------------------------------------------
:: Loop de monitoramento
:: -------------------------------------------------
echo [MONITOR] Todos os serviços foram iniciados.
echo [MONITOR] Monitorando integridade a cada 60 segundos...
echo.

:LOOP
    for %%S in (8090 8091 8080) do (
        powershell -Command "try { (New-Object Net.Sockets.TcpClient('127.0.0.1', %%S)).Close(); exit 0 } catch { exit 1 }"
        if !errorlevel! neq 0 (
            echo [ALERTA] Porta %%S inativa. Reiniciando System Manager...
            start "SystemManager" %PYTHON_EXE% "%BASE_PATH%\system_manager.py"
        )
    )

    echo [HEARTBEAT] %date% %time% — Serviços OK.
    timeout /t 60 >nul
goto LOOP
