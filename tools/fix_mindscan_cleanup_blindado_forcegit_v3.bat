@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM   FORCEGIT v3 (BAT WRAPPER) — Blindado, Seguro e Não-Destrutivo
REM   Inovexa Software — Diretor Leo Vinci
REM   Este .bat apenas executa o script Python v3 de forma segura.
REM   Não executa nenhum comando destrutivo diretamente.
REM ============================================================

echo ================================================
echo  Iniciando ForceGit v3 (Blindado e Seguro)
echo  Diretor: Leo Vinci — Inovexa Software
echo ================================================
echo.

REM Caminho absoluto para o diretório do MindScan
set ROOT=%~dp0..
set PYTHON_SCRIPT=%ROOT%\tools\fix_mindscan_cleanup_blindado_forcegit_v3.py

if not exist "%PYTHON_SCRIPT%" (
    echo ERRO: O arquivo Python fix_mindscan_cleanup_blindado_forcegit_v3.py nao foi encontrado.
    echo Caminho esperado:
    echo %PYTHON_SCRIPT%
    pause
    exit /b 1
)

echo Executando script Python com seguranca...
echo.

python "%PYTHON_SCRIPT%"

echo.
echo ================================================
echo ForceGit v3 concluido com seguranca.
echo Logs disponiveis em forcegit_v3.log
echo ================================================
echo.

pause
endlocal
exit /b 0
