# Documentação Técnica — Integração WhatsApp (Twilio API)

MindScan® — Inovexa Software | SynMind

---

## 1. Visão Geral

A integração WhatsApp permite comunicação direta entre o sistema MindScan® e seus usuários utilizando a Twilio WhatsApp API. O objetivo é oferecer **assistência operacional simples**, envio automatizado de relatórios e mensagens padronizadas, sem interferir no núcleo psicométrico do MindScan.

Esta integração é composta por quatro módulos principais:

1. **whatsapp.py** — Envio real (texto, mídia e relatório)
2. **whatsapp_ai.py** — IA leve (perguntas simples)
3. **whatsapp_utils.py** — Utilidades (sanitização, normalização, fallback)
4. **whatsapp_handler.py** — Orquestração central
5. **whatsapp_router.py** — Ponto público de acesso API

A pasta final:

```
backend/integrations/
    whatsapp.py
    whatsapp_ai.py
    whatsapp_utils.py
    whatsapp_handler.py
    __init__.py
backend/routers/
    whatsapp_router.py
```

---

## 2. Objetivos da Integração

* Enviar mensagens automáticas pós-avaliação.
* Enviar relatórios em PDF via link público.
* Auxiliar usuários com dúvidas simples sobre o MindScan.
* Manter o núcleo psicométrico totalmente isolado.
* Criar um canal operacional seguro e auditável.

---

## 3. Fluxo de Comunicação

### 3.1. Envio de mensagem simples

1. Cliente → endpoint `/whatsapp/send`
2. Router redireciona para `whatsapp.py`
3. Twilio envia a mensagem
4. Retorno com SID de envio

### 3.2. Envio de mídia

1. Cliente → `/whatsapp/send-media`
2. Router → `whatsapp.py`
3. Twilio envia
4. Registro no logger

### 3.3. Envio automático de relatório (PDF)

1. Pipeline gera PDF
2. PDF é hospedado externamente
3. Pipeline aciona `/whatsapp/send-report`
4. Twilio envia o link do PDF

### 3.4. Atendimento básico (FAQ)

1. Cliente → `/whatsapp/faq`
2. Router → `whatsapp.py`
3. Heurística local responde
4. Twilio envia a resposta

### 3.5. IA leve (Operational Concierge)

1. Cliente → `/whatsapp/ai`
2. Router → `whatsapp_ai.py`
3. Texto normalizado
4. IA determina resposta simples
5. Handler envia via Twilio

---

## 4. Limitações (Intencionais)

A IA não:

* interpreta resultados psicométricos
* influencia no diagnóstico
* analisa perfis
* gera insights psicológicos
* substitui o MindScan

A IA leve é **puramente operacional**, protegida para impedir usos indevidos.

---

## 5. Segurança

* Chaves Twilio via variáveis de ambiente.
* Captura de exceções com fallback.
* Sanitização completa do número.
* Logs padronizados.
* Isolamento do núcleo MindScan.

---

## 6. Dependências

* FastAPI
* Twilio Python SDK
* Pydantic

No backend, instalar:

```
pip install twilio
```

---

## 7. Estrutura dos Módulos

### 7.1 whatsapp.py

* Envia mensagens reais via Twilio.
* Envia PDFs (via URL pública).
* Envia imagens e mídias.
* Possui funções: `_send_text`, `_send_media`.

### 7.2 whatsapp_ai.py

* Implementa IA leve por heurística.
* Responde dúvidas comuns.
* Não usa modelos generativos.

### 7.3 whatsapp_utils.py

* Sanitização de números.
* Normalização de texto.
* Formatação.
* Metodologia de fallback.

### 7.4 whatsapp_handler.py

* Orquestra IA + envio.
* Gateway seguro para mensagens.
* Centraliza lógica antes do envio.

### 7.5 whatsapp_router.py

* Endpoints públicos.
* Conecta tudo ao FastAPI.

---

## 8. Endpoints Disponíveis

### POST `/whatsapp/send`

Envia mensagem simples.

### POST `/whatsapp/send-media`

Envia imagens ou arquivos.

### POST `/whatsapp/send-report`

Envia link do relatório PDF.

### POST `/whatsapp/faq`

Responde perguntas simples via tabela fixa.

### POST `/whatsapp/ai`

Envia pergunta à IA leve.

---

## 9. Fluxo de Erros

* Falha Twilio → fallback local
* Falha no número → exceção sanitizada
* Falha no módulo → logger + fallback

---

## 10. Como integrar ao Pipeline MindScan

1. Após geração do PDF, publicar arquivo.
2. Chamar o endpoint `/whatsapp/send-report`.
3. Enviar link público ao usuário.
4. Registrar notificação.

Exemplo:

```
requests.post("/whatsapp/send-report", json={
  "to": "+55XXXXXXXXX",
  "pdf_url": "https://link-do-pdf"
})
```

---

## 11. Conclusão

A integração WhatsApp está concluída, modularizada, escalável e pronta para produção. O pacote respeita todas as diretrizes da Inovexa e mantém o núcleo psicométrico inviolado.

Esta documentação serve como referência oficial para desenvolvedores, auditoria e futuras expansões.
