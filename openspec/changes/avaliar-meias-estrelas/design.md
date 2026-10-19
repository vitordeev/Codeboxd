## Context

Ver proposal.md. `user_media_interaction.rating` já é decimal e PUT /interactions
valida passos de 0,5. A interface usa cinco botões inteiros e número não controlado;
o evento/LocalStorage só aceitam inteiros. Formulário tem key incluindo a nota.

## Goals / Non-Goals

**Goals:** escala consistente entre visitante/conta, metades clicáveis, vírgula na
exibição e restauração exata. **Non-Goals:** alterar a escala, notas arbitrárias
como 1,2, agregações públicas, schema Xano ou infraestrutura.

## Decisions

- Validar com Decimal após trocar vírgula por ponto; aceitar somente finitos de
  zero a cinco e múltiplos de 0,5. Estado canônico sem zero decimal desnecessário.
- Cinco estrelas com duas áreas acionáveis por estrela e preenchimento 0/50/100%.
  Botões nativos com aria-label/aria-pressed permitem teclado e nomes explícitos.
- Seletor controlado com todas as onze opções, rótulos com vírgula e zero sem nota.
  Evita diferenças de separador decimal de input number entre navegadores.
- Compartilhar controle entre visitante e conta. LocalStorage guarda valor canônico;
  PUT envia número. Campo de review permanece montado ao trocar a nota.
- Não publicar backend sem evidência de necessidade: contrato atual já suporta.

## Risks / Trade-offs

- Áreas de meia estrela menores → cada metade mede 24×48px e há seletor alternativo.
- Notas legadas inteiras/decimais em strings → normalização aceita ambas ao restaurar.
- Ambiente remoto com rate limit → probes limitados, conta controlada e restauração.

## Migration Plan

Aplicar UI/estado, testar e compilar, reiniciar instância local de validação 3033.
Sem migração de registros. Rollback do código não altera notas já armazenadas.
