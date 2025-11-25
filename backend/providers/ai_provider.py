import os
from pathlib import Path
from typing import Dict, Any, Optional

from openai import OpenAI

class AIProvider:
    """
    AIProvider
    ----------
    Responsável por carregar o prompt institucional da MI (Mind Intelligence),
    injetá-lo no modelo LLM e executar análises que exigem processamento cognitivo
    avançado.

    Este provider NÃO contém o prompt dentro dele, deixando-o totalmente
    desacoplado, limpo e carregado de arquivo externo.
    """

    def __init__(
        self,
        model: str = "gpt-5.1",
        prompt_path: Optional[str] = None,
    ) -> None:
        self.model = model

        # Caminho padrão do prompt institucional da MI
        if prompt_path is None:
            root = Path(__file__).resolve().parents[1]
            prompt_path = root / "prompts" / "prompt_mi_synmind.md"

        self.prompt_path = Path(prompt_path)

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"[AIProvider] Prompt não encontrado em: {self.prompt_path}"
            )

        self.prompt_text = self._load_prompt()

        # Inicialização com OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # ============================================================
    # Carregamento do prompt
    # ============================================================

    def _load_prompt(self) -> str:
        """
        Carrega o prompt institucional MI a partir do arquivo Markdown.
        """
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    # ============================================================
    # Função principal de chamada ao LLM
    # ============================================================

    def run(
        self,
        user_content: str,
        temperature: float = 0.0,
        max_tokens: int = 4096,
        additional_context: Optional[str] = None,
    ) -> str:
        """
        Executa consulta ao modelo LLM aplicando:

        - O prompt MI institucional
        - O conteúdo enviado pelo usuário
        - Contextos extras (opcional)
        """

        messages = [
            {"role": "system", "content": self.prompt_text},
            {"role": "user", "content": user_content},
        ]

        if additional_context:
            messages.append({"role": "user", "content": additional_context})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.choices[0].message.content

    # ============================================================
    # Utilitários inteligentes
    # ============================================================

    def analyze_text(self, text: str) -> str:
        """
        API simplificada para análises MI rápidas.
        """
        query = f"Analise o conteúdo a seguir:\n\n{text}"
        return self.run(query)

    def generate_insights(self, answers: Dict[str, Any]) -> str:
        """
        Gera insights psicométricos complexos com base nas respostas
        estruturadas do usuário.
        """
        query = (
            "Gere insights psicométricos a partir das respostas estruturadas abaixo.\n\n"
            f"{answers}"
        )
        return self.run(query)

    def generate_report_section(
        self,
        section_title: str,
        data: Dict[str, Any]
    ) -> str:
        """
        Gera uma seção específica dos relatórios MindScan.
        """
        query = (
            f"Crie a seção '{section_title}' do relatório MindScan, com base nos dados:\n\n"
            f"{data}"
        )
        return self.run(query)
