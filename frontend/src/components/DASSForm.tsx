import React, { useState } from 'react';

const questions = [
  '1. Tenho sentido vontade de chorar.',
  '2. Perdi o interesse por coisas que antes me davam prazer.',
  '3. Me sinto sem esperança em relação ao futuro.',
  '4. Me sinto incomodado facilmente.',
  '5. Tenho dificuldades para relaxar.',
  '6. Me sinto desmotivado com frequência.',
  '7. Sinto medo sem motivo aparente.',
  '8. Me preocupo demais com situações cotidianas.',
  '9. Tenho dificuldades para dormir ou durmo em excesso.',
  '10. Me sinto cansado(a), mesmo sem ter feito esforço.',
  '11. Tenho tido alterações de apetite.',
  '12. Tenho me sentido inútil ou sem valor.',
  '13. Me sinto impaciente ou irritado.',
  '14. Sinto que estou sempre no limite.',
  '15. Tenho dificuldades de concentração.',
  '16. Evito interações sociais com mais frequência que o normal.',
  '17. Tenho dores físicas frequentes sem causa médica identificada.',
  '18. Me sinto sobrecarregado mesmo com tarefas simples.',
  '19. Tenho pensamentos negativos recorrentes.',
  '20. Me preocupo excessivamente com o que os outros pensam.',
  '21. Tenho pensamentos autodepreciativos com frequência.',
];

export default function DASSForm() {
  const [answers, setAnswers] = useState<number[]>(Array(questions.length).fill(0));
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (index: number, value: number) => {
    const updatedAnswers = [...answers];
    updatedAnswers[index] = value;
    setAnswers(updatedAnswers);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    // Aqui você pode enviar os dados para a API futuramente
    console.log('Respostas enviadas:', answers);
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-white dark:bg-gray-800 shadow-lg rounded-2xl">
      <h1 className="text-2xl font-bold mb-6 text-center text-gray-800 dark:text-white">
        Questionário DASS-21
      </h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        {questions.map((question, index) => (
          <div key={index}>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              {question}
            </label>
            <select
              required
              value={answers[index]}
              onChange={(e) => handleChange(index, parseInt(e.target.value))}
              className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
            >
              <option value={0}>0 - Não se aplicou a mim de forma alguma</option>
              <option value={1}>1 - Aplicou-se em algum grau ou por pouco tempo</option>
              <option value={2}>2 - Aplicou-se em grau considerável ou por boa parte do tempo</option>
              <option value={3}>3 - Aplicou-se muito ou na maior parte do tempo</option>
            </select>
          </div>
        ))}
        <div className="text-center">
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-300"
          >
            Enviar Respostas
          </button>
        </div>
        {submitted && (
          <p className="mt-4 text-green-600 dark:text-green-400 text-center">
            Respostas enviadas com sucesso!
          </p>
        )}
      </form>
    </div>
  );
}
