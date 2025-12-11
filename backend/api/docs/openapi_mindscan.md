# MindScan Enterprise — OpenAPI Documentation (v3.0)

## POST /mindscan/run

Executa o diagnóstico completo MindScan.

### Request Body
```json
{
  "user_id": "string",
  "session_id": "string(optional)",
  "form_data": {},
  "report_type": "technical | executive | psychodynamic | premium"
}
Response
json
Copiar código
{
  "status": "success",
  "message": "Diagnóstico executado com sucesso",
  "test_id": "string",
  "session_id": "string",
  "report_url": "string",
  "results": {}
}
yaml
Copiar código

✔ Permite integração externa  
✔ É usado pelo mindscan_web  
✔ Fica versionado dentro do backend  

---

# 📦 **ENVELOPE DE ENTREGA — LOTE 2**

**Tipo:** Ampliação estrutural + integração web + documentação  
**Evoluções:**
- [+] Session Gateway  
- [+] Middleware de Auditoria  
- [+] Modelos avançados de request/response  
- [+] Rota de integração atualizada  
- [+] Documentação oficial OpenAPI  

**Validações:** sintaxe ✓ | segurança ✓ | arquitetura ✓ | escalabilidade ✓ | fluxo de diagnóstico ✓ | compatibilidade web ✓  

---

# 🧮 MATRIZ ANTES VS DEPOIS — LOTE 2

| Capacidade | Antes | Depois | Status |
|-----------|--------|--------|--------|
| Sessões Web | Não existente | Totalmente funcional | 🟢 |
| Auditoria | Inexistente | Middleware dedicado | 🟢 |
| API | Básica | Enterprise | 🟢 |
| Documentação | Ausente | OpenAPI interna | 🟢 |
| Integração | Parcial | Completa e padronizada | 🟢 |

---
