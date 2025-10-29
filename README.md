# MindScan Compliance Pack — 2025-10-22
Barreiras técnicas para impedir regressões e forçar planejamento/entrega correta.

## O que valida
- **API e tamanho**: não pode remover exports nem encolher arquivo >20% sem ganho (guard:exports).
- **Caminhos**: arquivos TSX devem estar sob `src/` e existir no workspace (guard:paths).
- **Planejamento**: todo TS/TSX alterado deve estar listado em `docs/work_plan.json` (guard:workplan).
- **Envelope**: corpo do PR deve conter as seções obrigatórias (guard:envelope).

## Instalação
1. Copie esta pasta para a raiz do repositório **MindScan**.
2. Ajuste `mindscan-manifest.json` se necessário.
3. Edite `docs/work_plan.json` (ledger) antes do PR.
4. Faça commit e abra PR — o workflow `MindScan Compliance` bloqueará PRs fora do padrão.
