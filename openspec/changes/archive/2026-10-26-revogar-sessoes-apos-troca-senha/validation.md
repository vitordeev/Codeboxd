# Validação final — 26/10/2026

## Contratos e publicação Xano

Planejamento criado antes da implementação, como dependência da tarefa 2.3 de proteger-credenciais-expostas, após autorização do usuário para concluir o trabalho. Nenhuma outra change funcional foi ampliada.

- Export com env=false e records=false, 78 documentos, backup privado em .local/session-revocation/baseline.xs. Nenhum registro de usuário ou segredo de workspace foi persistido no OpenSpec.
- Inventário completo: 39 queries autenticadas e três emissores. A primeira expressão reconhecia somente nomes entre aspas; foi corrigida antes da geração/publicação para também reconhecer identificadores simples. remote-inventory.json é a cobertura final.
- Delta: user.session_version default zero; função Security/require_current_session; claims e guardas em 42 queries existentes. O /likes local também recebeu a guarda no código, mas não foi publicado incidentalmente, pois não existia no workspace exportado.
- Dry-run HTTP 200 aprovado: preview.json, sem parse errors, exclusão ou truncamento. Nenhum workspace env ou records incluído.
- Publicação HTTP 200. A resposta de aplicação não tem operations como o dry-run; o executor inicial parou por essa diferença. A mutação não foi repetida. Export posterior comprovou publicação: 39 rotas protegidas, 40 chamadas de guarda (reset revalida duas vezes), versão no schema, uma única função adicionada e nenhum documento alheio alterado. deployment.json foi reconciliado com essa evidência e published-inspection.json contém passed=true.
- GUID da função publicada reconciliado no arquivo local. Arquivos locais mantêm o restante de sua lógica, inclusive verificação de papéis/propriedade. Não houve reescrita de catálogos, papéis ou conteúdo social.

## Testes locais

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests -q
```

Resultado: **392 testes, OK**, exit 0. Logs de falhas de provedor durante a suíte pertencem aos cenários simulados; não são medições reais de disponibilidade.

Os quatro testes específicos em test_session_revocation.py executam o JavaScript real da guarda via Node com onze combinações de versão/finalidade/tipo, verificam todas as rotas locais e a revalidação sob bloqueio. Rodadas direcionadas: 14 testes de autenticação, sete de recuperação, quatro da guarda e quatro do scanner aprovados. Nenhuma dependência foi adicionada.

## API real

tools/validate_session_revocation.py usa contas de teste já autorizadas. Tokens e substitutos ficam somente em .local ignorado.

- legacy-capture.json: quatro sessões válidas capturadas antes da implantação; depois, todas retornam 401.
- remote-validation.json: **29 checks reais aprovados**, incluindo leitura e mutação com tokens legados, login novo, membro sem acesso administrativo, duas alterações concorrentes com um sucesso/uma rejeição, senha anterior rejeitada e sessão de outra conta preservada.
- Recuperação: invocação do gerador privado existente por Metadata API, sem chamar o endpoint de envio de e-mail. Código consumido normalmente; token temporário rejeitado em identidade, social, admin e mutação social; alteração de senha permitida uma vez, reuso 401 e sessões normais anteriores revogadas. Não comprova entrega de e-mail nem fecha a change recuperar-senha-codigo-6-digitos.
- A primeira validação encontrou rate limit antes da alteração concorrente. Foi retomada com chamadas espaçadas a três segundos; nenhuma mutação sofreu retry automático. Os candidatos da corrida foram salvos privadamente antes das requisições e o vencedor foi gravado em .local/credential-rotation/account-01.json antes das verificações seguintes. Não restaurar senhas expostas.
- unusable-account-inspection.json: quinta identidade histórica A.02 ausente na tabela atual, comprovada por leitura paginada completa, uma página; registros apenas em memória, nenhum usuário apagado. As quatro contas existentes mantêm senhas novas válidas.
- Mutações de rejeição usaram /posts/0, sem alvo existente; não criaram nem removeram conteúdo social. Foram alterados somente o schema de sessão, senhas/versões da conta controlada e estados normais de recuperação/auditoria.

## Navegador real

tools/check_session_revocation_browser.py no Edge headless contra a aplicação .venv/produção em localhost:3030: token legado redirecionado ao login; novo login redirecionado à rota existente /conta; biblioteca e botão Sair visíveis, evidenciando sessão autenticada. browser-validation.json passou.

A primeira expectativa do teste assumia incorretamente redirecionamento para a home; o código existente usa /conta. Corrigido somente o teste, sem mudar o fluxo da aplicação. Nenhum screenshot, cookie ou formulário privado foi persistido no OpenSpec.

## Fechamento e limites

Mudança implantada no Xano e validada, não apenas código local. Tokens legados exigem novo login. Logout continua encerrando somente o armazenamento local; revogação global por logout não foi implementada, conforme exclusão planejada. Não foram usados Docker, reescrita Git, git add, commit ou push no projeto. Changes concluídas permanecem sem arquivamento automático.

Revisão de privacidade dos relatórios e arquivos modificados deve passar antes da entrega; scripts de verificação e comandos manuais constam nos artefatos da change de credenciais e em manual-git.md.

Fechamento executado: 96 arquivos novos/modificados revisados sem achados; auditoria dos relatórios das duas changes contra segredos atuais, históricos, senhas substitutas e sessões capturadas aprovada. Ambas as changes passaram em `openspec validate ... --type change`; `git diff --check` sem erro. Checklists finais: credenciais 9/9, sessões 6/6. Branch develop, upstream origin/develop, referências locais 0/0. Nenhum arquivo preparado no índice do projeto e nenhum commit/push executado.
