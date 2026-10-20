# Avaliação com confirmação e envio único — 20/10/2026

Complemento ativo de `media-interactions` e da entrega de meias estrelas.
Pedido: impedir repetição de envio, confirmar gravação e fechar o formulário.

- [x] Bloquear submissão concorrente e suprimir repetição do mesmo payload salvo.
- [x] Atualizar ficha e fechar formulário após sucesso; permitir edição explícita.
- [x] Restaurar estado salvo ao revisitar fichas internas e externas.
- [x] Testar envio repetido, falha/retry, edição e isolamento de identidade localmente.

Contrato local existente: PUT `/interactions` usa `db.add_or_edit` por
`identity_key=conta:obra`, com índice único na tabela. Não é necessário alterar
ou publicar contratos Xano para implementar o bloqueio da interface. A unicidade
remota não foi revalidada nesta rodada; testes locais não equivalem a esse teste.

Interface: formulário desabilitado durante envio, botão “Salvando…”, limitação
de eventos no cliente a um por segundo. Após sucesso mostra resumo/nota/crítica
e “Editar avaliação”, sem redirecionamento e recarga das APIs de catálogo.
Em erro preserva o rascunho e libera nova tentativa. Consulta por identidade
externa restaura a avaliação existente sem criar outra obra. Cache de envio
é limpo na troca de identidade e invalidado por alterações via listas rápidas.

Validação: 165 testes locais e compilação Reflex `--dry` passaram; diff sem
erros. Sete regressões novas: 100 envios sequenciais iguais geram um PUT;
100 tentativas concorrentes geram um PUT; estado de carregamento antes de rede;
falha com rascunho/retry; edição da mesma obra; restauração interna/externa;
cancelamento libera bloqueio e troca de identidade limpa confirmação.
As requisições desses testes são simuladas, sem carga real de 100 pedidos no
Xano. Fluxo autenticado no navegador e persistência remota não foram executados
nesta rodada; o contrato remoto não mudou.
