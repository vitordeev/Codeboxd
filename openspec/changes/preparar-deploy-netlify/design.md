## Context

Consulte a motivação em `proposal.md`. O repositório usa Reflex 0.9.11.post1, e `.env.example` contém nomes de configuração com placeholders. A aplicação depende de Xano e provedores externos. A configuração local continua sem Docker.

## Goals / Non-Goals

**Goals:** produzir ZIP reproduzível a partir de arquivos explicitamente permitidos e instruções que expliquem a publicação do frontend e do backend.

**Non-Goals:** configurar ou publicar conta Netlify, escolher um host backend, cadastrar segredos, migrar dados ou expor a instância Xano de produção. O pacote não deve incluir usuários/posts temporários nem `.local`.

## Decisions

- Usar exportação estática do frontend Reflex e hospedar separadamente o backend Python, pois o frontend estático precisa de uma URL de backend alcançável e o backend precisa aceitar o origin do site. Reflex documenta `REFLEX_API_URL` na exportação e `REFLEX_DEPLOY_URL` no backend.
- Usar `netlify.toml` e build command que falha claramente se `REFLEX_API_URL` não for pública, ao invés de fixar localhost ou gravar uma URL presumida.
- Montar o pacote por allowlist e verificar membros do ZIP após gravar; exclusões amplas baseadas apenas no `.gitignore` são insuficientes como garantia de privacidade.
- Gerar o ZIP em `dist/`, que fica ignorado pelo Git. O deploy real só pode ser conferido depois de configurar URL e variáveis em serviços do usuário.

## Risks / Trade-offs

- [Sem backend público, a exportação estática funcional não pode ser finalizada] → entregar pacote-fonte e instruções; deixar o build falhar com mensagem acionável até `REFLEX_API_URL` estar configurada.
- [Reflex e Netlify podem alterar dependências/ambiente de build] → fixar a versão Reflex existente, deixar versões de ferramentas explícitas e validar via build quando a URL estiver disponível.
- [Dados temporários de demonstração estão no workspace] → excluir `.local`, arquivos de dados e artefatos locais por allowlist, além de inspecionar o ZIP.

## Migration Plan

1. Configurar um backend Reflex com WebSocket e variáveis privadas no host escolhido pelo usuário.
2. Definir o `REFLEX_DEPLOY_URL` do backend como a URL `*.netlify.app` do site e configurar `REFLEX_API_URL` na Netlify com a URL pública do backend.
3. Gerar/exportar o frontend, publicar `dist` do cliente por Netlify e executar jornadas de login, feed e upload.
4. Para rollback, restaurar o deploy anterior na Netlify; backend e dados externos permanecem independentes.

## Open Questions

- Qual será a URL pública do backend Reflex? A configuração e o ZIP-fonte podem ser preparados sem ela, mas o build final do frontend deve permanecer pendente até esse endereço existir.
