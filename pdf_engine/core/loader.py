"""
pdf_engine/core/loader.py
Módulo: Data Loader para o PDF Engine do MindScan

Responsabilidades:
- Carregar dados consolidados dos algoritmos MindScan
- Validar e estruturar dicionários/objetos recebidos
- Normalizar campos, garantindo padrão uniforme para as seções do PDF
- NÃO executar cálculos psicométricos (isso já pertence aos algoritmos)
"""

from typing import Any, Dict


class DataLoaderError(Exception):
    """Erro específico dos processos de carregamento do PDF Engine."""
    pass


class DataLoader:
    """
    Classe central de carregamento e normalização de dados.
    Converte entradas em um pacote padronizado acessível ao pipeline PDF.
    """

    REQUIRED_FIELDS = [
        "big5",
        "teique",
        "dass21",
        "esquemas",
        "performance",
        "ocai",
        "cruzamentos",
        "bussola",
    ]

    def __init__(self, data: Dict[str, Any]):
        """
        :param data: Dicionário contendo a saída consolidada dos algoritmos.
        """
        if not isinstance(data, dict):
            raise DataLoaderError("DataLoader exige um dicionário como entrada.")

        self.raw = data
        self.cleaned = {}

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    def validate_presence(self):
        """
        Verifica se todas as chaves esperadas estão presentes no pacote.
        """
        missing = [k for k in self.REQUIRED_FIELDS if k not in self.raw]

        if missing:
            raise DataLoaderError(
                f"Dados incompletos para PDF Engine. Faltando: {missing}"
            )

    # -------------------------------------------------------------------------
    # Normalização
    # -------------------------------------------------------------------------

    def normalize_section(self, name: str, value: Any):
        """
        Normalização individual de cada seção.
        Pode ser estendida de acordo com a necessidade.
        """
        if value is None:
            raise DataLoaderError(f"A seção '{name}' está vazia.")

        # Normalização simples → garantir dicionário
        if not isinstance(value, dict):
            return {"value": value}

        return value

    # -------------------------------------------------------------------------
    # Execução
    # -------------------------------------------------------------------------

    def load(self) -> Dict[str, Any]:
        """
        Carrega, valida e normaliza todos os dados, retornando um pacote único.
        """
        self.validate_presence()

        for section in self.REQUIRED_FIELDS:
            self.cleaned[section] = self.normalize_section(
                section, self.raw.get(section)
            )

        return self.cleaned


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def load_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função auxiliar para carregamento direto,
    permitindo uso simples no pipeline.
    """
    return DataLoader(data).load()
