# 🧠 MindScan PDF Engine — ARCHITECTURE.md  
Inovexa Software — Documento Arquitetural Oficial  
Versão: 1.0.0  
Atualizado em: 2025-11-30

---

# 📘 1. Visão Macro da Arquitetura

O **MindScan PDF Engine** é composto por cinco camadas arquiteturais:

┌───────────────────────────────────────────────┐
│ 1. CLI (Interface de Execução) │
└───────────────────────────────────────────────┘
│ chama
┌───────────────────────────────────────────────┐
│ 2. Validação de Dados │
└───────────────────────────────────────────────┘
│ valida
┌───────────────────────────────────────────────┐
│ 3. PDFBuilder (Orquestração) │
└───────────────────────────────────────────────┘
│ chama
┌───────────────────────────────────────────────┐
│ 4. Renderers (WeasyPrint / ReportLab) │
└───────────────────────────────────────────────┘
│ produz PDF
┌───────────────────────────────────────────────┐
│ 5. Logger + Telemetria (Observabilidade) │
└───────────────────────────────────────────────┘


Essa arquitetura garante:

- robustez  
- extensibilidade  
- testabilidade  
- separação absoluta de responsabilidades  
- rastreamento corporativo ponta-a-ponta  

---

# 📐 2. Objetivos Arquiteturais

1. **Confiabilidade em produção**  
   - Zero tolerância a falhas silenciosas  
   - Todos os erros são logados e rastreáveis  

2. **Extensibilidade**  
   - Seções modulares  
   - Renderers plugáveis  
   - Telemetria evolutiva  

3. **Isolamento de responsabilidades**  
   - PDFBuilder não calcula nada  
   - Renderers não conhecem regras de negócio  
   - Validator não conhece HTML  
   - CLI não monta HTML  

4. **Performance e observabilidade**  
   - Telemetria avançada  
   - Stress tests reais  
   - Separação entre HTML Builder e Renderer  

---

# 🧱 3. Arquitetura de Pastas (macro)



mindscan/
│
├── backend/
│ └── services/
│ └── pdf/
│ ├── pdf_sections/ ← 14 seções modulares
│ ├── templates/ ← HTML/CSS premium
│ ├── renderers/ ← Weasy / ReportLab
│ ├── validators/ ← integridade dos dados
│ └── telemetry/ ← logs + telemetria avançada
│
├── mindscan_pdf/ ← pacote instalável (CLI)
│ ├── init.py
│ └── cli.py
│
├── mindscan_cli/ ← CLI standalone opcional
│
├── tests/ ← testes unitários, stress, performance
│
├── mindscan_examples/ ← scripts de exemplo
│
├── README.md ← documentação para usuários
├── DEV_GUIDE.md ← documentação para devs
└── ARCHITECTURE.md ← ESTE DOCUMENTO


---

# 🧩 4. Componentes Principais

## 4.1 CLI (mindscan-pdf)
- Ponto de entrada do motor
- Faz parsing de argumentos
- Carrega JSONs
- Inicia logger
- Chama validator
- Chama builder e renderer
- Exporta logs e telemetria

## 4.2 Validator
- Verifica integridade dos dados
- Garante o contrato entre camadas
- Impede PDFs corrompidos
- Protege contra regressões de estrutura

## 4.3 PDFBuilder
- Cérebro da pipeline
- Monta HTML final
- Coordena renderização
- Calcula tempos (telemetria)
- Registra logs estruturados

## 4.4 Renderers
### WeasyRenderer (principal)
- HTML → PDF real
- CSS completo
- Templates premium
- Suporte a imagens base64
- Performance otimizada

### ReportLabRenderer (fallback)
- PDF simples
- Zero dependências externas
- Ideal para ambientes restritos

## 4.5 Telemetria + Logger
- Tempo total da pipeline  
- Tempo por seção  
- Tamanho final do PDF  
- Renderer utilizado  
- Sessões + métricas em JSONL  
- Logs auditáveis corporativos  

---

# 🧬 5. Diagrama de Fluxo (detalhado)



mindscan-pdf gerar
│
▼
┌───────────────────────┐
│ Carregar JSONs │
└───────────────────────┘
│
▼
┌───────────────────────┐
│ Validação (Validator) │
└───────────────────────┘
│
▼
┌───────────────────────┐
│ PDFBuilder │
| - telemetria total |
| - telemetria seções |
| - logs |
└───────────────────────┘
│ monta HTML
▼
┌──────────────────────────┐
│ Renderers │
│ - WeasyRenderer │
│ - ReportLabRenderer │
└──────────────────────────┘
│ produz PDF
▼
┌──────────────────────────┐
│ Logs + Telemetria │
└──────────────────────────┘


---

# ⚙️ 6. Contratos Arquiteturais

### 6.1 Templates
- Devem conter `{{conteudo}}`  
- O CSS deve referenciar apenas assets locais  
- Proibido fazer cálculos dentro do template  

### 6.2 Seções
- Devem retornar **HTML puro**  
- Devem ser autocontidas  
- Devem receber contexto via `.render(ctx)`  

### 6.3 Renderers
- Devem aceitar:  
  `renderer.render_html_to_pdf(html, output_path)`  
- Devem ser totalmente substituíveis  
- Não podem conhecer regras do MindScan  

### 6.4 Telemetria
- Deve ser opcional mas recomendada  
- Deve registrar tempo por seção  
- Deve exportar JSONL por sessão  

---

# 🧪 7. Testabilidade

O projeto possui:

### ✔ Testes unitários essenciais  
`test_pdf_engine.py`

### ✔ Testes de performance / stress  
`test_performance_stress.py`

### ✔ Stress test REAL com WeasyRenderer  
`test_stress_weasy_real.py`

### Garantias:
- 200 ciclos de HTML  
- 50 ciclos completos simulados  
- 10 PDFs REAIS com WeasyPrint  
- Detecção de regressão automática  

---

# 🚀 8. Regras de Evolução Arquitetural

1. Nenhuma lógica nova deve ir para o renderer  
2. Novas seções devem seguir padrão Section  
3. Nenhum dado sensível vai para logs  
4. Qualquer mudança nos templates requer migração versionada  
5. Telemetria não deve poluir o código  
6. PDFBuilder nunca deve “saber demais”  
7. CLI nunca deve fazer processamento  
8. Sempre adicionar testes ao introduzir novas seções  

---

# 📈 9. Roadmap Arquitetural Futuro

- Motor de renderização assíncrono (WeasyAsync)  
- Cache de seções pré-compiladas  
- Geração paralela de múltiplos PDFs  
- Engine distribuída (cluster)  
- Exportação para DOCX e HTML5  
- Sistema de plugins para seções  
- Dashboard interno de telemetria Inovexa  

---

# 🧠 MindScan PDF Engine  
**Arquitetura corporativa. Observabilidade de ponta.  
Excelência Inovexa/SynMind.**