@echo off
cls
echo =============================================
echo     PUSH PARA GITHUB - MINDSCAN
echo =============================================

:: Caminho do projeto (ajuste se necessário)
cd /d D:\projetos-inovexa\mindscan

:: Solicita mensagem de commit
set /p commitMsg=Digite a mensagem do commit: 

echo.
echo Adicionando arquivos ao Git...
git add .

echo.
echo Criando commit...
git commit -m "%commitMsg%"

echo.
echo Enviando para o repositório remoto...
git push -u origin main

echo.
echo =============================================
echo     PUSH CONCLUÍDO COM SUCESSO!
echo =============================================
pause
