# MindScan — Deploy Web (NGINX + FastAPI + Docker)

## Estrutura final

mindscan/
│
├── backend/
├── engine/
├── services/
├── mindscan_web_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── web/
│   └── index.html
│
└── deploy/
    ├── nginx.conf
    ├── docker-compose.yml
    └── README_DEPLOY.md

---

## Para iniciar em produção:

docker compose -f deploy/docker-compose.yml up --build -d

Acessar:

UI → http://localhost  
API → http://localhost/api/docs  
PDFs → http://localhost/files/
