# Correção da coleção pessoal — 26/10/2026

> Histórico da etapa inicial. Estado final, incluindo backend e validação real, em [conclusao.md](conclusao.md); contagens abaixo preservam a rodada em que foram registradas.

## Implementação local

- Entrada em `/listas` inicia no contexto pessoal para membro; visitante recebe descoberta pública.
- GET /lists fornece a coleção pessoal, com filtro adicional por proprietário, sem consulta ao diretório público.
- O botão “Explorar listas públicas” abre contexto separado, com link ao perfil do autor; “Minhas listas” retorna à coleção pessoal.
- Troca de contexto limpa seleção/itens e invalida requisições antigas. Mudança de conta ou contexto durante leitura impede publicação de resultado anterior.
- Abrir lista alheia usa GET /lists/public/{id}/items mesmo com usuário autenticado; controles de escrita continuam limitados ao dono.
- Nenhuma alteração de contrato, publicação ou escrita no Xano. A prevenção backend prevista no grupo 3 permanece aberta; o diagnóstico não encontrou duplicatas persistidas.

## Testes e compilação

`.venv/Scripts/python.exe -B -m unittest tests.test_personal_lists tests.test_list_mutation_performance tests.test_stale_social_reads tests.test_social -q`: 56 testes aprovados na execução final.

Os cinco testes novos cobrem coleção pessoal com lista privada/personalizada e título homônimo de outro dono; descoberta e abertura pública; visitante; leitura atrasada após mudança de conta/contexto; retorno à coleção pessoal ao entrar novamente na página. O teste de chamadas de mutação foi atualizado porque o carregamento pessoal deixa de consultar o diretório público: 5 chamadas com recarga completa, 4 com recarga sem catálogo.

`.venv/Scripts/python.exe -m reflex compile --dry`: aprovado. Uma primeira tentativa detectou título dinâmico incompatível com o helper da página; corrigido usando título estático e subtítulo de seção reativo. A primeira execução do teste de chamadas tinha a expectativa histórica anterior; corrigida e reexecutada com sucesso.

## Validações em andamento

Servidor normal recarregado em produção na porta 3030, usando frontend próprio isolado e ambiente normal, com verificação prévia de conectividade pública. Compilação/build e disponibilidade `/login` aprovadas; log local `lists-correction-server.log` (ignorado pelo Git). Não houve login real ou escrita no Xano nesta implementação.

Primeiro navegador isolado: build do cliente e servidor gerados, mas pré-renderização excedeu tempo; falha preservada em browser/result.json e log correspondente. Segunda execução: quatro casos desktop aprovados; primeiro caso mobile falhou na expectativa de lista pública vazia porque a fixture compartilhava itens do caso desktop anterior. A tela mostrou a obra fictícia anterior corretamente. Limpeza da fixture corrigida para isolar os casos; evidência parcial em browser-retry/result.json.

Execução final: **8/8 cenários aprovados** no Edge headless, larguras 1440 e 390px, sem erros JavaScript ou overflow horizontal. Cobriu membro com três listas próprias (duas padrão e uma personalizada privada), descoberta separada, retorno à coleção pessoal, visitante com listas públicas, abertura pública sem controles de escrita, inclusão de obra na lista própria e seletor de listas na ficha. Serviços locais fictícios; nenhuma chamada ao Xano real. Resultados e screenshots em [browser-final/result.json](browser-final/result.json). Servidor isolado encerrado pelo executor; servidor normal na porta 3030 preservado.

Comando final: `.venv/Scripts/python.exe -B openspec/changes/corrigir-duplicacao-listas-padrao/validation/browser_check.py --output openspec/changes/corrigir-duplicacao-listas-padrao/validation/browser-final --frontend-workdir .local/frontends/feed-lists-2004`.

`openspec validate corrigir-duplicacao-listas-padrao --type change --strict` e `git diff --check`: aprovados.

Não há validação autenticada de duas contas Xano nem comprovação da prevenção concorrente remota. Checklists correspondentes permanecem abertos; 2.2 exige ainda remoção de obra no navegador, não coberta pelos casos de inclusão reutilizados. Implementação local da separação corresponde à tarefa 2.1; a change permanece ativa com 2/9 tarefas concluídas.
