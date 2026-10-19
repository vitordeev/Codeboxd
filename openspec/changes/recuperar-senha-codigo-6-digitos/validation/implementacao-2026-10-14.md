# Recuperação por seis dígitos — 14/10/2026

Pedido explícito do usuário: enviar ao e-mail cadastrado um código de exatamente
seis dígitos para recuperar a senha. A change acompanha P.6 e permanece ativa
até a chegada real do e-mail e fluxo completo em caixa controlada.

## Implementação publicada

- Gerador nativo `security.random_number`, intervalo 100000–999999, convertido
  em texto e armazenado em `password_reset.token` (coluna password/hash).
- Prazo de 15 minutos, cinco tentativas por código e cooldown de 60 segundos.
- Campos aditivos em user: attempts, requested_at e format de recuperação.
- Geração/validação serializadas por linha em transação; leitura depois da edição
  de updated_at para observar o estado bloqueado. Rejeição fora da transação
  preserva o contador de erro. Código consumido rejeita reutilização.
- Solicitação de e-mail tem resposta genérica para inexistente/cooldown, sem
  retornar código. HTML contém os dígitos inseridos diretamente, sem placeholder.
- Token intermediário configurado para cinco minutos; segue direto para a
  atualização de senha, sem virar cookie ou session storage.
- Formulário aceita seis dígitos ASCII, teclado numérico, autofill one-time-code;
  código/senha/confirmacão inválidos não consomem o código. Submissão duplicada
  durante carregamento é ignorada.
- UUIDs antigos deixam de funcionar; solicitar novo código.

Referências utilizadas: [segurança Xano](https://docs.xano.com/xanoscript/function-reference/security),
[operações de banco](https://docs.xano.com/xanoscript/function-reference/database-operations)
e [input Reflex](https://reflex.dev/docs/library/forms/input/).

## Publicação e preservação

Exportação sem registros/variáveis de ambiente: CLI salvou 77 documentos em
`.local/xano-before-six-digit-reset-2026-10-14`. Preview limitado a quatro arquivos
mostrou uma tabela alterada com três campos novos, uma função e dois endpoints
alterados. Push confirmou **4 documentos publicados**. Dry-run posterior dos
mesmos includes: **No changes to push**. Sem importação de registros, concessão
de papel, exclusão de tabela ou Docker.

```powershell
xano workspace push -d xano -w 147717 --dry-run -i 'table/user.xs' -i 'function/quick_start/generate_magic_link.xs' -i 'api/authentication/reset/request_reset_link_GET.xs' -i 'api/authentication/reset/magic_link_login_POST.xs'
```

## Evidências por camada

| Camada | Resultado | Limite |
| --- | --- | --- |
| Local/simulada | 127 testes passaram; sete novos testes do formulário/fluxo | Respostas controladas não comprovam chegada de e-mail |
| Local | Reflex compilou | Execução local com `.venv` |
| Xano real, conta de teste | [16 cenários](remote-2026-10-14.json) passaram | Geração pela função interna; não enviou e-mail |
| Xano real, privacidade/expiração | [6 cenários](expiry-and-generic-2026-10-14.json) passaram | Conta controlada, fixture expirada pelo operador |
| Browser | [7 cenários](browser-2026-10-14.json) passaram, sem exceções JS | UI desktop/celular e código inválido; não solicitou e-mail |
| Entrega de e-mail | Não executada | Aguarda e-mail de conta cadastrada com caixa controlada |

Os testes remotos comprovaram geração de seis dígitos, código diferente do valor
armazenado/hash, prazo, cooldown, contador de falhas persistido após HTTP 401,
bloqueio depois de cinco erros, invalidade do anterior após reenvio, concorrência
com somente um sucesso, consumo persistido, troca de senha e novo login; a senha
original deixou de funcionar durante o teste e foi restaurada depois.

A rodada complementar preservou o hash ao expirar a fixture, rejeitou o código
correto expirado e conferiu que ele não consumiu tentativa. Respostas de e-mail
inexistente e cooldown foram iguais e não incluíram código. Senha e campos de
recuperação da conta de teste foram restaurados em finally. Nenhuma conta recebeu
papel administrativo nem foi suspensa. Cenário de conta desativada não foi
executado; os contratos locais exigem estado active explicitamente.

As tentativas iniciais do probe falharam pela interpretação do envelope duplo
`result` da Metadata API; a execução final acima usou o envelope correto. Não
foram defeitos de geração. Nenhum código, token, hash, senha ou e-mail pessoal
foi publicado nos resultados. Scripts auxiliares/snapshots sensíveis ficam em
`.local/`, ignorada no Git. O servidor do browser foi encerrado.

## Pendência de fechamento

Validar recebimento do e-mail e fluxo completo usando caixa real controlada.
Usuário foi consultado sobre o e-mail; até informar a conta e verificar a caixa,
não marcar 3.2 concluída. O serviço de envio é o Xano já usado pelo projeto; não
há evidência desta rodada sobre quota, entrega/spam ou domínio de remetente.
