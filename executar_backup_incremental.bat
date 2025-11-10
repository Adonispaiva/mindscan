@echo off
setlocal enabledelayedexpansion

echo Iniciando backup incremental do projeto MindScan...
cd /d D:\projetos-inovexa\mindscan

REM Ativar o ambiente virtual, se houver
REM call venv\Scripts\activate

REM Executar o script Python de backup incremental
python backup_incremental_mindscan.py

echo.
echo Backup concluído.
pause
