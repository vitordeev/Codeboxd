# Ambiente de desenvolvimento

Ambiente canônico desde 13/10/2026: `.venv`. O `venv` anterior permanece no disco para compatibilidade; não é necessário usar ambos.

## Preparação no Windows

Na raiz do projeto, verificar primeiro se `.venv\Scripts\python.exe` existe. Se não existir, criar com Python 3.10 ou superior:

```powershell
python -m venv .venv
```

Instalar/verificar as dependências:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s tests -q
.venv\Scripts\python.exe -m reflex compile --dry
```

Executar pela raiz garante que configuração e imports sejam resolvidos corretamente. Não executar `reflex init` de novo para corrigir dependências deste projeto existente.

Dependências diretas fixadas: Reflex 0.9.11.post1, httpx 0.28.1 e python-dotenv 1.2.3. A instalação verificada usa Python 3.14.6 no Windows. Dependências transitivas continuam resolvidas pelo pip; isso não equivale a um lock integral nem ao teste da imagem Linux/Python 3.12.

Configuração privada fica em `.env`, a partir de `.env.example`. Não copiar valores reais para documentação, comandos compartilhados ou Git. Tanto `.venv` quanto `venv` são ignorados pelo Git.

## Execução

Incidente de rede em 20/10: iniciar o servidor pelo ambiente restrito do agente
pode produzir HTML local válido e falhas WinError 10013/ConnectError em todos os
provedores. Usar terminal normal ou execução de processo explicitamente aprovada
com acesso à rede. Depois de restaurar o app, conferir uma seleção real e a UI;
HTTP 200 estático sozinho não comprova integração. restore_normal_app agora
recusa substituir processos se o HEAD público de conectividade falhar, e o
executor performance_continuation_browser verifica isso antes de mudar frontend.
[Evidência](changes/otimizar-performance-app/validation/tmdb-rede-restaurada-2026-10-20.md).

Seguir a skill `reflex-process-management`; o modo padrão do projeto é produção, com log:

```powershell
.venv\Scripts\python.exe -m reflex run --env prod --single-port 2>&1 | Tee-Object -FilePath reflex.log
```

Consultar o log para a porta efetiva. Esse modo não faz hot reload; reiniciar o processo da aplicação para incorporar alterações. Os testes de correção não iniciam servidor automaticamente.

## Segurança do histórico

Retirar arquivos privados do índice preserva as cópias locais e evita novos commits desses arquivos; não remove commits antigos. Nesta revisão, o `.env` consta de commit contido na referência local de `origin/main`; arquivos de contas `.local/` também estavam rastreados. Revisar/rotacionar chaves expostas e contas de teste pelo procedimento seguro dos provedores. Não reescrever histórico compartilhado sem coordenar com a equipe.

## Execução sem Docker e imagens locais

Por decisão explícita do usuário, executar localmente com `.venv`, sem adicionar, iniciar ou usar Docker nesta etapa. Os ajustes Docker desta rodada foram revertidos; os arquivos de preparação anteriores permanecem apenas como histórico.

Banners são gravados no diretório local `uploaded_files/` (ou `REFLEX_UPLOADED_FILES_DIR` quando configurado). Preservar e fazer backup desse diretório: ignorá-lo no Git não é backup. A URL de banner enviada ao Xano é concreta, construída pelo endpoint configurado do backend.

Hospedagem, migração de arquivos e escolha de armazenamento são uma etapa futura, quando solicitada.

Referência do diretório e da URL de upload: [documentação Reflex](https://reflex.dev/docs/library/forms/upload/).

## Backup e validação de navegador

Criar snapshot sem sobrescrever cópias anteriores:

```powershell
.venv\Scripts\python.exe tools/backup_uploads.py
```

O ZIP e seu manifesto ficam em `.local/backups/`, com CRC/SHA-256 conferidos.
Para diretório personalizado, usar `--source`. Copiar os backups para armazenamento
externo escolhido pelo usuário quando disponível; uma cópia no mesmo disco não
protege contra perda do disco. [Entrega P.3](validation/backup-uploads-2026-10-13.md),
commit `f93287e`.

Ferramentas de browser são opcionais, separadas em `requirements-dev.txt`
(Playwright 1.64.0 instalado no `.venv`; Edge headless usado nesta rodada):

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

No teste desta rodada, Reflex rodou em produção na porta única 3030. Em
`--single-port`, frontend/backend devem ter o mesmo valor explícito:

```powershell
.venv\Scripts\python.exe -m reflex run --env prod --single-port --frontend-port 3030 --backend-port 3030 2>&1 | Tee-Object -FilePath .local/reflex-validation.log
```
