# Correções operacionais — 13/10/2026

## Resultado

Correções locais aplicadas e verificadas. 113 testes passaram (106 anteriores e 7 novos); compilação Reflex passou no ambiente canônico `.venv`. `pip check` não encontrou requisitos incompatíveis. O usuário decidiu continuar sem Docker. Os ajustes desta rodada foram revertidos e o teste de recriação foi retirado do escopo, sem ser contado como entrega concluída.

## Por tarefa

| ID | Alteração/evidência | Estado |
| --- | --- | --- |
| 1.1 | `.gitignore` protege configuração, ambientes, `.local`, `.web`, estados, uploads, caches e logs; 441 entradas retiradas do índice com cached; hashes dos 434 arquivos existentes preservados imediatamente após a operação; nenhum ignorado rastreado | Concluída |
| 1.2 | `.env` e arquivos de contas locais constam do commit `aed4810`, contido em `origin/main` conforme referências locais; nenhum valor foi impresso ou copiado para o relatório | Diagnóstico concluído; tratamento de credenciais externo pendente |
| 2.1 | `.venv` instalada com Python 3.14.6, Reflex 0.9.11.post1, httpx 0.28.1 e python-dotenv 1.2.3; dependências diretas fixadas; comandos em `openspec/AMBIENTE.md`; pip check passou | Concluída |
| 2.2 | Mensagens usam Unicode real; transporte multipart, erros HTTP, rede e JSON inválido cobertos por 4 testes | Concluída |
| 2.3 | URL de banner construída pelo endpoint configurado do backend, não Var de frontend; 3 testes verificam URL/prefixo, arquivo, limpeza após rejeição e ownership | Concluída |
| 3.1 | Volume `app_uploads`, diretório `/app/uploaded_files`, variável Reflex e dono app preparados; `docker compose ... config --no-env-resolution --quiet` passou sem precisar de `.env.production`; backup/migração documentados | Histórico: ajuste revertido por decisão do usuário |
| 3.2 | `docker version` falhou dentro e fora do sandbox: pipe do Docker Engine ausente | Retirada do escopo por decisão do usuário |
| 4.1 | Suíte 113/113, compilação e pip check passaram; OpenSpec estrito aprovou 18 itens ativos/consolidados e duas arquivadas | Concluída |
| 4.2 | Contexto, pendências, relatório e checkpoints atualizados; 63 links locais em 66 documentos conferidos sem erro naquela rodada; diff passou | Concluída |

## Comandos executados

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*upload*.py' -v
.venv\Scripts\python.exe -m unittest discover -s tests -q
.venv\Scripts\python.exe -m reflex compile --dry
docker compose --env-file deploy/production.env.example config --no-env-resolution --quiet
docker version --format '{{.Server.Version}}'
```

A instalação inicial foi bloqueada por rede no sandbox; foi repetida com acesso autorizado e terminou com sucesso. A configuração Compose terminou com código zero, embora o Docker CLI tenha mostrado avisos de leitura de configuração pessoal no sandbox. A consulta de Engine fora do sandbox confirmou serviço ausente, não erro do aplicativo.

## Preservação e limites

Saída estruturada: [results-2026-10-13.json](results-2026-10-13.json). Depois dos testes, 301 arquivos privados/auxiliares (incluindo `.env` e banners antigos) também foram conferidos e permaneceram intactos. Contagens de links/documentos representam a rodada registrada, antes dos links finais acrescentados a este relatório e ao checklist.

`git rm --cached` prepara remoções do índice, sem apagar os arquivos locais. Não houve commit, push nem reescrita de histórico. As sete entradas `.states` já não existiam antes desta correção. Logs/caches/build podem ser regenerados pela compilação; a preservação por hash foi conferida antes dessa execução.

A limpeza atual não elimina credenciais de commits antigos. É necessário revisar/rotacionar chaves expostas e tratar contas de teste pelo procedimento seguro dos provedores. Nenhuma rotação ou alteração de conta foi executada. Não copiar valores antigos do histórico para relatórios.

A proposta de volume foi cancelada e seus ajustes revertidos. A execução atual usa `.venv` e armazenamento local, sem Docker; backup de arquivos e eventual hospedagem são tópicos separados. Testes de banner usam API simulada e arquivos temporários; não equivalem a upload Xano ou navegador real.

Referência para diretório de upload e URL backend: [documentação Reflex](https://reflex.dev/docs/library/forms/upload/), conferida também no código instalado 0.9.11.post1.

## Decisão posterior do usuário — execução sem Docker

O Docker Desktop chegou a ser iniciado para tentar completar o teste; a consulta retornou Engine 29.4.1. Antes de executar qualquer teste de contêiner, o usuário pediu continuar sem Docker. O Desktop foi encerrado com `docker desktop stop`, e o diff de Dockerfile/Compose voltou a zero. Não houve build, criação de volume nem execução de contêiner nesta correção.

Os IDs 3.1/3.2 foram retirados do checklist ativo e do contrato delta, preservados como histórico. A change tem 7/7 tarefas do escopo local concluídas e aguarda arquivamento. Preferência registrada no AGENTS.md, configuração/contexto OpenSpec e documentos de retomada.
