# 🧠 MindScan PDF Engine — Guia Técnico para Desenvolvedores (DEV_GUIDE.md)
Inovexa Software — Documentação técnica oficial  
Versão: 1.0.0  
Última atualização: 2025-11-30

---

# 📘 1. Visão Arquitetural

O **MindScan PDF Engine** é composto por 6 pilares técnicos:

1. **PDFBuilder**  
   Orquestra a geração do HTML final e envia para o renderer.

2. **Renderers**  
   - `WeasyRenderer` → renderização HTML/CSS profissional  
   - `ReportLabRenderer` → fallback de emergência (texto puro)

3. **Templates Premium**  
   HTML e CSS corporativos.

4. **Validação de Dados**  
   `MindScanDataValidator` assegura integridade antes da geração.

5. **CLI (Command Line Interface)**  
   A interface executável do pacote instalado (`mindscan-pdf`).

6. **Telemetria + Logger**  
   - Logs corporativos (mindscan_pdf.log)  
   - Telemetria avançada (performance, seções, tamanho, renderer)  

---

# 🧩 2. Estrutura de Pastas

mindscan/
│
├── backend/
│ └── services/
│ └── pdf/
│ ├── pdf_sections/
│ ├── templates/
│ ├── renderers/
│ ├── validators/
│ └── telemetry/
│
├── mindscan_pdf/ ← pacote instalável
│ ├── init.py
│ └── cli.py
│
├── mindscan_cli/
│ └── mindscan_pdf_cli.py
│
├── tests/
│ ├── test_pdf_engine.py
│ └── test_performance_stress.py
│
├── mindscan_examples/
│ ├── gerar_jsons_modelo.py
│ └── gerar_relatorio_pdf.py
│
├── setup.py
├── setup.cfg
├── pyproject.toml
└── DEV_GUIDE.md


---

# 🧬 3. Fluxo Interno da Geração de PDF



┌────────────┐ ┌──────────────┐ ┌────────────┐
│ CLI │ ---> │ DataValidator│ ---> │ PDFBuilder │
└────────────┘ └──────────────┘ └────────────┘
│
monta HTML final
│
passa HTML
│
┌────────────────┐
│ Renderer │
└────────────────┘
│
gera PDF
│
salva arquivo


O Logger acompanha cada etapa.

---

# 🧱 4. PDFBuilder

Arquivo: `pdf_builder.py`

Funções:

- montar todas as seções (Capa, Identidade, Big Five, etc.)
- concatenar HTML
- chamar o renderer
- integrar logger + telemetria

Chamada:

```python
builder = PDFBuilder(logger=my_logger)
pdf_path = builder.gerar_relatorio(usuario, resultados, mi, renderer)

🎨 5. Renderers
5.1 WeasyRenderer (principal)

Arquivo: renderers/weasy_renderer.py

Responsável por transformar HTML+CSS em PDF final.

Funções:

carregar base.html

aplicar estilo corporativo

processar HTML

renderizar PDF real

5.2 ReportLabRenderer (fallback)

Arquivo: renderers/reportlab_renderer.py

Usado quando:

servidor não possui dependências do WeasyPrint

modo de compatibilidade é necessário

🧪 6. Testes Automatizados

test_pdf_engine.py → funcionalidade geral

test_performance_stress.py → stress & performance

Rodar:

pytest -q


Cobertura:

validações

HTML montado corretamente

pipeline completa simulada

stress test em 200 ciclos

performance média por ciclo

📜 7. Validador

Arquivo: validators/data_validator.py

Funções:

validar identidade

validar Big Five

validar DASS

validar esquemas

validar MI

lançar ValueError em caso de inconsistência

Uso:

validator = MindScanDataValidator()
validator.validar(usuario, resultados, mi)

🔧 8. CLI (mindscan-pdf)

Arquivo: mindscan_pdf/cli.py

Comando:

mindscan-pdf gerar --usuario usuario.json --resultados resultados.json --mi mi.json


Funções internas:

carregar JSONs

validar dados

instanciar builder

instanciar renderer

registrar logs

exportar telemetria

📡 9. Logger e Telemetria
Logger

Arquivo: telemetry/logger.py

Registra:

início da pipeline

renderer utilizado

JSONs carregados

validação OK / erro

finalização do PDF

Telemetria Avançada

Arquivo: telemetry/telemetry_advanced.py

Mede:

tempo por seção

tempo total

tamanho final do PDF

renderer usado

performance geral

Exporta para:

logs/mindscan_telemetry_advanced.jsonl

🔌 10. Integração Telemetria + Builder

Exemplo:

with telemetry.bloco("BigFive"):
    secao_big_five = BigFiveSection().render(ctx)

📦 11. Empacotamento (pip install)
Instalar localmente:
pip install .

Arquivos-chave:

pyproject.toml

setup.py

setup.cfg

EntryPoint:

mindscan-pdf

🧩 12. Convenções de Desenvolvimento
1. Nunca editar templates direto em produção

Crie variações em:

pdf/templates/variantes/

2. PDFBuilder nunca deve conter lógica de cálculo

Somente orquestração.

3. Renderers nunca devem conhecer a estrutura interna das seções.
4. Telemetria deve ser sempre opcional, mas recomendada.
🚀 13. Boas Práticas Internas

Cada seção deve ser isolada e autocontida

Nome de seções = PascalCase + “Section”

Evitar lógica duplicada

Nunca manipular HTML direto no renderer

Garantir que todos os templates contenham {{conteudo}}

Garantir testes de stress sempre verdes

🛡 14. Segurança e Privilégios

Nenhum dado sensível deve ir para logs

Telemetria deve registrar apenas métricas, não documentos

Geração de PDF deve ser sandboxed quando possível

📚 15. Roadmap Técnico Futuro

Renderização distribuída

Relatórios interativos

Exportação para DOCX

Telemetria de cluster

Dashboards internos SynMind

🧠 MindScan PDF Engine

Arquitetura corporativa.
Alta performance.
Padrão Inovexa/SynMind.