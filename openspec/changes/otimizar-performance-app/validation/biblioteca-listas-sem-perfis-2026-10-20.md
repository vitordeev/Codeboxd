# Biblioteca/listas sem consulta de pessoas — 20/10/2026

## Escopo aprovado

Usuário aprovou remover somente a consulta de pessoas dos loaders de biblioteca
e listas, com testes e registros. Em ambos, `_load_reference()` foi substituído
por `_load_media()`. Outros consumidores de referências não foram alterados.
Catálogo para apresentar/selecionar obras, dados de listas públicas/privadas e
preparação de padrões permanecem. Sem mudança de contrato, paginação ou cache.

## Verificação

217 testes locais e `reflex compile --dry` passaram. Onze testes específicos
conferem contagens, integridade/IDs, catálogo disponível, listas públicas e
privadas, preparação de padrões e falhas. Testes que reproduziam bloqueio por
perfis agora exigem carregamento sem essa consulta. Novo teste mantém erro e
liberação de busy quando a fonte necessária de mídia retorna 429.

90 execuções simuladas adicionais (18 cenários × cinco amostras) registradas em
[biblioteca-listas-sem-perfis-2026-10-20.json](biblioteca-listas-sem-perfis-2026-10-20.json).
Antes preservado em
[biblioteca-listas-diagnostico-2026-10-20.json](biblioteca-listas-diagnostico-2026-10-20.json).

| Cenário | Biblioteca antes → depois | Listas antes → depois |
| --- | --- | --- |
| Pequeno, cache vazio | 4 → 3 chamadas | 5 → 4 chamadas |
| N=100 por coleção | 7 → 5 chamadas | 9 → 7 chamadas |
| N=250 por coleção | 10 → 7 chamadas | 13 → 10 chamadas |
| Perfis em 429, pequeno | Nenhuma obra → 5 obras | Nenhuma lista → 12 listas |
| Padrões ausentes, pequeno | Não se aplica | 8 → 7 chamadas |
| Reparo legado, pequeno | Não se aplica | 9 → 8 chamadas |

Contagens incluem a primeira validação de sessão. N significa N mídias/perfis/
interações e, para listas, N próprias personalizadas + duas padrão + N públicas
fictícias. As 250 obras e 502 listas do cenário grande continuam disponíveis,
sem IDs duplicados. Nenhuma chamada de perfis, inclusive no cenário de lentidão.
“Mostrar mais” continua apenas revelando dados já carregados, para intervenção
posterior. Erro de catálogo continua visível; falha não vira sucesso vazio.

## Limites e retomada

Somente handlers reais com HTTP simulado. Sem conta, rede, navegador, publicação
ou reinício nesta rodada; servidor atual ainda precisa de reinício para aplicar
o código. Gravações do fixture de listas afetam apenas estruturas em memória.
Não atribuir ganho de latência real a estas contagens. Aviso preexistente de
parse de `.env` persiste, sem alterar ou expor o arquivo.

Próxima etapa proposta: aprovar reinício e executor de navegador com dados
locais fictícios para biblioteca/listas, antes de uso real ou paginação nova.
Preparação de listas será simulada, sem permitir mutações reais incidentais.

6.1 concluída como diagnóstico simulado com contagens e aprovação da primeira
intervenção; não representa linha de base real completa. 6.2–6.4 permanecem
abertas. Rollback: reverter somente as duas substituições e testes associados,
preservando trabalho anterior e dados.
