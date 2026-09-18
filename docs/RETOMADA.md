# Ponto de retomada — CodeBoxd

## Pedido e escopo

Implementar a rede social prevista nas changes `definir-fundacao-codeboxd` e `criar-modelo-dados-xano`, com Reflex e Xano. O usuário pediu encerrar esta etapa com o trabalho salvo para continuar no dia seguinte. Não interpretar este checkpoint como conclusão das 117 tarefas.

## Aplicado e verificado localmente

- Skills oficiais reflex-docs, setup-python-env e reflex-process-management instaladas em `C:/Users/victo/.codex/skills`.
- Ambiente existente: `venv`, Python 3.14.6, Reflex 0.9.11.post1.
- Designs completos e referências a Streamlit substituídas por Reflex; as duas changes passaram no `openspec validate`.
- Autenticação ativa usa `state/session.py`; `auth_state.py` é um alias de compatibilidade.
- Login por submit (incluindo Enter e validação HTML), sem senha como variável sincronizada de estado. Cookie de 24 horas para lembrar sessão e SessionStorage caso contrário.
- Identidade/papel confirmados por `/auth/me`, acesso ao admin condicionado ao papel e guard de carregamento, tratamento distinto para credenciais e falhas de serviço.
- Rotas conectadas: `/`, `/login`, `/cadastro`, `/conta`, `/admin`. Login redireciona admin para `/admin` e demais usuários para `/conta`.
- CSS personalizado conectado; removido carregamento duplicado de Tailwind por CDN. O plugin TailwindV4 existente continua responsável pelas classes.
- Cadastro tem formulário e validação, mas permanece bloqueado quando `XANO_SOCIAL_URL` está ausente. O endpoint antigo publicado não garante username/perfil. NÃO configurar a variável como se a migração já estivesse publicada.
- `.env.example` documenta configuração; `.gitignore` protege ambientes, segredos e `.local/`.

Validações executadas:

```powershell
python -m reflex compile --dry
python -m unittest discover -s tests -v
openspec validate definir-fundacao-codeboxd
openspec validate criar-modelo-dados-xano
```

Resultado: compilação OK, 12 testes OK, duas changes válidas. Os testes usam respostas simuladas; não validam um login real ou publicação Xano. O módulo `state/social.py` foi importado com sucesso, mas seus fluxos não foram testados nem conectados a páginas.

## Preparado, ainda não finalizado

- `services/api.py`: transporte assíncrono Xano, normalização de URL e erros.
- `services/catalog.py`: busca/detalhes TMDB, Jikan e Open Library; precisa de testes dos adaptadores e `TMDB_READ_TOKEN` para filmes/séries.
- `state/social.py`: rascunho de biblioteca, perfis, seguidores, feed, posts, comentários, curtidas e listas. Ainda precisa de revisão, testes e telas. Não faz parte das rotas ativas.
- `xano/table/`: nove tabelas sociais adicionadas em arquivos XanoScript.
- `xano/api/codeboxd/`: 30 endpoints preparados, canonical proposto `codeboxd`.
- Correções Xano locais: autorização dos writes de titulos, registro de logs sem objetos de usuário, cadastro transacional com perfil, bloqueio de contas desativadas.

## Estado remoto

**Nenhuma alteração foi publicada no Xano.**

- CLI autenticado no perfil default; workspace identificado: Pedro's Workspace, ID 147717.
- Exportação remota sem registros/segredos em `.local/xano-remote/`, incorporada aos arquivos locais para preservar os campos já existentes.
- Remoto tem `titulos`, campos adicionais de user e papel moderator; preservar tudo. Games do legado não devem ser convertidos em séries.
- `xano sandbox get` falhou: sandbox não está disponível no plano Free.
- Dry-run executado: 9 tabelas criadas, 1 grupo criado, 30 endpoints criados e 9 endpoints atualizados. Dry-run é prévia de alterações, NÃO prova de compilação ou execução do XanoScript.
- Não usar truncamento, importação de registros, exclusão de objetos ausentes ou sobrescrever variáveis remotas.

## Próximos passos

1. Ler este documento, `AGENTS.md`, os designs e tasks das duas changes; preservar alterações locais e remotas da equipe.
2. Revisar/validar os XanoScripts antes de publicar: sintaxe, retorno de variáveis em condicionais/transações, unicidade sob concorrência, limites/paginação, validação backend de username/URLs, autorização e privacidade. Rever a recuperação de senha legada e revogação de sessões.
3. Construir páginas sociais que usem `SocialState`, com estados vazios/erro/carregamento, paginação e confirmação para exclusões. Tratar recarregamento das páginas e evitar dados de outro usuário após logout/login.
4. Testar adaptadores externos, falhas parciais, normalização, sessões e ownership com dois usuários. Configurar TMDB somente pelo `.env` local.
5. Comparar novamente o remoto, apresentar a prévia final e aplicar migração revisada no workspace autorizado. Não declarar tarefas remotas concluídas com base somente nos arquivos.
6. Configurar a URL social publicada, liberar cadastro e executar fluxo real de cadastro/login/perfil, interações, feed e listas. Não publicar credenciais ou registrar senhas/tokens em relatórios.
7. Atualizar checkboxes somente conforme a evidência. Arquivar OpenSpec apenas depois da implementação completa.

Os arquivos estão salvos no diretório de trabalho. Não foi criado commit; o projeto já tinha diversos arquivos não rastreados antes desta implementação.

## Checkpoint atualizado — 17/09/2026

### Implementado nesta sessão

