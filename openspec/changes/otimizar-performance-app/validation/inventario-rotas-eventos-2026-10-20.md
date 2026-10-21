# Inventário completo de fontes — tarefa 1.1 — 20/10/2026

## Escopo autorizado e resultado

Nesta rodada o usuário solicitou escolher e realizar uma tarefa pendente após
a revisão de performance. Selecionada 1.1: completar o inventário estático,
com ferramenta offline, testes e registros OpenSpec. Não altera o produto.
As regras históricas de aprovação por intervenção permanecem para trabalhos
posteriores; esta solicitação cobre o inventário escolhido nesta rodada.

Resultado reproduzível em [JSON](inventario-rotas-eventos-2026-10-20.json):
19 arquivos Python, 21 rotas, 99 vínculos explícitos `on_*` e 279 funções.
Cada arquivo tem hash SHA-256; cada rota registra componente e on_load; cada
função registra nome qualificado, linha, decorators e chamadas com argumentos.
Funções internas têm entradas separadas. Inclui estados, componentes, serviços,
callbacks em argumentos posicionais e funções auxiliares, além dos eventos
decorados. O JSON conserva expressões do código público, não avalia valores
nem lê `.env`, uploads, bases, tokens, cookies ou contas.

## Matriz de cobertura e interpretação

Fonte de rotas: `Codeboxd_main/Codeboxd_main.py`. Os aliases de estado usados
pelas páginas devem ser interpretados conforme os imports de cada arquivo;
AuthState herda SessionState. Setters gerados são controles locais, não novas
requisições por si só. As chamadas de cada função estão discriminadas no JSON.

| Rotas (21 ao todo) | Entrada e subfluxos conferidos | Fronteiras de serviço / custo a medir |
| --- | --- | --- |
| `/login`, `/cadastro` | login/signup → `_authenticate`; visibilidade de senha, validação, lembrar sessão, logout | POST auth/login ou auth/signup; validação auth/me; destino por papel |
| `/redefinir-senha` | request_password_reset, reset_password; duas etapas, confirmação e feedback | GET reset/request-reset-link tem efeito colateral; POST magic-link-login e update_password; envio real de e-mail separado |
| `/admin/login` | guard_admin_login, admin_login, alternância de senha | auth/me, auth/login; autorização administrativa fresca |
| `/` | visit(home), `_home_updates`, coleções, filtros/categoria, busca, continuação, retorno | Xano mídia/comunidade; catalog TMDB/Kitsu/Open Library; cache público e privado alteram volume |
| `/obra/[media_id]`, `/obra` | visit(media/external), detalhes, trailers, disponibilidade, relacionados, críticas; avaliar/editar, status, spoiler, salvar, denúncia, lista | Xano mídia/interações/listas/reports; catálogo externo, tradução DeepL condicional e cache persistente; possíveis páginas extras |
| `/biblioteca` | visit(library), load_library, show_more_library; navegação para ficha | Flag: GET library com cursor por interação e 20 itens; legado: mídia e interações integrais; cooldown e retry manual |
| `/listas` | visit(lists), load_lists; selecionar, criar/editar/excluir, adicionar/remover obra e listas padrão | Mídia, listas públicas/próprias e itens no Xano; `_ensure_default_lists` pode gravar durante leitura; ainda sem paginação na origem |
| `/conta`, `/perfil/[profile_id]` | visit(profile), `_profile_updates`; edição de perfil/banner, seguir/deixar de seguir, denúncia | Sessão e detalhe antes de mídia/perfis; outro perfil pode pedir detalhe próprio para conexões; upload separado |
| `/comunidade` | visit(community), load_community; busca/exibição de pessoas, seguir e denunciar | Dependências de home/referências e perfil próprio; mais resultados pode ser somente recorte local |
| `/feed` | visit(feed), load_feed; compositor, busca/seleção de obra, imagem, criar/editar/excluir, discussão, curtida, comentário, denúncia | Posts/feed, referências e likes; discussão sob demanda; upload multipart; fallback de rota ausente não comprova publicação |
| `/admin` | load_dashboard → `_require_admin`; indicadores/recentes/pendências e atalhos | auth/me e admin/dashboard; erros não equivalem a total zero |
| `/admin/users` | guard_users_page, search_users, change_users_page, detalhes, diálogo de status/motivo, confirmação | admin/users e mutação de status; nova autorização e recarga; conta admin aprovada necessária para medição real |
| `/admin/catalog/movies`, `/admin/catalog/series`, `/admin/catalog/books`, `/admin/catalog/anime` | loaders por tipo, show_all_catalog, search_catalog, change_catalog_page, editor/cancelamento, save_catalog_edit, create_catalog_item | admin/catalog; filtros, páginas, validação fresca e recarga após gravação |
| `/admin/reports` | load_reports, search_reports, change_reports_page, open_report_review, save_report_review, fechar diálogo | admin/reports e atualização de decisão; verificar política de transições e auditoria no remoto |
| `/admin/demo` | admin_demo_page e componentes locais com dados fictícios | Demonstração sintética; não substitui validação de endpoints administrativos |

## Como conferir cobertura

O scanner usa AST, sem importar Reflex ou executar módulos. Percorre todos os
`.py` sob `Codeboxd_main/`, inclusive services, e todas as definições de função.
`routes` permite comparar os 21 registros app.add_page com seus componentes;
`bindings` relaciona cada propriedade on_* ao arquivo, função e handler;
`functions.calls` inclui os callbacks posicionais de helpers como button,
expressões lambda, self.*, request, catalog.* e upload. Seguir esses registros
permite conferir cada subfluxo da matriz até seu transporte. Dispatch por string
em visit, herança e callbacks não são resolvidos automaticamente como grafo.

Transporte social: `_call` → `_request_pages` → services.api.request.
Sessão/admin podem chamar request diretamente. Catálogo e upload têm seus
próprios transportes, todos incluídos no inventário de funções. Paginação,
retries, concorrência, condicionais e caches tornam incorreto contar chamadas
sintáticas como requisições efetivamente disparadas.

## Validação e limites

Comandos executados na `.venv`:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_performance_inventory.py -v
.venv/Scripts/python.exe -B -m tools.performance_inventory --output openspec/changes/otimizar-performance-app/validation/inventario-rotas-eventos-2026-10-20.json
```

Dois testes aprovados: extração sem executar um módulo que lança exceção,
isolamento de funções internas, bindings/callbacks e expressões dinâmicas;
extração determinística e presença das rotas/handlers críticos no repositório.
Inspeção manual das rotas, páginas e estados complementou a extração na matriz.

Camada: análise estática e testes offline da ferramenta. Sem servidor,
compilação Reflex, navegador, acesso remoto, login, dados de teste ou Docker.
Não estabelece latência, quantidade dinâmica de chamadas, quota ou autorização
real. Não encerra 1.2–1.5 nem tarefas de otimização/integração. O inventário
inicial histórico permanece preservado; este registro atualiza sua cobertura.

Rollback: remover apenas ferramenta, testes e os dois novos arquivos de
evidência; desfazer os acréscimos documentais desta rodada e reabrir 1.1.
