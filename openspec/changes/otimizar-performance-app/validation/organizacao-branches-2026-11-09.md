# Organização das branches e base de performance — 09/11/2026

Preparação do ambiente Git para a change ativa otimizar-performance-app e futuras
medições 1.3/1.5. Escopo autorizado: leitura das regras, consulta GitHub, fetch e
nova branch/worktree baseada em origin/develop. Sem implementação, merge, push,
movimentação das branches existentes, instalação ou acesso Xano. Nenhum checkbox
de performance foi alterado; permanece 17/37. Administração 33/34, 9.2 aberta.

## GitHub e referências atualizadas

Executado `git fetch origin`, sem prune ou integração. Após o fetch, consulta
direta autenticada e somente leitura da API GitHub confirmou:

| PR | Destino | Estado | Merge |
| --- | --- | --- | --- |
| [28](https://github.com/vitordeev/Codeboxd/pull/28), feedback dos modais e aceite administrativo | develop | merged=true, closed | a21c806, 05/11/2026 23:49:09 UTC |
| [29](https://github.com/vitordeev/Codeboxd/pull/29), Develop | main | merged=true, closed | f244987, 05/11/2026 23:51:05 UTC |

As consultas de branches na mesma API coincidem com as referências obtidas pelo
fetch: origin/main=f244987622f099dcf65c49f4822a673638b55089;
origin/develop=a21c806118f7234ec051d455a9b6619767572167.
Evidência sanitizada privada `.local/branches-github-20261109.json`; credencial
obtida pelo helper Git apenas em memória, sem impressão ou cópia para arquivos.

| Branch | Local | Remota conhecida | Situação |
| --- | --- | --- | --- |
| main | 832f728 | origin/main f244987 | Local 29 commits atrás, nenhum exclusivo; mantida intacta |
| develop | ac3317d | origin/develop a21c806 | Local cinco commits atrás, nenhum exclusivo; mantida intacta |
| task/admin-acceptance-9-2-20261105 | c400ab9 | Mesmo commit em origin | Trabalho commitado integrado por PR 28 e depois PR 29; branch não removida |
| task/performance-context-20261109 | a21c806 | Sem upstream | Diretório original com trabalho administrativo/documental local preservado |
| task/performance-20261109 | a21c806 | Upstream origin/develop como base | Nova branch local na worktree independente; não publicada |

`git rev-list --left-right --count origin/main...origin/develop` = **16 / 0**:
nenhum commit de develop falta em main. `merge-base --is-ancestor` confirma que
origin/develop é ancestral de origin/main. Os 16 commits exclusivos de main são
15 merges históricos e o commit documental 0f72ac9, auditoria/backlog. A diferença
de árvores contém 39 arquivos, todos em openspec/ (692 inserções), incluindo
planejamento/auditoria e evidências administrativas. Nenhuma reconciliação foi
feita ou presumida: a base solicitada continua sendo origin/develop.

## Nova worktree para continuar

Comando executado:

```powershell
git worktree add -b task/performance-20261109 'D:\Repositorios GIT\Codeboxd-performance-20261109' origin/develop
```

Diretório recomendado: **D:\Repositorios GIT\Codeboxd-performance-20261109**.
Branch: **task/performance-20261109**. `git status --porcelain=v1` vazio;
HEAD...origin/develop = 0/0; `git diff --quiet HEAD origin/develop` aprovado.
Os commits 9ce7dcc, 1372215, c400ab9 e o merge a21c806 são ancestrais da nova
branch: ela contém o trabalho administrativo já integrado, além da base anterior.
Não contém as mudanças administrativas locais ainda sem commit do diretório
original; essas foram preservadas, não transferidas incidentalmente.

Worktree criada com o usuário normal do Windows. A primeira consulta pelo usuário
do sandbox encontrou ownership diferente; as verificações finais foram executadas
pelo mesmo usuário criador, sem adicionar exceção global safe.directory. A criação
terminou com exit 0; não há lock temporário de checkout na lista final de worktrees.

O Git/OpenSpec está pronto para retomar o planejamento/diagnóstico de performance.
`openspec list --json` reconhece as três changes funcionais na nova pasta e
`openspec validate otimizar-performance-app --type change` passou. Primeiras
pendências: 1.3 (baseline) e 1.5 (metas aprovadas), sem encerrá-las por esta
preparação. Não foi executado benchmark ou teste da aplicação.

A nova pasta não tem `.venv` nem `.env`. Antes de executar Reflex/testes que
exijam dependências/configuração, seguir a skill setup-python-env e AMBIENTE.md
para preparar o ambiente próprio, depois as demais skills Reflex quando cabíveis.
Não foram copiadas credenciais, uploads, node_modules ou ambiente virtual do
diretório administrativo. Sem Docker.

## Preservação

Diretório original: **D:\Repositorios GIT\Codeboxd**, mantido na branch
task/performance-context-20261109. Antes de criar a worktree, checkpoint privado
`.local/checkpoints/branch-organization-20261109-165148` guardou ZIP, hashes de
18 arquivos locais, status, branches/worktrees e SHAs das referências locais.
ZIP verificado; todos os 18 hashes e o status original coincidiram após a criação.
main, develop, branch administrativa e HEAD originais não foram movidos.

`reflex.lock/package.json` mantém exatamente SHA-256
60953f76d66b9864a8ccf100dfc3520f6a5d07f7b3759cc52d4fd5747a54c3e0.
Este registro é o único arquivo de projeto acrescentado nesta rodada, no diretório
original, para manter a nova worktree limpa. Os demais arquivos e seus diffs não
foram alterados, incluídos no índice ou commitados.

Nenhum push, merge, reset, stash, rebase, exclusão de branch/worktree, atualização
de main/develop locais, operação Xano ou arquivamento foi realizado.
