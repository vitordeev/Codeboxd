# Feed e inclusão em listas — 22/10/2026

## Entrega

Edição captura ID, identidade da sessão e token do editor antes do primeiro
yield. O formulário envia ID/token; contexto perdido ou formulário antigo
não vira POST. Fechamento/nova publicação ficam bloqueados durante gravação,
e envio antigo repetido é descartado após salvar. Obra opcional pode ser
mantida, trocada ou removida; referência existente é preservada mesmo fora do
cache. PUT JSON/multipart mantém a identidade original e imagem não alterada.

Lista própria oferece busca por título nos quatro tipos via adaptadores
existentes TMDB/Kitsu/Open Library e catálogo local. Inclusão é explícita,
persiste obra externa quando necessário, rejeita resultado obsoleto e não
repete inclusão já confirmada. Falha conserva itens e resultados utilizáveis.

Ficha oferece “Adicionar a outra lista”, carrega apenas listas próprias
(públicas/privadas) e exige destino/confirmar. Não altera nota ou status de
biblioteca ao adicionar em lista personalizada. Guardas impedem gravação em
contexto de outra conta/ficha/lista. Atalhos de listas base preservados.

Arquivos principais: Codeboxd_main/state/social.py e pages/social.py.
Sem novas dependências, Docker, mudança de schema, publicação Xano ou limpeza
de dados históricos. PUT posts e POST itens de lista locais já possuem
autoria/db.edit e deduplicação; não foram modificados.

## Reprodução e testes locais

- Reprodução isolada da implementação anterior do HEAD, somente com mocks:
  limpar edit_post_id durante autenticação transforma edição em POST /posts.
  [Resultado](regressao-original.json). Isso comprova o caminho defeituoso;
  não é uma reprodução em conta de produção nem diagnóstico de cada duplicata histórica.
- `.venv/Scripts/python.exe -B -m unittest tests.test_feed_list_workflows`:
  **13 testes aprovados**, incluindo suspensão de sessão, imagem, perda de ID,
  submissões antigas, quatro tipos, duplicação, falha e mudança de contexto.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests`:
  **298 testes aprovados** na execução final. A rodada anterior tinha 295,
  antes de acrescentar as últimas três regressões. Avisos de 429/rede são
  cenários simulados esperados, sem restauração real de servidor nessa suíte.
- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado. O processo
  isolado subsequente também recompilou o código final e completou o build
  de produção via npm antes dos testes de navegador.
- `git diff --check`: aprovado; avisos existentes de normalização LF/CRLF
  nos locks Reflex não foram tratados como alteração de dependências.

## Navegador

Comando final:

```powershell
.venv/Scripts/python.exe -B -m tools.feed_lists_browser --output openspec/changes/corrigir-edicao-feed-e-inclusao-listas/validation/browser-fixture-app-2026-10-22 --frontend-workdir .local/frontends/feed-lists-29552
```

**8/8 cenários aprovados**: quatro por viewport (1440 e 390px). Edição sem
obra; remoção de referência durante edição; busca/inclusão/duplicata na lista
privada; inclusão da ficha em lista própria sem escrita de avaliação. Casos de
edição conferiram um PUT no ID original, zero POST e um único registro fictício.
Nenhum erro JavaScript ou overflow. Captura mobile de listas inspecionada.
[Resultado e capturas](browser-fixture-app-2026-10-22/result.json).

O runner usa app_module_import alternativo apenas no ambiente do processo de
teste: páginas/estado reais, busca e APIs fictícias. Frontend/dependências
isolados em .local/frontends, produção em 3031 e fixture em 3040; processos
do teste encerrados ao final. Servidor normal não foi iniciado nem reiniciado.

As duas primeiras tentativas de build estão preservadas em
[browser-2026-10-22](browser-2026-10-22/result.json) e
[browser-npm-2026-10-22](browser-npm-2026-10-22/result.json). O proxy usado para
bloquear provedores também bloqueou npm; a segunda tentativa manteve o erro
403 do registro apesar do ajuste específico do npm. O runner final substitui
a busca por fixture no módulo de teste, sem proxy nem mudança no app normal.
Não são falhas de gravação dos fluxos implementados.

## Limites e encerramento

Sem login de usuário real, envio de posts/listas remotos ou verificação de
latência/quota nesta rodada. Os testes cobrem lógica e navegador com registros
fictícios; não comprovaram integração autenticada com o Xano atual. Não houve
alteração de backend a publicar. Ativar código em um processo normal já aberto
exige reinício conforme a skill de processos; não declarar que ele foi atualizado.

Documentação central reconciliada e checklist 6/6. Change validada pelo
OpenSpec e mantida concluída/ativa, sem sincronização ou arquivamento automáticos.
Uma alteração independente (incomplete=true) apareceu no relatório histórico
de recuperação de senha; foi preservada sem inclusão no escopo desta change.

Encerramento posterior em 22/10, autorizado pelo usuário: três requisitos
sincronizados em `social-feed` e `user-lists`, preservando os demais requisitos
e cenários existentes. Comparação pós-merge aprovada; 19 specs e a change
validadas. Arquivada em `2026-10-22-corrigir-edicao-feed-e-inclusao-listas`.
O estado ativo mencionado acima descreve o momento anterior ao arquivamento.
