# Continuação para conclusão — 05/11/2026

## Escopo e decisões antes da execução

O usuário pediu concluir o projeto inteiro e delegou a condução técnica nesta
rodada. Usar as três changes ativas, sem Docker, sem hospedagem nova e sem
alterar privilégios de contas. Não substituir critérios por simulações.

Na change de performance, retomar primeiro 1.3/1.4/3.5/4.4/7.1/9.1:
executar o navegador existente com cinco amostras em 1440/390px, conta
descartável criada pelo cadastro normal e proxy que bloqueia mutações.
Preparar/limpar somente os registros próprios pelo journal privado existente.
Preservar os relatórios anteriores. Inicializar frontend isolado; diagnosticar
o prerender se falhar antes da navegação. Nenhum benchmark parcial encerra
as tarefas de comparação de toda a jornada.

A delegação permite decisões rotineiras e execução dos instrumentos. Não
constitui evidência de metas atingidas nem permite inventar uma linha de base
anterior. Metas adicionais serão registradas como decisões técnicas desta
rodada e avaliadas com resultados, sem atribuir aprovação numérica ao usuário.

## Verificações iniciais

- Git limpo; três changes ativas, 26 tarefas abertas.
- `.venv`, Reflex 0.9.11.post1 e Playwright disponíveis.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -q`: **484 testes OK**.
- Acesso de rede exige processo autorizado fora do sandbox; metadata Xano
  respondeu HTTP 200. Não houve publicação nessa verificação.

## Resultados

Execuções e limitações serão acrescentadas após cada verificação.

### Navegação real e diagnóstico de 429 (1.4)

`navegacao-real-2026-11-05.json`: primeira volta desktop completa
(home/busca/ficha/perfil/biblioteca/listas/feed/comunidade), mais
home/busca/ficha da segunda volta; 11 etapas concluídas. Proxy sem pausas
internas, sem mock de respostas, bloqueando gravações exceto login normal.
32 respostas registradas: 30 HTTP 200, uma 404 de `/likes` (fallback previsto)
e uma 429 em GET `/social/media`, chamada Python ao Xano durante o segundo
perfil. `Retry-After: 20`; interrompido o ensaio sem repetir mutações. O contador
de 33 requisições reservadas não é uma contagem de 33 respostas recebidas.

Origem: Xano, não TMDB/Kitsu/Open Library. A [documentação oficial de planos](https://www.xano.com/pricing)
informa limite de 10 chamadas de API/20s no plano gratuito, o mesmo plano
identificado nas recusas históricas de branch/fonte isolada. As chamadas
observadas atravessam os grupos de autenticação e social do mesmo workspace;
não inferir limite exclusivo de `/auth/me` ou somente do navegador. A captura
mede as requisições Python encaminhadas pelo proxy. Não foram executados testes
de carga com múltiplos usuários nem provada independência por IP/conta.

O executor usa recarga completa (`page.goto`) e declara `cache_controlled=false`;
isto reinicializa o estado de navegação e não equivale à navegação pelos links
da SPA nem à comparação cache frio/aquecido. Manter 1.3/3.5/9.1/9.2 abertas.
1.4 pode ser concluída pelo diagnóstico real do serviço, sequência, contexto
e prazo; não representa correção ou eliminação do limite externo.

Instrumentação: a primeira tentativa parou na allowlist antiga, sem enviar a
rota bloqueada. Adicionados somente GET `/media-list-status/<id>` e consulta
pública dos itens; PUT/DELETE continuam recusados, com regressões.

## Executor da jornada com gravações (5.3/6.3/7.3/9.1)

Antes da alteração: adaptar `tools/main_journey_browser.py` para aceitar o mesmo
journal descartável validado pelo executor de leituras. Preencher o formulário
normal de login com esse usuário e executar em navegador sem janela quando
solicitado; preservar login manual. Nunca aceitar credenciais de contas
existentes, promover usuário ou emitir token pelo metadata. Reutilizar as
verificações de persistência e limpeza por marcador do executor. Testes de
validação do journal existentes continuam obrigatórios. A alteração elimina
uma dependência de interação manual; não reduz o critério de aceite.

## Remoção de item de lista — implementação planejada (6.3)

Inspeção encontrou `remove_list_item` sem guarda de envio, sem feedback de
pendência e sem fixar a lista/sessão antes da validação de identidade. A UI
também não desabilitava sua confirmação durante outra mutação de item.
Adicionar guarda `list_item_saving`, publicar pendência antes da rede e
verificar rota/token/proprietário/lista antes da escrita e após respostas.
Validar IDs positivos e propriedade, ignorar resposta antiga e não repetir
DELETE automaticamente. Testar concorrência, troca durante auth/escrita,
erro/cancelamento e preservação dos itens. Não alterar endpoints Xano.
Compilar e aplicar ao servidor somente depois da jornada em andamento.

## Resultados finais desta rodada

`jornada-real-2026-11-05.json`: **34 etapas aprovadas**, 17 em 1440px e 17 em
390px, pela aplicação real com login normal da conta descartável. Avaliação
4,5 → edição 3,5, persistência conferida; biblioteca; criar/editar/remover lista;
adicionar/remover obra; criar/editar/excluir publicação; perfil; logout e recusa
de biblioteca protegida após logout. As 38 consultas de verificação retornaram
HTTP 200. Zero erros JavaScript; comparação de quatro conjuntos confirmou
preservação dos registros anteriores; limpeza do ensaio aprovada.

O executor espera 22s entre etapas para isolar a validação funcional da quota.
Essas pausas estão fora dos tempos registrados. Uma amostra por viewport não
é benchmark de cinco amostras nem prova navegação rápida sem 429. Não conclui
5.4/6.4/7.4/9.1 ou a change inteira.

`remocao-interface-real-2026-11-05.json`: aplicação reiniciada com a correção
de remoção e CSS móvel. Remoção na interface de 390px e ausência do item no
Xano confirmadas; ficha real sem interseção capa/título e sem overflow;
lista descartável removida. Script de reprodução privado:
`.local/project-final-20261105/verify_updated.py`, sem credenciais embutidas.

`.venv/Scripts/python.exe -B -m unittest discover -s tests -q`: **494 testes OK**
em 36,587s. Inclui concorrência/envio único, rascunho em falha e invalidação de
avaliações; sete testes novos de remoção com contexto, cancelamento e sessão
expirada; três testes de sanitização do diagnóstico Resend. Não somar execuções
dirigidas às contagens da suíte. `pip check` e `reflex compile --dry` aprovados.

Build atualizado de produção aprovado em 23s e iniciado em **3030** com
`.venv`, sem Docker. Log privado `app-updated.log`, frontend isolado
`.local/frontends/project-final-20261105`. Nenhuma dependência foi atualizada;
o manifesto de lock reescrito pelo compile foi restaurado aos bytes originais.

Limpeza final por `tools.list_status_browser_fixtures cleanup --private-dir
.local/project-final-20261105`: `fixture_cleanup_complete=true`; contas, perfis,
listas, obra, post e interação descartáveis removidos somente por seus IDs e
proprietários. Journal de usuários/obras vazio. Eventos operacionais normais
de autenticação não foram apagados.

**Tarefas concluídas nesta rodada:** 1.4, 5.3 e 6.3. Estado **17/37**.
5.3 combina persistência real com as regressões de duplicação/falha/cache;
6.3 combina CRUD real nos dois tamanhos, correção de remoção e regressões de
concorrência/rascunho/respostas atrasadas. Nenhum aceite de benchmark foi inferido.

## Critérios ainda abertos

As 20 tarefas restantes exigem comparações e metas das demais jornadas,
cache frio/aquecido, coleções grandes e isolamento entre contas, paginação de
listas, sequências sociais completas (incluindo upload/curtidas/comentários),
administração autenticada e integração final. A sessão admin legítima da rodada
anterior não está disponível neste executor; não emitir token administrativo
via metadata nem promover conta descartável. O limite externo foi diagnosticado,
não removido. Não arquivar a change ou declarar o projeto inteiro concluído.

## Conferência de encerramento desta execução

- Login, recuperação, login administrativo e `/_health` locais responderam
  HTTP 200 após o build atualizado. Isso confirma disponibilidade, não envio
  de e-mail nem autenticação administrativa.
- Journal final: zero contas e zero obras descartáveis restantes.
- `openspec validate --all --strict --json`: **22/22 válidos** (três changes,
  19 specs). As três changes ativas têm 23 tarefas abertas ao todo.
- Scanner heurístico em 30 arquivos novos/modificados: nenhuma ocorrência de
  segredo conhecida ou padrão bloqueado; cobertura limitada a esses arquivos.
- `git diff --check`: aprovado. Sem commit ou push.
- Correção visual arquivada em `2026-11-05-corrigir-capa-sinopse-mobile` após
  sincronização manual de `Readable mobile media details` em `media-catalog`
  e validação da spec. A opção `--skip-specs` no archive evitou uma segunda
  aplicação; `specsUpdated=false` do CLI se refere à operação de arquivo,
  não à sincronização manual anterior.
