import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function HistoricoDiagnosticosPage() {
  const [registros, setRegistros] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregar() {
      const response = await fetch("/diagnostic/history");
      const data = await response.json();
      setRegistros(data);
      setCarregando(false);
    }
    carregar();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h2 className="text-2xl font-bold">📚 Histórico de Diagnósticos</h2>
      {carregando ? (
        <p>Carregando...</p>
      ) : registros.length === 0 ? (
        <p>Nenhum diagnóstico encontrado.</p>
      ) : (
        <ScrollArea className="h-[600px] w-full rounded border p-4">
          {registros.map((r, i) => (
            <Card key={i} className="mb-4">
              <CardContent className="space-y-2 p-4">
                <div className="font-semibold">{r.nome}</div>
                <div className="text-sm text-muted-foreground">
                  {new Date(r.data).toLocaleString("pt-BR")}
                </div>
                <div className="text-sm">Depressão: {r.score_depressao}</div>
                <div className="text-sm">Ansiedade: {r.score_ansiedade}</div>
                <div className="text-sm">Estresse: {r.score_estresse}</div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigator.clipboard.writeText(r.relatorio)}
                >
                  Copiar Relatório
                </Button>
              </CardContent>
            </Card>
          ))}
        </ScrollArea>
      )}
    </div>
  );
}
