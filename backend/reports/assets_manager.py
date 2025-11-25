# ============================================================
# MindScan — Assets Manager
# ============================================================
# Gerencia todos os recursos estáticos utilizados pelos relatórios:
# - Logotipos
# - Paletas de cores
# - Ícones
# - Fontes (futuras)
#
# Este módulo padroniza o acesso aos assets visuais, garantindo
# consistência entre PDF, HTML, relatórios e futuro front-end.
#
# Versão: SynMind 2025 — Completo e definitivo.
# ============================================================

import os
from typing import Dict


class AssetsManager:
    """
    Centralizador dos recursos estáticos do MindScan.
    """

    def __init__(self):
        # Caminho do logotipo principal
        self.paths = {
            "logo_synmind": "/mnt/data/LogoSMok.png"
        }

        # Paleta de cores oficial extraída do logotipo
        self.colors = {
            "primary_blue": "#506482",
            "secondary_blue": "#4A5E78",
            "primary_orange": "#D78E2A",
            "deep_orange": "#C98324",
            "background_light": "#F4F6FA",
            "text_dark": "#2A2A2A"
        }

    # ------------------------------------------------------------
    # Recuperar caminho de asset
    # ------------------------------------------------------------
    def get(self, name: str) -> str:
        return self.paths.get(name, "")

    # ------------------------------------------------------------
    # Paleta de cores completa
    # ------------------------------------------------------------
    def color_palette(self) -> Dict[str, str]:
        return self.colors

    # ------------------------------------------------------------
    # Verificar existência real do arquivo
    # ------------------------------------------------------------
    def exists(self, name: str) -> bool:
        path = self.paths.get(name, "")
        return os.path.exists(path)


# Instância pública
assets_manager = AssetsManager()
