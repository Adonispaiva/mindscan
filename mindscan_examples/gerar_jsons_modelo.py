# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindscan_examples\gerar_jsons_modelo.py
# Última atualização: 2025-12-11T09:59:27.745995

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_jsons_modelo.py — Gerador de JSONs Modelo do MindScan
-----------------------------------------------------------

Gera automaticamente três arquivos JSON:

- usuario.json
- resultados.json
- mi.json

Esses arquivos são totalmente compatíveis com o CLI:
    mindscan_pdf_cli.py gerar --usuario usuario.json --resultados resultados.json --mi mi.json
"""

import json
from pathlib import Path


# =====================================================================
# Paths
# =====================================================================
ROOT = Path(__file__).resolve().parent
JSON_DIR = ROOT / "jsons_modelo"
JSON_DIR.mkdir(exist_ok=True, parents=True)


# =====================================================================
# Dados Modelo — Usuário
# =====================================================================
usuario_json = {
    "nome": "João Carvalho",
    "idade": 32,
    "genero": "Masculino",
    "cargo": "Analista de Sistemas",
    "senioridade": "Pleno",
    "empresa": "Inovexa Software"
}


# =====================================================================
# Dados Modelo — Resultados dos Algoritmos
# =====================================================================
resultados_json = {
    "big_five": {
        "abertura": 72,
        "conscienciosidade": 66,
        "extroversao": 41,
        "agradabilidade": 58,
        "neuroticismo": 37
    },
    "lideranca": {
        "decisao": "Moderado",
        "influencia": "Alto",
        "gestao_emocional": "Adequado",
        "direcao": "Bom",
        "relacional": "Consistente"
    },
    "ocai": {
        "cla": 58,
        "adhocracia": 65,
        "mercado": 52,
        "hierarquia": 47
    },
    "esquemas": {
        "Autoexigência": "Moderado",
        "Aprovação": "Baixo",
        "Abandono": "Muito baixo"
    },
    "dass": {
        "depressao": "Normal",
        "ansiedade": "Leve",
        "estresse": "Moderado"
    },
    "performance": {
        "2023-S1": 72,
        "2023-S2": 79,
        "2024-S1": 83,
        "2024-S2": 81
    },
    "bussola": {
        "Analítico": "Alto",
        "Criativo": "Moderado",
        "Relacional": "Adequado",
        "Executor": "Forte"
    },
    "anexos": [
        "Pontuação Big Five detalhada",
        "Tabela TEIQue de facetas"
    ]
}


# =====================================================================
# Dados Modelo — MI (Mind Intelligence)
# =====================================================================
mi_json = {
    "resumo_executivo": {
        "texto": "O avaliado demonstra solidez comportamental e potencial estratégico.",
        "destaques": [
            "Clareza analítica em cenários complexos.",
            "Boa estabilidade emocional em tarefas críticas."
        ],
        "alertas": [
            "Refinar consistência em ambientes de alta pressão."
        ]
    },
    "lideranca": {
        "texto": "Apresenta traços de liderança colaborativa com foco em clareza e resolução."
    },
    "cultura": {
        "texto": "Compatibilidade elevada com ambientes flexíveis e orientados à inovação."
    },
    "esquemas": {
        "texto": "Os padrões cognitivo-emocionais apontam segurança estrutural adequada."
    },
    "dass": {
        "texto": "Níveis emocionais estáveis, com pequenos pontos de atenção situacionais."
    },
    "performance": {
        "texto": "Histórico de evolução consistente, especialmente nos últimos ciclos."
    },
    "bussola": {
        "texto": "Direcionamento forte para análise e execução estratégica."
    },
    "recomendacoes": {
        "texto": "Recomendações formuladas para evolução contínua.",
        "lista": [
            "Fortalecer consistência em entregas de alta demanda.",
            "Expandir autonomia decisória.",
            "Potencializar comunicação analítica com stakeholders."
        ]
    },
    "pdi": {
        "texto": "Plano estruturado para manter desenvolvimento constante.",
        "curto_prazo": ["Melhorar priorização semanal de tarefas."],
        "medio_prazo": ["Ampliar repertório de gestão emocional."],
        "longo_prazo": ["Consolidar liderança estratégica."]
    },
    "anexos": {
        "texto": "Informações complementares relevantes ao processo."
    }
}


# =====================================================================
# Escrita dos arquivos
# =====================================================================
def escrever(nome: str, data: dict):
    path = JSON_DIR / nome
    path.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
    print(f"✔ Criado: {path}")


def main():
    print("\n=== Gerador de JSONs Modelo MindScan ===")

    escrever("usuario.json", usuario_json)
    escrever("resultados.json", resultados_json)
    escrever("mi.json", mi_json)

    print("\n✔ Todos os JSONs foram gerados com sucesso!")
    print(f"📂 Pasta: {JSON_DIR}\n")


if __name__ == "__main__":
    main()
