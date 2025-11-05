# 📦 MindScan · Manual de Execução CI/CD

Este documento descreve como executar, testar, versionar e publicar o projeto **MindScan** localmente e via GitHub Actions.

---

## 🧪 1. Execução Local

> Requisitos:
> - Windows com PowerShell ou Git Bash
> - Python 3.11+
> - Node.js 18+
> - Git instalado e configurado
> - Acesso ao repositório remoto (GitHub)

### ▶️ Scripts Disponíveis

| Script                | Ação                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `setup_backend.bat`   | Cria o ambiente virtual do Python, instala dependências e ativa o backend. |
| `setup_frontend.bat`  | Instala os pacotes npm do frontend (Angular ou React).              |
| `start_all.bat`       | Executa frontend e backend em paralelo.                             |
| `build_all.bat`       | Builda frontend e valida o backend (tests).                         |
| `deploy_stub.bat`     | Empacota o projeto em um `.zip` para deploy manual.                 |

> Execute no PowerShell com:
> ```powershell
> .\start_all.bat
> ```

---

## 🚀 2. CI no GitHub Actions

### 🧩 Gatilhos

A pipeline é ativada automaticamente ao:

- Push para `main` ou `principal`
- Pull Request para `main` ou `principal`

### 📜 Etapas da Pipeline

1. Checkout do código
2. Setup de Node.js e Python
3. Instalação de dependências (front e back)
4. Build do frontend
5. Testes do backend
6. Geração de artefato `.zip`
7. Upload do artefato

---

## 📁 3. Artefatos do Deploy

> Após o build no GitHub, vá para:

1. **Ações (Actions)** no topo do repositório
2. Selecione o workflow executado
3. Role até a etapa final chamada **"Publicar artefato"**
4. Clique em **mindscan-build** para baixar o `.zip`

---

## 🛠️ 4. Dicas de Debug

- Se o build do frontend falhar no GitHub, revise o `package.json`.
- Se os testes do backend falharem, revise o diretório `backend/tests`.
- Para builds manuais, use:
  ```bash
  .\build_all.bat && .\deploy_stub.bat
