## 1. Configuração de publicação

- [x] 1.1 Documentar arquitetura de frontend estático e backend separado, requisitos de URLs, variáveis e passos de deploy; conferir instruções em `docs/DEPLOY_NETLIFY.md`.
- [x] 1.2 Adicionar `netlify.toml` e build reprodutível; `python -m py_compile tools/netlify_build.py` passou, e `python tools/netlify_build.py` sem URL terminou com o erro de configuração esperado (código 2).

## 2. Pacote de distribuição

- [x] 2.1 Implementar `tools/package_netlify.py` com allowlist e bloqueio de diretórios/arquivos locais; conferir os arquivos de configuração e aplicação presentes no pacote.
- [x] 2.2 Ajustar `.gitignore`; `git check-ignore` confirmou `.env`, `.local`, uploads, `.web`, `.states`, `dist` e `.netlify`, preservando arquivos-fonte.
- [x] 2.3 Gerar `dist/Codeboxd-Netlify-Source.zip` (41 entradas, 1.985.287 bytes); `ZipFile.testzip()` confirmou integridade, lista proibida ficou vazia e os arquivos obrigatórios estão presentes.

## 3. Validação e limites

- [x] 3.1 `openspec validate preparar-deploy-netlify --type change` passou e `git diff --check` não apontou erros de whitespace (apenas avisos CRLF/LF dos locks já existentes).
- [ ] 3.2 Exportar/publicar frontend e validar jornadas somente após receber a URL pública do backend; manter pendente enquanto a dependência não existir.
