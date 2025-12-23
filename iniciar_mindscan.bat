@echo off
cls
echo ==================================================
echo      MINDSCAN V4 - DIAGNOSTICO DE INICIALIZACAO
echo ==================================================
echo.
echo [1/2] Verificando Bibliotecas...
pip install fastapi uvicorn jinja2 python-multipart pydantic
echo.
echo [2/2] A iniciar o Servidor...
echo Se a janela fechar, o erro estara escrito abaixo:
echo.
python backend/main.py
echo.
echo ==================================================
echo O Servidor foi interrompido.
pause