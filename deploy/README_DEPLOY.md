# 🧠 MindScan v2.1 – Guia de Deploy

Este documento descreve o processo completo para subir o backend e frontend do MindScan v2.1 no Render.com.

---

## 🚀 Backend (FastAPI + Uvicorn)

### 📁 Local do código
```
D:\MindScan\backend
```

### 📁 Arquivos de deploy (Render)
```
D:\MindScan\deploy\
├── render.yaml
├── Procfile
├── Dockerfile (opcional)
├── .env.example
```

### ✅ Passo a passo
1. Suba o projeto no GitHub (com a pasta `deploy/` inclusa)
2. Acesse [https://render.com](https://render.com)
3. Clique em **New Web Service**
4. Escolha seu repositório do GitHub
5. Render detectará automaticamente o `render.yaml`
6. Clique em **Create Web Service**
7. Aguarde o deploy e acesse sua API em:
```
https://mindscan-backend.onrender.com
```

---

## 🌐 Frontend (React + Tailwind)

### 📁 Local do código
```
D:\MindScan\frontend
```

### ⚙️ Configuração
1. Crie um arquivo `.env` com:
```
VITE_API_URL=https://mindscan-backend.onrender.com
```

2. Execute:
```bash
npm install
npm run build
```

3. Faça deploy em:
   - **Render (static site)**
   - **Vercel**
   - **Netlify**

---

## 🛡️ Segurança (opcional)
- Proteja o painel com login (para Milena)
- Use token JWT ou autenticação básica

---

## 📦 API
### `POST /diagnostic`
Gera diagnóstico narrativo a partir dos scores do DASS-21

### `POST /diagnostic/save`
Salva um diagnóstico no histórico

### `GET /diagnostic/history`
Retorna todos os diagnósticos anteriores

---

## ✅ Status Final
**Projeto 100% pronto para uso clínico.**
- Backend funcional e testado
- Frontend finalizado com UI de diagnóstico e histórico
- Exportação de PDF automática
- Deploy com 1 clique via Render

---

Desenvolvido por Inovexa ⚡
