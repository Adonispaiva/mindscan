@echo off
setlocal

echo ============================================
echo        PUSH AUTOMATICO PARA GITHUB
echo ============================================
echo.

REM Ir para a pasta raiz do projeto
cd /d "%~dp0.."

echo [1] Adicionando arquivos ao Git...
git add .

echo [2] Criando commit automático...
set TIME_TAG=%DATE:/=-%_%TIME::=-%
git commit -m "Auto-push %TIME_TAG%"

echo [3] Sincronizando com repositorio remoto (git pull)...
git pull

echo [4] Enviando alterações (git push)...
git push

echo.
echo --------------------------------------------
echo PUSH FINALIZADO COM SUCESSO!
echo --------------------------------------------
pause
endlocal
