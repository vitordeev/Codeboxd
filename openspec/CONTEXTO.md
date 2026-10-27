# Contexto técnico e funcional — 27/10/2026

Busca administrativa em 27/10: GET /admin/users usa modos separados de ID,
texto e listagem sem termo, includes com escape de curingas e filtros/paginação
preservados. Publicado após autorização, com backup e dry-run posterior sem
delta. 79 checks reais aprovados; tarefa 3.1 concluída, administração **22/34**.
[Evidências e limites](changes/gerenciamento-website/validation/busca-parametros-2026-10-27.md).

Listas: coleção pessoal separada de descoberta pública agrupada por autor; nome permanece à direita do avatar. Backend usa `user_list.default_key` anulável e único para proprietário/tipo padrão, preservando personalizadas homônimas. Cadastro e preparação compartilham função que reaproveita a lista sem sobrescrever suas personalizações. Contratos publicados, 16 chaves legadas atribuídas sem perda de 19 listas/8 vínculos e flag privada habilitada. Validação com 411 testes, 18 checks API e 14 critérios de navegador real concluída, incluindo limpeza descartável. [Conclusão da change, 11/11](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/validation/conclusao.md). Quatro requisitos sincronizados e change arquivada em 26/10/2026; tabelas históricas abaixo preservam seu contexto original.

Atualização de segurança nesta data: [resultado da change arquivada](changes/archive/2026-10-26-proteger-credenciais-expostas/status.md).
TMDB exposto revogado, substituto e recarga validados no navegador; quatro senhas
de teste substituídas, quinta identidade histórica confirmada ausente. A política
de versões da change revogar-sessoes-apos-troca-senha foi publicada em 39 rotas:
tokens legados e anteriores à troca são rejeitados; outra conta é preservada.
Credencial de recuperação só pode alterar senha e é revogada após o uso.
Tarefa 2.3 concluída, 29 checks remotos e 392 testes locais aprovados, navegador
autenticado validado. Tokens legados exigem novo login; logout global não mudou.
Novo check manual antes de commit: `.venv/Scripts/python.exe -B tools/check_staged_secrets.py`.
Ignore inclui .xano/; substitutos privados ficam em .local, sem valores nos relatórios.
As descrições anteriores abaixo preservam contexto e evidências das respectivas rodadas.

As duas changes de segurança foram arquivadas por solicitação do usuário em
26/10/2026, com deltas sincronizados em operational-reliability e user-authentication.
Ferramentas/scripts de implantação dessas entregas possuem destinos datados ou
da change então ativa: adaptar em nova change antes de reutilizar, sem sobrescrever
os relatórios arquivados. O scanner permanente de commits não depende dessas pastas.

| Change funcional ativa | Concluídas | Abertas | Critérios restantes |
| --- | ---: | ---: | --- |
| [gerenciamento-website](changes/gerenciamento-website/tasks.md) | 22/34 | 12 | Autorização completa, mutações, auditoria, catálogo/reports e navegador real |
| [otimizar-performance-app](changes/otimizar-performance-app/tasks.md) | 14/37 | 23 | Metas das demais jornadas, comparações completas, mutações, duas contas e browser real |
| [recuperar-senha-codigo-6-digitos](changes/recuperar-senha-codigo-6-digitos/tasks.md) | 8/10 | 2 | Envio Resend aceito, chegada na caixa e ciclo completo de recuperação |

As contagens vêm dos checklists, não medem o percentual global do produto.
As três changes têm planejamento completo; isso não significa implementação concluída.

Evidências mais recentes:

