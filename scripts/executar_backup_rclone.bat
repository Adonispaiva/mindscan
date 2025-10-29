@echo off
cd /d D:\projetos-inovexa\mindscan\scripts

REM === Ativa o ambiente virtual Python, se existir ===
IF EXIST "..\venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call "..\venv\Scripts\activate.bat"
)

REM === Gera timestamp para nome do log ===
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set timestamp=%%i

REM === Caminho do log ===
set LOG_PATH=logs\execucao_backup_%timestamp%.log

REM === Executa o script Python de backup com redirecionamento de log ===
echo Iniciando backup... > %LOG_PATH%
python backup_mindscan_rclone.py >> %LOG_PATH% 2>&1

REM === Verifica se houve erro na execução ===
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] A execução do backup falhou. Verifique o log: %LOG_PATH%
    echo [ERRO] A execução do backup falhou. Verifique o log: %LOG_PATH% >> %LOG_PATH%
    pause
    exit /b %ERRORLEVEL%
)

REM === Sucesso ===
echo [SUCESSO] Backup executado com sucesso. Log salvo em: %LOG_PATH%
echo [SUCESSO] Backup executado com sucesso. Log salvo em: %LOG_PATH% >> %LOG_PATH%
pause
