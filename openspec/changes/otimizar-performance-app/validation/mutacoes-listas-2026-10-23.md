# Mutações de listas — 23/10/2026

## Plano anterior à implementação

Continuação explicitamente solicitada pelo usuário na change de performance.
Incremento da tarefa 6.3: criar/editar/excluir lista chama `load_lists`, que baixa
`/media` integralmente mesmo quando apenas metadados da lista foram alterados.
O cache social é invalidado por gravações; portanto a recarga custa chamadas
reais, inclusive paginação do catálogo. A abertura normal da tela continua
precisando das referências para os seletores existentes.

Intervenção: permitir que somente a atualização após essas mutações preserve
as referências de mídia já carregadas. Manter diretório próprio/público,
reparo das listas padrão e recarga dos itens conforme o fluxo atual. Não usar
atualização otimista para declarar sucesso antes da resposta do backend.

Acrescentar bloqueio de envio em andamento para salvar/remover e guardas de
rota/conta/seleção para resultados tardios. Publicar estado de espera antes da
rede e preservar editor/rascunho em falha. Nenhum contrato remoto ou dado real
será alterado nesta rodada local.

Arquivos previstos: `Codeboxd_main/state/social.py`, controles do editor em
`pages/social.py`, regressões pertinentes, executor de medição local se necessário,
este registro e tasks.md. Verificação: operações sintéticas criar/editar/excluir,
catálogo pequeno/grande, concorrência, falha, troca de conta/seleção, manutenção
dos itens e listas padrão; suíte, compile --dry e browser com fixtures quando
aplicável. Comparar chamadas com a recarga anterior, distinguindo simulação de
validação remota. Risco: referências preservadas enquanto outro cliente altera
o catálogo; retorno normal à tela ainda consulta a origem. Rollback: retirar
somente a opção de preservar mídia e os controles novos, sem alterar dados.

6.3 continua aberta até confirmar também inclusão/remoção de obras e integração
real exigida; não fechar por apenas otimizar metadados de listas.

## Implementação e regressões locais

- `load_lists(refresh_media=False)` é usado somente após salvar/excluir lista;
  a entrada normal continua recarregando mídia. Atualização incremental mantém
  seleção/editor quando falha a consulta do diretório, evitando sucesso falso.
- `list_saving` bloqueia salvamento/exclusão concorrentes e desabilita os
  controles correspondentes; o handler publica espera antes da rede. Respostas
  antigas de outra rota/credencial/seleção não substituem a tela atual.
- Oito testes dirigidos aprovados. Cinco amostras de cada tamanho (5/250 obras)
  compararam o fluxo anterior reconstruído (gravar, recarregar tela, abrir lista)
  ao atual: chamadas lógicas no handler `[6,6,6,6,6]` para `[5,5,5,5,5]`.
  Mediana/pior 6/6 para 5/5. Mock de `_call`, não HTTP físico nem medição de
  latência de rede; não atribuir redução global de tempo a esse resultado.
- Confirmados criação/edição/exclusão, itens e padrões preservados, ausência
  de recarga de `/media`, entrada normal intacta, bloqueio de duplicatas, falha
  sem retry, rascunho/editor preservados e descarte em troca de conta/seleção.
- Teste preexistente de listas personalizadas adaptado para consumir os yields
  do handler, preservando suas asserções; 11 testes desse arquivo passaram.
- Suíte completa: **327 testes aprovados**, 14,370 s.
- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado, 2,418 s.

## Navegador

Primeira tentativa `mutacoes-listas-browser-2026-10-23` falhou sem concluir
cenários. Tentativa com diagnóstico em `mutacoes-listas-browser-diagnostico-2026-10-23`
mostrou criação e edição confirmadas; o teste conferia DELETE enquanto o diálogo
de confirmação ainda ocultava o título da página. Corrigida somente a espera do
teste para exigir a mensagem "Lista removida." antes de conferir chamadas.
Tentativas anteriores preservadas; nenhuma foi contabilizada como aprovada.

`mutacoes-listas-browser-final-2026-10-23`: primeiro cenário aprovado; segundo
falhou por seletor ambíguo da mensagem (ela aparece na página e no modal).
Seletor restringido ao diálogo. Não contabilizar essa tentativa como suíte aprovada.

`mutacoes-listas-browser-verificado-2026-10-23/result.json`: **8/8 aprovados**,
quatro cenários em 1440/390px: criar/editar/excluir; falha de gravação com
rascunho; escrita lenta com controle desabilitado/sem repetição; escrita aceita
seguida de falha na recarga, sem fechar editor ou mostrar sucesso falso.
Nenhuma recarga de catálogo durante as mutações; zero erros JavaScript e
zero overflow. Build de produção isolado concluído (aproximadamente 11 s).
Servidor normal preservado e subprocesso de teste encerrado.

O build reformatou `reflex.lock/package.json`; como o arquivo estava limpo antes
dos testes, seus bytes de HEAD foram restaurados após terminar, sem mudança
de dependências na entrega. Nenhuma chamada remota Xano, login ou mutação real
foi executada nesta rodada. Implementação é local; tarefas amplas 6.3/6.4
permanecem abertas. Contagem **14/37** preservada.

## Disponibilização local prevista

Verificação de socket encontrou portas 3000, 3030 e 3031 sem listener. Para
disponibilizar a implementação ao usuário, iniciar a aplicação normal em
produção local na porta 3030, com rede autorizada e frontend isolado pelo helper
existente `restore_normal_app([], ...)`. Lista vazia de processos impede parar
qualquer servidor anterior; o helper faz preflight de rede antes de iniciar.
Log novo em `.local/normal-performance-20261023.log`. Conferir HTTP e navegação
pública sem autenticação; não considerar isso validação de mutação remota.

Resultado: primeira inicialização atingiu timeout e o log registrou erro de
prerender/build. Nenhum sucesso atribuído a essa tentativa. Repetição com npm
e o frontend já aprovado (`.local/frontends/feed-lists-29552`), encerrando somente
o launcher de 3030 identificado pelo helper, concluiu build de produção em
aproximadamente 17 s. Log: `.local/normal-performance-npm-20261023.log`.
`NORMAL_APP_READY=True`; `/`, `/login` e `/listas` responderam HTTP 200.

`home-normal-apos-listas-2026-10-23.json`: navegador com TMDB real aprovado,
20 cards em cada uma das três seleções de filmes (cinema, bem avaliados e
próximos). Sem login, gravações ou alteração de dados. Aplicação atualizada
disponível em `http://localhost:3030`.

O frontend `.local/frontends/feed-lists-29552` agora pertence ao servidor
normal ativo: **não reutilizar esse diretório em testes paralelos**. Preparar
outro diretório isolado em próximas rodadas. Arquivo de dependências reformatado
automaticamente pelo segundo build restaurado novamente, sem delta de versões.

Fechamento desta rodada: `openspec validate otimizar-performance-app --type change`
e `git diff --check` aprovados; somente avisos de conversão LF/CRLF.
