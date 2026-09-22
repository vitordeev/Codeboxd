# Ponto de retomada — CodeBoxd

## Status atual — 19/09/2026

- Fundação OpenSpec: 79/81 concluídas; permanecem 2 tarefas: busca Jikan ao vivo e validação final da change.
- Xano OpenSpec: 37/37 concluídas após testes remotos reversíveis de posts com/sem mídia opcional e mídia compartilhada entre listas. A interação também foi atualizada, relida após novo login e restaurada; persistência e isolamento entre contas passaram.
- Jikan real: detalhe de `/v4/anime/1/full` passou pelo adaptador e retornou Cowboy Bebop com sinopse; busca do anime segue retornando HTTP 504 após retries. Sem outra chave de API necessária.
- Verificações locais: 39 testes, compilação Reflex, ambas as changes validadas e `git diff --check` aprovados.
- Hospedagem/domínio continuam fora do escopo por orientação do usuário.

Nesta retomada, a lista do Xano foi testada com filme, série, livro e anime. A lista temporária foi removida; Cowboy Bebop permanece como um registro real no catálogo compartilhado. O browser confirmou buscas para filme, série e livro. Busca Jikan ainda devolve HTTP 504, então a busca agora também consulta o catálogo Xano em caso de falha externa: o browser encontrou Cowboy Bebop salvo e exibiu o aviso do provedor. A interface local está no `localhost:3001` e seu backend no `localhost:3002`, ambos respondendo.

## Correção do catálogo local — 18/09/2026

- Causa: o frontend local em `localhost:3001` estava compilado para enviar eventos ao backend `localhost:3002`, mas somente o frontend estava ativo. A interface carregava e não conseguia executar buscas.
- Correção aplicada neste ambiente: backend Reflex em modo produção iniciado em `localhost:3002` com acesso de rede; `/ping` responde HTTP 200. O `.web/env.json` foi alinhado à configuração do bundle (`3002`).
- Smoke real no navegador passou para busca TMDB de filmes/séries, Open Library para livros e detalhe Jikan de `Cowboy Bebop`. Busca Jikan continua indisponível (HTTP 504 vindo do provedor).
- Após reiniciar a máquina/processo, iniciar também o backend no diretório do projeto: `python -m reflex run --env prod --backend-only --backend-port 3002 --backend-host 0.0.0.0`. Ele precisa de saída de rede para consultar os catálogos.

## Atualização — continuidade e contexto OpenSpec — 18/09/2026

- Busca, filtro de filmes e navegação até a ficha agora foram validados juntos no navegador com o TMDB (exemplo: “Interestelar”). Corrigidos o campo controlado sem atualização, o ID externo `"0"` confundido com ID interno, e o filtro `identity_key` ignorado pela versão publicada do `/media`; a aplicação filtra a resposta antiga antes de decidir redirecionar.
- `/likes` continua ausente remotamente (404); fallback por `/posts/{id}/discussion` permanece ativo.
- Nenhuma chave além de `TMDB_READ_TOKEN` é necessária: Jikan e Open Library são públicos. A verificação mais recente do Jikan ficou indisponível; não atribuir isso a falta de chave.
- Contexto e critérios de evidência atualizados nos designs e tarefas de ambas as changes OpenSpec. Fundação: 69/80 verificações concluídas; Xano: 35/37. Permanecem a verificação de credenciais inválidas, validação completa dos provedores Jikan/TMDB/Open Library na busca e nos detalhes, os estados de progresso “em andamento”/“abandonado”, edição da avaliação/review, persistência após troca de sessão, listas compartilhando mídia entre duas listas e validação final completa.
- `python -m reflex compile --dry`, 30 testes unitários e `openspec validate` passaram antes da atualização final de contexto; repetir as validações OpenSpec antes de seguir.
- A publicação por domínio está fora do escopo atual por orientação do usuário. O código de preparação de produção anterior pode ser mantido como scaffolding; não há domínio configurado nem publicação.

## Atualização — referências complementares e preparação de publicação

