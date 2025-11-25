@echo off
chcp 65001 >nul
title MindScan - Auditoria e Push Automático
echo ==========================================================
echo     🚀 INICIANDO ROTINA AUTOMÁTICA DO MINDSCAN
echo ==========================================================
echo.

REM Caminho do projeto
set PROJECT_DIR=D:\projetos-inovexa\mindscan_rebuild
set LOG_DIR=%PROJECT_DIR%\logs
set TOOLS_DIR=%PROJECT_DIR%\tools

REM Criar pasta de logs se não existir
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set LOG_FILE=%LOG_DIR%\audit_push_%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%h%time:~3,2%m%time:~6,2%s.txt
set LOG_FILE=%LOG_FILE: =0%

echo Salvando log em:
echo %LOG_FILE%
echo.

echo ===================== ETAPA 1 =====================
echo 🟦 Executando Auditoria Completa...
cd "%PROJECT_DIR%"
python auditor_mindscan.py >> "%LOG_FILE%" 2>&1

echo Auditoria finalizada.
echo.

echo ===================== ETAPA 2 =====================
echo 🟦 Executando sincronização com GitHub...
python sincronizar_github.py >> "%LOG_FILE%" 2>&1

echo Sincronização concluída.
echo.

echo ===================== ETAPA 3 =====================
echo 🟦 PUSH FINAL PARA O REPOSITÓRIO
cd "%PROJECT_DIR%"
git add . >> "%LOG_FILE%" 2>&1
git commit -m "Auditoria e push automáticos (%date% %time%)" >> "%LOG_FILE%" 2>&1
git push -u origin main >> "%LOG_FILE%" 2>&1

echo Push concluído.
echo.

echo ==========================================================
echo     ✔ ROTINA COMPLETA! Auditoria e Push executados.
echo     Arquivo de log:
echo     %LOG_FILE%
echo ==========================================================
echo.
pause
