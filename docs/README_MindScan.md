# D:\projetos-inovexa\mindscan\docs\README_MindScan.md

# 🧠 MindScan - Manual de Uso e Execução

## 👩‍🔬 Para Testadores (Ex: Milena)

### 🔑 Acesso Inicial
1. Acesse o sistema pelo navegador em:
   ```
   http://localhost:3000
   ```
2. Clique em "Login" e entre com:
   - **Email:** admin@mindscan.com
   - **Senha:** admin123  *(pode ser alterada após login)*

### 📊 Funcionalidades Disponíveis
- **Enviar Quiz:** Acesse a tela de quiz e envie respostas simuladas.
- **Ver Resultados:** Veja o diagnóstico gerado pela IA.
- **Dashboard:** Acesse `/dashboard` para ver:
  - Total de usuários, quizzes e respostas
  - Botão para **exportar respostas** em `.csv`

### 📤 Exportar Dados
- Acesse a tela de **Dashboard**
- Clique no botão **Exportar Respostas (CSV)**
- O arquivo será baixado automaticamente para o seu computador

---

## 🛠 Para Desenvolvedores

### ▶️ Execução Local
1. Clone o repositório e entre na pasta `mindscan`
2. Execute backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
3. Em outro terminal, rode o frontend:
   ```bash
   cd web
   npm install
   npm run dev
   ```
4. Acesse via navegador: `http://localhost:3000`

### 📦 Dependências Relevantes
- **Backend:** FastAPI, SQLAlchemy, Pydantic, python-jose, passlib
- **Frontend:** React + TypeScript + Tailwind + Axios

### 📂 Estrutura Técnica
```
mindscan/
├─ backend/
│  ├─ routers/ (auth, quiz, admin)
│  ├─ models.py, database.py
│  ├─ services/analyzer.py
├─ web/
│  ├─ src/pages (Login, QuizForm, Dashboard...)
│  ├─ src/components, AppRouter.tsx
└─ docs/README_MindScan.md
```

---

✅ **Status Atual:**
MindScan está funcional, testado e pronto para coleta de feedback de usabilidade e ajustes finais.

📧 Para dúvidas técnicas, fale com a equipe Inovexa.
