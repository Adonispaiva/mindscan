@echo off
setlocal

echo Iniciando ambiente do frontend...
cd /d "%~dp0front-end"

if exist node_modules (
    echo Pacotes já instalados. Pulando instalação...
) else (
    echo Instalando dependências do frontend...
    npm install
)

npm start
endlocal
