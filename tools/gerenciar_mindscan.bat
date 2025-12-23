@echo off
:: =========================================================================
::  MINDSCAN COMMAND CENTER v5.2 - BY ORION
::  Interface de Gestão Inovexa Software
::  Caminho: D:\projetos-inovexa\mindscan\tools\gerenciar_mindscan.bat
:: =========================================================================

TITLE MindScan Command Center v5.2
COLOR 0B
cls

:: Captura o diretório onde o .bat está localizado
set "CURRENT_DIR=%~dp0"
set "PYTHON_SCRIPT=%CURRENT_DIR%mindscan_unified_manager.py"

echo =========================================================================
echo               MINDSCAN ENTERPRISE MANAGER - ORION V5.2
echo =========================================================================
echo.
echo [INFO] Inicializando ambiente de gestao...
echo [PATH] %CURRENT_DIR%
echo.

:: 1. Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO CRITICO] Python nao foi encontrado no sistema.
    echo Por favor, instale o Python ou adicione-o ao seu PATH.
    pause
    exit
)

:: 2. Verifica se o script unificado existe na pasta
if not exist "%PYTHON_SCRIPT%" (
    color 0C
    echo [ERRO CRITICO] Script "mindscan_unified_manager.py" nao encontrado!
    echo Certifique-se de que o arquivo .py esta na mesma pasta deste .bat.
    echo Local esperado: %PYTHON_SCRIPT%
    pause
    exit
)

:: 3. Execução do Script Master
echo [SISTEMA] Conectando ao Nucleo MindScan...
echo.
python "%PYTHON_SCRIPT%"

:: 4. Finalização
if %errorlevel% neq 0 (
    echo.
    echo [ALERTA] O script foi encerrado com um codigo de erro.
    pause
)

echo.
echo [SISTEMA] Sessao encerrada.
timeout /t 3
exit