# Continuação do aceite 9.2 — 05/11/2026

Complementa, sem substituir, plano-9-2-2026-11-05.md e aceite-9-2-2026-11-05.md.
Branch de trabalho task/admin-acceptance-9-2-20261105 criada a partir de develop,
sem commit/push; todas as alterações locais anteriores preservadas.

## Correção do executor

Catalogo: botão muda de Pesquisar para Buscando durante loading, portanto esperar
Pesquisar desabilitado era incorreto. Reports: ausência inicial de loading não
garante conclusão do on_load. tools/admin_browser_sync.py exige resposta da
operação atual, conteúdo semântico esperado, loading encerrado e controle pronto;
capture_ready também rejeita carregamento/salvamento ativo. Destinos do executor
real parametrizados, sem sobrescrever diagnósticos; modo reports-only evita
repetir percursos/sondas remotas já comprovados.

## Bateria nova com dados fictícios

tools/admin_acceptance_browser.py usa páginas/eventos reais e API local com
usuários, obras e reports mutáveis apenas em memória. Não altera dados Xano.
Os 61 testes e oito cenários anteriores foram aproveitados, sem reexecução.

Tentativa 1: produção bloqueada no npm/cache da sandbox antes do navegador.
Tentativa 2 fora da sandbox: **56 cenários automatizados aprovados**, divididos
em oito grupos (quatro por largura, 1440/390). Evidências por cenário:
[scenarios.json](browser-9-2-continuacao-2026-11-05-attempt2/scenarios.json).
Incluem esperado/observado, screenshots e journals de requisições/mutações
fictícias; result.json descreve execução dos grupos. Build: compile 2 s/build 23 s.
Página de Reports completamente carregada é validada com uma linha esperada,
loading ausente e botão Filtrar habilitado antes da captura.

## Defeito encontrado e proposta ANTES da correção funcional

**F1 — feedback de erro encoberto pelos modais.** A captura
catalog-invalid-1440.png mostra erro de ano no fundo escurecido, parcialmente
encoberto pelo editor. Mesmo padrão nas confirmações de conta e de report.
Os testes DOM detectavam texto, mas não sua apresentação útil no diálogo.
Logo passed=true no JSON não encerra o critério visual.

Causa: _admin_feedback renderiza erros somente na seção principal; os diálogos
com aria-modal=true não contêm feedback. Proposta registrada e apresentada ao
usuário antes de editar: reutilizar o feedback dentro dos três diálogos ativos,
suprimindo a cópia atrás deles. Preservar handlers, dados, rascunho e contratos.
Escopo coberto pela tarefa 9.2/estados de erro administrativos desta change.
Documentação Reflex consultada: https://reflex.dev/docs/components/conditional-rendering/.

Critério de regressão: erro dentro do diálogo, legível/não obstruído; campos
preservados; cancelar sem PUT; retry bem-sucedido quando a falha local cessa.
Repetir somente grupos afetados pela correção, sem refazer autenticação/permissões
ou jornadas já comprovadas. A aprovação visual desta primeira bateria é parcial.

## Correção funcional e regressão

Após registrar a proposta, Codeboxd_main/pages/admin.py passou a renderizar o
feedback de erro dentro do diálogo ativo de conta, catálogo ou report. A cópia
de erro no fundo é suprimida enquanto aquele diálogo estiver aberto. Nenhuma
regra de negócio, autorização, contrato ou handler de gravação foi alterado.

Regressão: [44 cenários dos grupos afetados](browser-9-2-dialog-regression-2026-11-05/scenarios.json)
aprovados (22 por largura), sem repetir permissões. As asserções agora exigem
alerta dentro do diálogo e verificam elementFromPoint para rejeitar alerta
encoberto. Inspeção de catalog-invalid-1440, catalog-write-error-390 e
report-required-decision-390 confirma correção e legibilidade. Campos/rascunhos,
cancelamento sem PUT e retry foram preservados. **F1 corrigido localmente.**

21 testes de test_admin.py repetidos justificadamente após alterar o componente:
OK, 0,912 s. Não repetir os 61 como uma nova entrega. Três testes novos de
test_admin_browser_sync.py: OK, 9,309 s; cobrem HTTP 200 anterior à renderização,
resposta antiga e método incorreto. O teste de DOM atrasado usa Edge headless
sem servidor/app ou Xano. Build de regressão: compile 5 s/build 35 s.

## Reports com dados reais — lacuna resolvida

[Resultado](reports-render-real-2026-11-05.json): aprovado em 1440x900 e 390x900;
quatro linhas e total quatro renderizados, loading encerrado e Filtrar disponível.
As duas capturas privadas em .local/reports-render-real-20261105 foram inspecionadas
e mostram a fila carregada, incluindo desktop. Quatro respostas GET 200 pelo
proxy (sessão/Reports nas duas larguras), mais duas requisições de autenticação
registradas separadamente. Zero 429, zero falha injetada, nenhuma mutação.
Build compile 3 s/build 47 s. A contagem checks=0 significa que as sondas de API
antigas foram deliberadamente omitidas; cases contém as duas verificações reais
de renderização. Não tratar HTTP 200 isolado como aceite.

## Limites de modalidade

O usuário autorizou fixtures ou ambientes autorizados; as ações administrativas
desta rodada foram acordadas em fixtures e a etapa Xano em somente leitura.
Testes locais aprovam os comportamentos visíveis na modalidade executada, mas
não são nova evidência de gravação/integridade/permissões no Xano. Os 119 checks
reais de 04/11 e os percursos anteriores são aproveitados com seus limites.
Não houve nova concessão de papel, escrita remota, criação/remoção de contas,
publicação, push, merge ou arquivo.

