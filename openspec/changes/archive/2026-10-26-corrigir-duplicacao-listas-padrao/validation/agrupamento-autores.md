# Descoberta pública por autor — 26/10/2026

> Histórico dos refinamentos de interface. Estado consolidado e encerramento dos critérios em [conclusao.md](conclusao.md); contagens por rodada abaixo são históricas.

## Refinamento de alinhamento

Por pedido do usuário, cabeçalho usa grid com duas colunas: avatar fixo de 44px à esquerda e nome na coluna flexível à direita. Ambos ficam na mesma linha do grid; nomes longos quebram dentro da coluna de texto. Classe específica no nome evita regras destinadas ao avatar padrão.

Compilação `reflex compile --dry`, build/recarga em produção na porta 3030 e verificação OpenSpec aprovados. Validação no Edge contra o app normal, visitante, somente leitura: oito cabeçalhos verificados em 1440, 390 e 320px, com nomes atuais e nomes longos injetados apenas no DOM temporário do navegador. 6/6 cenários aprovados; posição do nome sempre à direita do avatar e sem overflow horizontal. Nenhum nome, imagem ou dado pessoal nos resultados, nenhuma escrita remota e nenhum login. [Resultado](owner-alignment.json). Tarefa 2.4 concluída; change permanece ativa com 4/11 tarefas.

Refinamento solicitado após usuário conferir e aprovar a separação entre listas próprias e públicas.

## Implementação

- Listas públicas agrupadas por ID do proprietário, preservando ordem de primeira ocorrência dos autores e ordem das listas de cada autor.
- Cabeçalho único com avatar e nome do autor, ambos no mesmo link para `/perfil/{user_id}`; listas exibidas imediatamente abaixo.
- Consulta de perfis paginada pelo transporte existente, em lote, somente na descoberta pública; nenhuma consulta individual por lista.
- Perfil ausente ou serviço de perfis indisponível: nome neutro e avatar padrão, mantendo listas e destino correto do perfil.
- Coleção pessoal continua separada e não depende do serviço de perfis. “Mostrar mais” mantém a expansão da coleção visível antes do agrupamento.
- Nenhuma alteração de contrato, migração ou escrita remota.

## Validação local

`.venv/Scripts/python.exe -B -m unittest tests.test_personal_lists tests.test_list_mutation_performance tests.test_stale_social_reads tests.test_social -q`: **58 testes aprovados**. Dois testes adicionais verificam autores distintos com títulos iguais, ordem/atribuição das listas e uma única consulta de perfis; perfil ausente e falha do serviço mantêm as listas com identificação neutra.

`.venv/Scripts/python.exe -m reflex compile --dry`: aprovado.

Validação final de navegador: **8/8 cenários aprovados** em Edge headless, 1440/390px, com serviços locais fictícios. Conferidos dois autores com títulos de listas iguais, duas listas sob cada autor, foto carregada e avatar padrão, nome e destino do link, navegação até o perfil correto, visitante e membro, ausência de grupos públicos na coleção pessoal, inclusão na própria lista e seletor da ficha. Sem erros JavaScript ou overflow horizontal. Captura mobile inspecionada visualmente.

Resultados em [owner-groups-final/result.json](owner-groups-final/result.json); imagens `groups-{case}-{width}.png` no mesmo diretório. Comando: `.venv/Scripts/python.exe -B openspec/changes/corrigir-duplicacao-listas-padrao/validation/browser_owner_groups.py --output openspec/changes/corrigir-duplicacao-listas-padrao/validation/owner-groups-final`.

Primeira execução preservada em owner-groups-browser: a URL HTTP da foto fictícia foi rejeitada corretamente pelo sanitizador HTTPS do app. Fixture corrigida para HTTPS, com imagem interceptada localmente no navegador; nenhuma alteração do sanitizador de produção.

Não equivale a dois logins Xano reais. Evidências históricas anteriores preservadas. A tarefa 2.3 foi concluída; a change permanece ativa com 3/10 tarefas, incluindo pendências remotas e prevenção backend anteriores.

App normal recarregado em produção na porta 3030, reutilizando sua própria pasta de frontend após encerrar o processo anterior. Verificados domínio local do frontend, ambiente normal sem fixture e conectividade antes da parada; GET `/listas` respondeu após inicialização. Log privado local: `public-list-groups-server.log` (ignorado). Nenhuma escrita no Xano. `openspec validate corrigir-duplicacao-listas-padrao --type change --strict` e `git diff --check` aprovados.
