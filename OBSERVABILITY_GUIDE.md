📄 Conteúdo completo — OBSERVABILITY_GUIDE.md (Guia Oficial de Observabilidade · Inovexa/SynMind)
# 🛰 MindScan — OBSERVABILITY GUIDE
Inovexa Software — Guia Oficial de Observabilidade  
Versão: 1.0.0  
Última atualização: 2025-11-30

---

# 📘 1. Visão Geral

O MindScan PDF Engine possui um ecossistema de observabilidade corporativa baseado em:

1. **Logger Corporativo (mindscan_pdf.log)**
2. **Telemetria Avançada (mindscan_telemetry_advanced.jsonl)**
3. **Resource Monitor (mindscan_resource_monitor.jsonl)**
4. **Performance Governor (controle adaptativo)**
5. **Tracing de pipeline (sync & async)**
6. **Estrutura padronizada para dashboards (Grafana/Kibana)**

Este documento descreve **como monitorar, interpretar, rastrear e auditar** toda a execução do MindScan.

---

# 📡 2. Componentes da Observabilidade

## 2.1 Logger Corporativo
Arquivo:  


logs/mindscan_pdf.log


Eventos registrados:
- Início/fim da pipeline
- Carregamento de JSONs
- Validação OK / falhou
- Seções iniciando / terminando
- Renderers utilizados
- Eventos de erro estruturados
- Fallbacks automáticos
- Execuções paralelas (SectionEngine)
- Execuções assíncronas (AsyncPipeline)

Formato:


[2025-11-30 14:22:10] INFO — PDFBuilder inicializado.
[2025-11-30 14:22:11] WARN — TURBO ativado pelo PerformanceGovernor.
[2025-11-30 14:22:11] ERROR — ValidationError na seção BigFiveSection.


### Boas práticas:
- Nunca registrar dados sensíveis
- Registrar apenas metadados, eventos e coordenadas da pipeline

---

## 2.2 Telemetria Avançada
Arquivo:  


logs/mindscan_telemetry_advanced.jsonl


Cada linha representa uma sessão completa do PDF:

Exemplo:
```json
{
  "session_id": "20251130T174455Z",
  "timestamp": "2025-11-30T17:44:55.190822",
  "metrics": {
    "secao_CapaSection": 0.018,
    "secao_BigFiveSection": 0.046,
    "montagem_html": 0.122,
    "render_pdf": 1.842,
    "tamanho_pdf_bytes": 528443
  }
}


Métricas coletadas:

tempo por seção

tempo total da pipeline

tempo do HTML Builder

tempo de renderização local ou distribuída

tamanho final do PDF

renderer usado

tempo async (quando aplicável)

2.3 Resource Monitor

Arquivo:

logs/mindscan_resource_monitor.jsonl


Coleta:

% CPU

RAM (MB)

Pico de memória

Amostragem a cada 0.5s

Exemplo:

{
  "session_id": "20251130T174455Z",
  "timestamp": "2025-11-30T17:44:56.418391",
  "cpu_percent": 61.5,
  "memory_mb": 742.3,
  "peak_memory_mb": 744.8
}


Uso:

Diagnósticos de carga

Decisões adaptativas do Governor

Auditoria pós-execução

2.4 Performance Governor

Integrado ao Resource Monitor.

Regras:

CPU > 85% → TURBO desativado

CPU < 45% → TURBO ativado

RAM > 1500MB → TURBO desligado

Regiões neutras → mantém estado atual

Benefício:
Pipeline adaptativa, inteligente, resiliente a picos de carga.

2.5 Tracing de Pipeline
Sync (PDFBuilder):

pipeline_total

montagem_html

render_pdf

tempo por seção

Async (AsyncPipeline, AsyncPDFBuilder):

pipeline_total_async

html_async

render_pdf_async

telemetria async-safe

📊 3. Dashboards e Integrações

O formato JSONL é compatível com:

Grafana

Loki para logs

Promtail para ingestão

Grafana para dashboards de telemetria

Kibana / Elastic

Ingestão direta do JSONL

Visualização de eventos de pipeline

Timeline de renderizações

Prometheus

Criação de exporters personalizados

Integrado ao ResourceMonitor

Datadog / NewRelic

Observability pipeline opcional

Alerts dinâmicos

🧩 4. Fluxo Completo de Observabilidade
┌───────────────────────┐
│  PDFBuilder/Async     │
└───────────┬───────────┘
            │ métricas
            ▼
┌───────────────────────┐
│ Telemetria Avançada   │
└───────────┬───────────┘
            │ CPU/RAM
            ▼
┌───────────────────────┐
│ Resource Monitor       │
└───────────┬───────────┘
            │ decisões
            ▼
┌───────────────────────┐
│ Performance Governor   │
└───────────┬───────────┘
            │ logs
            ▼
┌───────────────────────┐
│ Logger Corporativo    │
└───────────────────────┘

🔧 5. Como depurar uma execução

Verifique os logs:

tail -f logs/mindscan_pdf.log


Verifique a telemetria:

tail -f logs/mindscan_telemetry_advanced.jsonl


Verifique carga:

tail -f logs/mindscan_resource_monitor.jsonl


Correlacione sessão pelo session_id.

🛡 6. Diretrizes de Segurança

Logs não devem conter:

dados do usuário

MI sensível

resultados de testes

Apenas metadados, tempos e eventos de pipeline.

Telemetria é compatível com auditorias corporativas.

🧠 7. Conclusão

A observabilidade do MindScan foi projetada para:

alta confiabilidade

auditoria completa

diagnósticos avançados

governança adaptativa

escalabilidade futura

distribuição em cluster

É uma solução nível Inovexa/SynMind, plenamente adequada para produção empresarial.