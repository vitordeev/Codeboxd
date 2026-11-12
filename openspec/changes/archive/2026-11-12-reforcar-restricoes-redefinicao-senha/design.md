## Context

Auditoria dos contratos publicados confirmou seis dígitos, 15 minutos, cinco tentativas persistidas, cooldown de 60s, uso único, hash, token de recuperação de cinco minutos e session_version para revogação. A tabela já exige oito caracteres/letra/número, mas endpoint final valida tardiamente no banco; aceita purpose=session porque o guard compartilhado permite sessão comum e recuperação. Não bloqueia senha igual à atual.

## Goals / Non-Goals

Fechar lacunas no endpoint final e feedback. Não redesenhar login/cadastro, voltar à indistinguibilidade de contas, impor símbolos/maiúsculas, integrar serviço de senhas vazadas, criar CAPTCHA ou alterar globalmente rate limits. Não prometer que oito caracteres satisfazem todas as recomendações OWASP/NIST; manter regra existente do produto.

## Decisions

- Preservar guard compartilhado em primeiro lugar e sob lock. Acrescentar validação de purpose=password_reset exclusivamente no endpoint final; token normal não substitui prova por código.
- Input 8..128 caracteres e confirmação limitada; lambda valida letra ASCII e dígito ASCII para corresponder ao frontend. Sem trim ou truncamento da senha. Unicode/espaços não são proibidos quando a política existente é atendida.
- Sob lock, reler id/password/account_status/session_version, exigir active e comparar nova senha com hash atual via security.check_password antes de incrementar versão ou salvar. Confirmação divergente/política inválida/reuso geram erro 400 sanitizado e rollback. Sessão/credencial desatualizada segue 401.
- Frontend valida tamanho máximo antes de consumir código. Separar rejeição do código de falha posterior: senha não aceita orienta senha diferente e novo código; credencial expirada/consumida orienta novo pedido; resposta incerta recomenda tentar login com a nova senha. Credencial temporária permanece apenas em memória, nunca cookie/storage.
- Após sucesso, limpar identidade/cookie/storage local somente se corresponder ao user_id recuperado; não desconectar outra conta local.
- Publicar somente endpoint final com backup sem segredos, assinatura de prévia e comparação de delta. Teste remoto usa uma única conta member com email example.invalid, senha aleatória e tokens temporários em memória, sem enviar e-mail. Após falha do interpretador sem esquema e confirmação de zero fixtures reais, usar signup publicado e função administrativa generate_magic_link, sem mailer. Testar rejeições/sucesso/replay e login; remover somente listas vazias da fixture e sua conta no finally, preservando auditoria. Credenciais inválidas incluem ausente, corrompida, sessão comum e versão revogada; expiração de cinco minutos permanece configuração existente do emissor, sem esperar cinco minutos para esse teste.

## Risks / Trade-offs

Consumo do código antecede tentativa de nova senha; rejeição de senha igual exige novo código, informado na UI. CLI histórico password_recovery_remote bloqueado antes de qualquer ação: restauração via sessão comum deixa de funcionar e exige adaptação antes do reuso. Mudança do endpoint não deve modificar o guard global nem demais rotas. Caso teste remoto/limpeza falhe, registrar limitação e manter tarefa aberta; não declarar sucesso por simulação.

## Migration Plan

Implementar e testar fronteiras de senha, finalidade e mensagens; compilar. Validar dry-run restrito, publicar com backup, executar matriz na fixture e confirmar remoção. Rollback restaura apenas query do backup com env/records=false, mantendo demais definições. Registrar inventário de restrições e limitações externas de entrega de e-mail.
