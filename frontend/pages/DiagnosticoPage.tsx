import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function DiagnosticoPage() {
  const [nome, setNome] = useState("");
  const [depressao, setDepressao] = useState("");
  const [ansiedade, setAnsiedade] = useState("");
  const [estresse, setEstresse] = useState("");
  const [relatorio, setRelatorio] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function gerarDiagnostico() {
    setCarregando(true);
    try {
      const response = await fetch("/diagnostic", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome,
          scores: {
            DEPRESSAO: Number(depressao),
            ANSIEDADE: Number(ansiedade),
            ESTRESSE: Number(estresse),
          },
        }),
      });
      const data = await response.json();
      setRelatorio(data.relatorio);
    } catch (error) {
      setRelatorio("Erro ao gerar diagnóstico.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <h2 className="text-2xl font-bold">🧠 Gerar Diagnóstico Psicodiagnóstico</h2>
      <Card>
        <CardContent className="space-y-4 p-4">
          <Input
            placeholder="Nome do usuário"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
          <div className="grid grid-cols-3 gap-2">
            <Input
              placeholder="Depressão"
              value={depressao}
              onChange={(e) => setDepressao(e.target.value)}
            />
            <Input
              placeholder="Ansiedade"
              value={ansiedade}
              onChange={(e) => setAnsiedade(e.target.value)}
            />
            <Input
              placeholder="Estresse"
              value={estresse}
              onChange={(e) => setEstresse(e.target.value)}
            />
          </div>
          <Button onClick={gerarDiagnostico} disabled={carregando}>
            {carregando ? "Processando..." : "Gerar Diagnóstico"}
          </Button>
        </CardContent>
      </Card>
      {relatorio && (
        <Textarea
          className="w-full h-80 whitespace-pre-wrap"
          value={relatorio}
          readOnly
        />
      )}
    </div>
  );
}
