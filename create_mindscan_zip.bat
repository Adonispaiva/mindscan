@echo off
REM ================================================
REM MindScan — Gerador de ZIP limpo do projeto
REM Autor: Inovexa / Leo Vinci
REM ================================================

SETLOCAL ENABLEDELAYEDEXPANSION

REM --- Ajuste se necessário ---
SET SCRIPT_NAME=create_mindscan_zip.py
SET PROJECT_DIR=D:\projetos-inovexa\mindscan
SET OUTPUT_ZIP=mindscan_clean.zip

REM --- Verificações básicas ---
IF NOT EXIST "%SCRIPT_NAME%" (
    echo [ERRO] Script %SCRIPT_NAME% nao encontrado no diretorio atual.
    pause
    exit /b 1
)

IF NOT EXIST "%PROJECT_DIR%" (
    echo [ERRO] Diretorio do projeto nao encontrado:
    echo %PROJECT_DIR%
    pause
    exit /b 1
)

REM --- Execucao ---
echo ================================================
echo Gerando ZIP limpo do MindScan...
echo Projeto : %PROJECT_DIR%
echo Saida   : %OUTPUT_ZIP%
echo ================================================

python "%SCRIPT_NAME%" ^
  --src "%PROJECT_DIR%" ^
  --out "%OUTPUT_ZIP%" ^
  --include-root ^
  --write-filelist

IF ERRORLEVEL 1 (
    echo.
    echo [FALHA] Erro durante a geracao do ZIP.
    pause
    exit /b 1
)

echo.
echo [OK] ZIP gerado com sucesso.
echo Arquivo: %OUTPUT_ZIP%
echo.

pause
ENDLOCAL
