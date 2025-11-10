// ===============================================================
//  COMPONENTE: NOT FOUND (404)
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Exibir página de erro padrão em rotas inexistentes
// ===============================================================

import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Home } from "lucide-react";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-indigo-950 text-gray-100 p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <AlertTriangle className="w-16 h-16 text-yellow-400 mb-4" />
      <h1 className="text-3xl font-bold text-indigo-400 mb-2">Página não encontrada</h1>
      <p className="text-gray-400 mb-6 text-center max-w-md">
        A rota que você tentou acessar não existe ou foi movida.
        <br />
        Retorne para a área inicial do MindScan para continuar.
      </p>

      <Button
        onClick={() => navigate("/")}
        className="bg-indigo-600 hover:bg-indigo-700 flex items-center gap-2"
      >
        <Home className="w-4 h-4" /> Voltar para o início
      </Button>

      <footer className="absolute bottom-6 text-xs text-gray-600">
        © {new Date().getFullYear()} Inovexa Software — SynMind
      </footer>
    </motion.div>
  );
}
