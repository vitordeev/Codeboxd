# Commit e push manuais

Branch conferida: develop. Upstream: origin/develop. Referências locais estavam alinhadas (0 à frente, 0 atrás); isso não substitui consultar o remoto no momento do push. Nenhum add, commit ou push foi executado no repositório pelo agente.

Executar na raiz do Codeboxd, em PowerShell. Os diretórios abaixo contêm as alterações de segurança revisadas nesta rodada; conferir status antes de preparar arquivos se houver trabalho adicional posterior.

```powershell
git status --short
git add -- .gitignore openspec xano tools tests
.\.venv\Scripts\python.exe -B tools/check_staged_secrets.py
if ($LASTEXITCODE -ne 0) { throw 'Verificação de segredos falhou; revise antes de continuar.' }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Revise os erros do diff antes de continuar.' }
git diff --cached --stat
git commit -m "fix(auth): revogar sessoes apos troca de senha e proteger credenciais"
if ($LASTEXITCODE -ne 0) { throw 'Commit não concluído.' }
git push origin develop
```

O scanner verifica o conteúdo preparado no índice. Não incluir .env, .local ou arquivos privados manualmente com force. Não há necessidade de force-push ou reescrita de histórico para estas alterações. Alterações Xano já foram publicadas e validadas; push Git registra os contratos e evidências, não executa a publicação Xano.