- [Performance e conexões Xano, 24/10](changes/otimizar-performance-app/validation/conexoes-xano-2026-10-24.md): 374 testes históricos, compile/build e comparação de leituras reais; não comprova a jornada inteira.
- [Leituras de admin e membro, 23/10](changes/otimizar-performance-app/validation/retomada-conclusao-2026-10-23.md): 44 e 70 checks, respectivamente; não substituem testes de mutações e navegador administrativo.
- [Administração, 22/10](changes/gerenciamento-website/validation/retomada-evidencias-2026-10-22.md): 21/34; interface local com fixtures e reports documentados.
- [Recuperação/Resend, 22/10](changes/recuperar-senha-codigo-6-digitos/validation/resend-integracao-2026-10-22.md): integração publicada; destinatário testado rejeitado pelo remetente de testes, sem entrega comprovada.

## Produto e arquitetura

Tradução opcional: `services/translation.py` usa DEEPL_API_KEY somente no servidor
para descrições das fichas Kitsu/Jikan/Open Library, com destino PT-BR, cache
SQLite local em `.local/description-translations.sqlite3` e original em falha.
TMDB permanece pt-BR nativo. [Change concluída e arquivada](changes/archive/2026-10-21-traduzir-descricoes-deepl/tasks.md).

Codeboxd reúne descoberta e registro de experiências com filmes, séries, animes e livros, além de perfis e relações sociais. A aplicação usa Python/Reflex; Xano é responsável por autenticação, persistência e autorização. Os adaptadores de catálogo executam no servidor Python.

| Camada | Arquivos principais | Responsabilidade |
| --- | --- | --- |
| Rotas/configuração | `Codeboxd_main/Codeboxd_main.py`, `rxconfig.py` | Páginas e carregamento de estados |
| Autenticação | `state/session.py`, `state/auth_state.py`, `pages/login.py`, `pages/account.py` | Identidade, sessão, cadastro, login e redefinição de senha |
| Social | `state/social.py`, `pages/social.py` | Descoberta, ficha, biblioteca, perfil, comunidade, feed e listas |
| Administração | `state/admin.py`, `pages/admin.py`, `pages/admin_demo.py` | Dashboard, usuários, catálogo, reports e demonstração sintética |
| Transporte | `services/api.py`, `services/uploads.py` | Requisições JSON e multipart ao Xano |
| Provedores | `services/catalog.py` | Normalização, busca, detalhes e falhas de fontes externas |
| Persistência | `xano/table/`, `xano/api/`, `xano/function/` | Esquema e contratos locais XanoScript |
| Visual | `assets/codeboxd.css`, `assets/default-movie-cover.png`, `Imagens/` | Estilos, capa padrão e referências |
| Verificação | `tests/`, relatórios `validation/` | Testes locais e evidências históricas |

Os caminhos da tabela são relativos à raiz do repositório, dentro de `Codeboxd_main/` quando começam por `state/`, `pages/` ou `services/`.

## Mapa de funcionalidades e contratos

Isolamento da avaliação em 20/10: resposta remota de `/media` não respeita
identity_key nesta instância; cliente seleciona correspondência exata e valida
ID antes de salvar. Formulário remonta por identidade da obra e rejeita envios
de outra ficha. [Correção e limites](validation/avaliacao-identidade-2026-10-20.md).

Avaliações em 20/10: formulário com bloqueio durante envio, confirmação local
e resumo após salvar; edição explícita e repetição idêntica suprimida antes da
rede. [Validação local](validation/avaliacao-envio-unico-2026-10-20.md).

Desempenho em 20/10: resultados da homepage enviados progressivamente, limites
de consulta separados por provedor e cache público de cinco minutos/128 entradas
por processo. [Medições e validação](validation/carregamento-home-2026-10-20.md).

Página principal em 20/10: obras persistidas mantêm destaques de filmes/séries
e categorias disponíveis quando os provedores falham. Configuração TMDB anterior
restaurada posteriormente: cinema, melhores avaliados e próximos filmes validados
com 20 cards por fileira no navegador.
[Validação TMDB](validation/restaurar-tmdb-2026-10-20.md).

