#!/bin/bash
# =========================================================
# MindScan | Grafana auto-provision via REST API
# =========================================================

GRAFANA_URL="http://localhost:3000"
USERNAME="admin"
PASSWORD="inovexa123"
DASHBOARD_FILE="/d/projetos-inovexa/mindscan/infra/monitoring/synmind_grafana_dashboard.json"

echo "🚀 Provisionando Grafana..."

# Aguarda Grafana subir
until curl -s -f "$GRAFANA_URL/api/health" > /dev/null; do
  echo "⏳ Aguardando Grafana iniciar..."
  sleep 5
done

# Configura datasource Prometheus
echo "⚙️  Registrando datasource..."
curl -s -u $USERNAME:$PASSWORD -X POST "$GRAFANA_URL/api/datasources" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "access": "proxy",
    "url": "http://mindscan-prometheus:9090",
    "isDefault": true
  }' > /dev/null

# Envia o dashboard SynMind
echo "📊 Publicando painel SynMind..."
curl -s -u $USERNAME:$PASSWORD -X POST "$GRAFANA_URL/api/dashboards/db" \
  -H "Content-Type: application/json" \
  -d "{\"dashboard\": $(cat $DASHBOARD_FILE), \"overwrite\": true}" > /dev/null

echo "✅ Grafana provisionado com sucesso!"