## Bateria direcionada restante — diagnóstico da primeira tentativa

browser-9-2-remaining-2026-11-05: recuperação de usuários aprovada em ambas
as larguras (quatro cenários). Grupos de catálogo/decisões falharam em 1440/390,
com JSON e capturas preservados. Não contam como aprovação nem como bug funcional:

- O teste usava Ver todas, que chama _open_catalog e limpa resultados para
  reiniciar critérios, mas exigia preservar a lista anterior. Corrigido para
  repetir Pesquisar com os mesmos critérios, exercitando _load_catalog.
- Havia dois reports pendentes; mover o primeiro para análise corretamente
  deixava o segundo na fila. O teste exigia vazio. Corrigido para filtrar tipo
  message antes da transição, isolando o alvo conhecido da fixture.

Essas causas/ajustes foram apresentados antes da repetição; nenhum código
funcional alterado para acomodar expectativas incorretas do teste. Repetir
somente grupos 3/4 em novo destino. O comportamento de recuperação de usuários
e as outras evidências aprovadas são reaproveitados.

Repetição [browser-9-2-remaining-2026-11-05-attempt2](browser-9-2-remaining-2026-11-05-attempt2/scenarios.json):
oito cenários aprovados (catálogo: erro/retry; reports: reviewing/rejected, nas
duas larguras). Com os quatro de recuperação de usuários, completam os 12
restantes. Nenhuma nova correção funcional foi necessária. Build: 4 s/35 s.

## Consolidado por critério

[Matriz completa por cenário](matriz-9-2-2026-11-05.md): **68 cenários distintos
aprovados com APIs fictícias**, com esperado, observado, resultado e captura;
mais dois casos de Reports renderizado com API real. As 44 regressões são
revalidações de parte dos 68. Não somar como novas entregas. Inspeções visuais:
login de membro móvel, suspensão desktop, snapshot móvel, três modais de erro
corrigidos e as duas capturas reais de Reports.

| Critério | Resultado observado | Modalidade |
| --- | --- | --- |
| Reports desktop carregado | Aprovado: quatro linhas, total correto, sem loading | API real atual; também 390px |
| Login/permissões/redirecionamento | Aprovado: visitante, membro, inválidas, admin e sessão existente | Navegador com fixtures; login admin real em janela segura |
| Confirmar/cancelar/diálogos | Aprovado: cancelar sem PUT, confirmar uma vez, suspender/reativar, feedback | Fixtures; F1 corrigido e revalidado |
| Edição/decisões | Aprovado: inválido/rascunho/503/retry, identidade preservada, resolved/reviewing/rejected | Fixtures; sem novas gravações Xano |
| Filtros/paginação/vazios | Aprovado localmente; filtros reports e continuação; usuários/catálogo aproveitam também a bateria anterior | Fixtures e contratos reais históricos |
| Snapshots/responsividade | Aprovado: mensagem sem alvo, script como texto, 1440/390 sem overflow | Fixtures; Reports real inspecionado nas duas larguras |
| Recuperação após falhas | Aprovado: usuários/catálogo/reports 503/retry; dashboard com seção inválida e recuperação | Falhas locais/sintéticas; não se derrubou fonte real |

### Reprovações e problemas

- F1 funcional (erros atrás dos modais): reprovado na inspeção inicial, corrigido
  e aprovado na regressão. Nenhum defeito aberto desse tipo nos casos executados.
- Esperas de catálogo/Reports: corrigidas no executor; três testes novos e
  renderização real comprovada. HTTP 200 isolado não encerra o critério.
- Quatro reprovações de grupos: expectativas de fixture incorretas, preservadas;
  repetição passou após corrigir somente o executor.
- Selo móvel: paginação permaneceu clicável nos cenários testados. Não se
  comprovou bloqueio que justifique alterar CSS nesta rodada.

### Não executados e bloqueios de modalidade

Nenhum teste local ficou bloqueado ao final. Bloqueio npm/sandbox inicial
resolvido com execução autorizada; registros preservados.

Não executados nesta continuação: UI acoplada ao Xano para membro/inválido,
confirmações de conta, edição/criação, decisões e filtros/paginação/snapshots
em toda a jornada. Os comportamentos têm fixtures ou API real histórica como
apoio; são evidências distintas. Também não se induziu falha parcial em fonte
real. Para homologação integrada de alterações, faltam contas/alvos descartáveis
definidos e escopo de escrita/limpeza autorizado; o acordo desta rodada foi
somente leitura remota. Não classificar como falha funcional comprovada nem
declarar execução remota que não ocorreu.

**Recomendação: manter 9.2 aberta, 33/34.** Os sete grupos foram exercitados nas
modalidades permitidas, mas o checklist exige interface completa com dados reais
de desenvolvimento. A aprovação local não encerra esse critério integrado.

## Validação final e preservação

OpenSpec validou gerenciamento-website (aviso preexistente de requisito longo).
git diff --check aprovado. Os três arquivos reflex.lock conferem byte a byte
com .local/admin-9-2-continuation-baseline; package.json mantém SHA-256
60953f76d66b9864a8ccf100dfc3520f6a5d07f7b3759cc52d4fd5747a54c3e0.
Nenhum upgrade Reflex aplicado. Servidores isolados encerrados pelos executores.
Branch de trabalho preservada, sem commit, push, merge, publicação ou arquivo.