Complemento `avaliar-meias-estrelas` (19/10), arquivado em 21/10: controle de nota com metades
clicáveis, escala 0,5–5 e zero sem nota; vírgula/ponto normalizados no servidor.
Visitantes restauram meias estrelas do LocalStorage; contas preservam decimais
no Xano. Trocar nota mantém a crítica em edição. [Evidência](changes/archive/2026-10-21-avaliar-meias-estrelas/validation/implementacao-2026-10-19.md).

| Tópico | Comportamento existente | Contratos/evidências |
| --- | --- | --- |
| Descoberta | Busca global nos quatro tipos; categoria independente; paginação e aviso de falha parcial | `specs/media-discovery/`; testes discovery/search relevance/home catalog |
| Home | Fileiras horizontais empilhadas por categoria; coleções distintas de filmes, séries, cinco de livros e três de animes | `services/catalog.py`, `pages/social.py`; atualização Kitsu de setembro |
| Ficha | Informações por tipo, capa, trailer quando disponível, críticas públicas e relacionados opcionais; streaming TMDB no Brasil | `specs/media-catalog/`, `specs/media-data-integration/`; provedores não garantem todos os campos |
| Visitantes | Descoberta/ficha públicas; nota pessoal somente no armazenamento do navegador | `specs/media-interactions/`; dados não publicados como avaliação de conta |
| Conta/sessão | Cadastro, login, logout; identidade verificada por `/auth/me`; cookie de até 24h ou SessionStorage | `specs/user-authentication/`; `validation/authentication-2026-09-22.md` no arquivo da fundação |
| Perfil | Visualização pública, edição própria, estatísticas e atividades; banner local | `specs/user-profile/`, `specs/data-user-management/` |
| Biblioteca | Status planned/in_progress/completed/dropped; notas 0,5–5; zero sem nota; review e spoiler | `specs/media-interactions/`, `specs/data-media-interactions/` |
| Seguidores | Seguir/deixar de seguir, sem duplicata nem auto-seguimento; feed dos seguidos | `specs/social-connections/`, `specs/data-social-connections/` |
| Feed | Posts com mídia opcional, curtidas, comentários e autoria; imagem multipart e pesquisa de obra adicionadas posteriormente | `specs/social-feed/`, `specs/data-social-content/`; complementos em HISTORICO.md |
| Listas | Listas públicas/privadas, ownership, itens sem duplicata, mesma mídia em listas diferentes | `specs/user-lists/`, `specs/data-user-lists/` |
| Administração | Login dedicado, dashboard, pesquisa de contas, suspensão/reativação, correção/cadastro de obras e reports | Deltas em `changes/gerenciamento-website/specs/`; ainda não consolidados como entrega concluída |

## Fontes e compatibilidade

| Tipo | Provedor atual | Configuração/limites |
| --- | --- | --- |
| Filme/série | TMDB | `TMDB_READ_TOKEN` somente no servidor; campos variam por obra/região |
| Anime | Kitsu | API pública; cache de sucesso de 5 minutos/128 entradas por processo; filtro adulto local |
| Livro | Open Library | API pública; busca por título e edições; críticas textuais podem não existir |
| Catálogo usado | Xano `media` | Persiste obras utilizadas, evitando copiar todo o catálogo externo |

Jikan foi substituída como provedor de consulta em 23/09/2026. Registros `jikan:anime:<id>` continuam válidos: usa-se mapeamento MyAnimeList/Kitsu, sem presumir igualdade de IDs. Avaliações e listas mantêm a identidade interna existente. [Diagnóstico Kitsu](../docs/KITSU.md).

O catálogo legado `titulos`, que inclui games, é preservado e separado de `media`. A unicidade do catálogo social considera fonte, categoria e identificador externo.

O último registro remoto de `/likes` é HTTP 404. O feed usa `/posts/{id}/discussion` sob demanda, sem uma consulta por publicação durante a carga inicial. Não afirmar que a rota foi publicada sem nova evidência.

