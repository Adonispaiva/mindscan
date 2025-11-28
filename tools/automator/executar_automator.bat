@echo off
title MindScan Automator - Execucao Completa
color 0A

echo ================================================
echo        INOVEXA - MINDSCAN AUTOMATOR
echo          Execucao Completa Automatizada
echo ================================================
echo.

REM ---------------------------------------------
REM Verifica se Python existe
REM ---------------------------------------------
echo Verificando instalacao do Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python nao encontrado no sistema.
    echo Instale Python 3.10+ e tente novamente.
    pause
    exit /b
)

echo Python encontrado.
echo.

REM ---------------------------------------------
REM Caminho base do projeto
REM ---------------------------------------------
set PROJECT_DIR=D:\projetos-inovexa\mindscan
set AUTO_DIR=%PROJECT_DIR%\tools\automator

cd /d %PROJECT_DIR%

echo Iniciando Automator...
echo.

REM ---------------------------------------------
REM Executa Automator com todas as tasks
REM ---------------------------------------------
python "%AUTO_DIR%\main.py" --all

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Houve falhas na execucao do Automator.
    echo Verifique o log em logs\automator.
    pause
    exit /b
)

echo.
echo ================================================
echo     EXECUCAO CONCLUIDA COM SUCESSO!
echo ================================================
echo.

REM ---------------------------------------------
REM Opcional: Abre o ultimo relatorio TXT
REM ---------------------------------------------
echo Abrindo ultimo relatorio TXT...
for /f "delims=|" %%f in ('dir "%PROJECT_DIR%\logs\reports\automator_report_*.txt" /b /o:-d') do (
    start "" "%PROJECT_DIR%\logs\reports\%%f"
    goto :done
)

:done

echo.
echo Pressione qualquer tecla para sair...
pause >nul
exit /b
