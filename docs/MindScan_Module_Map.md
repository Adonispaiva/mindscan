# 🧠 MindScan — Mapa Oficial de Módulos (Arquitetura Maximalista)
Versão: 1.0  
Data: 11/12/2025  
Diretor Técnico: Leo Vinci — Inovexa

Este documento estabelece o **contrato estrutural oficial** do projeto MindScan, definindo todos os módulos, seu papel, status atual e prioridade de implementação.  
Ele é a referência base para Anti-Regressão, desenvolvimento e auditorias.

---

# 1. Núcleo MindScan (CORE) — 100% Mantido
Módulos essenciais, imutáveis, diretamente ligados ao diagnóstico:

- `backend/core/`
- `backend/engine/`
- `backend/api/`
- `backend/orchestrator/`
- `backend/normalization/`
- `backend/scoring/`
- `backend/diagnostic_engine.py`
- `backend/diagnostic_engine_v3.py` (mantido até fusão futura)
- `backend/runtime_kernel.py`
- `backend/models/`
- `backend/instrument_pipeline/`

**Status:** Completo e funcional.  
**Prioridade:** Manter / expandir apenas conforme necessidade analítica.

---

# 2. Módulos de Compliance MI — MANTIDOS (Maximalista)
Todos os arquivos são necessários para a governança ética, regulatória e psicométrica:

## 2.1 Implementados
- `compliance_apa.py`
- `compliance_bias.py`
- `compliance_fairness.py`
- `compliance_privacy.py`
- `compliance_security.py`
- `compliance_transparency.py`

## 2.2 Placeholders (a implementar)
- `compliance_diagnostic.py`
- `compliance_ethics.py`
- `compliance_limits.py`
- `compliance_moderation.py`
- `compliance_organizational.py`
- `compliance_psycho.py`
- `compliance_root.py`

**Status:** Prioridade FASE 2.  
**Regra:** Nenhum é removido.

---

# 3. Sistema de Relatórios PDF (Premium) — MANTIDO
Arquitetura subdividida em 4 camadas:

## 3.1 Sections (conteúdo bruto do relatório)
`backend/services/pdf/pdf_sections/`  
**Todos os 22 arquivos são mantidos**, mesmo que vazios.

## 3.2 Templates (formas finais do documento)
`backend/services/pdf/report_templates/`  
**Todos os 10 templates permanecem.**

## 3.3 Renderers (motores de conversão)
`backend/services/pdf/renderers/`  
**Todos mantidos.**

## 3.4 PDF Engine
- **CANÔNICO:** `backend/services/pdf_engine.py`
- `pdf_engine_manifest.py`: mantido.
- `pdf.engine.py`, `engine/pdf.engine.py`: **LEGACY** (não usar, não apagar ainda).
- `pdf_renderer_engine_v4.py.txt`: marcador histórico. **LEGACY**.

---

# 4. Módulos Utils — MANTIDOS (Maximalista)
Todos os arquivos de utilidades são preservados:

backend/utils/api_utils.py
backend/utils/array_utils.py
backend/utils/config_loader.py
backend/utils/diagnostic_formatter.py
backend/utils/document_utils.py
backend/utils/hashing_utils.py
backend/utils/json_sanitizer.py
backend/utils/math_utils.py
backend/utils/pdf_utils.py
backend/utils/profile_formatter.py
backend/utils/resource_manager.py
backend/utils/scheduler_utils.py
backend/utils/token_manager.py
backend/utils/vector_utils.py

yaml
Copiar código

**Status:** Placeholders válidos.  
**Implementação:** FASE 2 (selectiva).

---

# 5. Módulos a Descontinuar (LEGACY)
Arquitetura antiga do gerador automático:

backend/routers/*.py
backend/services/pdf/pdf.engine.py
backend/services/pdf/engine/pdf.engine.py
export_v4/pdf/pdf_renderer_engine_v4.py.txt

yaml
Copiar código

**Regra:**  
Não deletar ainda — marcar como **LEGACY**.  
Serão removidos oficialmente na FASE 3 (Merge Técnico).

---

# 6. Módulos Complementares
- `backend/api/utils/error_response_builder.py` → canônico.
- `backend/services/mi/compliance_filter.py` → mantido.

---

# 7. Regras Anti-Regressão Atreladas ao Mapa
1. Nenhum módulo listado como **CORE** pode ser renomeado ou removido.  
2. Nenhum módulo **MAXIMALISTA** pode ser deletado sem aprovação diretiva.  
3. Módulos **LEGACY** não podem ser utilizados em importações.  
4. Placeholders identificados devem ser implementados nas FASES 2 e 3.  
5. Qualquer novo módulo deve seguir a estrutura definida neste mapa.

---

# 8. Próximas Fases
### 🟦 FASE 1 — Conclusão
- Consolidação estrutural (este documento)

### 🟧 FASE 2 — Preenchimento dos placeholders
- PDF Sections  
- PDF Templates  
- Renderers  
- Utils essenciais  
- Compliance MI  

### 🟥 FASE 3 — Limpeza definitiva (remoção de legacy)
- Routers antigos  
- Engines paralelos  
- Arquivos gerados automaticamente sem uso real

---

**Fim do Documento — MindScan_Module_Map.md**
