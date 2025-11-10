@echo off
setlocal

echo Iniciando ambiente do backend...
cd /d "%~dp0backend"

if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo Instalando dependências...
pip install -r requirements.txt

echo Iniciando o backend...
python app.py

endlocal
