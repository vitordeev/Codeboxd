# Biblioteca paginada no navegador — 20/10/2026

## Escopo aprovado

Usuário: “pode prosseguir vamos finalizar isso”, em resposta ao pedido para
validar no navegador com dados fictícios em desktop e celular. Autorização
cobre ferramenta local, servidor de teste em produção, restauração do app
normal e este registro. Publicação/ativação no Xano permanece uma etapa separada.

Skill aplicada: `reflex-process-management`; change `otimizar-performance-app`.
Ferramenta: `tools/library_pagination_browser_validation.py`. Python da `.venv`,
Reflex em produção, Edge headless, viewports 1440×900 e 390×900.
App de teste em 3031 e fixture HTTP em 3040; dados somente em memória.
Flag `LIBRARY_PAGINATION_ENABLED=true` apenas no processo de teste.
Navegador bloqueia requisições para hosts externos. Endpoints Xano substituídos
por URLs loopback no processo de teste; sem credenciais ou dados reais.

## Cenários e critério

Nove casos por viewport: vazio, cinco itens, exatamente 20, 250 itens,
primeira página lenta, próxima página lenta, erro inicial, erro na próxima
página e HTTP 429 na próxima página.

Verifica cards esperados, nota decimal, link da obra, continuação por cursor,
uma leitura de dados por lote, nenhum `/media`, `/interactions` ou `/profiles`,
fim da continuação, feedback de carregamento e botão desabilitado, cards
preservados na falha, recuperação manual, ausência de vazio falso e cooldown.
Na coleção grande percorre todos os 250 itens e verifica identidade por card.
Em 429 a fixture usa Retry-After de quatro segundos para conferir recuperação
após o prazo sem prolongar desnecessariamente a rodada; o teste unitário
também verifica o prazo de 20 segundos relatado pelo usuário.

Primeira tentativa: três casos desktop passaram. A asserção de identidade
da coleção grande contou separadamente os links de capa e título do mesmo
card. Corrigido somente o seletor da ferramenta para extrair um ID por card;
nenhum código de produto alterado nesta rodada. Evidência anterior preservada
em `biblioteca-paginada-browser-primeira-tentativa-2026-10-20.json`.

## Resultado final

18/18 cenários aprovados, nove em cada largura, sem erros JavaScript nem
overflow horizontal. Capturas de biblioteca pequena em 1440 e 390px também
inspecionadas visualmente. Compilação e build de produção concluídos;
`openspec validate otimizar-performance-app --strict` e `git diff --check`
aprovados. Não houve alteração de produto depois dos 229 testes unitários
aprovados na rodada anterior; somente ferramenta de browser e documentação.

| Cenário, em ambas as larguras | Resultado |
| --- | --- |
| Vazio / 5 itens / 20 exatos | Uma leitura de biblioteca, sem continuação indevida |
| 250 itens | 20 iniciais; 13 lotes para acessar todos, sem duplicatas/omissões |
| Lentidão inicial / próxima página | Feedback visível; cards anteriores utilizáveis |
| Erro inicial | Sem vazio falso; tentativa manual recupera a primeira página |
| Erro na continuação | 20 cards preservados; repetição do cursor 20 recupera os cinco restantes |
| HTTP 429 na continuação | Sem chamada durante cooldown; repetição após prazo recupera os itens |

Cada contexto teve uma chamada fictícia de sessão. Nenhuma consulta de catálogo
integral, interações legadas ou pessoas. Capturas `biblioteca-paginada-*.png`
e contagens/cursors por caso no [JSON](biblioteca-paginada-browser-2026-10-20.json).
Servidor normal restaurado em 3030, HTTP `/login` 200 confirmado pelo runner,
com ambiente normal e paginação desativada. Servidor de teste e fixture encerrados.
JSON final: `completed` com 18 casos, `failure` vazio, `normal_restored=true`.

## Limites e próxima entrega

Testa frontend/estado/transporte Reflex reais com serviço sintético. Não executa
o XanoScript candidato, não prova joins/índices/autorização real nem tempo de
resposta ou quota do Xano. Não há comparação estatística de latência nesta
rodada. A etapa local não encerra a change global de performance nem 6.2/6.4.

Trade-off de volume: para 250 itens e sessão fria, a abertura anterior simulada
precisava de sete chamadas (sessão + três páginas de mídia + três de interações).
O novo caminho precisa de duas (sessão + primeiro lote com mídia). Se a pessoa
percorrer todos os 250 itens, haverá 13 lotes + sessão = 14 chamadas, contra
sete no carregamento integral anterior. A melhoria está no trabalho inicial,
payload e carregamento sob demanda; não é redução de chamadas para leitura
integral da coleção. Interações sucessivas continuam sujeitas à quota real,
cujo comportamento ainda precisa ser medido antes de concluir a otimização.

Delta remoto proposto para revisão: somente novo
`xano/api/codeboxd/library_GET.xs` (GET autenticado `/library`). Sem mudar
tabelas, endpoints legados ou dados. Antes de publicar: backup apropriado,
preview limitado a esse arquivo, validação de sintaxe/projeção/cursor/lookahead,
autorização e comportamento com mídia ausente. Nenhuma publicação se o join
omitir interações; o contrato deve ser corrigido e novamente validado.
Após publicação aprovada e confirmação do contrato real: habilitar a flag,
reiniciar o app e validar com conta autorizada; rollback por flag desligada.
