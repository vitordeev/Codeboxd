## Context

Cadastro local já insere as duas listas dentro da transação de usuário/perfil.
O app também repara listas ausentes ao abrir listas ou fichas. O reset solicitado
é excepcional: não transformar reparo de navegação em exclusão recorrente.

## Goals / Non-Goals

Padronizar todas as contas existentes uma vez e garantir cadastro consistente.
Não excluir avaliações/interactions, obras/media, perfis ou usuários. Permitir
listas personalizadas posteriores. Sem Docker ou alterações de provedores.

## Decisions

Usar Metadata API autenticada para inventariar registros e salvar backup privado
completo de user_list e user_list_item antes de mutações. Ler usuários somente
para obter IDs; não persistir senhas ou tokens no backup. Conferir contagens e
identidades antes de apagar. Remover itens antes das listas, recriar duas listas
por usuário e verificar conteúdo vazio e propriedade. Registrar execução única
em manifesto local; não reexecutar automaticamente ao retomar ou fazer login.

## Risks / Trade-offs

Operações individuais podem sofrer falha parcial e não são transação global.
Parar em falha, preservar journal e backup para recuperação; nunca repetir POST
automaticamente. Conferir ausência de mudanças concorrentes antes de mutações.
Somente a janela do reset é destrutiva; listas futuras permanecem personalizáveis.
Inventário remoto encontrou quatro listas órfãs de contas removidas: fazem parte
do reset global autorizado, são incluídas integralmente no backup e removidas;
não recriar contas ausentes. Sete contas atuais recebem as duas listas base.
Execução encontrou HTTP 429 após exclusões e duas criações. Recuperação explícita
`reconcile` confere o backup, journal, catálogo/avaliações e conteúdo remoto;
apenas cria pares usuário/título ausentes, sem deletar nem repetir reset.
Recusa duplicatas ou listas personalizadas novas e usa chamadas espaçadas.
Remover limpeza legada de listas vazias "Gostei"/"Não gostei" do reparo de
navegação: após reset essas denominações podem ser listas personalizadas novas.
Manter somente criação/reparo das duas listas base, sem apagar personalizadas.

## Migration Plan

Inventário e backup, revisão do plano sanitizado, execução autorizada pela conversa,
verificação por usuário e evidência. Publicar signup apenas se remoto divergir do
contrato de inicialização, após backup do contrato. Não cadastrar contas de teste
sem necessidade. Rollback requer restaurar listas com IDs originais e itens do
backup, conferindo referências; não executar rollback automático destrutivo.

## Open Questions

Nenhuma sobre o comportamento: usuário confirmou reset sem preservar listas/itens
e permissão de criar listas personalizadas depois.
