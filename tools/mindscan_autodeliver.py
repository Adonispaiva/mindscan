"""
MindScan AutoDeliver
====================

Orquestrador de alto nível para:

1. Executar o pipeline de limpeza/backup/deploy (auto_orchestrator_v2.py);
2. Gerar automaticamente arquivos faltantes ou vazios (templates padrão);
3. Rodar a validação final (integridade + saúde + relatórios);
4. Registrar tudo em log dedicado.

Uso recomendado (a partir da raiz do projeto MindScan):

    venv\Scripts\python.exe tools\mindscan_autodeliver.py

Este script NÃO depende de caminhos absolutos; ele descobre a raiz com base
no próprio __file__, assumindo que está em: <root>/tools/mindscan_autodeliver.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Descoberta de caminhos principais
# ---------------------------------------------------------------------------

THIS_FILE = Path(__file__).resolve()
TOOLS_DIR = THIS_FILE.parent
ROOT_DIR = TOOLS_DIR.parent

SCRIPTS_DIR = ROOT_DIR / "scripts"
CONFIG_DIR = ROOT_DIR / "config"
DEPLOY_DIR = ROOT_DIR / "deploy"
INFRA_DIR = ROOT_DIR / "infra"
BACKEND_DIR = ROOT_DIR / "backend"
SERVICES_DIR = ROOT_DIR / "services"
LOGS_DIR = ROOT_DIR / "logs"

LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Logging centralizado
# ---------------------------------------------------------------------------

def setup_logger(verbose: bool = False) -> logging.Logger:
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"mindscan_autodeliver_{timestamp}.log"

    logger = logging.getLogger("MindScanAutoDeliver")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Evita handlers duplicados se o script for chamado mais de uma vez
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    logger.info("MindScan AutoDeliver iniciado.")
    logger.info("Raiz detectada do projeto: %s", ROOT_DIR)
    logger.info("Log registrado em: %s", log_file)

    return logger


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def run_subprocess(
    logger: logging.Logger,
    cmd: List[str],
    cwd: Path | None = None,
    allow_fail: bool = False,
    label: str | None = None,
) -> bool:
    """Executa um comando em subprocess, registrando saída."""
    display_label = label or " ".join(cmd)
    logger.info(">> Executando: %s", display_label)

    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=not allow_fail,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        logger.error("Falha ao executar %s", display_label)
        logger.error("Código de retorno: %s", exc.returncode)
        if exc.stdout:
            logger.error("STDOUT:\n%s", exc.stdout)
        if exc.stderr:
            logger.error("STDERR:\n%s", exc.stderr)
        if allow_fail:
            return False
        raise
    except OSError as exc:
        logger.error("Erro de sistema ao executar %s: %s", display_label, exc)
        if allow_fail:
            return False
        raise
    else:
        if result.stdout:
            logger.debug("STDOUT:\n%s", result.stdout)
        if result.stderr:
            logger.debug("STDERR:\n%s", result.stderr)
        logger.info("Concluído: %s (retorno=%s)", display_label, result.returncode)
        return result.returncode == 0


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Templates de arquivos faltantes ou vazios
# ---------------------------------------------------------------------------

def default_validator_policy_template() -> str:
    """Template padrão para config/validator_policy.json.

    Este conteúdo é equivalente ao definido manualmente, mas o AutoDeliver
    garante que o arquivo nunca fique vazio ou ausente.
    """
    data = {
        "version": "1.0",
        "environment": "MindScan-SynMind",
        "description": "Política de validação de integridade, estrutura e espaço em disco do ecossistema MindScan (SynMind).",
        "last_update": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "paths": {
            "root": str(ROOT_DIR).replace("\\", "/"),
            "backup_dir": str(ROOT_DIR / "backup").replace("\\", "/"),
            "logs_dir": str(LOGS_DIR).replace("\\", "/"),
            "alerts_dir": str(ROOT_DIR / "alerts").replace("\\", "/"),
            "scripts_dir": str(SCRIPTS_DIR).replace("\\", "/"),
        },
        "disk_min_free_percent": 25.0,
        "disk_warning_percent": 30.0,
        "directories_required": [
            "backup",
            "backup/_archive",
            "config",
            "core",
            "backend",
            "frontend",
            "web",
            "web_interface",
            "infra",
            "deploy",
            "logs",
            "alerts",
            "data",
            "tests",
            "tools",
            "services",
            "scripts",
            "mindscan_logs",
        ],
        "scripts_required": [
            "backup_manager.py",
            "backup_purger_progressive.py",
            "backup_mindscan_rclone.py",
            "structure_manager.py",
            "recovery_manager.py",
            "post_purge_validator.py",
            "integrity_scanner.py",
            "system_health_monitor.py",
            "maintenance_reporter.py",
            "alert_dispatcher.py",
            "alert_watcher.py",
            "auto_orchestrator_v2.py",
            "policy_loader.py",
            "weight_auditor.py",
            "manifest_registrar.py",
            "verificar_ambiente_mindscan.py",
        ],
        "recovery": {
            "auto_create_missing_directories": True,
            "auto_recreate_missing_scripts": True,
            "log_only_when_changes": True,
        },
        "alerts": {
            "disk_warning": "MindScan/SynMind — Atenção: espaço em disco no volume alvo abaixo do limite de segurança. Revise backups e arquivos de log.",
            "disk_critical": "MindScan/SynMind — CRÍTICO: espaço em disco insuficiente no volume alvo. Execute imediatamente a rotina de manutenção para evitar falhas e perda de dados.",
            "recovery_directory_created": "MindScan — Diretório ausente recriado automaticamente pela política de recuperação.",
            "recovery_script_recreated": "MindScan — Script essencial ausente foi recriado automaticamente pela política de recuperação.",
        },
        "logging": {
            "enable_verbose": True,
            "include_policy_snapshot_in_logs": True,
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def deploy_dockerfile_template() -> str:
    """Dockerfile padrão de backend FastAPI para MindScan."""
    return f"""# MindScan / SynMind - Dockerfile de Deploy (Backend)
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

