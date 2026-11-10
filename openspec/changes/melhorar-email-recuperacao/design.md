## Context

Envio direto Xano → SendGrid já publicado. Histórico: seis solicitações entre 0,035 e 0,565s, mediana 0,341s; inclui cooldown sem envio. Sem eventos de entrega, não representa latência até Gmail. Remetente verificado gmail.com preservado; autenticação de domínio próprio pode melhorar entregabilidade, mas exige domínio/DNS fora deste pedido.

## Goals / Non-Goals

Melhorar leitura e eliminar espera sem feedback e reenvios redundantes. Não reduzir timeout como se isso acelerasse entrega nem executar nova fila/retry. Não alterar segurança, senha ou configurações globais SendGrid.

## Decisions

- Template local HTML com tabelas e CSS inline para clientes de e-mail, sem fontes/imagens/links externos. Marca em texto, contraste laranja/preto, código contínuo selecionável, prazo e instrução de segurança. Texto simples vem primeiro no payload multipart. Preview contém apenas dígitos fictícios.
- Desativar open/click/subscription tracking somente nessa mensagem; nenhum send_at ou anexo. Não afirmar redução de tempo de caixa por essas opções sem medição.
- Wrapper de evento com yield antes da chamada permite publicar estado de envio ao navegador; manter handler existente para compatibilidade de testes. Guard adicional evita enfileirar cliques repetidos no wrapper. Reenvio usa mesmo wrapper.
- Cooldown local de 60 segundos por endereço após resposta genérica aceita evita novas chamadas imediatas; não faz retry. Informar prazo restante ao clicar em reenviar. Proteção backend continua sendo a autoridade.
- Ferramenta própria da change faz backup sem segredos, prévia limitada a uma query, confere assinatura antes de publicar e verifica delta posterior; não reutilizar relatório histórico de implantação.

## Risks / Trade-offs

Consulta posterior à atividade SendGrid confirmou adiamentos 421 4.7.32 (alinhamento SPF/DKIM com From); duas entregas em 27s/70s e uma ainda em processamento após sete adiamentos. A causa concreta exige remetente de domínio próprio autenticado, não mudança no HTML nem timeout. Usuário consultado sobre domínio/DNS. Não alterar remetente ou DNS sem essa informação; configuração atual mantida. Sandbox valida estrutura, não chegada. E-mail maior que o anterior por identidade visual não é gargalo presumido: manter HTML abaixo de 8KB e sem dependências externas.

## Migration Plan

Registrar baseline, criar template e preview, executar testes de eventos e sandbox SendGrid sem entrega, validar dry-run Xano. Publicar somente endpoint com backup e conferir preservação dos demais contratos. Rollback restaura o endpoint do backup, sem tocar ambiente. Medição de chegada permanece pendente até teste controlado informado pelo usuário.
