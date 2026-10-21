## Context

Ver proposal.md. `catalog.detail` obtém sinopses Kitsu e Open Library. TMDB já
recebe pt-BR. Há httpx e dotenv instalados. O Git tem conflitos preexistentes;
esta change não os resolve. Execução local com .venv.

## Goals / Non-Goals

**Goals:** tradução opcional no servidor, cache local durável e falhas limitadas.
**Non-Goals:** migrações remotas, alterações de UI, tradução em massa ou Docker.

## Decisions

- Usar httpx assíncrono com endpoint fixo oficial Free (chave com sufixo :fx) ou
  Pro, header DeepL-Auth-Key e destino PT-BR. Sem dependência SDK adicional.
- Traduzir apenas `catalog.detail` de livros/animes, preservando Jikan legado.
  Evitar tradução nas buscas/home limita consumo e latência. TMDB permanece nativo.
- Idioma desconhecido usa autodetecção DeepL; se detectar PT, conservar original.
  A primeira detecção de português desconhecido também consome cota. Não usar
  heurística de palavras que poderia classificar descrições incorretamente.
- SQLite em `.local/description-translations.sqlite3`, chave SHA-256 de versão,
  destino e conteúdo. I/O via asyncio.to_thread; falha de cache mantém original.
  Cache limitado a 10 mil entradas. Serializar miss concorrente no mesmo loop.
- Timeout limitado, sem retry automático de POST para evitar cobrança duplicada.
  Backoff de 60 segundos em falha, 15 minutos para credencial/cota (403/456).
  Limitar texto a 20 mil caracteres por requisição; textos maiores mantêm original.
- Credencial só em .env não rastreado; exemplo vazio. Logs mostram apenas tipo
  de falha/status, nunca headers, corpo, descrição ou chave.

## Risks / Trade-offs

- Cota compartilhada → cache, chamadas sob demanda e backoff; não garante teto
  mensal global em múltiplas instâncias. Operação atual é local.
- Perda do cache → novas traduções consomem cota; preservar .local quando necessário.
- Tradução automática pode variar → original é preservado quando detectado PT;
  qualidade de sinopses será avaliada em smoke limitado, sem prometer perfeição.

## Migration Plan

Configurar chave local, aplicar serviço e testes, testar chamadas remotas limitadas.
Rollback: remover DEEPL_API_KEY desativa tradução; cache pode ser preservado.
Sem publicação Xano. Browser será registrado separadamente se executado.

Referências oficiais: https://developers.deepl.com/api-reference/translate/request-translation
e https://developers.deepl.com/docs/getting-started/auth.
