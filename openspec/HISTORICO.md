# Histórico e decisões preservadas

Consolidação documental em 13/10/2026. Datas abaixo indicam a rodada original, não execução nova.

## Evolução

Rodada posterior 13–14/10/2026: publicação autorizada de report/nove endpoints
administrativos; GETs de visitante/membro rejeitados; duas APIs de posts corrigidas
e publicadas para converter arquivo bruto em metadados. Corrigidos rascunho em
falha transitória e cancelamento com limpeza. 120 testes locais, compilação e 15
cenários de browser passaram; posts e blobs de teste removidos. Backup verificado
registrado no commit `f93287e` de 13/10 às 23h42, somente três arquivos. Admin/
desativado, e-mail completo e rotação TMDB permanecem pendentes. Essa entrega
complementa o histórico arquivado sem substituir suas evidências.

| Data | Entrega/verificação | Evidência e limites |
| --- | --- | --- |
| 17–18/09/2026 | Migração social inicial Xano, contas, perfis, mídias, interações, seguidores, posts, curtidas, comentários e listas | Modelo de dados 37/37; `.local/remote-results.json` lista 10 grupos de verificações reais; checklist e docs de retomada descrevem ownership e isolamento |
| 18–19/09/2026 | Posts com/sem mídia, mídia em listas distintas, persistência após login e lista com os quatro tipos | `docs/RETOMADA.md` e tasks originais; objetos temporários removidos/restaurados conforme os registros históricos |
| 19/09/2026 | Navegação pública, notas locais de visitante, trailers e otimizações de carga/curtidas | Fundação grupo 12; smoke histórico do Edge e 48 testes; 429 Xano tratado como recuperável |
| 22/09/2026 | Cadastro/login revalidados | 14 testes locais, 6 verificações Xano e compilação; relatório de autenticação não incluiu navegador nessa rodada |
| 22/09/2026 | Busca global, categorias independentes, capas/fallback e paginação | 54 testes e 7 verificações de navegador; relatório discovery |
| 22/09/2026 | Relevância por título e populares em grades verticais | 61 testes e smoke desktop/celular; comportamento de home substituído posteriormente |
| 23/09/2026 | Kitsu substitui consultas Jikan; mapeamento legado e deduplicação Xano | `docs/KITSU.md`; ranking 20, busca 4, Cowboy Bebop, 3 relacionados, 1 trailer; Naruto preserva identidade Jikan; 86 testes e navegador histórico |
| 23/09/2026 e checkpoint posterior | Home com fileiras horizontais, cinco coleções de livros/três de animes; pôster inteiro; streaming TMDB BR | `docs/CHECKPOINT_ATUAL.md`, catálogo, página e CSS atuais; não repetir a exigência antiga de home exclusivamente vertical |
| Até 26/09/2026 | Planejamento e implementação administrativa local | `docs/ADMIN_OPERATIONS.md`: dry-run reconheceu contratos; não comprova publicação administrativa |
| 27/09/2026 | `/admin/demo` com dados fictícios e sem escrita | `changes/gerenciamento-website/validation/local-demo-2026-09-27.md`; HTTP 200 e compilação históricos; não substitui integração real |
| 13/10/2026 | Reanálise local | 106 testes e compilação passaram; revisão documental, correção de contagem e arquivamento das duas entregas concluídas |
| 13/10/2026, após reanálise | Correções operacionais | Ignore/índice corrigidos preservando 434 arquivos existentes; `.venv` instalada; Unicode/URL de banner corrigidos; volume configurado; 113 testes e compilação passaram; teste Docker e tratamento de credenciais antigos pendentes |

## Mudanças arquivadas

- [Modelo Xano](changes/archive/2026-10-13-criar-modelo-dados-xano/tasks.md): 37 tarefas; sete capacidades de dados consolidadas em `specs/`.
- [Fundação](changes/archive/2026-10-13-definir-fundacao-codeboxd/tasks.md): 87 tarefas; nove capacidades funcionais consolidadas em `specs/`.
- [Administração ativa](changes/gerenciamento-website/tasks.md): 34 tarefas próprias, 17 concluídas e 17 abertas.

