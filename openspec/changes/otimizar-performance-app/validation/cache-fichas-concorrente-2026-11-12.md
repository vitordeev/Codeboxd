# Cache local de fichas e disponibilidade — 12/11/2026

## Alteração

O cache de resultados de fichas e disponibilidade agora compartilha leituras
equivalentes em andamento por loop/evento e chave, sem cancelar a operação quando
um consumidor é cancelado. O cache permanece limitado a 256 resultados; leituras
pendentes, a 128. Resultados são copiados para consumidores e falhas não são
armazenadas.

A chave da ficha inclui o item completo. Isso evita que registros locais distintos
com a mesma identidade externa compartilhem campos dependentes do registro, como
o ID interno legado do anime. Disponibilidade continua separada por fonte, tipo,
identificador e região.

## Verificação local

- Regressões novas: compartilhamento de carga concorrente, cópias independentes,
  falha não armazenada e isolamento do ID de registro Jikan.
- Suíte focada: `.venv\Scripts\python.exe -m unittest tests.test_home_performance tests.test_catalog tests.test_kitsu tests.test_translation` — 50 testes aprovados.
- Suíte completa: `.venv\Scripts\python.exe -m unittest discover -s tests -q` — 635 testes aprovados.
- `git diff --check` nos arquivos desta alteração — aprovado.

## Limites

São testes locais com provedores simulados. Não medem redução real de latência,
não comprovam cache frio/aquecido no navegador e não validam a jornada ficha/
disponibilidade em desktop ou celular. Por isso, não encerram as tarefas 4.4,
5.4 ou 9.x, nem demonstram atendimento às metas aprovadas por jornada.
