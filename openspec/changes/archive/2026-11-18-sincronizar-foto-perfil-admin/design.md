## Context

O endpoint autenticado `/admin/me` retorna o `avatar_url` salvo no perfil da sessao administrativa. O estado atual busca os dados na primeira abertura e os mantem em cache enquanto o token nao muda.

## Goals / Non-Goals

**Goals:** atualizar a identidade a cada abertura do menu e refletir alteracoes recentes de foto sem novo login.

**Non-Goals:** mudar como a foto e enviada ou salva no perfil; alterar endpoint, banco Xano ou permissoes.

## Decisions

- Forcar a leitura de `/admin/me` quando o menu fechado for aberto. Isso atualiza nome e foto juntos, reutiliza a validacao de sessao existente e evita estado duplicado.
- Manter a resposta anterior se houver falha temporaria; o fallback existente continua cobrindo contas sem foto.

## Risks / Trade-offs

- Uma requisicao adicional acontece a cada abertura do menu; o endpoint e uma leitura autenticada pequena.
- Falha de rede pode atrasar a atualizacao; os dados anteriores permanecem visiveis e o controle de nova tentativa continua disponivel.

## Migration Plan

Sem migracao de dados ou mudanca remota. Rollback: remover a leitura forcada e retornar ao cache por sessao.
