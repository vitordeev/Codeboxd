# Limpeza local de arquivos — 20/10/2026

Pedido: retirar arquivos sem utilidade para o projeto. Vínculo: manutenção
operacional posterior à change `corrigir-erros-operacionais`, preservando sua
entrega histórica e os IDs existentes.

- [x] Conferir contexto, ambiente, pendências, validação e estado do Git.
- [x] Identificar e remover somente caches Python descartáveis.
- [x] Conferir destinos dentro do workspace e conteúdo limitado a `.pyc`/`.pyo`.

Removidos 28 arquivos, totalizando 540.904 bytes, de nove diretórios
`__pycache__`: raiz, `Codeboxd_main/`, suas pastas `pages/`, `services/` e
`state/`, `tests/`, `tools/`, `openspec/validation/` e
`openspec/changes/gerenciamento-website/validation/`.
Nenhum desses arquivos estava rastreado no Git. São recriados pelo Python;
esta limpeza não impede sua geração futura. As regras de ignore já existem.

Preservados código, testes, dependências, `.venv`, ambiente legado `venv`
(compatibilidade documentada), uploads, backups, dados locais, referências
visuais, evidências e arquivos de preparação de publicação. Não há evidência
suficiente para afirmar que esses arquivos nunca mais serão necessários.
As alterações preexistentes em `.gitignore` e `reflex.lock/` foram preservadas.

Validação local: remoção concluída sem erro; nenhum código Reflex foi alterado.
Não foram executados testes funcionais, compilação, navegador, Docker ou
operações remotas, pois o escopo foi apenas excluir bytecode descartável.
