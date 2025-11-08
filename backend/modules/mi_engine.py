# ===============================================================
#  MÓDULO: MI ENGINE (Mind Intelligence)
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Geração de relatório interpretativo narrativo
# ===============================================================

from datetime import datetime
from typing import Dict

def gerar_relatorio_mi(dados_usuario: Dict) -> str:
    """
    Gera um relatório textual interpretativo humanizado com base
    nos resultados do diagnóstico DASS-21 e quadrante da Bússola.

    Parâmetros:
        dados_usuario: {
            "nome": str,
            "scores": {
                "DEPRESSAO": int,
                "ANSIEDADE": int,
                "ESTRESSE": int
            },
            "quadrante": str
        }

    Retorna:
        Texto narrativo formatado (str)
    """

    nome = dados_usuario.get("nome", "Usuário")
    scores = dados_usuario.get("scores", {})
    quadrante = dados_usuario.get("quadrante", "Indefinido")

    dep = scores.get("DEPRESSAO", 0)
    ans = scores.get("ANSIEDADE", 0)
    est = scores.get("ESTRESSE", 0)

    # Interpretação simplificada dos eixos
    def interpretar(valor):
        if valor <= 9:
            return "nível normal"
        elif valor <= 13:
            return "nível leve"
        elif valor <= 20:
            return "nível moderado"
        elif valor <= 27:
            return "nível severo"
        return "nível extremamente severo"

    interpretacoes = {
        "DEPRESSAO": interpretar(dep),
        "ANSIEDADE": interpretar(ans),
        "ESTRESSE": interpretar(est)
    }

    # Narrativa base
    relatorio = f"""
🧠 RELATÓRIO MIND INTELLIGENCE — SYNMIND MI v2.0
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Usuário: {nome}

---

**1️⃣ EIXOS EMOCIONAIS — DASS-21**
- Depressão: {dep} pontos → {interpretacoes['DEPRESSAO']}
- Ansiedade: {ans} pontos → {interpretacoes['ANSIEDADE']}
- Estresse: {est} pontos → {interpretacoes['ESTRESSE']}

---

**2️⃣ PERFIL DE TALENTO — BÚSSOLA SYNMIND**
Com base na sua combinação emocional e comportamental, o sistema o posiciona no quadrante **{quadrante.upper()}**.

Este quadrante reflete a forma como você lida com desafios, propósito e energia criativa.
"""

    # Quadrantes com mensagens
    if quadrante.lower() == "inspirador":
        relatorio += """
✨ Você é movido por propósito e imaginação. 
Seu papel é inspirar, criar e gerar novas conexões. 
Use sua energia emocional para transformar ideias em realidades, 
mantendo o equilíbrio para não se sobrecarregar emocionalmente.
"""
    elif quadrante.lower() == "especialista":
        relatorio += """
🔬 Seu foco e precisão são suas maiores forças. 
Você traz profundidade técnica e estabilidade emocional às equipes. 
Atenção apenas ao perfeccionismo — lembre-se de respirar entre as entregas.
"""
    elif quadrante.lower() == "promissor":
        relatorio += """
🚀 Você aprende rápido e se adapta com facilidade. 
Seus resultados surgem da experimentação e da coragem de tentar. 
Valorize seu ritmo e procure mentores que te ajudem a manter constância.
"""
    elif quadrante.lower() == "buscador":
        relatorio += """
🌱 Você está em uma fase de construção interna e busca por sentido. 
Acolha esse momento como um período fértil de autoconhecimento. 
Cada passo que dá fortalece sua clareza e direção.
"""
    else:
        relatorio += "\n🔍 Quadrante não identificado. Recomenda-se refazer o diagnóstico.\n"

    # Síntese emocional
    relatorio += f"""
---

**3️⃣ SÍNTESE EMOCIONAL**
De modo geral, {nome.split()[0]}, suas respostas indicam uma presença emocional {interpretacoes['DEPRESSAO']} em depressão, 
{interpretacoes['ANSIEDADE']} em ansiedade e {interpretacoes['ESTRESSE']} em estresse.

Esses índices demonstram que sua mente está em {quadrante.lower() if quadrante else 'fase neutra'}, 
com boa capacidade de autorregulação e clareza sobre suas emoções.

---

**4️⃣ RECOMENDAÇÕES MI**
- Fortaleça hábitos de autocuidado e pausas mentais.
- Reforce relações interpessoais de apoio.
- Pratique reconhecimento de emoções diárias.
- Utilize o MindScan semanalmente para medir evolução.

---

🪶 *Mensagem final da MI:*
> “O autoconhecimento é um processo contínuo.  
> Cada emoção que você entende é um passo rumo à sabedoria interior.”  

Com carinho,  
**MI — Mind Intelligence SynMind**
"""

    return relatorio.strip()
