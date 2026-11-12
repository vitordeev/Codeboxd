# Busca administrativa: parâmetros reais — 27/10/2026

Continuação solicitada pelo usuário após o commit da rodada anterior. Git limpo;
change ativa gerenciamento-website, 21/34. Vínculo: tarefas 3.1 e 9.1.

## Plano antes da alteração

Adicionar modo de diagnóstico ao executor de leituras administrativas existente,
reutilizando login manual legítimo, ID admin aprovado (14), intervalo, limite de
requisições, interrupção em 429 e relatórios sem dados privados. Comparar por API
real: parâmetros omitidos, user_id zero explícito, filtros de texto vazios e
busca pelo nome/username da própria conta. Capturar somente total, número de itens
e quantidade de correspondências; não exportar termos, nomes, tokens ou respostas.
Nenhuma mutação, publicação, promoção de conta ou reinício do app nesta etapa.

Usar os resultados para preparar uma correção delimitada, com regressões e
dry-run antes de qualquer publicação. Manter o checklist aberto até comprovar
os critérios reais. O interpretador isolado anterior não prova consulta ao banco
real e não será usado como critério de correção.

## Comparação real

`busca-parametros-api-2026-10-27.json`: login manual confirmado; 11 requisições
HTTP 200, 19 checks de execução/contrato aprovados. Consulta por ID encontra
a própria conta; os oito cenários sem ID positivo retornam total zero,
inclusive zero explícito e todos os filtros vazios. Assim, explicitar defaults
no cliente não corrige o defeito. `search_acceptance_passed: false`.

Próxima comparação isolada usará uma tabela fictícia exclusiva no código do
interpretador, com três registros sintéticos e sem referências à tabela user
real. Comparar a expressão original com busca separada por condicional. Nenhum
push/multidoc de publicação; só endpoint debug já usado. Esses resultados serão
testes simulados no interpretador Xano, não aceitação dos dados reais.

## Reprodução e correção delimitada

`busca-fixture-xano-2026-10-27.json`: tabela fictícia com três registros.
Consulta original retorna zero em quatro cenários; consulta sem o ramo numérico
retorna 3/1/2/0 para vazio/username/trecho/ausente. Controle por ID retorna um.
A expressão que combina escolha do modo por ID com OR dentro de `where` está
reproduzida como origem do defeito, sem depender de dados privados.

Preparar apenas `xano/api/codeboxd/admin_users_GET.xs`: escolher o modo por
`conditional` antes de `db.query`; ramo numérico filtra ID e ramo textual filtra
nome/username. Manter autorização, papel/estado, projeção sem segredos, ordenação
e paginação. Validar a consulta extraída do arquivo de produção no interpretador
com fixtures, depois testes locais e dry-run de um endpoint. Rollback: arquivo
anterior preservado no backup local da publicação. Publicação é etapa separada,
após revisão do delta, e exige confirmação final no fluxo aplicável.

## Implementação candidata

