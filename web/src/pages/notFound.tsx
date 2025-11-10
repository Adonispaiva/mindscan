function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-blue-600">404</h1>
        <p className="mt-4 text-lg text-gray-700">Página não encontrada.</p>
        <p className="text-sm text-gray-500">Verifique se o endereço está correto.</p>
      </div>
    </div>
  );
}

export default NotFound;
