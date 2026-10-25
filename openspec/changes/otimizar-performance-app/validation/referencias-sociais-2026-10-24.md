# Referências sociais sem trabalho desnecessário — 24/10/2026

## Plano anterior à implementação

Continuação autorizada pelo usuário, mantendo funcionalidades e design.
Incremento de 7.1/7.2 e comparações locais parciais de 7.4. Preservar alterações
anteriores do cache do feed e a exclusão já presente de
`reflex.lock/package-lock.json`; não restaurar arquivos de outra rodada.

Diagnóstico estático: `_load_reference` é usado apenas por `load_feed`, mas
`_load_media` sempre transforma todas as obras em `catalog_items`, variável
pública da tela de descoberta. O feed usa `_media` para capas/títulos/edição,
`_profiles` para autores e `people` para sugestões. O seletor atual de obra do
post usa busca própria, não `catalog_items`. Preparar os cards completos custa
CPU e altera estado público sem necessidade para o feed. Não remover referências
ou a consulta paginada existente; reduzir somente a transformação redundante.

Segundo custo: `_profile_updates` sempre consulta `/media`, mesmo quando o
contrato autenticado/público do perfil já informou `interactions=[]`. Nenhum
card de atividade pode ser gerado nesse caso. Não consultar mídia para atividade
vazia; manter consulta de pessoas, estatísticas e controles de conexão existentes.
Perfil com atividades preserva o caminho original e suas falhas por seção.

Arquivos: `state/social.py`, testes de regressão, executor offline comparativo,
design/tasks/README e esta evidência. Medir cinco amostras frias/aquecidas com
5/250 obras fictícias, chamadas, transformações e tamanho JSON de `catalog_items`
(estimativa da variável, não tráfego WebSocket medido). Comparar igualdade de
posts, autores, sugestões, referências de edição, estatísticas e relações.
Medir também perfil vazio/com atividade. Usar HTTP fictício, sem Xano real.

Riscos: omitir preparação do catálogo em tela que precise dele ou deixar spinner
do perfil vazio ativo. Opção nova será interna, com padrão preservando preparação
para home/biblioteca/listas; só feed usa modo sem cards. Perfil vazio encerra
flag de atividade antes da primeira publicação e não altera `_media` existente.
Guardas de rota/conta continuam aplicáveis. Sem CSS, componentes ou contratos
remotos alterados. Rollback: retirar opção interna e restaurar job incondicional
de mídia no perfil; preservar cache do incremento anterior.

Validar regressões pertinentes, suíte, compilação seca e OpenSpec. Navegador e
API real serão registrados separadamente se executados; não encerrar critérios
integrais por resultados sintéticos. Não reiniciar servidor normal neste incremento.

## Implementação e comparação

`_load_media` aceita `prepare_catalog=False` apenas nas referências do feed:
mantém todas as obras em `_media`, sem preparar/substituir `catalog_items`.
Padrão verdadeiro preservado para home, biblioteca legada e listas. Perfis
sem atividades não criam o job `/media` e publicam atividade já concluída;
relações e estatísticas seguem independentes. Sem ampliar cache ou concorrência.

Executor reproduzível:

```powershell
.venv/Scripts/python.exe tools/social_reference_measurement.py --output <arquivo-novo.json>
```

Seis cenários (feed, perfil vazio e perfil com atividade, com 5/250 obras),
cinco amostras por cenário, fases fria/aquecida: 60 execuções por versão.
HTTP fictício de 5 ms e autenticação fictícia substituída para isolar referências.
Não são tempos de navegador ou API real.

Resultados com 250 obras:

| Cenário | Chamadas frias antes/depois | Cards extras antes/depois | Mediana fria antes/depois | Mediana aquecida antes/depois |
| --- | --- | --- | --- | --- |
| Feed | 5 / 5 | 250 / 0 | 72,721 / 57,115 ms | 7,124 / 3,274 ms |
| Perfil vazio | 3 / 2 | 0 / 0 | 40,057 / 29,970 ms | 3,341 / 2,109 ms |
| Perfil com atividade | 3 / 3 | 1 / 1 | 38,793 / 39,423 ms | 3,185 / 3,262 ms |

