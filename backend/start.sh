#!/bin/bash

# Ativação do ambiente virtual
source .venv/bin/activate

# Carregamento de variáveis de ambiente
export $(grep -v '^#' .env | xargs)

# Inicialização do servidor
uvicorn main:app --host=0.0.0.0 --port=8000 --reload
