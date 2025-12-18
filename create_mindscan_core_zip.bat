@echo off
REM =====================================================
REM MindScan — ZIP TECNICO (CORE APENAS)
REM Uso exclusivo para auditoria e correção estrutural
REM =====================================================

SETLOCAL ENABLEDELAYEDEXPANSION

REM --- Configuracao ---
SET SCRIPT_NAME=create_mindscan_zip.py
SET PROJECT_DIR=D:\projetos-inovexa\mindscan
SET OUTPUT_ZIP=mindscan_core.zip

REM --- Verificacoes ---
IF NOT EXIST "%SCRIPT_NAME%" (
    echo [ERRO] Script %SCRIPT_NAME% nao encontrado.
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
echo Gerando ZIP TECNICO (CORE APENAS)
echo Projeto : %PROJECT_DIR%
echo Saida   : %OUTPUT_ZIP%
echo ================================================

python "%SCRIPT_NAME%" ^
  --src "%PROJECT_DIR%" ^
  --out "%OUTPUT_ZIP%" ^
  --include-root ^
  --write-filelist ^
  --exclude-dir inputs ^
  --exclude-dir outputs ^
  --exclude-dir scoring ^
  --exclude-dir data ^
  --exclude-dir datasets ^
  --exclude-dir logs ^
  --exclude-dir tmp ^
  --exclude-dir reports ^
  --exclude-dir pdf ^
  --exclude-dir docs ^
  --exclude-ext .pdf ^
  --exclude-ext .csv ^
  --exclude-ext .xlsx ^
  --exclude-ext .jsonl ^
  --exclude-ext .db ^
  --exclude-ext .zip

IF ERRORLEVEL 1 (
    echo.
    echo [FALHA] Erro durante a geracao do ZIP tecnico.
    pause
    exit /b 1
)

echo.
echo [OK] ZIP tecnico gerado com sucesso.
echo Arquivo: %OUTPUT_ZIP%
echo.

pause
ENDLOCAL
