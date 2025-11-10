@echo off
setlocal

echo ================================
echo   PUSH PARA GITHUB - MINDSCAN
echo ================================
echo.

REM Caminho do projeto (ajustável se necessário)
cd /d D:\projetos-inovexa\mindscan

REM Mensagem de commit
set /p MSG=Digite a mensagem do commit: 

echo.
echo Adicionando arquivos ao Git...
git add .

echo Criando commit...
git commit -m "%MSG%"

echo Enviando para o repositório remoto...
git push -u origin main

echo.
echo ================================
echo PUSH CONCLUÍDO COM SUCESSO!
echo ================================
pause