- Criadas as páginas sociais Reflex em `Codeboxd_main/pages/social.py`: descoberta, obra, biblioteca, comunidade, perfil, feed e listas.
- Rotas conectadas em `Codeboxd_main/Codeboxd_main.py`.
- Mantido o login visual original em `Codeboxd_main/pages/login.py`; a tela social nova é uma base funcional provisória e deve ser adaptada ao mockup original quando o usuário indicar os demais arquivos visuais.
- `SocialState` agora cobre busca, detalhes, interações, perfis, seguidores, feed, comentários, curtidas, listas, estados de carregamento, paginação local e limpeza de dados ao trocar de usuário/logout.
- Detalhes externos preservam `external_source` e `external_id`; mídias persistidas abrem pelo ID interno após recarregar a página.
- Catálogo ganhou validação rigorosa de URLs HTTPS, identidade externa e detalhes de Open Library; falhas parciais dos provedores são exibidas sem apagar dados locais.
- Adicionado retry para HTTP 429 em `services/api.py`.
- Adicionada paginação backend e agregação de páginas em `SocialState`.
- Adicionado `xano/api/codeboxd/likes_GET.xs` para restaurar curtidas no feed.
- Corrigidos erros encontrados pelo parser XanoScript em loops/condicionais; 68 arquivos agora passam no parser local.
- Adicionadas 27 regressões unitárias em `tests/`, todas passando.
- Adicionados scripts locais de verificação em `.local/` e capturas visuais; não contêm segredos publicados.

### Estado remoto confirmado

- Migração inicial publicada no workspace Xano `147717` (Pedro's Workspace): 9 tabelas, grupo Codeboxd e 30 endpoints; 9 endpoints legados atualizados.
- Paginação publicada depois em 11 endpoints de consulta.
- Teste real contra Xano passou em 10 grupos: cadastro/login de duas contas, duplicidade, privacidade, perfis, mídia, interações independentes, seguidores, feed, autoria, curtidas, comentários, listas e exclusões.
- Contas de teste e tokens ficam somente em `.local/test-accounts.json`; não registrar nem publicar esses valores.
- `.env` local recebeu `XANO_SOCIAL_URL` após a publicação. `TMDB_READ_TOKEN` continua ausente; filmes e séries ficam indisponíveis até o usuário configurá-lo localmente.
- Open Library respondeu; Jikan retornou HTTP 504 temporário e o app trata essa falha corretamente.

### Verificações

- `python -m reflex compile --dry`: OK.
- `python -m unittest discover -s tests -q`: 27 testes OK.
- Parser XanoScript: 68 arquivos, 0 erros.
- Servidor produção local respondeu HTTP 200 em `http://localhost:3001`.
- Smoke test no Edge passou por descoberta, login, perfil, biblioteca, feed, comunidade e listas; houve uma falha conhecida ao testar logout porque `SessionState.logout` usava `external=True`, já corrigida para `is_external=True`. Reexecutar o smoke test amanhã.

### Próximo passo exato

1. Reexecutar `.local/browser_smoke.py` depois da correção do logout.
2. Confirmar no Xano a prévia/publicação de `likes_GET.xs` e do filtro de identidade em `media_GET.xs` (a publicação foi iniciada no fim da sessão e deve ser conferida).
3. Adaptar `pages/social.py` ao mockup visual original que o usuário indicará, preservando os handlers de `SocialState`.
4. Configurar `TMDB_READ_TOKEN` somente no `.env` local e testar filmes/séries.
5. Atualizar checkboxes OpenSpec apenas após essa evidência; não arquivar as changes ainda.

## Checkpoint — 18/09/2026: referências visuais e cadastro

- Referências recebidas em `Imagens/HomePage.png`, `Imagens/MoviePage.png` e `Imagens/image 3.png`.
- Página inicial adaptada ao tema escuro/amarelo, cabeçalho com logo, navegação ativa, busca, filtros por categoria e cards. Banner de boas-vindas usa o mascote fornecido, copiado para `assets/mascot.png`.
- Detalhes de obra com painel de capa/sinopse e avaliação conectada ao handler existente. Não foram inventados trailers, elenco ou comentários ausentes no backend.
- Cadastro com layout responsivo, mascote, rótulos e orientação de username. Mantida integração real com Xano.
- CSS compartilhado em `assets/codeboxd.css`, carregado pelo cabeçalho global.
- Corrigido logout: `is_external=True` abria outra aba; agora usa navegação interna com `replace=True`. Regressão verifica limpeza dos tokens, identidade e dados sociais privados.
- Compilação Reflex aprovada. 28 testes unitários passaram.
- Teste no navegador criou uma conta real pelo cadastro e confirmou login automático e sessão após recarregar. Também verificou confirmação de senha e rejeição de cadastro duplicado pelo Xano.
- Credenciais da conta de teste ficam somente em `.local/signup-test-account.json` (ignorado pelo Git).
- Servidor de produção local em `http://localhost:3001`, log atual `.local/reflex-current.log`. A execução precisa de acesso à rede para alcançar o Xano.
- `TMDB_READ_TOKEN` continua pendente; não declarar busca de filmes/séries validada. Restante do mockup, como trailers e enriquecimento dos detalhes, permanece para as próximas etapas.
- Alterações salvas nos arquivos; nenhum commit criado nesta etapa. Preservado o checkpoint anterior que já estava no staging.
- Após corrigir o logout, smoke tests passaram por login, perfil, biblioteca, feed, comunidade, listas, saída na mesma aba e bloqueio de rota privada após sair. A conta nova também fez logout e novo login com sucesso.
- Navegação da descoberta aos detalhes de uma obra validada no navegador; cadastro e detalhes conferidos em 390 px sem overflow horizontal. Capturas e scripts de verificação ficam em `.local/`.
