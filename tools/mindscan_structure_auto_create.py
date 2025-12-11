# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\mindscan_structure_auto_create.py
# Última atualização: 2025-12-11T09:59:27.792836

import os
import json
import hashlib
from pathlib import Path

# ============================================================
#   MINDSCAN — AUTO STRUCTURE CREATOR v2 (SIM 2 — FULL SYNC)
#   Reconstruído por Leo Vinci — Inovexa
# ============================================================

BASE = "D:/projetos-inovexa/mindscan"

# ============================================================
#   CORE: LEITOR DE ÁRVORE ATUAL
#   Carrega a árvore real do projeto e compara com ALL_FILES.
# ============================================================

def scan_existing_files(base_path: str):
    existing = []
    base = Path(base_path)
    for path in base.rglob("*"):
        if path.is_file():
            rel = str(path.relative_to(base)).replace("\\", "/")
            existing.append(rel)
    return existing


EXISTING = scan_existing_files(BASE)

# ============================================================
#   ALL_FILES (VERSÃO RECONSTRUÍDA — COMPLETA)
#   Inclui: backend, engines, pipelines, MI, PDF, Bussola,
#           Big5, Esquemas, DASS, TEIQue, OCAI, Cruzamentos,
#           Utilitários, Serviços, Relatórios, Tests, Tools.
# ============================================================

