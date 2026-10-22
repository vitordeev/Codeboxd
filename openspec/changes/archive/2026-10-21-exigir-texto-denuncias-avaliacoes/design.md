## Context

Report.description e interaction.review são opcionais atualmente. HTML não bloqueia
campos vazios; o handler normaliza, mas envia mesmo sem texto.

## Decisions

Usar required/min_length no HTML e strip no handler Python antes de qualquer
requisição. A descrição do report é exigida para todos os motivos e alvos.
O formulário de avaliação exige crítica mesmo se a nota for zero. O contrato
genérico de interações também atende organização da biblioteca: no Xano, nota
positiva exige review, enquanto status sem nota permanece válido. Quick_add com
nota positiva também exige texto. Não criar nota mínima, tamanho arbitrário
de texto ou apagar registros existentes.

Preparar XanoScript e publicar somente os dois endpoints, com backup remoto,
comparação restrita e validação que não crie registros vazios. Não inferir
publicação do arquivo local. Rejeições conservam rascunho/modal/formulário.

## Risks / Trade-offs

Clientes antigos com nota positiva e review vazio passam a receber erro de entrada.
Migração de avaliações antigas e alteração dos registros organizacionais não fazem parte.
Rollback: reverter só os trechos desta change; restaurar os dois endpoints pelo backup
se publicados, mantendo as demais mudanças do workspace.
