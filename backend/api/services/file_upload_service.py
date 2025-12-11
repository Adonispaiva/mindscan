# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\file_upload_service.py
# Última atualização: 2025-12-11T09:59:20.761538

import os
from fastapi import UploadFile, HTTPException

class FileUploadService:

    UPLOAD_FOLDER = "uploads"

    @staticmethod
    async def save_file(file: UploadFile, session_id: str):
        try:
            os.makedirs(FileUploadService.UPLOAD_FOLDER, exist_ok=True)
            path = f"{FileUploadService.UPLOAD_FOLDER}/{session_id}_{file.filename}"

            with open(path, "wb") as f:
                f.write(await file.read())

            return path

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
