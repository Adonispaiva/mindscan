# Integração do MindScan com SynMind Cloud

Este documento descreve como o MindScan se integra ao ecossistema SynMind.

---

## 🚀 Objetivos da Integração

- Disponibilizar relatórios MI para o sistema SynMind
- Permitir consultas internas via API Gateway
- Unificar autenticação entre plataformas
- Disponibilizar dashboards analíticos corporativos

---

## 🔐 Autenticação Integrada

SynMind utiliza JWT universal.  
O MindScan consome e valida o mesmo token:

Authorization: Bearer <token_synmind>


O middleware `AuthMiddleware` já interpreta o token.

---

## 🌐 Rotas expostas à SynMind

| Endpoint | Descrição |
|----------|-----------|
| `/mindscan/mi-hybrid` | Gera relatório MI completo |
| `/analytics/summary` | Dados agregados para dashboards |
| `/live/stream` | Streaming SSE de métricas |
| `/files/<pdf>` | Acesso aos relatórios gerados |

---

## 🔁 Pipeline de Integração

1. SynMind envia dados brutos do usuário (`raw_scores`)  
2. MindScan processa MI (Original/Advanced/Hybrid)  
3. Gera PDF + payload estruturado  
4. Retorna `pdf_url` + pacote MI  
5. SynMind armazena ou exibe conforme dashboard interno  

---

## 🧱 Requisitos para Deploy na SynMind

- Docker image publicada (`mindscan:latest`)  
- Configuração NGINX + SSL ativa  
- Token SynMind configurado no `.env`  
- WebApp compilado (`webapp/dist`) incluído no container  

---

## 📡 Monitoração

SynMind utiliza:

- `/health` → heartbeat  
- `/analytics/summary` → consumo dos dashboards corporativos  
- `/live/stream` → live metrics nos painéis internos  

---

## 📁 Estrutura recomendada no cluster



/synmind/
mindscan/
api/
web/
logs/
reports/
config/


MindScan está 100% compatível com essa estrutura.