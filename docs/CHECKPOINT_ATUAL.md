> Atualiza??o de 19/10/2026: consulte [o resumo de retomada](RETOMADA_2026-10-19.md) antes de continuar. Funda??o encerrada; fluxo OpenSpec documentado; backend administrativo em valida??o, sem publica??o autorizada. O conte?do abaixo ? hist?rico.

# Checkpoint atual do Codeboxd

## Atualização — 13/10/2026

Fonte de contexto atual: [OpenSpec](../openspec/README.md), [relatório de estado](../openspec/RELATORIO_STATUS.md) e [pendências](../openspec/PENDENCIAS.md). Toda alteração deve ser acompanhada nessa pasta.

- Fundação (87/87) e modelo Xano (37/37) arquivados; administração permanece 17/34.
- `.gitignore` e índice corrigidos; arquivos locais preservados. Credenciais no histórico compartilhado ainda precisam de tratamento.
- Ambiente canônico `.venv` instalado e verificado; dependências diretas fixadas.
- Mensagens de upload e URL de banner no backend corrigidas e testadas.
- Execução local com `.venv`, sem Docker por decisão do usuário. Ajustes Docker desta rodada revertidos.
- Validação atual: 113 testes, `pip check` e compilação Reflex passaram; verificação Compose anterior ficou fora do escopo atual.
- Evidência e limites: [correções operacionais](../openspec/changes/corrigir-erros-operacionais/validation/correcoes-2026-10-13.md).

## Registro anterior — 23/09/2026

- Cards de obras preservam o pôster inteiro no enquadramento.
- A página de detalhes mostra serviços legais de streaming informados pelo TMDB para filmes e séries no Brasil.

Estado salvo em 23/09/2026.

- A busca filtra resultados por palavras completas do título.
- A homepage usa fileiras horizontais empilhadas verticalmente para filmes, séries, livros e animes.
- A numeração sobre as capas foi removida.
- A homepage tem três fileiras de animes: mais bem avaliados, populares e em destaque agora.
- A homepage tem cinco fileiras de livros, incluindo livros conhecidos (`1984`, `Duna`, `Harry Potter`, `Sapiens` e `O Hobbit`) e a busca específica `Teoria dos Jogos`.
- A capa padrão está em `assets/default-movie-cover.png`.
- Animes usam Kitsu. Registros antigos da Jikan são resolvidos pelo mapeamento MyAnimeList/Kitsu.
- O endpoint remoto `POST /media` do Xano foi atualizado para aceitar Kitsu e evitar duplicação de obras antigas.
- Diagnóstico das APIs: `docs/KITSU.md`.
- Validação daquela rodada: 86 testes passaram e `reflex compile --dry` foi concluído com sucesso.

Para continuar, consultar primeiro o OpenSpec; as referências de implementação do catálogo seguem em `Codeboxd_main/services/catalog.py`, `Codeboxd_main/pages/social.py` e `Codeboxd_main/state/social.py`.