O teste da expressão extraída do arquivo candidato mostrou que a escolha por ID
não era o único problema. Foram separados três modos (ID, texto, sem termo),
com alternativas de nome/username distribuídas e os filtros de papel/estado
aplicados em ambas. Teste direto com `~`: 13/14 cenários passaram, mas caixa
alta falhou. A gramática da extensão oficial Xano instalada identifica `~` como
regex e aceita `includes`; adotado `includes`, com busca sem diferenciar caixa.
Referências primárias consultadas: [consulta/paginação](https://docs.xano.com/xanoscript/function-reference/database-operations),
[condicionais](https://docs.xano.com/xanoscript/function-reference/data-manipulation/conditionals)
e [operadores textuais](https://docs.xano.com/the-function-stack/functions/database-requests/query-all-records).

Teste direto com `includes`: 15/16 passaram, com `_` tratado como curinga.
Versão atual escapa barra invertida, `%` e `_` antes de usar o valor em includes.
A matriz final cobre 18 cenários. Resultados intermediários reprovados são
preservados; não constituem aceite. Não houve publicação de candidatos.

Resultado final: [busca-candidata-literal-xano-2026-10-27.json](busca-candidata-literal-xano-2026-10-27.json),
**18/18 aprovados**, interpretador Xano com dados sintéticos. Valida ID, nome,
username, caixa alta, trecho, vazio, ausência, caracteres literais, filtros
combinados, identidade, projeção permitida, totais e três páginas com next_page.
O executor extrai os inputs, ramos de consulta e resposta do arquivo candidato;
somente a autorização é retirada do cenário sintético. Autorização e dados
reais exigem o probe autenticado após publicação.

Backup privado do endpoint publicado salvo em
`.local/admin-search-fix-20261027/before-users-GET.xs`, sem registros/env.
SHA-256: `63757ba757e3cc7e12eb14e7e86ab0ad3270fc31ba251d6e57a8f36ef5237bad`.

## Validação local e limites

- Suíte completa após os dois testes novos do diagnóstico: **415 testes aprovados**
  em 16,645 s. Testes simulados de aplicação/instrumentação, sem aceite remoto.
- Após ampliar a conferência real para buscas em maiúsculas: **33 testes admin
  aprovados**. A ferramenta mantém termos e dados privados fora dos relatórios.
- Dry-runs intermediários limitados reconheceram exatamente uma atualização:
  `admin/users GET`, sem tabelas, registros, variáveis ou outros endpoints.
- `openspec validate gerenciamento-website --type change` e `git diff --check`:
  aprovados; avisos de conversão LF/CRLF preservados.
- Sem alterações de código Reflex, build ou reinício do app normal. Tarefa 3.1
  continua aberta até publicação autorizada e busca real/paginação comprovadas;
  a change permanece 21/34.

## Publicação preparada para revisão

Dry-run final da versão com escape, aprovado: exatamente uma atualização,
`admin/users GET`. Sem tabelas, dados, env ou outros endpoints no delta.

```powershell
xano workspace push -p default -d xano -w 147717 --include api/codeboxd/admin_users_GET.xs
```

Publicação ainda não executada: a tarefa 9.3 exige que alterações remotas não
sejam publicadas automaticamente. Após confirmação do usuário, executar o push
restrito, repetir dry-run sem delta e rodar o probe completo com novo login manual:

```powershell
.venv/Scripts/python.exe -B -m tools.admin_reads_remote --output openspec/changes/gerenciamento-website/validation/leituras-admin-apos-correcao-2026-10-27.json
```

Rollback, se necessário: usar apenas o arquivo anterior no diretório privado
de backup indicado, primeiro com dry-run e revisão; não importar registros.
Isso restaura o endpoint anterior, incluindo o defeito conhecido, sem apagar dados.

## Continuação autorizada

Usuário respondeu "prossiga com as atualizacoes" ao pedido de publicação limitada
e validação real. Autorização cobre GET /admin/users no workspace 147717 e
repetição das consultas com login admin manual. Conferir o remoto contra o
backup antes de publicar; preservar endpoints, registros e env fora do delta.
Sem solicitar novamente aprovação funcional para a mesma atualização.

## Publicação e aceite real concluídos

- Git limpo antes da continuação; endpoint remoto conferido por exportação
  sem registros/env: correspondia exatamente ao backup revisado.
- Prévia interativa confirmou um único UPDATE, `admin/users GET`. Após
  confirmação dentro do escopo autorizado, CLI retornou **Pushed 1 documents
  to workspace 147717 from xano in 2.7s**. Transação padrão preservada;
  sem `--force`, `--sync`, registros, env ou mudanças de privilégio.
- Dry-run posterior, com o mesmo include: **No changes to push**.
- [Resultado real](leituras-admin-apos-correcao-2026-10-27.json): **79/79 checks
  aprovados**, 34 requisições incluindo login e /auth/me; nenhum 429. Credenciais
  digitadas somente no formulário local, identidade admin ativa ID 14 confirmada
  pelo servidor. Senhas, token, termos e corpos de resposta não foram exportados.
- Busca de usuários comprovou ID exato, nome/username reais, versões em caixa
  alta com os mesmos totais, ausência de resultado, estados active/disabled,
  papéis member/admin, combinação de ID/papel/estado, rejeição de filtros
  inválidos com 400, formato/continuação paginada sem IDs repetidos e projeção
  sem email/senha/token/segredos. Caracteres literais e três páginas completas
  seguem também cobertos pelos 18 cenários sintéticos do candidato publicado.
- Leituras de dashboard, quatro tipos de catálogo e filtros de reports também
  passaram com os dados disponíveis. Não comprovam contagens independentes,
  todos os estados possíveis, mutações/auditoria ou interface completa.
- Tarefa **3.1 concluída**. Administração passa a **22/34**, com 12 abertas.
  2.1–2.3, 3.2–3.3, 4.1–4.2, 5.2–5.4 e 9.1–9.2 continuam pendentes.
  Performance e recuperação de senha não tiveram seus critérios alterados.
- Sem alterações de código Reflex ou processo normal; nenhuma compilação
  adicional necessária nesta continuação de publicação/validação. Registros
  de negócio preservados; login pode gerar a auditoria normal de autenticação.
