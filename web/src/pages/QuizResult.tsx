import { useLocation } from "react-router-dom";

function QuizResult() {
  const location = useLocation();
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="p-4 text-red-600 font-semibold">
        Resultado não disponível. Volte e preencha o formulário primeiro.
      </div>
    );
  }

  return (
    <div className="p-6 bg-white rounded shadow-md max-w-2xl mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4 text-center">Resultado do Quiz</h2>
      <pre className="bg-gray-100 text-sm text-gray-800 p-4 rounded overflow-x-auto">
        {JSON.stringify(result, null, 2)}
      </pre>
    </div>
  );
}

export default QuizResult;
