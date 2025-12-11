import React, { useState } from "react";

export default function App() {
  const [raw, setRaw] = useState("{}");
  const [mode, setMode] = useState("hybrid");
  const [report, setReport] = useState("technical");
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function generateReport() {
    setPdfUrl(null);
    setLoading(true);

    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (err) {
      alert("JSON inválido.");
      setLoading(false);
      return;
    }

    const response = await fetch("/api/mindscan/mi-hybrid", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject_id: "WEB_UI_USER",
        raw_scores: parsed,
        mi_mode: mode,
        report_type: report
      })
    });

    const data = await response.json();
    setLoading(false);

    if (data?.pdf_url) {
      setPdfUrl(data.pdf_url);
    } else {
      alert("Erro: " + JSON.stringify(data));
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>MindScan WebApp</h1>

      <textarea
        style={styles.textarea}
        value={raw}
        onChange={(e) => setRaw(e.target.value)}
      />

      <label style={styles.label}>Modo MI</label>
      <select
        style={styles.select}
        value={mode}
        onChange={(e) => setMode(e.target.value)}
      >
        <option value="hybrid">Híbrido</option>
        <option value="original">Original</option>
        <option value="advanced">Avançado</option>
      </select>

      <label style={styles.label}>Tipo de Relatório</label>
      <select
        style={styles.select}
        value={report}
        onChange={(e) => setReport(e.target.value)}
      >
        <option value="technical">Técnico</option>
        <option value="executive">Executivo</option>
        <option value="psychodynamic">Psicodinâmico</option>
        <option value="premium">Premium</option>
      </select>

      <button style={styles.button} onClick={generateReport} disabled={loading}>
        {loading ? "Gerando..." : "Gerar Relatório"}
      </button>

      {pdfUrl && (
        <div style={styles.result}>
          <a href={pdfUrl} target="_blank">Abrir PDF</a>
        </div>
      )}
    </div>
  );
}

const styles: any = {
  container: {
    maxWidth: "600px",
    margin: "40px auto",
    padding: "20px",
    borderRadius: "12px",
    background: "#ffffff",
    boxShadow: "0 4px 18px rgba(0,0,0,0.1)"
  },
  title: {
    marginBottom: "20px",
    textAlign: "center"
  },
  textarea: {
    width: "100%",
    height: "160px",
    marginBottom: "20px",
    padding: "10px"
  },
  label: {
    marginTop: "10px",
    display: "block"
  },
  select: {
    width: "100%",
    padding: "8px",
    marginBottom: "15px"
  },
  button: {
    width: "100%",
    padding: "12px",
    background: "#000",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer"
  },
  result: {
    marginTop: "20px",
    background: "#f0f0f0",
    padding: "15px",
    borderRadius: "8px"
  }
};
