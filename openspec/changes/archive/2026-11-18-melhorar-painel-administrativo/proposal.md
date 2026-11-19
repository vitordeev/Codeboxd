## Why

O painel administrativo existente já mostra indicadores, catálogo e uma fila de reports, mas os indicadores não levam às áreas correspondentes e o cabeçalho não identifica claramente a pessoa administradora conectada. As listas de catálogo carregam 25 obras por página, e o fluxo de reports precisa de uma verificação explícita para que uma denúncia não seja confundida com uma ação de remoção.

## What Changes

- Tornar navegáveis os indicadores de usuários, obras cadastradas e reports pendentes, levando às áreas administrativas existentes; o card de publicações permanece apenas informativo, conforme decisão do usuário.
- Fazer a área de usuários abrir com uma listagem paginada útil mesmo sem termo de busca, para que o indicador de usuários tenha um destino funcional.
- Exibir, no cabeçalho administrativo, um avatar circular que abre nome, usuário e cargo da pessoa administradora autenticada, com fallback quando não houver foto.
- Carregar até 35 registros por página nas abas administrativas de filmes, séries e animes, sem criar conteúdo fictício ou importar obras externas. A aba de livros mantém o comportamento atual.
- Verificar por testes e contrato que enviar ou revisar um report apenas registra a denúncia e sua decisão; não remove, oculta ou edita o comentário, publicação ou obra reportada.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `admin-dashboard`: navegação dos indicadores e identificação da sessão administrativa no cabeçalho.
- `admin-user-management`: listagem inicial paginada quando a área é aberta sem busca.
- `admin-catalog-management`: 35 resultados por página para filmes, séries e animes.

O contrato `content-moderation` já define que o report não remove o conteúdo automaticamente. A change verificará e protegerá esse comportamento existente, sem introduzir remoção automática nem criar uma nova ação de exclusão.

## Impact

Afeta `Codeboxd_main/pages/admin.py`, `Codeboxd_main/state/admin.py`, rotas administrativas e, se os dados atuais não fornecerem foto/nome de exibição de forma leve, um contrato Xano restrito para obter a identidade da pessoa administradora. A leitura de catálogo usa o endpoint existente, que já aceita `per_page` até 100. A validação deverá separar testes locais, navegador e qualquer mudança/publicação Xano; esta proposta não autoriza mutações remotas. Não altera telas públicas, reports fora do painel, Cloudinary, autenticação de membros ou outras áreas administrativas não descritas aqui.
