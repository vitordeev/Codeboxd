## Context

Página atual exibe cinco campos em dois formulários ao mesmo tempo. A recuperação e proteção após sucesso já existem.

## Goals / Non-Goals

Reduzir carga visual e eliminar repetição de e-mail. Preservar validação de senha e confirmação; não dividir a validação de código em chamada adicional, pois ela consome o código.

## Decisions

- Evolução posterior em 10/11/2026: a change impedir-recuperacao-email-sem-conta determina rejeição de endereço sem conta ativa e permanência na primeira etapa, substituindo a premissa genérica de avanço para qualquer endereço. Histórico e validações desta entrega preservados.

- Etapa inicial com e-mail; resposta genérica aceita avança para código e duas senhas, usando e-mail guardado em estado. Manter fallback de e-mail no handler para compatibilidade de chamadas existentes.
- Mostrar endereço resumido na etapa seguinte com ação de trocar; reenvio reutiliza o e-mail guardado. Erros mantêm etapa e dados. Trocar e-mail limpa feedback e estado da jornada, sem chamar API.
- Sucesso substitui formulários por confirmação e CTA de login; nenhuma senha ou código vira variável sincronizada.
- Cartão central com largura máxima de 440px, indicador discreto de etapa, texto curto e código com tipografia destacada; manter paleta e logo existentes. Sem ilustrações novas.
- Estados existentes de loading e cooldown preservados. A mensagem de solicitação não afirma existência da conta.

## Risks / Trade-offs

Resposta de envio genérica não comprova entrega; manter texto condicional. Dois campos de senha seguem necessários à confirmação e só aparecem na etapa final. Sem navegador disponível, registrar limites de validação visual sem simular evidência real.

## Migration Plan

Mudança local reversível de UI/estado; testar transições com transporte simulado, compilar Reflex e verificar navegador quando disponível. Sem Docker ou publicação Xano.
