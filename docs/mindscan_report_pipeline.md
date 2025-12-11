# MindScan — Report Pipeline (Arquitetura Oficial)
Versão: 1.0  
Autor: Leo Vinci — Diretor de Tecnologia & Produção Inovexa

---

# 1. Visão Geral
O pipeline de relatórios do MindScan é composto por:

1. **Input** (payload da API)
2. **Preparação** (normalização e validação)
3. **Renderer** (Corporate)
4. **Geração HTML**
5. **Geração PDF (WeasyPrint)**
6. **Entrega à API**

---

# 2. Estrutura do Payload
O payload segue o modelo Pydantic definido em `report_schema.py`:

- `test_id`
- `context`
- `summary`
- `sections`

Cada seção contém:
- título
- descrição
- blocos com conteúdo

---

# 3. Render Pipeline
O renderer corporativo executa:

1. `prepare_payload_for_render(payload)`
2. `build_html()`
3. `build_pdf()`
4. retorno dos caminhos dos arquivos

---

# 4. Corporate Renderer
O Corporate Renderer implementa:
- Capa
- Resumo Executivo
- Competências
- Padrões Comportamentais
- Riscos
- Desenvolvimento
- Cultura
- Conclusão Executiva

HTML Premium  
PDF Profissional via WeasyPrint

---

# 5. Service Layer
`report_service.py` coordena:

1. criação de caminhos  
2. invocação do renderer  
3. retorno dos paths  

---

# 6. Controllers & Rotas
A API expõe:

`POST /reports/generate`

---

# 7. Expansão
O pipeline permite:

- novos templates  
- novas narrativas  
- novos renderers  
- integração com inteligência artificial  
- outputs híbridos (B2B/B2C)

---

# FIM
