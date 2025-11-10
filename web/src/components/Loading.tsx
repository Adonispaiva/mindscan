function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500 border-solid"></div>
      <span className="ml-4 text-lg font-medium text-gray-700">Carregando...</span>
    </div>
  );
}

export default Loading;
