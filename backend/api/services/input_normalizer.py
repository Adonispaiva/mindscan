# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\input_normalizer.py
# Última atualização: 2025-12-11T09:59:20.761538

class InputNormalizer:

    @staticmethod
    def normalize(payload: dict) -> dict:
        """
        Padroniza a entrada antes de ser enviada para o motor MindScan.
        Aqui podemos tratar:
        - conversão de tipos
        - limpeza de campos vazios
        - padronização de chaves
        - migração de versões antigas de formulários
        """
        # Exemplo básico: remove campos nulos
        return {k: v for k, v in payload.items() if v is not None}
