@echo off
TITLE MindScan - Auditoria e Push Automatico
chcp 65001 >nul

echo ============================================================
echo      🚀  INICIANDO ROTINA AUTOMÁTICA DO MINDSCAN
echo ============================================================
echo.

set ROOT_DIR=%~dp0..
set LOG_DIR=%ROOT_DIR%\logs
set LOG_FILE=%LOG_DIR%\audit_push_%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%h%time:~3,2%m%time:~6,2%s.txt

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo Salvando log em:
echo %LOG_FILE%
echo ======================== >> "%LOG_FILE%"

echo.
echo =============== ETAPA 1 ===============
echo ▶ Executando Auditoria Completa...
python "%ROOT_DIR%\auditar_mindscan.py" >> "%LOG_FILE%" 2>&1
echo Auditoria finalizada.
echo.

echo =============== ETAPA 2 ===============
echo ▶ Executando sincronização com GitHub...
python "%ROOT_DIR%\sincronizar_github.py" >> "%LOG_FILE%" 2>&1
echo Sincronização concluída.
echo.

echo =============== ETAPA 3 ===============
echo ▶ PUSH FINAL PARA O REPOSITÓRIO
git -C "%ROOT_DIR%" push >> "%LOG_FILE%" 2>&1
echo Push concluído.
echo.

echo ============================================================
echo   ✔ ROTINA COMPLETA! Auditoria e Push executados.
echo   ✔ Arquivo de log:
echo     %LOG_FILE%
echo ============================================================
pause
exit