Contagens iguais nas cinco amostras, inclusive com 5 obras; todas as fases
aquecidas fizeram zero chamadas. Perfil com atividade conserva o trabalho
original; não houve ganho de tempo nesse cenário. Pior tempo do perfil vazio
passou de 42,945 para 59,572 ms apesar da mediana menor: não afirmar ganho
universal de latência a partir da simulação.

No feed, JSON estimado de `catalog_items` em sessão nova caiu de **294.534 para
2 bytes** (`[]`) com 250 obras e de 5.875 para 2 bytes com 5 obras. Catálogo
preexistente é preservado sem reatribuição. Isso mede uma variável, não bytes
WebSocket transmitidos; a consulta e paginação de mídia permanecem iguais.

Comparação de hashes funcionais antes/depois: **60/60 iguais**. Inclui posts,
ordem, pessoas, curtidas, IDs de referências; perfil, atividades, estatísticas,
seguidores/seguidos, flags e erros. Artefatos:
[antes](referencias-sociais-antes-2026-10-24.json) e
[depois](referencias-sociais-depois-2026-10-24.json).

## Validação

- Sete testes novos aprovados: feed com 250 referências, editor/sugestões,
  catálogo normal/per_page preservados, resposta tardia ignorada, perfil vazio
  próprio/outro/visitante e falha de pessoas sem erro/spinner de atividade.
- Três testes existentes de perfil com atividade aprovados.
- Primeira suíte: quatro expectativas antigas falharam. Perfil vazio passou
  de cinco para quatro chamadas totais incluindo login; com revalidação,
  seis para cinco. Expectativas corrigidas e fixture `references-429` recebeu
  atividade fictícia para continuar exercitando falha de mídia necessária.
  Seis testes desse executor passaram; relatórios históricos preservados.
- Suíte final: `.venv/Scripts/python.exe -m unittest discover -s tests -q`:
  **347 testes aprovados**, 20,682 s.
- `reflex compile --dry` com frontend separado em
  `.local/compile-social-references-20261024`: **aprovado**, 8,986 s.
- Compile reformatou `reflex.lock/package.json`: JSON conferido igual ao original
  e somente essa formatação gerada foi desfeita. Exclusão preexistente de
  `reflex.lock/package-lock.json` preservada.

`openspec validate otimizar-performance-app --type change` e `git diff --check`:
**aprovados** (avisos LF/CRLF em arquivos gerados).

Primeira tentativa de navegador, em
`referencias-sociais-browser-2026-10-24/result.json`: zero cenários executados;
preparação de produção falhou na escrita do cache npm fora do workspace. Log e
resultado preservados, sem atribuir falha ao app. Nova execução solicitada com
permissão de cache/rede, reutilizando frontend isolado: **8/8 cenários aprovados**,
em 1440/390px, zero erros JavaScript e sem overflow. Cobertura: editar post sem
obra, remover referência durante edição preservando ID, buscar/incluir obra em
lista sem duplicação e incluir pela ficha respeitando destino/ownership.
[Resultado](referencias-sociais-browser-rede-2026-10-24/result.json).

Build de produção isolado passou em 46 s; processo de teste encerrado pelo
executor. Navegador usa backend HTTP fictício: não comprova persistência Xano,
latência real, quota ou metas da jornada integrada. A primeira tentativa foi
preservada. Perfil vazio tem cobertura de handlers e de login/identidade nesses
cenários; perfis com atividades mantêm regressões locais anteriores.

Build npm alterou arquivos globais gerados em `reflex.lock`: manifest recebeu
prefixos `^` e formatação; lock previamente ausente foi recriado. Manifest
comparado ao original após remover somente os prefixos, com igualdade confirmada.
Saídas geradas preservadas em `.local/social-reference-build-generated/` e estado
anterior restaurado: manifest original e ausência do lock. Nenhuma atualização
de dependência faz parte desta entrega; exclusão preexistente permanece visível.

Sem reinício do servidor normal ou chamadas/mutações Xano reais. Manter 7.1–7.4 abertas por cobertura social completa,
orçamento e validação integrada ainda ausentes; estado **14/37**.
