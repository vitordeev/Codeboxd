## Context

Ver proposal.md e pendência P.6. A UI já usa os endpoints de solicitação, troca
de código por token e atualização de senha. A função original gera UUID com 60
minutos, e o token de recuperação tem 24 horas. Não há limite específico de
tentativas/reenvio. O provedor atual é `util.send_email` com serviço Xano.

## Goals / Non-Goals

**Goals:** código de seis dígitos, guarda como hash, controles no servidor e
entrega verificável. **Non-Goals:** alterar login comum, papéis, hospedagem ou Docker.

## Decisions

- Atualização autorizada em 22/10: substituir o serviço nativo indisponível por
  POST https://api.resend.com/emails a partir do Xano. Ler RESEND_API_KEY e
  RESEND_FROM somente do ambiente privado do backend; nunca embutir a chave
  no XanoScript, frontend, logs ou evidências. O `.env` local fornece a
  configuração inicial para implantação, mas não configura o Xano sozinho.
  Confirmar envio apenas com HTTP 2xx e ID da mensagem, sanitizar falhas e não
  repetir automaticamente envios. Resposta pública de sucesso continua genérica.
  `onboarding@resend.dev` restringe testes ao e-mail proprietário da conta
  Resend; destinatários gerais exigem domínio verificado. Antes de publicar,
  preservar backup do endpoint e conferir delta restrito. Rollback restaura o
  contrato do backup; preservar demais variáveis do backend e remover somente
  as configurações criadas nesta migração se necessário.

- Reutilizar as rotas existentes para preservar integração e reduzir migração.
  UUIDs antigos deixam de ser aceitos; é necessário solicitar outro código.
- Gerar no Xano com `security.random_number` entre 100000 e 999999 e converter
  para texto. Guardar na coluna password `password_reset.token`; código em claro
  existe apenas na função/emissor de e-mail. Nunca retorna na API pública.
- Expiração de 15 minutos, cinco tentativas e intervalo de 60 segundos. Campos
  aditivos em user: `password_reset_attempts`, `password_reset_requested_at` e
  `password_reset_format`, sem reestruturar dados históricos.
- Serializar por conta dentro de `db.transaction`: a primeira edição de
  `updated_at` obtém o bloqueio de linha; reconsultar estado após essa edição.
  Incremento de tentativas permanece na transação, enquanto a rejeição ocorre
  depois de seu commit para não reverter a contagem de erros.
- Consumo usa `password_reset.used`; token temporário de auth dura cinco minutos
  e é passado diretamente à atualização de senha, sem cookie/session storage.
- Solicitação retorna sempre mensagem genérica para conta inexistente,
  desativada ou em cooldown. Envio usa o provedor Xano atual, condicionado a um
  resultado de geração; falhas do provedor têm acompanhamento operacional.

## Risks / Trade-offs

- Espaço curto de códigos → prazo, tentativas persistidas e serialização.
- Falha de e-mail → verificar provedor/entrega em caixa controlada; não marcar
  entrega real pelo código local, dry-run ou resultado de teste simulado.
- Código consumido antes da troca → UI valida senha antes de consumir; se a
  atualização falhar, pedir novo código. Credencial temporária expira em cinco minutos.
- Rollback de UUID → invalidar códigos numéricos em circulação antes de voltar
  ao validador antigo, preservando esquema aditivo e auditoria.

## Migration Plan

Exportar estrutura remota sem registros/segredos. Validar e publicar somente
tabela user aditiva, função geradora e endpoints de reset modificados. Compilar
interface e testar limites/uso único e troca/restauração de senha em conta
controlada. Registrar separadamente simulação, Xano e chegada do e-mail.

## Open Questions

Diagnóstico de 22/10/2026: o envio nativo retornou objeto com status=error e
"Workspace admin not found" dentro de HTTP 200. Portanto, retorno HTTP da
solicitação não comprova envio. Capturar o resultado de util.send_email e
rejeitar falha interna com mensagem pública sanitizada, preservando respostas
genéricas para inexistente/desativado/cooldown. Entrega exige correção do
serviço nativo ou configuração explícita de outro provedor; seleção/configuração
do provedor ainda aguarda informação do usuário. Não conceder papéis do app
para tentar corrigir administração interna da plataforma Xano.

Qual caixa de e-mail controlada será usada para comprovar chegada e fluxo real?
Solicitado ao usuário; implementação e testes locais podem avançar enquanto isso.
