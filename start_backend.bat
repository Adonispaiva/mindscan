@echo off
echo ============================================
echo INICIANDO SERVIDOR MINDSCAN BACKEND
echo ============================================

REM --- Ir para a pasta do backend ---
echo.
echo > Indo para a pasta backend...
cd /d D:\projetos-inovexa\mindscan_rebuild\backend

if errorlevel 1 (
   echo [ERRO] Nao foi possivel acessar a pasta backend.
   pause
   exit /b
)

REM --- Ativar ambiente virtual ---
echo Ativando ambiente virtual...
call .\venv\Scripts\activate

if errorlevel 1 (
   echo [ERRO] O ambiente .venv nao foi encontrado.
   echo Verifique se a pasta existe em:
   echo D:\projetos-inovexa\mindscan_rebuild\backend\venv
   pause
   exit /b
)

REM --- Iniciar servidor FastAPI ---
echo Iniciando servidor FastAPI...
uvicorn main:app --reload

pause
