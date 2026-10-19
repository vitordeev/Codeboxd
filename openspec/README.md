# OpenSpec do Codeboxd

Meias estrelas em 19/10: seleção de 0,5 a 5, preenchimento parcial, vírgula decimal
e restauração para visitante/conta. 148 testes, compilação e navegador/Xano real
aprovados, com limpeza da avaliação de teste. [Change](changes/avaliar-meias-estrelas/tasks.md),
5/5 tarefas verificadas.

Retorno à descoberta aprimorado em 19/10: botão arredondado com seta amarela,
hover/foco e área de toque de 46px. Compilação e navegador desktop/celular
aprovados. [P.13 / evidência](validation/voltar-descoberta-2026-10-19.md).

Denúncia de obras corrigida em 19/10: erros visíveis no modal, rascunho preservado,
espera de 429 respeitada e identidade externa resolvida ao enviar. 143 testes,
compilação, Xano real e fluxo de sucesso no navegador aprovados, com limpeza dos
reports de teste. [Evidência](changes/gerenciamento-website/validation/denunciar-obras-2026-10-19.md).

Tradução em 19/10/2026: DeepL integrado localmente às descrições das fichas de
animes/livros, com cache persistente e fallback. Chave configurada privadamente;
smoke real DeepL e 136 testes locais passaram. Revisão de navegador pendente.
[Change](changes/traduzir-descricoes-deepl/tasks.md), 5/6 tarefas verificadas.

Atualização de 19/10/2026: os três GETs de buscas administrativas foram publicados
após backup e dry-run limitado; conferência final sem delta. 18 testes locais
passaram e o acesso de visitante/membro foi rejeitado. Validação funcional com
admin aprovado ainda pendente por falta de token. [Evidência atual](changes/gerenciamento-website/validation/publicacao-buscas-admin-2026-10-19.md).

Revisão documental: 13/10/2026. Este é o ponto de entrada para retomar o projeto.

Encerramento da rodada em 14/10/2026: administração publicada no Xano com
validação parcial de acesso; P.5 (imagem de post) corrigida/publicada e validada
em 15 cenários de browser; 120 testes locais passaram. Backup verificado no commit
`f93287e` de 13/10, às 23h42. Contas administrativas aprovadas, fluxo de e-mail e
rotação TMDB continuam pendentes. Evidências atuais:
[publicação administrativa](changes/gerenciamento-website/validation/publicacao-admin-2026-10-13.md)
e [uploads/sessão](validation/uploads-and-session-2026-10-13.md).

## Onde encontrar cada informação

| Documento/pasta | Responsabilidade |
| --- | --- |
| [RELATORIO_STATUS.md](RELATORIO_STATUS.md) | Relatório do que está pronto, implementado sem validação completa e ainda pendente |
| [AMBIENTE.md](AMBIENTE.md) | Setup canônico `.venv`, execução, segurança do histórico e armazenamento de uploads |
| [CONTEXTO.md](CONTEXTO.md) | Arquitetura, funcionalidades, decisões e mapa de arquivos por tópico |
| [HISTORICO.md](HISTORICO.md) | Evolução, entregas, evidências e decisões substituídas |
| [PENDENCIAS.md](PENDENCIAS.md) | Trabalho restante, prioridades e critérios de conclusão |
| [VALIDACAO.md](VALIDACAO.md) | Verificações desta revisão e limites das evidências |
| [documentation-checks-2026-10-13.json](documentation-checks-2026-10-13.json) | Resultado estruturado da conferência de tarefas, links, specs e evidências |
| `specs/<capability>/spec.md` | Contratos consolidados das mudanças concluídas |
| `changes/gerenciamento-website/` | Planejamento e tarefas administrativas em andamento |
| `changes/corrigir-erros-operacionais/` | Correções de Git, ambiente e uploads; execução local sem Docker |
| `changes/recuperar-senha-codigo-6-digitos/` | Recuperação com seis dígitos, publicada e validada por camadas; entrega real do e-mail pendente |
| `changes/archive/2026-10-13-criar-modelo-dados-xano/` | Modelo de dados concluído: 37/37 tarefas |
| `changes/archive/2026-10-13-definir-fundacao-codeboxd/` | Fundação concluída: 87/87 tarefas |

## Situação das mudanças

| Change | Estado | Concluídas | Restantes | Critério |
| --- | --- | --- | --- | --- |
| `criar-modelo-dados-xano` | Arquivada | 37 | 0 | Checklist histórico completo, evidências de persistência e validação documental |
| `definir-fundacao-codeboxd` | Arquivada | 87 | 0 | Busca Kitsu comprovada em setembro; marcador final corrigido e validação documental atual |
| `gerenciamento-website` | Ativa | 17 | 17 | Implementação local parcial/completa por tópico; integração remota e interface ainda não concluídas |
| `corrigir-erros-operacionais` | Concluída, aguardando arquivamento | 7 | 0 | Correções locais verificadas; Docker retirado do escopo pelo usuário |
| `recuperar-senha-codigo-6-digitos` | Ativa | 6 | 1 | Implementação publicada e backend/browser validados; chegada do e-mail em caixa controlada pendente |

A contagem administrativa anterior era 24/41 porque incluía sete itens H.1–H.7 de trabalho anterior. Eles foram preservados em [HISTORICO.md](HISTORICO.md), sem contar como implementação administrativa. Os 34 IDs administrativos originais permanecem estáveis.

## Como interpretar o estado

- **Concluída:** há evidência compatível com o critério original da tarefa. Ela pode ser histórica; a data e a camada estão documentadas.
- **Implementada localmente, validação pendente:** arquivos e testes simulados existem, mas falta a verificação real exigida. O checkbox continua aberto.
- **Arquivada:** o escopo original terminou e seus contratos foram sincronizados em `specs/`. Isso não garante disponibilidade contínua de provedores nem encerra melhorias posteriores.
- **Pendência transversal:** registrada em `PENDENCIAS.md`; não é incorporada silenciosamente a uma change arquivada.

## Rotina de retomada

Checkpoint de 14/10 para commit: [correção das buscas administrativas](changes/gerenciamento-website/validation/buscas-admin-2026-10-14.md).
Três endpoints corrigidos localmente, 18 testes admin passaram; publicação remota
da correção e teste com admin aprovado pendentes. Usuário pediu encerrar a sessão
para realizar o próprio commit; nenhum commit foi criado nesta rodada.

Por orientação do usuário, toda modificação no projeto deve ter vínculo e registro nesta pasta. A regra permanente está no `AGENTS.md` da raiz: identificar a change ou pendência relacionada e atualizar contexto, tarefas e evidências na mesma rodada. Arquivos de implementação continuam em seus diretórios próprios; a documentação de acompanhamento é centralizada no OpenSpec.

1. Ler os quatro documentos centrais e depois a proposta, o design e as tarefas da change ativa.
2. Conferir `git status --short` sem restaurar automaticamente arquivos de outras sessões.
3. Usar `.venv\Scripts\python.exe` para os comandos locais; ver AMBIENTE.md.
4. Consultar `openspec list --json` e `openspec status --change gerenciamento-website --json`.
5. Executar somente o trabalho autorizado, registrando data, camada, resultado e limitações da validação.
6. Atualizar tarefas e documentos centrais quando o estado mudar; não reescrever saídas históricas para fazê-las parecer recentes.

Artefatos completos no `openspec status` indicam planejamento completo, não implementação concluída. O checklist de tarefas e suas evidências determinam o encerramento.
