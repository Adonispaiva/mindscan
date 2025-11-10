// ===============================================================
//  COMPONENTE: DIAGNOSTIC PAGE (Usuário Final)
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Realizar diagnóstico DASS-21 e enviar dados ao backend
// ===============================================================

import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Brain, Activity, ChevronRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface DassResposta {
  id: number;
  valor: number;
}

export default function DiagnosticPage() {
  const [nome, setNome] = useState("");
  const [respostas, setRespostas] = useState<DassResposta[]>([]);
  const [progresso, setProgresso] = useState(0);
  const [enviando, setEnviando] = useState(false);
  const navigate = useNavigate();

  const totalPerguntas = 21;
  const perguntas = Array.from({ length: totalPerguntas }, (_, i) => i + 1);

  const registrarResposta = (id: number, valor: number) => {
    const novas = respostas.filter((r) => r.id !== id);
    novas.push({ id, valor });
    setRespostas(novas);
    setProgresso((novas.length / totalPerguntas) * 100);
  };

  const enviarDiagnostico = async () => {
    if (respostas.length < totalPerguntas) {
      alert("Responda todas as perguntas antes de continuar.");
      return;
    }

    setEnviando(true);
    try {
      const payload = { nome, respostas };
      const res = await axios.post("/api/diagnostic", payload);
      localStorage.setItem("mindscan_result", JSON.stringify(res.data));
      navigate("/relatorio");
    } catch (err) {
      alert("Erro ao enviar diagnóstico. Tente novamente.");
    } finally {
      setEnviando(false);
    }
  };

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-indigo-950 text-gray-100 flex flex-col items-center p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="max-w-3xl w-full">
        <Card className="bg-slate-900 border-slate-800 shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-3 text-indigo-400">
              <Brain className="w-6 h-6" /> Diagnóstico MindScan — SynMind
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-gray-400 mb-2">Seu nome completo</p>
              <Input
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                placeholder="Digite seu nome"
                className="bg-slate-800 border-slate-700 text-white"
              />
            </div>

            <div className="mt-4 space-y-4">
              {perguntas.map((num) => (
                <div key={num} className="border-b border-slate-800 pb-3">
                  <p className="text-gray-300 mb-2">Pergunta {num}</p>
                  <div className="flex gap-2">
                    {[0, 1, 2, 3].map((val) => (
                      <Button
                        key={val}
                        size="sm"
                        onClick={() => registrarResposta(num, val)}
                        className={`${
                          respostas.find((r) => r.id === num && r.valor === val)
                            ? "bg-indigo-600"
                            : "bg-slate-800 hover:bg-slate-700"
                        }`}
                      >
                        {val}
                      </Button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6">
              <Progress value={progresso} className="bg-slate-800 h-3" />
              <p className="text-sm text-gray-400 mt-2">
                Progresso: {Math.round(progresso)}%
              </p>
            </div>

            <div className="flex justify-end mt-6">
              <Button
                onClick={enviarDiagnostico}
                disabled={enviando}
                className="bg-indigo-600 hover:bg-indigo-700 flex items-center gap-2"
              >
                {enviando ? (
                  <>
                    <Activity className="w-4 h-4 animate-spin" /> Enviando...
                  </>
                ) : (
                  <>
                    Gerar Relatório <ChevronRight className="w-4 h-4" />
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}
