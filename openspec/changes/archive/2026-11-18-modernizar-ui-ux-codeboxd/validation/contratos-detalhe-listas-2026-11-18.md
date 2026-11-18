# Preparação dos contratos de detalhe de listas — 18/11/2026

## Escopo

Fechamento local da tarefa 5.2. Os endpoints públicos e pessoais existentes
foram revisados junto ao estado Reflex; nenhum arquivo de contrato remoto foi
publicado nesta rodada.

## Evidências

- `python -B -m unittest tests.test_list_details`: **13 testes aprovados**.
- A regressão nova verifica nos três endpoints autenticados de leitura que a
  sessão atual é exigida e que a conta desativada é rejeitada antes do acesso à
  lista.
- A cobertura existente inclui visitante, dono, outra conta, lista privada ou
  inexistente, paginação/itens, resposta obsoleta após mudança de visibilidade
  e projeção pública sem campos internos. A evidência de browser com fixture
  está em `busca-listas-frontend-2026-11-16.md`.

## Limite

São testes locais de código/estado e browser com fixture. Publicação, leitura
independente e execução integrada no Xano continuam nas tarefas 5.3 e 5.4.
