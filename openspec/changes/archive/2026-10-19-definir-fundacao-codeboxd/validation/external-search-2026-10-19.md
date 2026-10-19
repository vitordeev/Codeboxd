# Busca externa — 19/10/2026

## Escopo e resultado

Revalidação da tarefa 5.2 usando `catalog.search`, o serviço de busca da aplicação,
sem mocks nas consultas reais e sem fallback para o catálogo Xano. Todas as quatro
consultas retornaram resultados sem avisos de erro. Os itens retornados preservam
tipo, fonte, ID externo e chave de identidade.

| Tipo | Provedor | Consulta | Resultados | Exemplo confirmado |
| --- | --- | --- | ---: | --- |
| Filme | TMDB | Matrix | 20 | Matrix — `tmdb:movie:603` |
| Série | TMDB | Breaking Bad | 3 | Breaking Bad — `tmdb:series:1396` |
| Anime | Kitsu | Cowboy Bebop | 4 | Cowboy Bebop — `kitsu:anime:1` |
| Livro | Open Library | Duna | 7 | Duna — `openlibrary:book:OL35253654W` |

Execução concluída às 19:55 UTC, com código de saída 0.

## Testes automatizados

36 testes passaram: 14 de catálogo, 14 de Kitsu e 8 de relevância.
Cobrem adaptadores dos quatro tipos, identidade externa, paginação Kitsu,
falhas parciais, cache, compatibilidade de registros Jikan e filtragem de títulos.
As falhas HTTP e de conexão exibidas pelos testes Kitsu são cenários simulados
esperados, não falhas desta execução.

Comandos executados na raiz do repositório:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_catalog.py -v
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_kitsu.py -v
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_search_relevance.py -v
.venv/Scripts/python.exe -B openspec/changes/definir-fundacao-codeboxd/validation/search_live.py
```

O script reutiliza a configuração local via `dotenv`, sem exibir credenciais.
Consulta somente os provedores externos; não cria nem altera registros remotos.

## Conciliação com o histórico

A indisponibilidade da Jikan registrada em setembro deixou de bloquear a busca:
o código usa Kitsu para animes. A validação da migração em `docs/KITSU.md`
registra busca, detalhes e navegação real em 23/09/2026. Esta rodada confirma
novamente a busca pelo serviço atual para os quatro tipos de mídia.

## Limites

Resultados refletem a disponibilidade dos provedores no momento da execução.
Os testes automatizados usam mocks; as quatro consultas da tabela são reais.
Esta rodada não recompilou nem iniciou Reflex, não repetiu testes de navegador,
não validou o backend Xano e não constitui uma revalidação integral da fundação.
A tarefa 11.7 permanece aberta para a etapa de validação final da mudança.
