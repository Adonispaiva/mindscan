@echo off
setlocal ENABLEDELAYEDEXPANSION
title MINDSCAN OPTIMIZER — LAUNCHER OFICIAL (v2.3)

echo ================================================================
echo                MINDSCAN OPTIMIZER — LAUNCHER OFICIAL (v2.3)
echo ================================================================
echo.

REM ---------------------------------------------------------------
REM  DETECÇÃO DO PYTHON
REM ---------------------------------------------------------------
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado no PATH.
    echo Instale Python 3.10+ e tente novamente.
    echo.
    pause
    exit /b 1
)

echo Python detectado com sucesso.
echo.

REM ---------------------------------------------------------------
REM  DEFINIR RAIZ DO PROJETO (UM NIVEL ACIMA DE \tools)
REM ---------------------------------------------------------------
set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
echo Raiz detectada: %ROOT%
echo.

REM ---------------------------------------------------------------
REM  DEFINIR SCRIPT DO OPTIMIZER
REM ---------------------------------------------------------------
set "SCRIPT=%ROOT%\tools\mindscan_optimizer.py"

if not exist "%SCRIPT%" (
    echo [ERRO] Arquivo mindscan_optimizer.py nao encontrado em:
    echo   %SCRIPT%
    echo.
    pause
    exit /b 1
)

echo Script identificado: mindscan_optimizer.py
echo.

:MENU
cls
echo ================================================================
echo                  SELECIONE UMA OPERACAO
echo ================================================================
echo.
echo 1  - Executar TODOS os modos (ALL)
echo 2  - Limpeza profunda        (CLEAN)
echo 3  - Normalizar Python       (NORMALIZE)
echo 4  - Auditoria Legacy        (AUDIT)
echo 5  - Estatisticas            (STATS)
echo 6  - Atualizar Baseline      (BASELINE)
echo 7  - Correcao Estrutural     (FIXES)
echo 8  - Gerar Governanca        (GOVERNANCE)
echo 9  - Arvore Completa         (FULLTREE)
echo 10 - Arvore Classica         (TREE_LEGACY)
echo 0  - Sair
echo.
set /p choice="Escolha uma opcao: "

if "%choice%"=="0" goto SAIR
if "%choice%"=="" goto MENU

REM ---------------------------------------------------------------
REM  VALIDAÇÃO DE OPCOES (1-10)
REM ---------------------------------------------------------------
for %%A in (1 2 3 4 5 6 7 8 9 10) do (
    if "%choice%"=="%%A" goto EXEC
)

echo.
echo Opcao invalida. Tente novamente.
pause
goto MENU

REM ---------------------------------------------------------------
REM  EXECUCAO
REM ---------------------------------------------------------------
:EXEC
cls
echo ================================================================
echo  MINDSCAN OPTIMIZER 2.3 — EXECUCAO
echo ================================================================
echo.
echo Opcao selecionada: %choice%
echo.

python "%SCRIPT%" %choice%
set "ERR=%ERRORLEVEL%"

echo.
if NOT "%ERR%"=="0" (
    echo [AVISO] O script retornou codigo %ERR%.
) else (
    echo Processo concluido com sucesso.
)
echo.
pause
goto MENU

:SAIR
echo Encerrando MINDSCAN OPTIMIZER LAUNCHER (v2.3)...
echo.
endlocal
exit /b 0