- Novas referências de `Imagens/` aplicadas à descoberta (destaques e fileiras TMDB), feed com coluna lateral, perfil com capa/estatísticas e listas compactas. O login permaneceu como página; pop-up de login desconsiderado conforme pedido.
- Criação/edição de posts e listas e edição de perfil em diálogos; exclusões continuam com confirmação. Dados e ações usam os handlers Xano existentes.
- Confirmado que `/likes` ainda retorna 404 no Xano publicado. O feed agora usa as curtidas de `/posts/{id}/discussion` como compatibilidade quando essa rota estiver ausente. Outros erros continuam visíveis; nenhuma alteração remota foi publicada.
- Preparados `Dockerfile`, `.dockerignore` com lista de arquivos permitidos, `compose.yaml`, `deploy/Caddyfile`, modelo de ambiente e `docs/PUBLICACAO.md`. Domínio por `APP_DOMAIN`, HTTPS via Caddy e cookie seguro em produção.
- Compilação Reflex e 30 testes passaram. Compose validado sem resolver o arquivo de segredos. Docker Engine indisponível mesmo fora do sandbox: build Linux e emissão de certificado ainda não testados.
- Smoke no navegador confirmou TMDB real até detalhes, login, diálogos de perfil/feed/listas, logout e ausência de erros JavaScript. Capturas ficam em `.local/prepared-*.png`; o script `.local/prepared_smoke.py` verifica desktop e celular.
- Servidor local de produção em `http://localhost:3001`, log `.local/reflex-current.log`. Nenhum domínio configurado e nenhuma publicação realizada, conforme pedido de preparar a aplicação.
- OpenSpec: 4/80 tarefas marcadas na fundação, incluindo início real da aplicação e navegação/exibição de detalhes. As demais continuam exigindo validação específica; não arquivar.

## Atualização — 18/09/2026: TMDB validado

- `TMDB_READ_TOKEN` configurado somente no `.env` local, ignorado pelo Git. A pendência de credencial nos checkpoints abaixo foi resolvida.
- Consultas reais pelos adaptadores do projeto passaram: busca de `Interestelar` (2 resultados) e `Breaking Bad` (4 resultados), detalhes com sinopse/capa e populares (20 filmes e 20 séries).
- A validação exigiu execução com acesso à rede; o sandbox retornou erro de conexão.
- Esta verificação cobre os adaptadores contra a API real; não incluiu teste no navegador nem reinício do servidor.

## Atualizacao — ficha de detalhes com nova referencia — 18/09/2026

- Aplicada a referencia Imagens/Captura de tela 2026-09-18 154800.png a pagina de detalhes, com apresentacao responsiva, metadados por categoria, status rapidos de biblioteca, avaliacao por estrelas, review, criticas publicas e recomendacoes quando os provedores oferecem esses dados.
- Integracoes utilizadas: TMDB para filmes/series (creditos, elenco, criticas e recomendacoes), Jikan para anime e Open Library para livros/recomendacoes por tema. TMDB_READ_TOKEN ja esta configurado localmente; Jikan e Open Library nao exigem chave. Nao e necessaria outra API.
- Verificacao local: python -m reflex compile --dry, 33 testes unitarios, duas validacoes OpenSpec e git diff --check passaram. O smoke visual nao completou: o processo isolado nao conseguiu acessar a API TMDB (erro de fonte indisponivel), entao nao usar isso como evidencia de indisponibilidade da credencial; testes anteriores ja validaram a busca TMDB real.
- OpenSpec: definir-fundacao-codeboxd agora registra 70/81 tarefas (incluindo a ficha visual); criar-modelo-dados-xano permanece em 35/37. Hospedagem/dominio seguem fora do escopo.

## Continuidade — validações atuais — 18/09/2026

- Login com credenciais inválidas foi confirmado no Xano publicado: a API não retorna `authToken`; tarefa 2.7 marcada como concluída.
- O adaptador de anime usa `https://api.jikan.moe/v4/` e mantém `external_source=jikan`, como exige o Xano. A expectativa inválida de fallback para TMDB foi removida.
- Consulta real ao Jikan em 18/09/2026 retornou HTTP 504; o serviço informa que não conseguiu conectar ao MyAnimeList. Busca e detalhe reais de anime não puderam ser concluídos por indisponibilidade do upstream.
- Validação local atual: 38 testes unitários, compilação Reflex, duas validações OpenSpec e `git diff --check` passaram.
- Validações remotas reversíveis adicionais confirmaram: posts com e sem mídia opcional; mesma mídia em listas separadas; status “em andamento”/“abandonado”; atualização de nota e review; persistência após novo login; isolamento entre contas. Os registros alterados foram restaurados e listas/posts temporários removidos.
- Estado das tasks: fundação 77/80 (3 abertas: busca Jikan ao vivo, lista incluindo anime e validação final da change); Xano 37/37. O inventário remoto tem livro, filme e série, sem anime.

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

## Acesso público para visitantes - 19/09/2026

