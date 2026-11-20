## Why

As abas de series, animes e livros devem continuar uteis mesmo quando ha poucos registros persistidos. A equipe tambem precisa de uma acao explicita que remova o alvo correto quando uma analise de report justificar a medida.

## What Changes

- Complementar series, animes e livros com resultados reais de provedores somente para consulta, sem rotulos de cadastro nem gravacao no catalogo; a navegacao por categorias permanece na barra lateral, sem abas duplicadas no topo.
- Adicionar, nos reports de publicacao e obra, uma acao moderada que corresponda ao alvo do report (publicacao, obra, comentario ou avaliacao), com confirmacao e justificativa obrigatoria. A remocao deve preservar o report, seu snapshot e a auditoria; reports de mensagem/perfil nao recebem essa acao.
- Remover publicacoes de forma consistente com comentarios, curtidas e limpeza de imagem existente; ocultar obras removidas do catalogo comum preservando referencias de listas e interacoes.
- Manter 35 como limite visual da pagina e apresentar os resultados externos como obras comuns, sem sugerir que foram gravadas no catalogo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `admin-catalog-management`: importacao administrativa explicita de obras reais para series e animes e exclusao logica de obras apos moderacao.
- `content-moderation`: acao explicita e auditada para remover publicacoes/comentarios, ocultar obras e limpar avaliacao reportada.

## Impact

Afeta o painel e estado administrativo, servicos atuais TMDB/Kitsu/Open Library, endpoints Xano locais de moderacao, tabela `media` e leituras publicas do catalogo. O workspace Xano nao esta disponivel para publicacao nesta etapa; mudancas locais nao representam aceite integrado. Nao remover mensagens, perfis ou contas nesta change.
