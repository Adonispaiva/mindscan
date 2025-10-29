# D:\projetos-inovexa\mindscan\frontend\README.md

# 🌐 MindScan - Frontend

Interface web do projeto **MindScan**, desenvolvida com **React + TypeScript**, **Vite** e **TailwindCSS**.

---

## 🚀 Execução em Desenvolvimento
```bash
cd D:\projetos-inovexa\mindscan\frontend
pnpm install
pnpm dev
```

---

## 🔍 Estrutura de Pastas
```
frontend/
├── public/               # Assets estáticos
├── src/
│   ├── app/              # Entrypoint do app React
│   ├── components/       # Componentes reutilizáveis
│   ├── pages/            # Páginas de navegação
│   ├── store/            # Zustand / Redux Toolkit
│   └── index.tsx         # Inicialização do React
├── package.json          # Configuração de dependências
├── vite.config.ts        # Vite (build/dev)
├── tailwind.config.js    # Estilo
└── Dockerfile            # Docker build estático
```

---

## 🧪 Scripts Disponíveis
```bash
pnpm dev        # Dev server em http://localhost:3000
pnpm build      # Build de produção para /dist
pnpm preview    # Servidor de preview local do build
pnpm lint       # Lint com ESLint + auto-fix
```

---

## 🐳 Docker
```bash
cd D:\projetos-inovexa\mindscan\frontend
docker-compose up --build
```
Acesse: [http://localhost:3000](http://localhost:3000)

---

## 📦 Dependências Chave
- React 18
- Zustand & Redux Toolkit
- React Router DOM
- Tailwind CSS 3
- Lucide + Heroicons

---

## 🧠 Backend
O frontend consome dados da API backend disponível em:
```
http://localhost:8000
```
Revisar origem permitida em `.env` do backend.

---

## 📬 Contato
Interface desenvolvida por Inovexa · Engenharia: Leo + GPT Inovexa