A busca de anime pendente na fundação referia-se à Jikan. A evidência Kitsu de 23/09 resolveu o objetivo de busca externa, sem exigir recuperar um provedor substituído. O item 11.7 estava escrito como `- []`, invisível à contagem do CLI; foi corrigido e encerrado após a validação documental. Antes da revisão o CLI mostrava 85/86, mas havia 87 IDs reais.

## Complementos anteriores à administração — H.1–H.7

Esses IDs foram retirados apenas do checklist administrativo; o conteúdo e os limites permanecem aqui.

| ID histórico | Trabalho registrado | Evidência disponível / limite |
| --- | --- | --- |
| H.1 | Solicitação de código de senha por e-mail, validação do código e atualização da senha | Estado de sessão e endpoints reset existentes; entrega real de e-mail não comprovada |
| H.2 | Pesquisa de obra dos quatro tipos no compositor do feed e seleção de resultado | Página/estado social existentes; não equivale a smoke completo atual |
| H.3 | Upload multipart de imagem do post, validação, prévia e leitura no feed | `services/uploads.py`, estado e contratos Xano; publicação real com imagem no navegador pendente |
| H.4 | Bloqueio de envio duplicado enquanto post é salvo | Trava `post_saving` no handler; suíte/compilação locais |
| H.5 | Ajustes visuais de pesquisa, upload, card e exclusão | CSS e diálogos; validação visual atual completa pendente |
| H.6 | Atualização de campo de imagem e POST/PUT de posts no workspace | Registro histórico relata publicação, dry-run sem delta e 68 arquivos analisados; não revalidado nesta revisão |
| H.7 | Compilação depois das mudanças do feed | Evidência histórica; compilação geral também passou em 13/10 |

## Decisões substituídas e mantidas

- **Substituída:** Jikan como fonte de consulta de anime → Kitsu; identidade Jikan permanece por compatibilidade.
- **Substituída:** home só com grades verticais → coleções horizontais empilhadas; busca/categorias continuam paginadas.
- **Mantida:** login é página; pop-up das referências foi descartado.
- **Mantida:** adaptadores rodam no Python; Xano guarda dados e aplica autorização.
- **Mantida:** catálogo legado `titulos` não é convertido automaticamente em `media`.
- **Mantida:** `/likes` ausente não cria consultas de discussão para todo o feed; compatibilidade sob demanda.
- **Mantida:** publicar hospedagem/domínio não é parte desta etapa.
- **Corrigida:** afirmação documental de Git protegido → `.gitignore` vazio verificado; proteção precisa ser implementada.

## Preservação das evidências

Saídas `.txt`, `.json` e scripts de validação foram preservados com a fundação arquivada. Não foram executados novamente nem tiveram resultados alterados. Relatórios de setembro são históricos: URLs locais, comportamento visual e comandos podem ter envelhecido.

Os scripts históricos possuem caminhos fixos: `auth_live.py` usa uma profundidade de diretório anterior ao arquivo; scripts de browser escrevem na antiga change ativa. Antes de reutilizá-los, adaptar uma cópia fora do arquivo para o diretório atual e uma nova pasta de resultados. Não sobrescrever evidências arquivadas. O teste de autenticação real cria conta; não executá-lo apenas para validar documentação.

Resultados `.local/` são auxiliares e podem conter dados privados. Somente resumos sem segredos foram incorporados. Ausência desses arquivos em outra máquina não invalida o registro histórico, mas limita sua reprodução; consultar o relatório arquivado e revalidar quando necessário.

## Decisão posterior — sem Docker

Em 13/10/2026, o usuário solicitou manter o projeto sem Docker. Os ajustes Docker desta rodada foram revertidos e o Desktop iniciado para diagnóstico foi encerrado. Nenhum contêiner/volume foi criado. A execução permanece local com `.venv`; 3.1/3.2 saíram do escopo operacional, preservados no histórico, deixando 7/7 tarefas próprias concluídas. Permanecem as correções Git, dependências e uploads, verificadas em 113 testes e compilação.
