// tools/check-envelope.js
const body = process.env.GITHUB_PR_BODY || "";
const req = ["Projeto / Caminho completo:", "Tipo de melhoria:", "Evoluções nesta versão:", "Compatibilidade:", "Validações (7 níveis):", "Impacto previsto:"];
const miss = req.filter(t => !body.includes(t));
if (miss.length){ console.error("❌ Envelope ausente:", miss.join(", ")); process.exit(1); }
console.log("✅ guard:envelope OK");