ALL_FILES = [

    # --------------------------------------------------------
    # ROOT
    # --------------------------------------------------------
    "README.md",
    "ARCHITECTURE.md",
    "DEV_GUIDE.md",
    "PERFORMANCE_GUIDE.md",
    "OBSERVABILITY_GUIDE.md",
    "CLOSING_SUMMARY.md",
    "auditar_mindscan.py",

    # --------------------------------------------------------
    # BACKEND — CORE
    # --------------------------------------------------------
    "backend/app.py",
    "backend/config.py",
    "backend/main.py",
    "backend/database.py",
    "backend/models.py",
    "backend/pysettings.py",

    # --------------------------------------------------------
    # BACKEND / CORE ENGINE
    # --------------------------------------------------------
    "backend/core/engine.py",
    "backend/core/scoring.py",
    "backend/core/normalizer.py",
    "backend/core/nlp_processor.py",
    "backend/core/diagnostic_engine.py",
    "backend/core/runtime_kernel.py",

    # --------------------------------------------------------
    # ALGORITHMS — BIG 5
    # Versão completa (inclui módulos faltantes)
    # --------------------------------------------------------
    "backend/algorithms/big5/big5.py",
    "backend/algorithms/big5/big5_dimensions.py",
    "backend/algorithms/big5/big5_enrichment.py",
    "backend/algorithms/big5/big5_factor_weights.py",
    "backend/algorithms/big5/big5_insights.py",
    "backend/algorithms/big5/big5_norms.py",
    "backend/algorithms/big5/big5_profile_builder.py",
    "backend/algorithms/big5/big5_risk_flags.py",
    "backend/algorithms/big5/big5_strengths.py",
    "backend/algorithms/big5/big5_traits_map.py",
    "backend/algorithms/big5/big5_validation.py",

    # ---- ARQUIVOS FALTANTES AGORA INCLUÍDOS ----
    "backend/algorithms/big5/big5_alerts.py",
    "backend/algorithms/big5/big5_crosslinks.py",
    "backend/algorithms/big5/big5_factor_map.py",
    "backend/algorithms/big5/big5_needs_map.py",
    "backend/algorithms/big5/big5_output_formatter.py",
    "backend/algorithms/big5/big5_predictor.py",
    "backend/algorithms/big5/big5_risk_map.py",
    "backend/algorithms/big5/big5_summary.py",
        # --------------------------------------------------------
    # ALGORITHMS — TEIQue
    # --------------------------------------------------------
    "backend/algorithms/teique/teique.py",
    "backend/algorithms/teique/teique_dimensions.py",
    "backend/algorithms/teique/teique_insights.py",
    "backend/algorithms/teique/teique_norms.py",
    "backend/algorithms/teique/teique_profile_builder.py",
    "backend/algorithms/teique/teique_validation.py",
    "backend/algorithms/teique/teique_risk_flags.py",
    "backend/algorithms/teique/teique_strengths.py",
    "backend/algorithms/teique/teique_traits_map.py",

    # Arquivos faltantes TEIQue (completando a arquitetura)
    "backend/algorithms/teique/teique_alerts.py",
    "backend/algorithms/teique/teique_crosslinks.py",
    "backend/algorithms/teique/teique_output_formatter.py",
    "backend/algorithms/teique/teique_summary.py",

    # --------------------------------------------------------
    # ALGORITHMS — DASS21
    # --------------------------------------------------------
    "backend/algorithms/dass21/dass21.py",
    "backend/algorithms/dass21/dass21_factors.py",
    "backend/algorithms/dass21/dass21_insights.py",
    "backend/algorithms/dass21/dass21_norms.py",
    "backend/algorithms/dass21/dass21_validation.py",
    "backend/algorithms/dass21/dass21_profile_builder.py",

    # Arquivos faltantes DASS
    "backend/algorithms/dass21/dass21_alerts.py",
    "backend/algorithms/dass21/dass21_output_formatter.py",
    "backend/algorithms/dass21/dass21_summary.py",

    # --------------------------------------------------------
    # ALGORITHMS — OCAI
    # --------------------------------------------------------
    "backend/algorithms/ocai/ocai.py",
    "backend/algorithms/ocai/ocai_dimensions.py",
    "backend/algorithms/ocai/ocai_profile_builder.py",
    "backend/algorithms/ocai/ocai_norms.py",
    "backend/algorithms/ocai/ocai_insights.py",
    "backend/algorithms/ocai/ocai_validation.py",

    # Arquivos faltantes OCAI
    "backend/algorithms/ocai/ocai_alerts.py",
    "backend/algorithms/ocai/ocai_output_formatter.py",
    "backend/algorithms/ocai/ocai_summary.py",

    # --------------------------------------------------------
    # ALGORITHMS — Esquemas (Schema Therapy)
    # --------------------------------------------------------
    "backend/algorithms/esquemas/esquemas.py",
    "backend/algorithms/esquemas/schema_dimensions.py",
    "backend/algorithms/esquemas/schema_profile_builder.py",
    "backend/algorithms/esquemas/schema_insights.py",
    "backend/algorithms/esquemas/schema_validation.py",

    # Arquivos faltantes Esquemas
    "backend/algorithms/esquemas/schema_alerts.py",
    "backend/algorithms/esquemas/schema_output_formatter.py",
    "backend/algorithms/esquemas/schema_summary.py",
    "backend/algorithms/esquemas/schema_risk_map.py",

    # --------------------------------------------------------
    # ALGORITHMS — Performance
    # --------------------------------------------------------
    "backend/algorithms/performance/performance.py",
    "backend/algorithms/performance/performance_dimensions.py",
    "backend/algorithms/performance/performance_insights.py",
    "backend/algorithms/performance/performance_norms.py",
    "backend/algorithms/performance/performance_validation.py",
    "backend/algorithms/performance/performance_profile_builder.py",

    # Arquivos faltantes Performance
    "backend/algorithms/performance/performance_alerts.py",
    "backend/algorithms/performance/performance_output_formatter.py",
    "backend/algorithms/performance/performance_summary.py",

    # --------------------------------------------------------
    # BÚSSOLA DE TALENTOS — COMPLETA
    # --------------------------------------------------------
    "backend/algorithms/bussola/bussola.py",
    "backend/algorithms/bussola/bussola_coordinates.py",
    "backend/algorithms/bussola/bussola_matrix.py",
    "backend/algorithms/bussola/bussola_archetypes.py",
    "backend/algorithms/bussola/bussola_directions.py",
    "backend/algorithms/bussola/bussola_recommendations.py",
    "backend/algorithms/bussola/bussola_risks.py",
    "backend/algorithms/bussola/bussola_strengths.py",
    "backend/algorithms/bussola/bussola_validation.py",
    "backend/algorithms/bussola/bussola_output_formatter.py",
    "backend/algorithms/bussola/bussola_alerts.py",
    "backend/algorithms/bussola/bussola_crosslinks.py",

    # --------------------------------------------------------
    # CRUZAMENTOS — CROSS ENGINE
    # --------------------------------------------------------
    "backend/algorithms/cruzamentos/cross_engine.py",
    "backend/algorithms/cruzamentos/cross_alerts.py",
    "backend/algorithms/cruzamentos/cross_risks.py",
    "backend/algorithms/cruzamentos/cross_strengths.py",

    # BIG5 Kombinationen
    "backend/algorithms/cruzamentos/cross_big5_teique.py",
    "backend/algorithms/cruzamentos/cross_big5_dass.py",
    "backend/algorithms/cruzamentos/cross_big5_esquemas.py",
    "backend/algorithms/cruzamentos/cross_big5_ocai.py",
    "backend/algorithms/cruzamentos/cross_big5_performance.py",

    # Outros cruzamentos
    "backend/algorithms/cruzamentos/cross_teique_dass.py",
    "backend/algorithms/cruzamentos/cross_teique_esquemas.py",
    "backend/algorithms/cruzamentos/cross_ocai_dass.py",
    "backend/algorithms/cruzamentos/cross_ocai_teique.py",
    "backend/algorithms/cruzamentos/cross_ocai_big5.py",
        # --------------------------------------------------------
    # MODELS — INPUTS
    # --------------------------------------------------------
    "backend/models/inputs/big5_input.py",
    "backend/models/inputs/teique_input.py",
    "backend/models/inputs/ocai_input.py",
    "backend/models/inputs/dass_input.py",
    "backend/models/inputs/esquemas_input.py",
    "backend/models/inputs/performance_input.py",
    "backend/models/inputs/bussola_input.py",
    "backend/models/inputs/cross_input.py",
    "backend/models/inputs/user_profile.py",
    "backend/models/inputs/metadata_input.py",
    "backend/models/inputs/session_input.py",
    "backend/models/inputs/device_input.py",
    "backend/models/inputs/cognitive_input.py",
    "backend/models/inputs/behavioral_input.py",
    "backend/models/inputs/mi_input.py",
    "backend/models/inputs/pdf_input.py",
    "backend/models/inputs/export_input.py",
    "backend/models/inputs/pipeline_input.py",

    # --------------------------------------------------------
    # MODELS — OUTPUTS
    # --------------------------------------------------------
    "backend/models/outputs/big5_output.py",
    "backend/models/outputs/teique_output.py",
    "backend/models/outputs/ocai_output.py",
    "backend/models/outputs/dass_output.py",
    "backend/models/outputs/esquemas_output.py",
    "backend/models/outputs/performance_output.py",
    "backend/models/outputs/bussola_output.py",
    "backend/models/outputs/cross_output.py",
    "backend/models/outputs/risk_report.py",
    "backend/models/outputs/strengths_report.py",
    "backend/models/outputs/summary_output.py",
    "backend/models/outputs/pdf_output.py",
    "backend/models/outputs/mi_output.py",
    "backend/models/outputs/diagnostic_output.py",
    "backend/models/outputs/metadata_output.py",
    "backend/models/outputs/token_output.py",
    "backend/models/outputs/user_output.py",
    "backend/models/outputs/pipeline_output.py",

    # --------------------------------------------------------
    # MODELS — SCORING
    # --------------------------------------------------------
    "backend/models/scoring/scoring_big5.py",
    "backend/models/scoring/scoring_teique.py",
    "backend/models/scoring/scoring_ocai.py",
    "backend/models/scoring/scoring_dass.py",
    "backend/models/scoring/scoring_esquemas.py",
    "backend/models/scoring/scoring_performance.py",
    "backend/models/scoring/scoring_bussola.py",
    "backend/models/scoring/scoring_cross.py",
    "backend/models/scoring/scoring_global.py",
    "backend/models/scoring/scoring_validation.py",

    # --------------------------------------------------------
    # PDF SECTIONS
    # --------------------------------------------------------
    "backend/services/pdf/pdf_sections/capa_executiva.py",
    "backend/services/pdf/pdf_sections/capa_enterprise.py",
    "backend/services/pdf/pdf_sections/resumo_estrategico.py",
    "backend/services/pdf/pdf_sections/narrativa.py",
    "backend/services/pdf/pdf_sections/perfil_integrado.py",
    "backend/services/pdf/pdf_sections/mapa_cultural.py",
    "backend/services/pdf/pdf_sections/mapa_lideranca.py",
    "backend/services/pdf/pdf_sections/mapa_esquemas.py",
    "backend/services/pdf/pdf_sections/mapa_emocional.py",
    "backend/services/pdf/pdf_sections/analise_performance.py",
    "backend/services/pdf/pdf_sections/riscos_globais.py",
    "backend/services/pdf/pdf_sections/forcas_globais.py",
    "backend/services/pdf/pdf_sections/inteligencia_emocional.py",
    "backend/services/pdf/pdf_sections/estilo_cognitivo.py",
    "backend/services/pdf/pdf_sections/matriz_diagnostica.py",
    "backend/services/pdf/pdf_sections/eixo_profissional.py",
    "backend/services/pdf/pdf_sections/maturidade_profissional.py",
    "backend/services/pdf/pdf_sections/trilha_de_carreira.py",
    "backend/services/pdf/pdf_sections/pdi_completo.py",
    "backend/services/pdf/pdf_sections/roadmap_completo.py",
    "backend/services/pdf/pdf_sections/match_duplo.py",
    "backend/services/pdf/pdf_sections/anexos_profissionais.py",

    # --------------------------------------------------------
    # PDF RENDERERS / TEMPLATE ENGINE
    # --------------------------------------------------------
    "backend/services/pdf/renderers/html_renderer.py",
    "backend/services/pdf/renderers/hybrid_renderer.py",
    "backend/services/pdf/renderers/pdf_sanitizer.py",
    "backend/services/pdf/renderers/pdf_integrity_validator.py",
    "backend/services/pdf/renderers/font_manager.py",
    "backend/services/pdf/renderers/resource_resolver.py",
    "backend/services/pdf/renderers/image_manager.py",
    "backend/services/pdf/renderers/pdf_theme_manager.py",
    "backend/services/pdf/renderers/pdf_layout_engine.py",
    "backend/services/pdf/renderers/pdf_styler.py",
    "backend/services/pdf/renderers/pdf_section_validator.py",
    "backend/services/pdf/renderers/pdf_accessibility.py",
    "backend/services/pdf/renderers/pdf_security.py",
    "backend/services/pdf/renderers/pdf_exporter.py",
    "backend/services/pdf/renderers/pdf_post_processor.py",

    # --------------------------------------------------------
    # PDF TEMPLATES
    # --------------------------------------------------------
    "backend/services/pdf/report_templates/leadership_template.py",
    "backend/services/pdf/report_templates/culture_template.py",
    "backend/services/pdf/report_templates/diagnostics_template.py",
    "backend/services/pdf/report_templates/fullstack_template.py",
    "backend/services/pdf/report_templates/integrated_template.py",
    "backend/services/pdf/report_templates/executive_enterprise_template.py",
    "backend/services/pdf/report_templates/lite_template.py",
    "backend/services/pdf/report_templates/compass_template.py",
    "backend/services/pdf/report_templates/analytic_template.py",
    "backend/services/pdf/report_templates/narrative_template.py",

    # --------------------------------------------------------
    # MI — (MENTE INTEGRADA)
    # --------------------------------------------------------
    "backend/mi/persona/persona_core.py",
    "backend/mi/persona/persona_voice.py",
    "backend/mi/persona/persona_rules.py",
    "backend/mi/persona/persona_style.py",
    "backend/mi/persona/persona_examples.py",
    "backend/mi/persona/persona_constraints.py",
    "backend/mi/persona/persona_filters.py",
    "backend/mi/persona/persona_metadata.py",

    "backend/mi/compliance/compliance_root.py",
    "backend/mi/compliance/compliance_psycho.py",
    "backend/mi/compliance/compliance_organizational.py",
    "backend/mi/compliance/compliance_diagnostic.py",
    "backend/mi/compliance/compliance_apa.py",
    "backend/mi/compliance/compliance_ethics.py",
    "backend/mi/compliance/compliance_limits.py",
    "backend/mi/compliance/compliance_moderation.py",

    "backend/mi/mi_chain_of_thought.py",
    "backend/mi/mi_reasoning.py",
    "backend/mi/mi_postprocessing.py",
    "backend/mi/mi_structurer.py",
    "backend/mi/mi_validator.py",
    "backend/mi/mi_sanitizer.py",

    # --------------------------------------------------------
    # ROUTERS
    # --------------------------------------------------------
    "backend/routers/pdf_router.py",
    "backend/routers/report_router.py",
    "backend/routers/metadata_router.py",
    "backend/routers/analytics_router.py",
    "backend/routers/mi_router.py",
    "backend/routers/export_router.py",
    "backend/routers/user_profile_router.py",
    "backend/routers/diagnostics_router.py",

    # --------------------------------------------------------
    # SERVICES
    # --------------------------------------------------------
    "backend/services/analytics_service.py",
    "backend/services/metadata_service.py",
    "backend/services/insight_service.py",
    "backend/services/flags_service.py",
    "backend/services/recommendation_service.py",
    "backend/services/pdi_service.py",
    "backend/services/roadmap_service.py",
    "backend/services/leadership_service.py",
    "backend/services/culture_service.py",
    "backend/services/performance_service.py",
    "backend/services/narrative_service.py",
    "backend/services/export_service.py",
    "backend/services/mi_compiler_service.py",
    "backend/services/pdf_validator_service.py",
    "backend/services/diagnostic_matrix_service.py",
        # --------------------------------------------------------
    # PIPELINES
    # --------------------------------------------------------
    "backend/pipelines/big5_pipeline.py",
    "backend/pipelines/teique_pipeline.py",
    "backend/pipelines/ocai_pipeline.py",
    "backend/pipelines/dass_pipeline.py",
    "backend/pipelines/esquemas_pipeline.py",
    "backend/pipelines/performance_pipeline.py",
    "backend/pipelines/bussola_pipeline.py",
    "backend/pipelines/cross_pipeline.py",
    "backend/pipelines/diagnostic_pipeline_async.py",
    "backend/pipelines/full_pipeline.py",

    # --------------------------------------------------------
    # ENGINES
    # --------------------------------------------------------
    "backend/engine/parallel_engine.py",
    "backend/engine/sequential_engine.py",
    "backend/engine/integration_engine.py",
    "backend/engine/scoring_engine.py",
    "backend/engine/validation_engine.py",
    "backend/engine/normalization_engine.py",
    "backend/engine/insight_engine.py",
    "backend/engine/synthesis_engine.py",
    "backend/engine/metadata_engine.py",
    "backend/engine/pre_diagnostic_engine.py",
    "backend/engine/post_diagnostic_engine.py",
    "backend/engine/mi_engine_advanced.py",
    "backend/engine/pdf_engine_advanced.py",
    "backend/engine/runtime_engine.py",

    "backend/engine/score_aggregator.py",
    "backend/engine/insight_aggregator.py",
    "backend/engine/risk_aggregator.py",
    "backend/engine/summary_aggregator.py",
    "backend/engine/profile_aggregator.py",

    # --------------------------------------------------------
    # UTILS
    # --------------------------------------------------------
    "backend/utils/math_utils.py",
    "backend/utils/array_utils.py",
    "backend/utils/vector_utils.py",
    "backend/utils/json_sanitizer.py",
    "backend/utils/config_loader.py",
    "backend/utils/hashing_utils.py",
    "backend/utils/profile_formatter.py",
    "backend/utils/diagnostic_formatter.py",
    "backend/utils/pdf_utils.py",
    "backend/utils/api_utils.py",
    "backend/utils/scheduler_utils.py",
    "backend/utils/token_manager.py",
    "backend/utils/resource_manager.py",
    "backend/utils/document_utils.py",

    # --------------------------------------------------------
    # TOOLS
    # --------------------------------------------------------
    "tools/mindscan_structure_auto_create.py",
    "tools/mindscan_file_generator.py",
    "tools/mindscan_tree_validator.py",
]

# ============================================================
#  FILTRO: arquivos faltantes
# ============================================================

def compute_missing_files(all_files, existing_files):
    return [f for f in all_files if f not in existing_files]


MISSING = compute_missing_files(ALL_FILES, EXISTING)

# ============================================================
#  CRIAÇÃO AUTOMÁTICA DOS ARQUIVOS
# ============================================================

def create_file(path: str):
    full_path = Path(BASE) / path
    folder = full_path.parent
    folder.mkdir(parents=True, exist_ok=True)

    if not full_path.exists():
        full_path.write_text("", encoding="utf-8")
        print(f"[OK] Criado: {full_path}")
    else:
        print(f"[SKIP] Já existe: {full_path}")


def create_missing_structure():
    print("\n=== MINDSCAN STRUCTURE AUTO-CREATOR v2 (SIM 2 — FULL SYNC) ===\n")

    if not MISSING:
        print("Nenhum arquivo faltante encontrado. Estrutura 100% atualizada.")
        return

    print(f"Arquivos faltantes detectados: {len(MISSING)}\n")

    for rel_path in MISSING:
        create_file(rel_path)

    print("\nProcesso concluído com sucesso.\n")


# ============================================================
#  EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":
    create_missing_structure()
