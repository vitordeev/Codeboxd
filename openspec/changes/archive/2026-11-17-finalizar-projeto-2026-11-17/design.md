## Context

Ver proposta. A linha de base contém sete changes funcionais, 51/111 tarefas concluídas, 60 abertas, e alterações locais de busca/listas preservadas. Reflex 0.9.11.post1 está instalado na `.venv`; TMDB/Kitsu/Open Library e identidade Jikan continuam existentes.

## Goals / Non-Goals

Priorizar contratos que bloqueiam funcionalidades já expostas, executar regressões e apresentar plano verificável para hoje. Não substituir critérios de aceite por contagem de testes, nem prometer conclusão de integrações sem destino e acesso.

## Decisions

Usar checklists e fontes atuais como autoridade, com evidências datadas. Manter implementação funcional nas changes existentes e documentação transversal nesta. A restauração da conta preserva a recusa anterior de novo envio; não executar incidentalmente recuperação ou mutações remotas. Estimativas do plano são esforço de execução, condicionado a acessos.

## Risks / Trade-offs

Os 669 testes aprovados e compile local não validam publicação Xano. DNS, caixa controlada, destino isolado e dispositivo físico dependem do usuário. Contratos candidatos permanecem locais até prévia/backup e aceite específico.

## Migration Plan

Adicionar relatório datado e apontadores nos documentos centrais. Preservar registros históricos e alterações anteriores. Reverter apenas os trechos desta rodada se houver inconsistência. Sem Docker, push, merge ou publicação automática.
