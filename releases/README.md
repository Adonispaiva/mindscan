# MindScan — MI Hybrid Intelligence Platform  
Release Candidate 1 (RC-1)  
Direção Técnica: Leo Vinci — Inovexa Software  
Data: 10/12/2025

---

## 📌 Visão Geral

O **MindScan** é a plataforma oficial de Inteligência MI (Mind Intelligence) criada pela Inovexa, unindo:

- MI Original  
- MI Advanced  
- MI Hybrid (média dinâmica O/A)  
- Relatórios PDF profissionais  
- WebApp completo (dashboards, autenticação, admin)  
- Analytics agregados  
- Métricas em tempo real (SSE)  
- Deploy corporativo via Docker/NGINX  
- CI/CD integrado à SynMind Cloud  

---

## 🧠 Componentes Principais

| Componente | Descrição |
|-----------|-----------|
| `mindscan_web_api.py` | API completa (MI + Auth + Admin + Analytics + Live Metrics) |
| `backend/engine` | Motores MI Original / Advanced / Formatter |
| `analytics/*` | Sistema analítico e métricas live |
| `webapp/` | Front-end completo React |
| `deploy/` | Dockerfiles, Compose, NGINX e Cloud configs |
| `releases/` | Manifesto, notas, licença e pacote final |

---

## 🚀 Como executar localmente

### 1. Backend + WebApp + NGINX (produção)

```bash
docker compose -f deploy/docker-compose.prod.yml up --build