- Visitantes podem descobrir, buscar e abrir páginas de obras sem sessão. Filmes e séries exibem até três trailers/teasers do TMDB quando disponíveis, com embed YouTube sem cookies e fallback de idioma pt-BR para en-US. Jikan/Open Library não fornecem aqui um player equivalente; a página segue acessível.
- Nota de visitante fica em LocalStorage por identidade da obra, sem envio ou persistência no Xano. Conta continua necessária para escrever crítica, salvar status/biblioteca/listas, postar, comentar e seguir. Handlers de abrir publicação e seguir verificam sessão.
- Verificações deste checkpoint: 42 testes unitários, `python -m reflex compile --dry`, duas validações OpenSpec e `git diff --check` passaram. Próximo passo: reiniciar processos locais de produção para atualizar o browser e validar visualmente a navegação pública; confirmar disponibilidade real de trailers para título específico.
- OpenSpec agora contabiliza 82/85 tarefas da fundação e 37/37 do modelo Xano. A validação no navegador permanece aberta (12.4); as duas pendências históricas continuam busca Jikan ao vivo e validação final.

## Revalidação da nova instância - 19/09/2026

- Corrigida a lentidão do feed quando o workspace remoto não expõe `/likes`: a carga não consulta a discussão de cada publicação; estado e alternância de curtidas são resolvidos sob demanda. Falhas temporárias na validação de sessão preservam a navegação autenticada; operações protegidas continuam validadas pelo Xano.
- 48 testes unitários passaram. Smoke no Edge em `http://localhost:3012` passou por home responsiva em desktop/celular, busca e detalhe públicos, login, perfil, biblioteca, feed, comunidade, listas, logout e redirecionamento da biblioteca protegida após logout. Sem erros JavaScript. As rotas autenticadas foram repetidas em sequência, aguardando o carregamento antes da navegação.
- A sondagem de leitura confirmou HTTP 200 em login, `/auth/me`, `/media`, `/profiles`, `/feed` e `/posts`. Muitas requisições consecutivas durante o debug acionaram HTTP 429; a UI exibiu a mensagem recuperável e manteve a sessão.
- O processo antigo que escuta em `3011` não pôde ser localizado/encerrado por esta sessão. A build atual está ativa em `3012` (interface) e `8012` (backend), modo desenvolvimento. Uma tentativa de build de produção nessa porta falhou no pré-render da raiz por timeout; produção ainda precisa de restart/validação em ambiente livre.
- OpenSpec da fundação segue 85/87: busca Jikan ao vivo e validação final continuam pendentes. A change Xano permanece 37/37; não arquivar a fundação até cumprir as pendências.

## Debug e otimização de latência - 19/09/2026

- Gargalos confirmados pelo código: início carregava catálogo/perfis completos e popular movies/series sequencialmente; detalhe consultava Xano mesmo para visitante e carregava metadados opcionais em sequência; fallback de likes no feed fazia uma consulta serial por publicação. Agora a Home carrega somente 20 obras, consultas independentes são concorrentes, o detalhe público dispensa Xano, dados opcionais da ficha são concorrentes e fallback do feed limita a 20 posts/5 chamadas simultâneas.
- Tempo limite de catálogos reduzido de 15s para 8s (conexão 3s); Xano de 20s para 10s (conexão 3s) e Retry-After limitado a 3s. Acesso a parâmetros de rota usa a API atual do Reflex, removendo avisos deprecatados.
- Diagnóstico do log local: sem traceback de aplicação no log disponível; contém avisos de depreciação da versão anterior e tentativa de iniciar outro fullstack quando a porta 3001 já estava ocupada. Frontend e /ping estavam respondendo HTTP 200; processo existente não pôde ser reiniciado a partir deste ambiente Windows, então o browser ainda requer conferência após restart.
- Validação após otimização: 44 testes, `python -m reflex compile --dry`, ambas validações OpenSpec e `git diff --check` passaram.
- OpenSpec após este debug: fundação 83/86; Xano 37/37. Ainda aguardam verificação ao vivo a busca Jikan, o smoke após reiniciar o backend e a validação final da change.
- Também corrigido o estado visual de carregamento: a tela deixava o conteúdo inteiro invisível sempre que qualquer consulta estava pendente; agora mantém a página e mostra somente um indicador de atividade.
- OpenSpec após diagnóstico visual: fundação 84/87, Xano 37/37; seguem pendentes Jikan ao vivo, smoke depois do restart e validação final.
- Smoke browser da versão atualizada na porta 3011 passou: busca Interestelar abre a ficha responsiva; painel de avaliação local aparece, nota persiste em LocalStorage (`tmdb:movie:157336`), três trailers foram renderizados e nenhum erro JavaScript ocorreu. Testes de backend cobrem bloqueio de post/seguir sem sessão.
- OpenSpec após validação browser: fundação 85/87; Xano 37/37. Restam busca Jikan ao vivo e validação final.
