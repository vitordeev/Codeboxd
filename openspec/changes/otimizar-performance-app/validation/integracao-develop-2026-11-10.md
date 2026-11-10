# Git branch audit and integration preparation - 2026-11-10

## Base and branches

`git fetch origin` updated `origin/develop` to `4a7cabe` (`Feat:ajustanto a recuperacao de senha e as imagens`). This commit adds the remote password-recovery, image, and OpenSpec work. Local `develop` remains at `ac3317d`, six commits behind and with no unique commits; it was not moved during preparation.

The three administrative commits `9ce7dcc`, `1372215`, and `c400ab9`, plus merge `a21c806` associated with PR #28, are ancestors of `origin/develop`. The public page we could access still displays "Open" in an older snapshot; the current PR object state was not confirmed because GitHub CLI is unavailable. Git history confirms the commits are present in the remote branch.

`task/performance-context-20261109` and `task/performance-20261109` point to `a21c806`, have no unique commits, and retain separate local changes. `task/admin-acceptance-9-2-20261105` is at `c400ab9`, also an ancestor of the base. `origin/VT` and `origin/feature/xano-data-model` have no unique commits. `origin/pedro` has two unique commits from 2026-09-22: six general planning documents describing the project before its current frontend and Xano workspace 151345, and a blank line in a spec that does not exist on the current base. Both commits and the branch remain preserved and were excluded because the documents are outdated relative to the current project and workspace 147717 recorded by A0.

`origin/main` is at `f244987`; local `main` is at `832f728`, 29 commits behind. `main` and `develop` have diverged. No changes were integrated into `main`.

## Prepared scope

Temporary branch `integration/sync-develop-20261110` is based on `origin/develop` (`4a7cabe`). It includes the administrative rehearsal executor restricted to synthetic tests, its guards, tests, and local A0/A1 evidence. `PENDENCIAS.md`, `README.md`, and task records were reconciled manually: the newer 10/11 records from the base were retained, local 09/11 records were preserved chronologically, and no task checkbox was closed. Administration remains 33/34; performance remains 17/37.

The Home P0 was kept out of this integration. Its four fictional-API browser cases passed. In the real-API browser run, 12 of 20 cases were recorded before a Kitsu timeout: desktop completed five pairs, with search-availability medians of 1.349 s cold and 0.778 s warm; at 390 px there was only one cold sample (3.444 s) and one warm sample (0.952 s). No 429, non-GET methods, UI errors, or horizontal overflow appeared in recorded samples. The mobile cold sample exceeded the 3 s target and there are not enough repetitions. Its code and lockfiles remain intact in the separate worktree.

The lockfiles in the original root match their checkpoint. In the performance worktree, `reflex.lock/package.json` and `package-lock.json` differ from the pre-P0 checkpoint hashes (`e52c126c...` and `c2eff921...`; current `d9f78097...` and `c42d4173...`). `package.json` is compacted and uses `^` version ranges; its origin is undetermined. No lockfile was included in this integration branch.

## Local integration validation

- Administrative executor and guard tests: 48 passed; synthetic `.invalid`/MockTransport only, no Xano calls.
- Full suite: 566 tests passed.
- `openspec validate --all --no-interactive`: 30 items passed, zero failures; existing long-requirement warnings remain.
- `reflex compile --dry`: passed in 6.562 s; the two integration-branch lockfiles were restored byte-for-byte after compilation.
- Heuristic secret scan over all 19 staged files: no findings; diff had no whitespace errors.

These checks validate the updated base and included local administrative work. They do not close integrated 9.2, validate mobile P0, or authorize remote administrative operations.

## Publication status

This branch is temporary as of this record. No commit, push, PR, or merge had been made when this evidence was drafted. Before publication, recheck that `origin/develop` has not advanced. Any PR must target `develop`; `main` remains out of scope.
