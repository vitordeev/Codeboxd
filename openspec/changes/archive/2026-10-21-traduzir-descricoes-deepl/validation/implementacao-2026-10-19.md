# Tradução DeepL — 19/10/2026

Usuário escolheu delegar a seleção da API e forneceu chave após a escolha DeepL.
Credencial configurada somente no .env local, não rastreado. Exemplo público vazio.

## Implementação local

- Serviço `Codeboxd_main/services/translation.py`: POST oficial Free/Pro, destino
  PT-BR, timeout de oito segundos e sem retry automático. Nenhuma dependência nova.
- Fichas Kitsu/Jikan e Open Library traduzem a descrição, preservando identidade,
  título e demais metadados. TMDB continua com pt-BR nativo, sem chamada DeepL.
- Cache SQLite `.local/description-translations.sqlite3`, por hash do conteúdo,
  versão e destino; limitado a 10 mil entradas. Acesso em thread e serialização
  de misses por event loop para evitar POSTs duplicados concorrentes.
- Ausência de chave, vazio, mais de 20 mil caracteres, falhas de rede/HTTP/formato
  ou cache preservam o original. Backoff 60s em falhas e 15min para 403/456.
- Português identificado pela resposta DeepL conserva o original e entra no cache.
  Essa primeira chamada de detecção também consome cota; não há detecção local.
- Buscas e home não disparam tradução; ela acontece sob demanda na ficha.

## Testes locais

- `python -m unittest discover -s tests -p test_translation.py -q`: oito testes
  aprovados: cache durável/concorrência/invalidação, PT, ausência de chave,
  HTTP 403/429/456/500, rede/formato, cache indisponível, integração de três
  fontes e ausência de tradução adicional TMDB.
- `python -m unittest discover -s tests -p test_catalog.py -q`: 14 aprovados.
- `python -m unittest discover -s tests -q`: **136 testes passaram**, na .venv.
  Logs de falha Kitsu na suíte são cenários simulados esperados.
- `.env` fora do índice e comparação da chave com os arquivos alterados sem
  emitir seu valor. Os conflitos Git preexistentes permanecem sem alteração.

## DeepL real

`validation/smoke_deepl.py` executado com acesso de rede autorizado. Duas frases
públicas curtas, sem dados de usuários. Resultado em
[deepl-smoke-2026-10-19.json](deepl-smoke-2026-10-19.json).

- Tradução EN → PT-BR retornou texto traduzido.
- Repetição com cliente HTTP impedido confirmou reaproveitamento do cache.
- Frase original em português foi preservada.
- Chave e corpos de erro não foram emitidos em logs ou relatórios.

## Limites

Não foi executada revisão de navegador nem reiniciado o servidor existente.
Nenhuma compilação Reflex ou publicação Xano foi necessária para os serviços
Python; esta rodada não afirma validação de interface. A execução em produção
precisa ser reiniciada para carregar o código e o .env novos. Tarefa 2.3 aberta.
Não houve tradução em lote ou teste remoto dos catálogos reais nesta rodada.
Cache local não estabelece teto de cota mensal para múltiplos processos.
