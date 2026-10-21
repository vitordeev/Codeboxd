# Perfil progressivo — 20/10/2026

## Escopo autorizado

Após proposta de separar perfil de referências, usuário aprovou alteração do
estado, página, testes e registros, com preservação da sessão. Implementação
local; nenhuma alteração/publicação Xano, conta real ou reinício nesta rodada.

## Comportamento

`visit('profile')` publica a identidade, banner, bio e contagens obtidas do
detalhe do perfil antes de consultar mídia e pessoas. A verificação de sessão
permanece. As referências são consultadas em paralelo e cada seção é publicada
ao terminar. Falha em atividades não oculta seguidores, nem o inverso; erro
por seção substitui a mensagem de vazio. Contagens vêm do detalhe, não do
número de referências já carregadas. Ação de seguir aguarda as informações de
relacionamento. Edição do perfil próprio permanece disponível no componente.

Resultados atrasados são descartados se rota ou token mudarem. Tarefas pendentes
são canceladas se o gerador for fechado. A interface recebe atualizações por
yield, conforme [documentação Reflex](https://reflex.dev/docs/events/yield-events/).
`load_profile` mantém compatibilidade para chamadas diretas; a atualização
progressiva é propagada pela entrada de navegação `visit('profile')`.

O número de chamadas de sucesso continua seis. Com 429 no catálogo, agora são
seis em vez de cinco porque o detalhe do perfil é consultado antes da falha.
Esta intervenção remove uma dependência de apresentação, não resolve quota
remota nem reduz tráfego. A fila de eventos e a interatividade enquanto o evento
termina ainda precisam ser conferidas no navegador; não afirmar que apenas
yield garante execução paralela de novos eventos do usuário.

## Evidência local

- 188 testes locais passaram, incluindo cinco do executor atualizado e três
  novos testes de perfil (falhas independentes, dados/contagens e troca de rota).
- `reflex compile --dry` passou; servidor não iniciado/reiniciado.
- A compilação também atualizou arquivos gerados em `reflex.lock/`, que já
  tinham alterações anteriores. Não foram restaurados integralmente, para
  preservar trabalho preexistente; esse delta deve ser revisado antes de commit.
- 25 execuções simuladas, cinco por cenário, armazenadas em
  [perfil-progressivo-2026-10-20.json](perfil-progressivo-2026-10-20.json).
- No cenário de referências com 50 ms de espera, mediana até o primeiro yield
  com perfil foi 16,961 ms e conclusão total 83,767 ms. São tempos de handlers
  sintéticos, sem navegador/rede, não benchmark de produção.
- Com 429 no catálogo, perfil presente nas cinco amostras; erro restrito à
  seção de atividades. Na evidência anterior o detalhe nem era solicitado.
- Histórico anterior permanece em `login-simulado-2026-10-20.*`; novos dados
  não sobrescrevem medições históricas. Executor passou a registrar o marco
  `profile_primary_ms`, inexistente no relatório anterior.

Houve aviso preexistente de parse de `.env` na primeira linha; arquivo privado
não alterado. Nenhuma conta/avaliação foi consultada ou modificada remotamente.

## Limites e próximos passos

Não há linha de base real, meta numérica aprovada ou validação desktop/celular.
As tarefas amplas 2.2/2.4 continuam abertas; esta entrega é um incremento local
do perfil posterior ao login. Próximo passo recomendado é aprovar reinício e
cenário de navegador para verificar os estados com a versão atualizada, antes
de escolher outra intervenção de performance.

Rollback: reverter somente os trechos desta intervenção no estado/página e
executor/testes correspondentes, mantendo cache e trabalho anterior. Não apagar
dados ou restaurar arquivos completos de outras rodadas.
