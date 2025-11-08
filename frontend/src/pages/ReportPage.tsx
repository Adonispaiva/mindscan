// ===============================================================
//  COMPONENTE: REPORT PAGE (Usuário Final)
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Exibir relatório personalizado gerado pela MI
// ===============================================================

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, Brain, FileText, RefreshCcw } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function ReportPage() {
  const [report, setReport] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem("mindscan_result");
    if (stored) {
      setReport(JSON.parse(stored));
    } else {
      navigate("/diagnostico");
    }
  }, [navigate]);

  const baixarRelatorio = () => {
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `relatorio_mindscan_${report?.nome || "usuario"}.json`;
    link.click();
  };

  if (!report)
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-400">
        <p>Carregando relatório...</p>
      </div>
    );

  const { nome, resultados, analise, quadrante, data } = report;

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-indigo-950 text-gray-100 p-6 flex justify-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="max-w-4xl w-full">
        <Card className="bg-slate-900 border-slate-800 shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-3 text-indigo-400">
              <Brain className="w-6 h-6" /> Relatório MindScan — Resultados Individuais
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-6">
            <section className="border-b border-slate-800 pb-4">
              <h2 className="text-xl font-semibold text-indigo-300 mb-1">{nome}</h2>
              <p className="text-sm text-gray-400">
                Data do diagnóstico: {data ? new Date(data).toLocaleString() : new Date().toLocaleString()}
              </p>
              <p className="mt-2 text-gray-300">
                Quadrante emocional predominante:{" "}
                <span className="font-semibold text-indigo-400">{quadrante || "N/A"}</span>
              </p>
            </section>

            <section>
              <h3 className="text-lg font-semibold mb-2 text-indigo-300">Resultados DASS-21</h3>
              <ul className="space-y-1 text-sm text-gray-300">
                {Object.entries(resultados || {}).map(([categoria, valor]) => (
                  <li key={categoria}>
                    {categoria}: <span className="text-indigo-400 font-semibold">{valor}</span>
                  </li>
                ))}
              </ul>
            </section>

            <section className="border-t border-slate-800 pt-4">
              <h3 className="text-lg font-semibold mb-2 text-indigo-300">Análise da MI</h3>
              <p className="whitespace-pre-wrap text-gray-200 text-justify leading-relaxed">
                {analise || "Aguardando processamento da MI..."}
              </p>
            </section>

            <div className="flex justify-end gap-3 mt-6">
              <Button
                onClick={baixarRelatorio}
                className="bg-indigo-600 hover:bg-indigo-700 flex items-center gap-2"
              >
                <Download className="w-4 h-4" /> Baixar
              </Button>
              <Button
                onClick={() => navigate("/diagnostico")}
                className="bg-slate-800 hover:bg-slate-700 flex items-center gap-2"
              >
                <RefreshCcw className="w-4 h-4" /> Novo Diagnóstico
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}
