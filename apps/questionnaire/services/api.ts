type Territory = "REALIZADOR" | "INOVADOR" | "INSPIRADOR" | "ESTRATEGISTA";

interface QuizResponse {
  territory: Territory;
}

export async function submitQuiz(performance: number[], matcher: number[]): Promise<Territory> {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/quiz/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ performance, matcher })
    });

    if (!response.ok) {
      throw new Error(`Erro ${response.status}: ${response.statusText}`);
    }

    const data = (await response.json()) as QuizResponse;

    if (!data.territory) {
      throw new Error("Resposta da API inválida.");
    }

    return data.territory;
  } catch (err) {
    console.error("Erro no submitQuiz:", err);
    throw new Error("Não foi possível enviar o questionário. Tente novamente.");
  }
}