COPY backend/ ./backend/
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""


def deploy_procfile_template() -> str:
    """Procfile de deploy padrão (backend FastAPI)."""
    return "web: uvicorn backend.main:app --host 0.0.0.0 --port 8000\n"


def infra_procfile_template() -> str:
    """Procfile alternativo para ambiente que exija múltiplos processos."""
    return (
        "web: uvicorn backend.main:app --host 0.0.0.0 --port 8000\n"
        "worker: python scripts/system_health_monitor.py\n"
    )


def admin_api_ts_template() -> str:
    """Template para backend/api/admin/AdminAPI.ts (cliente TS auxiliar)."""
    return """// Auto-gerado pelo MindScan AutoDeliver
// Cliente mínimo para endpoints administrativos da API MindScan (SynMind).

import axios, { AxiosInstance } from "axios";

export class AdminAPI {
  private client: AxiosInstance;

  constructor(baseURL: string = "/api") {
    this.client = axios.create({
      baseURL,
      withCredentials: true,
    });
  }

  async getHealth() {
    const resp = await this.client.get("/admin/health");
    return resp.data;
  }

  async getStats() {
    const resp = await this.client.get("/admin/stats");
    return resp.data;
  }

  async triggerSync() {
    const resp = await this.client.post("/admin/sync");
    return resp.data;
  }
}

export const adminAPI = new AdminAPI();
"""


def services_api_init_template() -> str:
    """Template para services/api/__init__.py."""
    return (
        '"""Camada de serviços/integração da API MindScan.\n\n'
        "Este módulo pode ser expandido com clients específicos\n"
        "para consumo interno (ex.: integrações SynMind, jobs, etc.).\n"
        'Gerado automaticamente pelo MindScan AutoDeliver.\n'
        '"""\n\n'
        "__all__ = []\n"
    )


def synmind_verificacao_template() -> str:
    """Template para synmind-verificacao.txt (marcador de integração)."""
    return (
        "MindScan verificado para integração com SynMind.\n"
        "Este arquivo é apenas um marcador lógico usado por rotinas de auditoria.\n"
    )


def large_objects_template() -> str:
    """Template para large-objects.txt (lista de artefatos grandes)."""
    return (
        "# MindScan - Large Objects Registry\n"
        "# Liste aqui manualmente arquivos grandes que não devem ir para o controle de versão\n"
        "# ou que exigem atenção especial em rotinas de backup.\n"
    )


def lcov_placeholder_template() -> str:
    """Template mínimo para frontend/coverage/lcov.info caso ferramenta exija arquivo."""
    return "TN:\nend_of_record\n"


# Mapa: caminho relativo -> função que gera conteúdo
TEMPLATE_REGISTRY: Dict[Path, callable] = {
    Path("config/validator_policy.json"): default_validator_policy_template,
    Path("deploy/Dockerfile"): deploy_dockerfile_template,
    Path("deploy/Procfile"): deploy_procfile_template,
    Path("infra/Procfile"): infra_procfile_template,
    Path("backend/api/admin/AdminAPI.ts"): admin_api_ts_template,
    Path("services/api/__init__.py"): services_api_init_template,
    Path("synmind-verificacao.txt"): synmind_verificacao_template,
    Path("large-objects.txt"): large_objects_template,
    Path("frontend/coverage/lcov.info"): lcov_placeholder_template,
}


