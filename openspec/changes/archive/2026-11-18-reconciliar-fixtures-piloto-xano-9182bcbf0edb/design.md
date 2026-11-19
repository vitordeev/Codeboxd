## Escopo e segurança

- Change operacional separada porque a change funcional prevê exclusão pelos endpoints proprietários; as credenciais temporárias dessas contas não foram preservadas.
- Alvo fixo: run `cbshared_9182bcbf0edb`, usuários 48/49 e listas 119/120, workspace 147717. Rejeitar qualquer divergência de marcador, dono, título, status ou contagem de registros.
- Fazer inventário de listas e itens, confirmar zero referências para 119/120 e confirmar que 119 é a única exposição pública do lote antes de qualquer escrita.
- Privacidade/exclusão de listas usa a API de metadata Xano, com recibo explícito de desvio da auditoria do app. Contas são desativadas pelo endpoint administrativo autenticado como admin 14.
- Ordenar ações: privatizar 119 e verificar; excluir 119 e 120, cada uma precedida por nova leitura de identidade e referências; desativar 49 e 48 via endpoint admin e verificar estado após cada escrita. Sem retries automáticos.
- Se a identidade/estado divergir, a leitura falhar ou uma escrita for incerta/rejeitada, parar e preservar recibos; nunca ampliar o conjunto de IDs.

## Limites

Esta reconciliação não valida autoria funcional, visibilidade entre usuários nem mutação cruzada. Ela só reduz os efeitos residuais do piloto parcial. A change funcional permanece aberta até haver evidência de aceite funcional por caminho autorizado.

## Execução

Leitura real autorizada concluída no recibo `reconciliation-execution-escalated.json`: identidades e status ativos esperados, listas 119/120 sem referências e somente 119 pública. O primeiro acesso foi bloqueado pelo sandbox e não enviou escrita; a tentativa com rede permitida concluiu as leituras, depois ficou aguardando login do administrador 14. Até autenticação, `remote_writes=0`; não declarar a reconciliação nem a change principal como concluídas.

Conclusão posterior: `reconciliation-execution-console.json` registra autenticação do admin 14, cinco escritas HTTP 200 e seis verificações aprovadas. A lista 119 foi privatizada e removida; a 120 foi removida; contas 49/48 foram desativadas via endpoint admin. As senhas não foram incluídas no recibo. Execução concluída; o teste de autoria funcional não é coberto por esta change.

Para autenticar sem compartilhar a senha no chat nem depender de janela gráfica, o executor oferece `--console-login`: solicita o e-mail e usa `getpass` para ocultar a senha no PowerShell local. Só autenticação válida do admin 14 libera a primeira escrita.
