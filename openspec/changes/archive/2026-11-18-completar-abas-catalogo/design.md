## Context

A tela administrativa pagina registros persistidos. Os servi?os existentes retornam resultados paginados do TMDB, Kitsu e Open Library; esses resultados externos podem complementar a leitura sem alterar o cat?logo Xano.

## Goals / Non-Goals

**Goals:**

- Padronizar o limite visual em 35 nas quatro categorias.
- Completar a primeira p?gina de s?ries, animes e livros com resultados externos somente de leitura.
- Distinguir claramente registros persistidos de resultados externos.

**Non-Goals:**

- Gravar resultados externos ou oferecer controle para import?-los em lote.
- Alterar contratos Xano ou as obras j? persistidas.

## Decisions

1. Consultar p?ginas do provedor para categorias com menos de 35 itens cadastrados, deduplicar por identidade externa contra registros salvos e limitar o resultado combinado a 35.
2. Marcar candidatos sem ID Xano como somente leitura; manter edi??o dispon?vel apenas para registros persistidos.
3. N?o criar endpoints nem chamar o POST administrativo para resultados externos.
4. Buscar tamb?m no provedor quando a administradora filtrar por t?tulo, mantendo pesquisa paginada do cat?logo Xano.

## Risks / Trade-offs

- Fontes externas podem falhar ou retornar poucos candidatos ? manter registros cadastrados, exibir candidatos j? obtidos e informar falha parcial.
- Resultados externos n?o pertencem ao Xano ? identificar origem e ocultar edi??o para evitar opera??o sobre ID inexistente.

## Migration Plan

N?o h? migra??o de esquema nem altera??o remota. Reverter a composi??o de resultados externos mant?m o cat?logo Xano intacto.
