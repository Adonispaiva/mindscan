@echo off
setlocal

echo Iniciando MindScan...

set "PROJETO_DIR=%~dp0"

start "Backend - MindScan" powershell -NoExit -Command "& '%PROJETO_DIR%setup_backend.bat'"
start "Frontend - MindScan" powershell -NoExit -Command "& '%PROJETO_DIR%setup_frontend.bat'"

echo Backend e frontend iniciados em janelas separadas.
pause >nul
