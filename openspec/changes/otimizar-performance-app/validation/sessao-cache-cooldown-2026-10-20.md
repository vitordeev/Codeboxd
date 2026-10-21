# Identidade de navegação, detalhe de perfil e cooldown — 20/10/2026

## Autorização

Usuário aprovou ("bora") a proposta de reutilizar identidade validada por até
15 segundos somente em navegação de leitura, cachear detalhe do perfil e
respeitar cooldown do 429. O limite de até 15 segundos para refletir mudanças
externas de identidade foi apresentado na aprovação. Escopo: estados de sessão/
social, testes, executor simulado usado nos testes e documentação OpenSpec.

## Implementação local

- Sessão guarda hash do token, ID verificado e validade, apenas no backend.
  Presença de cookie ou ID local sem verificação não ativa reutilização.
- Loaders de home, fichas, perfil, listas, biblioteca e feed podem reutilizar
  identidade de membro. Admin e demais papéis não usam essa reutilização.
- Ações protegidas e guards admin continuam chamando validação fresca. Falhas
  transitórias mantêm o fallback social anterior: o endpoint Xano ainda deve
  autorizar a própria gravação; não foi criado cache de autorização de escrita.
- Troca de token descarta identidade anterior, mesmo se a consulta seguinte
  falhar. Logout e 401/403 na validação removem identidade e validade. Resposta
  de validação atrasada de token antigo não altera a identidade atual.
- 429 de `/auth/me` grava prazo por token/sessão. Consultas seguintes durante
  o prazo retornam erro local com segundos restantes, mantendo login e sem
  atingir o endpoint. Depois do prazo, nova consulta é permitida e sucesso
  limpa a mensagem de erro. Não há cooldown global presumido para todo Xano.
- Detalhe `/profiles/<id>` usa cache existente (15 s/32 entradas), com cópias
  profundas, isolamento por token/parâmetros e expiração. Mutações invalidam
  antes e depois; contador de geração evita repovoamento por leitura antiga.
  Respostas 401/403 em dados também descartam a reutilização da identidade.

## Testes e resultados

205 testes locais passaram e `reflex compile --dry` passou. Dez novos testes
cobrem expiração, escrita/admin sem reutilização, conta desativada em consulta
fresca, troca de token após falha, cooldown/retomada sem logout, logout/isolamento,
invalidação de perfil/cópias, resposta de leitura antiga e dados com 403.
Um novo teste integrado cobre cinco visitas rápidas ao perfil.

Executor simulado atualizado: cenário `profile-session-429` expira explicitamente
a validade depois do login, para continuar exercitando nova consulta em falha.
Os testes anteriores de seis chamadas/duas validações passaram a esperar cinco
chamadas/uma validação no sucesso. Histórico de evidências não foi sobrescrito.

[Dados simulados](sessao-cache-cooldown-2026-10-20.json): 25 execuções (cinco por
cenário) mais uma execução de cinco visitas rápidas. Uma visita de sucesso usa
cinco chamadas; cinco visitas dentro da validade também usam cinco chamadas
no total (login, validação, detalhe, mídia e pessoas). Nenhuma rede real nesses
resultados. Isso não comprova eliminação do 429 remoto nem ganho de tempo real.

## Limites e retomada

Não houve nova medição autenticada, reinício ou publicação remota nesta rodada.
Servidor de produção previamente iniciado ainda precisa ser reiniciado para
incorporar o código. Repetição real deve corrigir primeiro a correlação dos
marcos da interface com cada ciclo on_load identificada na medição anterior,
sem sobrescrever a evidência histórica. Solicitar aprovação do escopo de
reinício/executor e nova entrada manual no navegador antes de executar.

Continuam abertas as tarefas amplas de linha de base e validação integrada;
o cooldown implementado é específico de `/auth/me`, não prova tratamento de
todos os limites dos provedores. Aviso preexistente de parse de `.env` permanece,
sem alteração ou exibição do arquivo. Rollback: reverter somente esta intervenção
nos estados e testes, preservando cache anterior, perfil progressivo e dados.
