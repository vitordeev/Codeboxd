# Catálogo inicial no dashboard — 20/10/2026

Tarefas relacionadas: 4.1, 6.2 e 8.1. Pedido: mostrar algumas obras ao abrir
Filmes, Séries e Livros dentro do dashboard administrativo. O usuário corrigiu
explicitamente a interpretação inicial de alterar a página principal.

- [x] Retirar o ajuste equivocado de descoberta e seus testes específicos.
- [x] Abrir cada aba na primeira página, sem busca anterior, limpando lista e editor.
- [x] Incluir “Ver todas” e texto que explica a listagem automática.
- [x] Verificar suíte e compilação.
- [ ] Validar navegador com admin aprovado e catálogo remoto real.

O endpoint administrativo continua sendo a fonte da lista (até 25 registros
por página), com autorização original e paginação. Não foram inseridos dados
fictícios nem trocado o endpoint protegido pelo público. A consulta pública
anterior confirmou existência de 7 filmes, 3 séries e 1 livro; isso não comprova
a resposta administrativa com token admin. Filtro/página compartilhados entre
abas foram identificados no código, sem afirmar que explicam todo vazio remoto.

Validação local: suíte completa com 150 testes passou, incluindo abertura das
três abas sem filtro/página herdados, pesquisa, “Ver todas” e proteção de acesso.
Compilação Reflex `--dry` e `git diff --check` passaram. Não havia sessão admin
aprovada disponível ao diagnóstico; validação administrativa real e navegador
autenticado continuam pendentes, sem alterar os checkboxes originais.
