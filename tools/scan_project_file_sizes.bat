@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo ================================================
echo    MINDSCAN - SCAN DE TAMANHO DE ARQUIVOS
echo ================================================
echo.

REM --- Caminho REAL para o script Python ---
SET SCRIPT_PATH="D:\projetos-inovexa\mindscan\tools\scan_project_file_sizes.py"

REM --- Executa o script ---
echo Executando scanner...
python %SCRIPT_PATH%

echo.
echo Relatório concluído.
echo Arquivo gerado em: D:\projetos-inovexa\mindscan\logs\estrutura\relatorio_tamanho_arquivos.txt
echo.
pause
