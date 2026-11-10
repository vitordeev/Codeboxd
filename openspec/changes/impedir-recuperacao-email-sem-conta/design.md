## Context

A API retorna sucesso genérico para contas inexistentes e a interface converte também erros 400/404 em sucesso. O usuário solicitou explicitamente impedir avanço sem cadastro. Trata-se de existência de conta no Codeboxd, não de comprovação de existência/entrega de uma caixa externa.

## Goals / Non-Goals

Impedir avanço e envio sem conta ativa. Não verificar caixas de e-mail por SMTP nem enviar e-mails de teste, não criar contas para validar e não alterar senhas.

## Decisions

- Fazer consulta mínima id/account_status antes da função geradora; retornar 404 igual para inexistente/inativa. Assim não alterar geração, cooldown e formato do e-mail. Conta ativa em cooldown mantém contrato de sucesso e código anterior.
- Interface só avança com resposta HTTP aceita. 404 retorna à primeira etapa com endereço mantido e mensagem de conta ativa não encontrada; 400 informa falha de envio sem sucesso falso. 429 mantém espera existente.
- Decisão anterior de indistinguibilidade deixa de valer por escolha explícita do usuário; isso permite inferir existência de conta pelo avanço. Não acrescentar consulta pública de usuários no frontend nem expor detalhes da conta.
- Publicar somente endpoint com backup e prévia; estender executor existente para caminhos por change, preservando relatórios e backups anteriores.

## Risks / Trade-offs

Enumeração de contas passa a ser possível pelo fluxo, consequência comunicada ao usuário e documentada. Consulta adicional mínima no envio ativo; sem mudança de retry/SMTP. Corrida com suspensão continua tratada pela função geradora e pelo validador existente.

## Migration Plan

Testar UI com 404/400 e 200; dry-run endpoint; backup e publicação restrita; verificar HTTP404 usando endereço sintético em example.invalid, sem envio nem mutação de conta. Rollback restaura apenas endpoint do backup, com env/records false. Manter verificação integrada de conta ativa sem novo e-mail em testes simulados e compilação.
