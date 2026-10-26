# Tasks

## 1. Diagnóstico

- [x] 1.1 Consultar todas as listas no Xano em leitura e comparar propriedade/títulos com composição local; verificar total e IDs únicos e registrar resultados sanitizados em diagnostico.md. Resultado: 19 listas, 8 proprietários, 16 padrões, zero duplicatas por proprietário; app mistura listas públicas e próprias.
- [x] 1.2 Conferir contratos e esquema efetivamente publicados e reproduzir a tela com duas contas, distinguindo retorno remoto e navegador; registrar evidências sem credenciais. Contratos/índice conferidos por exportação, isolamento na API e duas contas reais em 1440/390px comprovados; ver validation/conclusao.md.

## 2. Coleção pessoal e descoberta

- [x] 2.4 Manter nome sempre à direita da foto no cabeçalho público, com colunas fixas para avatar/texto; verificar geometria no navegador em desktop/celular inclusive com nome longo e registrar evidências. Grid de 44px/texto, compilação e recarga aprovadas; 6/6 cenários em 1440/390/320px com oito cabeçalhos, nomes atuais e nomes longos. Ver validation/owner-alignment.json e validation/agrupamento-autores.md.

- [x] 2.1 Separar listas próprias e públicas no estado e na interface, identificar propriedade na descoberta e preservar acesso de visitantes; verificar com testes de listas homônimas de donos diferentes, privadas e troca de conta, registrando resultado. Implementado com seletor de contexto, filtro de proprietário, link ao perfil do autor e rota pública para obras alheias. Cinco testes novos e 51 regressões passaram; ver validation/implementacao.md.
- [x] 2.2 Validar desktop/celular no navegador, abrir listas e adicionar/remover obra nos destinos próprios; comprovar que a coleção pessoal exibe só suas listas, preserva personalizadas e não oferece escrita nas de outros perfis. 14 critérios reais comprovados em validation/default-lists-browser-coverage.json; inclusão/remoção em 1440/390px somente na lista privada descartável. Condições de espaçamento e tentativas anteriores preservadas em validation/conclusao.md.
- [x] 2.3 Agrupar listas públicas por autor com foto/nome clicáveis acima das listas; verificar agrupamento, links, ausência/falha de perfil e preservação da coleção pessoal em testes, compilação e navegador desktop/celular, registrando evidências. 58 testes, compilação e 8/8 cenários de navegador com serviços fictícios aprovados; ver validation/agrupamento-autores.md.

## 3. Prevenção de duplicatas

- [x] 3.1 Preparar identidade de tipo padrão por proprietário e delta backend mínimo com backup/rollback; verificar compatibilidade dos registros existentes e dry-run sem alterações fora do escopo, registrando decisões. Backup 79 contratos/19 listas/8 itens, delta de quatro documentos com cinco operações aprovado no dry-run; plano de 16 chaves e rollback em validation/backend-identidade.md.
- [x] 3.2 Tornar cadastro e preparação de padrões idempotentes e completos sob paginação; testar concorrência, padrão após primeira página, erro e troca de conta sem criar listas em duplicidade, documentando evidência local. Seis testes de identidade aprovados; cadastro real, três requisições simultâneas convergindo a um ID e preservação de padrão renomeado/privado aprovados em validation/default-lists-remote.json. Feature habilitada no ambiente privado após publicação e backfill.
- [x] 3.3 Publicar somente delta revisado e validar simultaneidade e isolamento reais entre contas, registrando o que foi publicado e conferindo contagens antes/depois sem apagar listas personalizadas. Publicação/backfill, 18 checks API, índice único/campo anulável e zero alterações alheias comprovados. Limpeza descartável concluída, com 19 listas/8 vínculos originais preservados e zero duplicatas no inventário final; ver validation/conclusao.md.

## 4. Preservação e integração

- [x] 4.1 Implementar diagnóstico/plano de reconciliação sem escrita quando não há duplicatas; testar união de itens, privacidade e ambiguidades com fixtures. Se surgirem duplicatas reais, preparar backup privado e plano antes de qualquer aplicação; registrar explicitamente ausência de limpeza quando não necessária. tools/default_list_integrity.py produz plano sem expor operações de escrita; seis testes aprovados. Snapshot real preservado; nenhuma limpeza necessária, títulos homônimos sem identidade vão para revisão e não são mesclados.
- [x] 4.2 Executar testes pertinentes e compilação conforme skills Reflex, comparar regressões de listas e registrar limites por camada; atualizar documentos centrais e executar openspec validate corrigir-duplicacao-listas-padrao --type change --strict. 411 testes, compilação/build e recarga aprovados; documentação central reconciliada e evidência consolidada em validation/conclusao.md. Validações local, remota e navegador distinguidas, com falhas/quota anteriores preservadas; OpenSpec estrito e diff check aprovados.

## Evidências da preparação

- Consulta real e leitura de código documentadas em [diagnostico.md](diagnostico.md); nenhuma mutação remota ou alteração de código nesta rodada.
- Planejamento validado com `openspec validate corrigir-duplicacao-listas-padrao --type change --strict`; testes e compilação de produto ficam para implementação.

## Workflow follow-up

- Sincronizar specs e arquivar somente depois de critérios atendidos e dentro do escopo autorizado.
