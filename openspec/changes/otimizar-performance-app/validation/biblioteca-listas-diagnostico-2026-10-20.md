# Diagnóstico simulado de biblioteca/listas — 20/10/2026

## Escopo aprovado e execução

Usuário autorizou criar cenários simulados, testes e registros OpenSpec para
coleções pequenas/grandes, lentidão, falhas e listas padrão ausentes. Criados
`tools/library_lists_performance_scenario.py` e dez testes em
`tests/test_library_lists_performance_scenario.py`. Código de produto não alterado.
Não houve reinício, navegador, conta real ou tráfego externo nesta rodada.

Executor usa `SocialState.visit`, loaders e transporte HTTP reais com clientes
forçados a MockTransport. Toda resposta e mutação de listas é fictícia e
restrita a estruturas em memória; não criar ou reparar listas reais ao reproduzir
o script. Autenticação é simulada, sem POST login; cada amostra inicia estado
novo com token fictício e exige a primeira GET `/auth/me`.

```powershell
.venv/Scripts/python.exe -B -m tools.library_lists_performance_scenario --samples 5
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_library_lists_performance_scenario.py -v
```

## Dados e contagens

18 cenários × cinco amostras = 90 execuções, com resultados detalhados em
[biblioteca-listas-diagnostico-2026-10-20.json](biblioteca-listas-diagnostico-2026-10-20.json).
Tamanho N significa N mídias, N perfis e N interações; para listas, N próprias
personalizadas + duas padrão + N públicas de outra conta fictícia. Paginação de
100 itens por resposta reproduz os contratos locais, sem afirmar que a versão
remota seja idêntica. Títulos e dados de fixture não representam dados reais.

| Cenário | Biblioteca | Listas |
| --- | --- | --- |
| Vazio (sem registros; listas padrão existentes) | 4 chamadas | 5 chamadas |
| Pequeno (N=5) | 4 chamadas; 5 obras | 5 chamadas; 12 listas |
| N=100 | 7 chamadas; 100 obras | 9 chamadas; 202 listas |
| N=250 | 10 chamadas; 250 obras | 13 chamadas; 502 listas |
| Segunda visita rápida, N=5 | 0 chamadas adicionais | 1 chamada adicional para listas públicas |
| Perfis retornam 429 | 3 chamadas; nenhuma obra carregada | 3 chamadas; nenhuma lista carregada |
| Catálogo retorna 429 | 3 chamadas; nenhuma obra carregada | 3 chamadas; nenhuma lista carregada |

Listas sem padrões: oito chamadas, incluindo dois POST simulados. Lista padrão
legada/corrompida: nove chamadas, incluindo PUT de reparo, consulta de itens e
DELETE da lista legada vazia, tudo apenas no fixture. Isso confirma que abrir
a página pode disparar gravações no comportamento atual.

## Gargalos comprovados no cenário

1. `_load_reference` consulta catálogo e pessoas antes de biblioteca/interações
   ou diretório de listas. Biblioteca e essas partes de listas não usam os perfis.
   A falha dessa consulta impede carregar as informações principais.
2. Injetar 50 ms em perfis atrasou as telas: mediana de 72,859 ms para biblioteca
   e 77,169 ms para listas, contra 9,027/10,043 ms nos pequenos sem atraso.
   São tempos sintéticos, não latência real ou SLA; o teste de precedência
   confirma que a consulta de interações começa após terminar perfis.
3. `_request_pages` percorre coleções inteiras antes da apresentação. Com 250
   obras, todas foram carregadas, embora só 20 apareçam inicialmente. “Mostrar
   mais” passou a 40 sem nenhuma chamada adicional. IDs permaneceram únicos.
4. Uma resposta cheia de 100 itens exige página vazia adicional para descobrir
   o fim, pois os contratos locais retornam listas sem metadados de paginação.
5. GET `/lists/public` não participa do cache atual; repete na segunda visita.
   GET `/lists` é reutilizado entre preparação dos padrões e listagem quando
   não há gravação. Criações/reparos invalidam o cache e provocam releitura.

## Validação e limites

Dez testes passaram: contagens pequenas/grandes, integridade/IDs únicos,
mostrar mais local, página extra na fronteira, espera por perfis, falha de
perfis, criação/reparo simulados e comportamento de revisitas. Em falhas,
mensagem presente e busy liberado. Aviso preexistente de parse do `.env` foi
emitido; arquivo privado não foi exibido nem alterado.

Nenhuma mudança Reflex para compilar; somente ferramenta, testes e documentação.
Dados reais, navegador, rede, imagens, escala de conta e quota Xano não foram
medidos. A tarefa 6.1 permanece aberta até proposta aprovada; demais tarefas
da etapa continuam pendentes. Preservar este resultado ao medir futuras mudanças.

## Primeira intervenção proposta — aguarda aprovação

Retirar somente a consulta de pessoas dos loaders de biblioteca e listas,
mantendo mídia, identidades, listas padrão e comportamento das ações existentes.
Arquivos: `Codeboxd_main/state/social.py`, cenários/testes correspondentes e
registros da change. Expectativa no cenário pequeno: biblioteca 4→3 chamadas
e listas 5→4; com 250 perfis, evitar três chamadas de paginação em cada tela.
Verificar que 429 de perfis não afeta essas telas e que obras, listas públicas/
privadas, media select e preparação de padrões permanecem corretos. Compilar
após alterar código. Rollback limitado aos loaders e testes dessa intervenção.

Paginação na origem, carga progressiva do diretório e preparação de padrões
somente quando necessária são próximas intervenções candidatas, dependentes
de proposta própria. Não absorver essas mudanças na primeira correção.
