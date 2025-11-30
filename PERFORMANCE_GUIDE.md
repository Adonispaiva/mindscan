📄 Conteúdo completo — PERFORMANCE_GUIDE.md (Guia Oficial de Performance · Inovexa/SynMind)
# ⚡ MindScan — PERFORMANCE GUIDE
Guia Oficial de Performance e Tuning  
Inovexa Software / SynMind Technologies  
Versão: 1.0.0  
Data: 2025-11-30

---

# 🚀 1. Objetivo do Guia
Este documento estabelece a **política oficial de performance** do MindScan, cobrindo:

- motores de renderização (sync / async / distribuído)
- paralelização inteligente (SectionEngine)
- pipelines assíncronas (AsyncPipeline / AsyncPDFBuilder)
- uso de CPU/RAM
- tuning do Performance Governor
- limites recomendados
- stress testing
- recomendações de hardware
- guidelines de cluster

---

# ⚙️ 2. Arquitetura de Performance

O MindScan PDF Engine foi projetado para operar em três modos:



SYNC → PDFBuilder v36
ASYNC → AsyncPipeline / AsyncPDFBuilder v43
DISTRIBUÍDO → DistributedRenderer v42


Em todos os casos, há suporte para:

- pré-compilação de seções  
- chunking de HTML  
- render pipeline otimizada  
- telemetria profunda  
- monitoramento de CPU/RAM  
- governança adaptativa de performance  

---

# 🧠 3. Perfis de Execução

## 3.1 ECO MODE
- uso mínimo de CPU  
- sem paralelização  
- renderer local síncrono  
- adequado para máquinas pequenas

Configuração sugerida:


turbo = False
max_workers = 2
PerformanceGovernor desativado
ResourceMonitor opcional


---

## 3.2 NORMAL MODE
- comportamento balanceado  
- paralelização moderada  
- render sync ou async  
- ideal para ambientes solo

Configuração sugerida:


turbo = True
max_workers = 4
PerformanceGovernor ativo
ResourceMonitor ativo


---

## 3.3 TURBO MODE (recomendado)
- paralelização inteligente máxima  
- SectionEngine paralelo  
- AsyncPipeline ativo  
- WeasyRendererAsync  
- governança adaptativa ativa  

Configuração sugerida:


turbo = True
max_workers = 6
PerformanceGovernor ativo
monitor ativado


---

## 3.4 EXTREME MODE (cluster)
- render remoto  
- vários nós distribuídos  
- async total  
- alta concorrência

Configuração:


turbo = True
max_workers = 8–12
DistributedRenderer ativo
Remote Pool ≥ 2 nós
Governor ativo (CPU thresholds customizados)


---

# 🖥 4. Requisitos de Hardware

### Mínimo:
- 2 cores  
- 4 GB RAM  

### Recomendado:
- 4–8 cores  
- 8–16 GB RAM  

### Produção Intensiva:
- 8+ cores  
- 16–32 GB RAM  
- SSD de alto IOPS  
- Nós distribuídos opcionais

---

# 🧩 5. Tuning do SectionEngine

Valores recomendados para `max_workers`:

| Cores da máquina | max_workers |
|------------------|-------------|
| 2                | 2           |
| 4                | 4           |
| 8                | 6           |
| 16+              | 8–12        |

Regra:
> “Nunca usar mais threads do que cores físicos + 2.”

---

# 🧲 6. Tuning do Performance Governor

Parâmetros padrão:



cpu_limit_high = 85%
cpu_limit_low = 45%
ram_limit_mb = 1500MB
cool_down = 2s


Recomendações:

### Para servidores intensivos:


cpu_limit_high = 92%
cpu_limit_low = 40%
ram_limit_mb = 2500MB


### Para clusters:


cpu_limit_high = 90%
cpu_limit_low = 50%
ram_limit_mb = 3200MB
cool_down = 1.5


---

# 📈 7. Benchmarks Oficiais (Referência)

### Máquina:
- 8 cores  
- 16 GB RAM  
- Renderer local + AsyncPipeline  

| Benchmark | Resultado |
|----------|-----------|
| Pipeline Sync (v36) | 2.5–3.8 s |
| Pipeline Async | 1.2–1.9 s |
| SectionEngine Turbo | +35% velocidade |
| Distributed Renderer | 0.6–1.4 s (dependendo da latência) |
| Pico de memória | 600–850 MB |

---

# 🔥 8. Stress Testing Oficial

Rodar:



pytest tests/stress/


Testes recomendados:
- 100 PDFs em sequência  
- 25 PDFs simultâneos (async)  
- pipeline distribuída com fallback  

Registrar:
- CPU  
- RAM  
- throughput  
- latência  
- falhas recuperadas  

---

# 🛰 9. Distribuição em Cluster

Topologia recomendada:



Client / API Async
|
Load Balancer
|
┌─────────┬─────────┐
| Node A | Node B | ← Workers Weasy / DistributedRenderer
└─────────┴─────────┘


Regras:
- cada nó deve ter cache local de templates  
- telemetria sincronizada  
- logs independentes por nó  
- recomendável: “sticky sessions”  

---

# 🧪 10. Manual de Diagnóstico

### Pipeline lenta?
- verifique `resource_monitor.jsonl`  
- CPU > 85% → Governor deve desligar TURBO  
- RAM > 1500MB → ativar chunking (já padrão)  

### PDF corrompido?
- verificar `DistributedRenderer → fallback_local`  
- checar tamanho do PDF via Telemetria  

### Deadlock?
- use AsyncPipeline (elimina bloqueio)  

### Seção travando?
- ativo no SectionEngine: logs por thread  

---

# 🧠 11. Conclusão

O MindScan possui um dos motores PDF mais avançados do mercado:

- total paralelização  
- async real  
- renderização distribuída  
- governança de performance  
- telemetria de nível enterprise  
- monitoramento contínuo  
- tuning detalhado  

Este guia completa o ciclo de **Performance e Otimização**, deixando o MindScan pronto para operações intensivas, clusters e ambientes críticos.
