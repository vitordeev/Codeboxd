## Context

Ver `proposal.md` e os contratos em `specs/`. O painel já possui rotas `/admin/users`, `/admin/catalog/{movies,series,books,anime}` e `/admin/reports`. Os cards de métricas são artigos sem link. O endpoint administrativo de catálogo aceita `per_page` até 100, mas o estado Reflex solicita 25. A tela de usuários só busca quando há termo, embora o endpoint suporte consulta paginada sem termo.

O cabeçalho usa `AdminState` e `SessionState`. A sessão validada fornece ID, nome de usuário e role; ela não fornece avatar nem nome de exibição. A tabela `profile` possui `display_name` e `avatar_url`. A rota pública de perfil inclui também listas de interações e conexões, portanto é excessiva para preencher somente o cabeçalho.

O contrato atual de reports foi conferido: `POST /reports` valida e registra o report e um snapshot, sem remover seu alvo. `PUT /admin/reports/{id}` altera status, revisor, decisão e horário, e registra evento de auditoria em transação; não executa exclusão do comentário, publicação ou obra. A spec principal `content-moderation` já exige que o conteúdo permaneça intacto ao receber uma denúncia.

## Goals / Non-Goals

**Goals:**

- Conectar indicadores a destinos administrativos existentes e tornar a listagem de usuários funcional sem busca.
- Identificar de forma compacta a pessoa administradora atual, sem expor dados a outras sessões.
- Pedir 35 itens por página nas abas de filmes, séries e animes, usando somente registros persistidos.
- Preservar e provar que denúncia e revisão de status não removem automaticamente o conteúdo reportado.
- Manter mudanças e validações restritas ao painel administrativo e aos contratos necessários.

**Non-Goals:**

- Criar uma seção de gerenciamento de publicações; o card de publicações permanece informativo por decisão do usuário.
- Criar obras fictícias, importar títulos de provedores externos ou garantir 35 itens quando o catálogo persistido tem menos.
- Alterar o tamanho de página de livros, controles de usuários, regras gerais de autenticação, telas públicas, Cloudinary ou outras mudanças de colegas.
- Fazer remoção automática de conteúdo ao receber ou resolver reports.
- Publicar contratos no Xano, alterar registros reais ou fazer aceite remoto sem autorização posterior específica.

## Decisions

1. **Usar destinos existentes para os cards.** Usuários abre `/admin/users`, com primeira página carregada sem termo; obras cadastradas abre a área existente do catálogo em `/admin/catalog/movies`, onde as abas de todos os tipos continuam visíveis; reports pendentes abre `/admin/reports` com o filtro pendente. O indicador de publicações permanece não interativo. Uma nova rota ou módulo de gerenciamento de posts aumentaria o escopo sem decisão do usuário.

2. **Adicionar navegação sem busca à área de usuários.** Reaproveitar o GET `/admin/users` com `search` vazio, mantendo paginação, filtros e autorização de backend. A paginação sem termo precisa deixar de ser bloqueada no estado local. O resultado deve continuar sem campos secretos.

3. **Obter identidade administrativa por resposta mínima e protegida.** Como `/auth/me` não traz avatar/nome de exibição e `/profiles/{user_id}` retorna listas de interações e conexões, adicionar um GET administrativo restrito para os campos de cabeçalho: ID, usuário, nome de exibição, avatar e cargo. O endpoint deve conferir sessão ativa e role `admin`; o cliente usa os campos já verificados da sessão como fallback para nome de usuário/cargo e iniciais quando o perfil não tem foto. Não chamar o endpoint em cada ação: guardar a identidade apenas no estado da sessão atual e invalidá-la ao sair/trocar sessão.

4. **Manter 35 como tamanho de página, não como total artificial.** Solicitar `per_page=35` para `movie`, `series` e `anime`. O endpoint atual já permite esse tamanho sem mudança no contrato de paginação. Se houver menos resultados, exibir os disponíveis; não fazer importação implícita. A aba de livros permanece em 25.

5. **Preservar o contrato seguro de reports.** Não alterar o comportamento de `POST /reports` nem introduzir exclusão em `PUT /admin/reports/{id}`. Adicionar cobertura de regressão local que confira o caminho completo no código/contratos e mantenha explícito que somente uma ação futura, separada, autorizada e auditada poderia remover conteúdo. Essa ação futura está fora desta change.

6. **Manter o diff estreito para facilitar o merge dos colegas.** Concentrar UI e eventos em `pages/admin.py` e `state/admin.py`; modificar `Codeboxd_main.py` somente se a nova leitura exigir registro de evento/rota. Manter estilos sob classes `.admin-*`. Contrato Xano novo, se necessário, fica isolado em seu arquivo de API. Não editar componentes sociais, CSS global fora do escopo admin, Cloudinary nem changes ativas relacionadas a outras frentes.

## Risks / Trade-offs

- **Perfil ausente ou avatar indisponível** → usar iniciais/nome de usuário e cargo da sessão sem bloquear o painel; não considerar URL inválida como foto carregada.
- **Endpoint de identidade não autorizado ou com dados a mais** → testar recusa para visitante/membro, conferir projeção mínima e não confiar em role enviada pelo cliente.
- **Menos de 35 obras persistidas** → mostrar a quantidade real, sem semear/importar dados. A meta é reduzir páginas subutilizadas, não fabricar volume.
- **GET de usuários vazio muda o estado inicial da área** → validar paginação, filtros, falha/429 e resultado vazio, além de preservar o caminho de busca atual.
- **Divergência entre XanoScript local e workspace publicado** → distinguir teste local de leitura integrada; não considerar contrato local como publicação ou aceite remoto.
- **Confundir denúncia com remoção** → manter casos de regressão explícitos e conferir registros/decisões sem excluir alvos.
- **Conflitos no merge de colegas** → revisar `git diff` por arquivo e não formatar/reorganizar módulos inteiros; integrar somente alterações administrativas relacionadas à change.

## Migration Plan

1. Implementar e validar localmente, em lote pequeno, a navegação dos cards/listagem inicial e depois a identidade do cabeçalho e o tamanho do catálogo.
2. Testar cenários autorizados e não autorizados com fixtures locais; compilar o Reflex e registrar por tarefa os resultados.
3. Revisar os contratos Xano e produzir prévia restrita caso o endpoint de identidade seja necessário. Parar antes de qualquer publicação remota até receber aprovação específica.
4. Validar no navegador as rotas existentes, perfil com/sem avatar, listagem/paginação e os três tipos de catálogo; registrar separadamente qualquer limitação de dados reais.
5. Para rollback local, reverter somente os arquivos listados em cada tarefa desta change; preservar demais arquivos modificados da worktree. Para Xano, não publicar nesta fase sem plano de rollback e aprovação próprios.

## Open Questions

Nenhuma decisão de comportamento pendente. A disponibilidade real de 35 ou mais registros por tipo e a aprovação de eventual publicação Xano serão verificações posteriores, não premissas desta proposta.
