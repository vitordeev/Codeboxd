# Proposal

## Why

A navegação apresenta HTTP 429 e esperas que prejudicam o uso do Codeboxd.
É necessário medir e otimizar a jornada inteira, começando pelo login, sem
perder dados, funcionalidades ou verificações de acesso.

## What Changes

- Inventariar todas as telas e ações, medir tempos e requisições e localizar
  gargalos antes de escolher intervenções.
- Reduzir consultas redundantes, cargas integrais desnecessárias e dependências
  que bloqueiam o conteúdo principal; revisar cache, concorrência e paginação.
- Tornar carregamentos, salvamentos e recuperação de falhas previsíveis,
  preservando rascunhos, identidade da obra e isolamento entre contas.
- Investigar a origem do HTTP 429, respeitar Retry-After e evitar tempestades
  de tentativas, sem mascarar erros nem ampliar limites sem diagnóstico.
- Validar login/cadastro/recuperação, descoberta, fichas, avaliações, biblioteca,
  listas, perfis, comunidade, feed e administração em desktop e celular.
- Pedir aprovação antes de cada alteração, inclusive documental, explicando
  arquivos, motivo, efeito esperado, riscos e verificação. A autorização atual
  cobre apenas a criação destes artefatos e sua referência no README.

Estado atual: cache público e carregamento progressivo da home têm evidências
históricas; cache de leituras sociais de 15 segundos tem validação local, mas
não comprova eliminação de 429. Esta change revisará essas decisões sem contar
entregas anteriores como tarefas concluídas.

## Capabilities

### New Capabilities

- `request-lifecycle`: coordenação de consultas, escopo de cache, invalidação,
  limitação de tentativas e tratamento consistente de HTTP 429.
- `page-loading`: carregamento progressivo, navegação coerente, estados de
  espera e critérios mensuráveis de resposta nas jornadas do aplicativo.

### Modified Capabilities

Nenhuma alteração dos contratos funcionais consolidados nesta proposta.
Os novos requisitos transversais complementam autenticação, descoberta,
integração de catálogo e funcionalidades sociais existentes.

## Impact

Áreas candidatas: rotas, estados de sessão/social/admin, transportes JSON/upload,
adaptadores de catálogo, componentes, imagens e CSS, testes e evidências OpenSpec.
Xano e provedores TMDB/Kitsu/Open Library serão avaliados; publicação remota,
alteração de contratos ou dependências exigirá proposta e aprovação específicas.
DeepL e identidades Jikan legadas continuam compatíveis.

Fora do escopo: novas funcionalidades, redesign geral, hospedagem, domínio,
Docker, migração de provedores e aumento de plano como solução presumida.
Execução local com `.venv`; nenhuma mudança de código autorizada nesta rodada.
