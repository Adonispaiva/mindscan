@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo       MINDSCAN - PUSH AUTOMATICO
echo ===========================================

:: Detecta o diretório do script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1] Entrando no diretório raiz do projeto...
cd ..

echo [2] Ativando ambiente virtual, se existir...
if exist ".\backend\venv\Scripts\activate.bat" (
    call ".\backend\venv\Scripts\activate.bat"
    echo Venv ativado.
) else (
    echo Nenhum venv encontrado. Continuando sem ativar.
)

echo [3] Garantindo branch MAIN...
git branch --show-current > current_branch.txt
set /p BRANCH=<current_branch.txt
del current_branch.txt

if /i not "%BRANCH%"=="main" (
    echo Você está na branch "%BRANCH%". Trocando para MAIN...
    git checkout main
)

echo [4] Adicionando arquivos ao git...
git add .

echo [5] Criando commit automático...
set TS=%date%_%time%
set TS=%TS::=% 
set TS=%TS:/=-%
set TS=%TS:.=%
git commit -m "Atualização automática MindScan — %TS%"

echo [6] Realizando push...
git push origin main

echo ===========================================
echo PUSH CONCLUIDO COM SUCESSO
echo ===========================================
pause
endlocal
exit /b 0
