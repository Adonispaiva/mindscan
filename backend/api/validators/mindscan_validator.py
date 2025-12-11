# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\validators\mindscan_validator.py
# Última atualização: 2025-12-11T09:59:20.777102

from fastapi import HTTPException

class MindScanValidator:

    @staticmethod
    def validate_form(data: dict):
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="form_data inválido")

        if len(data.keys()) == 0:
            raise HTTPException(status_code=400, detail="Nenhuma resposta enviada")

        # Exemplo: impedir respostas fora do range
        for key, value in data.items():
            if isinstance(value, (int, float)) and (value < 0 or value > 100):
                raise HTTPException(
                    status_code=400,
                    detail=f"Valor fora do range permitido: {key}"
                )