def generate_missing_files(logger: logging.Logger, dry_run: bool = False) -> Tuple[int, int]:
    """Gera arquivos que estão faltando ou vazios, a partir do TEMPLATE_REGISTRY.

    Retorna (count_created, count_skipped).
    """
    created = 0
    skipped = 0

    logger.info("Verificando arquivos faltantes/vazios para geração automática...")

    for rel_path, template_func in TEMPLATE_REGISTRY.items():
        target = ROOT_DIR / rel_path
        exists = target.exists()
        size = target.stat().st_size if exists else 0

        if exists and size > 0:
            logger.info("OK (mantido): %s (já existe com tamanho %d bytes)", rel_path, size)
            skipped += 1
            continue

        action = "criação" if not exists else "recriação (arquivo vazio)"
        logger.warning("Arquivo faltante/vazio detectado: %s -> %s", rel_path, action)

        if dry_run:
            logger.info("[DRY-RUN] Simulação de geração para: %s", rel_path)
            continue

        ensure_parent_dir(target)
        content = template_func()
        mode = "w" if isinstance(content, str) else "wb"

        with target.open(mode, encoding="utf-8" if mode == "w" else None) as f:
            f.write(content)

        new_size = target.stat().st_size
        logger.info("Gerado arquivo: %s (%d bytes)", rel_path, new_size)
        created += 1

    logger.info(
        "Geração automática concluída. Criados: %d | Mantidos/ignorados: %d",
        created,
        skipped,
    )
    return created, skipped


# ---------------------------------------------------------------------------
# Pipelines de alto nível
# ---------------------------------------------------------------------------

def run_orchestrator(logger: logging.Logger, skip: bool = False, dry_run: bool = False) -> None:
    if skip:
        logger.info("Pulo da etapa de orquestração (auto_orchestrator_v2.py) por opção de linha de comando.")
        return

    orchestrator = SCRIPTS_DIR / "auto_orchestrator_v2.py"
    if not orchestrator.exists():
        logger.warning("auto_orchestrator_v2.py não encontrado em %s. Etapa ignorada.", orchestrator)
        return

    if dry_run:
        logger.info("[DRY-RUN] auto_orchestrator_v2.py seria executado aqui.")
        return

    run_subprocess(
        logger,
        [sys.executable, str(orchestrator)],
        cwd=ROOT_DIR,
        label="Auto Orchestrator v2",
    )


def run_validation_pipeline(logger: logging.Logger, skip: bool = False, dry_run: bool = False) -> None:
    if skip:
        logger.info("Pulo da etapa de validação final por opção de linha de comando.")
        return

    scripts_sequence = [
        "recovery_manager.py",
        "post_purge_validator.py",
        "integrity_scanner.py",
        "system_health_monitor.py",
        "maintenance_reporter.py",
        "alert_watcher.py",
    ]

    for script_name in scripts_sequence:
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            logger.warning("Script de validação não encontrado: %s (ignorado)", script_path)
            continue

        if dry_run:
            logger.info("[DRY-RUN] %s seria executado aqui.", script_name)
            continue

        run_subprocess(
            logger,
            [sys.executable, str(script_path)],
            cwd=ROOT_DIR,
            allow_fail=True,
            label=f"Validação: {script_name}",
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MindScan AutoDeliver — limpeza, geração de arquivos faltantes, deploy e validação.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula todas as ações sem modificar arquivos ou executar scripts pesados.",
    )
    parser.add_argument(
        "--skip-orchestrator",
        action="store_true",
        help="Não executa scripts/auto_orchestrator_v2.py (apenas geração de arquivos + validação).",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Não executa a cadeia de validação final (recovery/validator/integrity/health/reporter/alerts).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Ativa logging detalhado (DEBUG).",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    logger = setup_logger(verbose=args.verbose)

    logger.info("Parâmetros recebidos: dry_run=%s, skip_orchestrator=%s, skip_validation=%s",
                args.dry_run, args.skip_orchestrator, args.skip_validation)

    # 1) Orquestração de limpeza/backup/deploy
    run_orchestrator(logger, skip=args.skip_orchestrator, dry_run=args.dry_run)

    # 2) Geração de arquivos faltantes ou vazios
    created, skipped = generate_missing_files(logger, dry_run=args.dry_run)

    # 3) Validação final (integridade + saúde + relatórios)
    run_validation_pipeline(logger, skip=args.skip_validation, dry_run=args.dry_run)

    logger.info(
        "MindScan AutoDeliver finalizado. Arquivos criados/recriados: %d | existentes: %d",
        created,
        skipped,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
