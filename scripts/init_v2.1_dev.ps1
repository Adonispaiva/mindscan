Write-Host "Inicializando ambiente MindScan v2.1-dev..." -ForegroundColor Cyan
Set-Location "D:\projetos-inovexa\mindscan"

git checkout v2.1-dev
pip install -r backend/requirements.txt
npm install --prefix frontend

Write-Host "Ambiente sincronizado e dependências instaladas." -ForegroundColor Green
Write-Host "Executando servidor backend e frontend em modo dev..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList "python backend/start.py"
Start-Process powershell -ArgumentList "npm run dev --prefix frontend"
