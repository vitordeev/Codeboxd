# Encerramento documental da fundação

Revisão: 13/10/2026. A change tem 87 IDs de tarefas. O CLI mostrava 85/86 porque 11.7 usava o marcador inválido `- []`.

## Reconciliação

| ID | Pendência anterior | Evidência de encerramento |
| --- | --- | --- |
| 5.2 | Busca Jikan ao vivo indisponível | Kitsu substituiu o provedor em 23/09; `docs/KITSU.md` registra busca de Cowboy Bebop, ficha e navegador reais; `.local/kitsu-live-result.json` confirma 4 resultados sem erros, ranking 20, ficha com capa, 3 relacionados e 1 trailer |
| 11.7 | Validação final e marcador malformado | Artefatos reconciliados com código atual; checklist corrigido; validação OpenSpec estrita de encerramento; síntese em `openspec/VALIDACAO.md` |

TMDB e Open Library responderam na mesma rodada histórica Kitsu. O objetivo original era obter busca externa para as categorias suportadas, não preservar Jikan como provedor obrigatório. A identidade de obras Jikan usadas por avaliações/listas permanece via mapeamento.

O contrato de home foi atualizado para fileiras horizontais empilhadas, coerente com a página/CSS atuais. A evidência vertical de 22/09 foi preservada como histórico de comportamento substituído. Os demais requisitos e cenários foram preservados.

## Limites

Não houve consulta remota nova nem smoke de browser nesta revisão. As 106 verificações locais e a compilação da reanálise passaram. Complementos posteriores de senha/imagem, integração administrativa, arquivos privados e publicação permanecem em `openspec/PENDENCIAS.md`; não foram marcados como entrega operacional completa.

Os scripts e resultados de setembro são históricos. Após o arquivo, comandos com caminho da antiga change ativa e a profundidade de diretório do `auth_live.py` precisam de adaptação em uma cópia, sem sobrescrever as saídas existentes.
