# Caminho: backend/config.py
# Status: LEGACY (DESCONTINUADO)
# Diretor Técnico: Leo Vinci — Inovexa Software
#
# Este arquivo pertence ao antigo sistema de configuração do MindScan.
# A partir do MindScan Backend v2.0 (SynMind), todo o backend utiliza
# exclusivamente o módulo "pysettings.py" como fonte única de configuração.
#
# Este arquivo é mantido apenas para:
#   - preservação histórica
#   - compatibilidade com repositórios legados
#   - consulta técnica e auditoria
#
# Ele NÃO é mais utilizado pelo backend.
# Qualquer tentativa de import irá lançar uma exceção controlada,
# evitando usos acidentais e garantindo integridade do sistema.

class _ConfigLegacyError(Exception):
    """Erro lançado se alguém tentar usar o módulo legacy."""
    pass


def __getattr__(name):
    raise _ConfigLegacyError(
        f"O módulo 'config.py' foi descontinuado. "
        f"Use 'pysettings.py' e 'get_settings()'. "
        f"Tentativa de acessar atributo: {name}"
    )


def __call__(*args, **kwargs):
    raise _ConfigLegacyError(
        "O módulo 'config.py' não pode mais ser utilizado. "
        "A configuração oficial está em 'pysettings.py'."
    )
