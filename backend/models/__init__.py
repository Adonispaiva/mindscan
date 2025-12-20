# =================================================================
# ORION: CENTRALIZAÇÃO DE MODELOS (PADRÃO ULTRA SUPERIOR)
# =================================================================
# Importações relativas para evitar conflitos de namespace no Windows
from .user import User
# As linhas abaixo devem ser descomentadas à medida que os ficheiros forem criados/validados
# from .candidate import Candidate
# from .mindscan_test import MindscanTest
# from .mindscan_answers import MindscanAnswers
# from .mindscan_result import MindscanResult
# from .mindscan_report import MindscanReport

__all__ = [
    "User",
    # "Candidate",
    # "MindscanTest",
    # "MindscanAnswers",
    # "MindscanResult",
    # "MindscanReport",
]