## Segurança e dados

Recuperação de senha atualizada em 14/10: código de seis dígitos, 15 minutos,
até cinco tentativas, intervalo de 60 segundos para reenvio e uso único sob
transação por conta. Envio pelo Xano integrado ao Resend desde 22/10; token intermediário de cinco
minutos não é salvo como sessão no navegador. Contratos publicados e testes
remotos/browser passaram, mas chegada em caixa real continua pendente na change
`recuperar-senha-codigo-6-digitos` (P.6). UUIDs antigos exigem novo pedido. O serviço nativo falhou; Resend foi publicado, mas rejeitou o destinatário testado com o remetente de testes. Entrega e ciclo real permanecem abertos (8/10).

Rodada 13–14/10/2026: tabela report e nove endpoints administrativos foram
publicados; os quatro GETs rejeitaram visitante/membro, com admin/desativado e
mutações ainda pendentes. POST/PUT de posts também foram publicados com entrada
opcional `file image_upload`, convertida em metadados após autorização; `image`
existente continua compatível. Rascunhos são preservados em falha transitória de
sessão e descartados com limpeza de arquivo ao cancelar. Browser de imagem passou
com limpeza local/remota. Referências em `validation/uploads-and-session-2026-10-13.md`
e `changes/gerenciamento-website/validation/publicacao-admin-2026-10-13.md`.

Autoria/ator vêm de `$auth.id`, não do payload. Endpoints protegem propriedade e acesso; listas privadas são filtradas no backend. Administração exige `admin` ativo em cada operação. Papel `moderator` não concede acesso administrativo automaticamente. Logs e respostas devem excluir credenciais.

Senha é enviada pelo submit, sem variável de senha sincronizada. Indisponibilidade transitória não equivale a token inválido; 401/403 podem limpar a sessão. Nota de visitante não escreve no Xano.

O `.gitignore` estava vazio na revisão inicial. A correção operacional adicionou regras e retirou 441 entradas privadas/geradas do índice, preservando arquivos locais. `.env` e arquivos de contas também estavam no histórico de um commit contido na referência `origin/main`: a limpeza atual não remove esse histórico. A revisão/rotação acompanhada pela P.1 foi concluída na cobertura auditada em proteger-credenciais-expostas e sua dependência de sessões, sem reescrever histórico. Não copiar valores secretos para relatórios. Evidência histórica em `changes/archive/2026-10-21-corrigir-erros-operacionais/validation/` e resultado atual nas duas changes de segurança.

## Ambiente e publicação

Ambiente canônico atual: `.venv`, Python 3.14.6, Reflex 0.9.11.post1, httpx 0.28.1 e python-dotenv 1.2.3. `requirements.txt` fixa dependências diretas; transitivas não têm lock integral. `venv` anterior foi preservada. Setup e comandos em [AMBIENTE.md](AMBIENTE.md). As skills Reflex exigidas pelo AGENTS.md estão em `C:/Users/victo/.codex/skills/`.

Docker/Caddy/Compose estão preparados; build Linux, DNS, HTTPS e publicação não foram comprovados. Docker usa Python 3.12, diferente do ambiente Windows validado. Por decisão do usuário, continuar sem Docker. Os ajustes de volume desta rodada foram revertidos; arquivos históricos de preparação não são a estratégia de execução atual. Hospedagem/domínio permanecem fora do escopo de execução.

Portas citadas em relatórios antigos são registros históricos; não garantem um servidor ativo hoje. Compilar pode limpar `.states`; não restaurar automaticamente pickles rastreados.

## Operação registrada e disponibilidade

A última ativação documentada é 24/10 em localhost:3030, com pools separados para catálogo e Xano. PIDs e diretórios anteriores estão nas evidências e nos snapshots, sem garantia de processo ativo hoje. As leituras admin reais de 23/10 foram aprovadas no cenário limitado da performance; não concluem a change administrativa.
