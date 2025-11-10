from typing import Dict

# ----------------------------
# 📄 GERAÇÃO DE RELATÓRIO MI
# ----------------------------

def gerar_relatorio_mi(dados: Dict[str, Dict[str, str]], nome: str = "Usuário") -> str:
    """
    Gera um texto de relatório psicométrico MI a partir dos dados processados pelo diagnostic_engine.
    Entrada esperada:
    {
        "DEPRESSAO": {"nivel": "NORMAL", "score": "6", "texto": "..."},
        "ANSIEDADE": {"nivel": "LEVE", "score": "8", "texto": "..."},
        "ESTRESSE": {"nivel": "MODERADO", "score": "18", "texto": "..."}
    }
    """
    bloco = f"""### 🧠 Relatório MindScan MI — DASS-21\n\n**Nome avaliado:** {nome}\n\n---\n\n"""
    for chave in ["DEPRESSAO", "ANSIEDADE", "ESTRESSE"]:
        dado = dados[chave]
        bloco += f"#### {chave.capitalize()}\n"
        bloco += f"**Score:** {dado['score']}\n\n"
        bloco += f"**Nível:** {dado['nivel']}\n\n"
        bloco += f"{dado['texto']}\n\n---\n\n"
    bloco += "\nEste relatório é gerado automaticamente com base na escala DASS-21 e não substitui avaliação clínica profissional."
    return bloco