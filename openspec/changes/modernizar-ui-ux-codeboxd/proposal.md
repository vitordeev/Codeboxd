# Proposal

## Why

O Codeboxd já tem catálogo, rede social, listas e administração funcionais, mas a descoberta, a navegação e os padrões visuais variam entre páginas. Evoluir os componentes atuais e tornar listas públicas encontráveis pela busca melhora clareza e acessibilidade preservando a marca preta e amarela.

## What Changes

- Consolidar cores, tipografia, espaços, controles, cards e feedback a partir da logo, dos mascotes ativos e das referências locais, sem reconstruir telas ou reativar o mascote revertido.
- Reorganizar a navegação em Início, Buscar, Feed e Biblioteca; manter acesso a listas, perfis e comunidade por rotas/atalhos reconhecíveis e revisar redundâncias com rastreabilidade.
- Oferecer busca em escopos separados **Obras, Pessoas e Listas públicas**, reutilizando o motor de obras e sua busca multiformato.
- Acrescentar busca paginada de listas públicas e perfis no servidor e detalhe de lista com URL estável, criador, obras e link copiável; preservar o diretório agrupado por autor e as listas privadas do proprietário.
- Evoluir as prateleiras horizontais existentes para mouse, toque e teclado, mantendo setas e rolagem nativa, sem transportar movimentos de ponteiro ao backend.
- Priorizar problemas reais de contraste, foco, densidade e responsividade; aplicar WCAG 2.2 AA aos fluxos alterados e respeitar movimento reduzido.
- Separar apresentação de mudanças de negócio. Investigar a atividade de listas relatada no feed antes de decidir qualquer alteração; não remover eventos, posts ou dados históricos.

## Capabilities

### New Capabilities

- `interface-consistency`: identidade e padrões de navegação, hierarquia, feedback e acessibilidade nas páginas existentes.
- `horizontal-collections`: coleções horizontais operáveis com arrasto, toque, controles e teclado sem efeitos colaterais de navegação.
- `unified-search`: entrada de busca comum com escopos independentes de obras, pessoas e listas públicas, privacidade e estado de consulta reproduzível.

### Modified Capabilities

- `user-lists`: preservar a separação pessoal/pública, ampliar descoberta com resultados por lista identificando autor e fornecer detalhes endereçáveis sem expor listas privadas. O requisito de agrupamento por criador continua no diretório; os resultados de busca podem ser ordenados por relevância, sempre com autoria visível.

## Impact

Futura implementação em páginas/estados Reflex existentes, CSS e componentes de navegação/prateleiras, contratos aditivos Xano de consulta/detalhe e testes. Não substituir Reflex, Xano, TMDB/Kitsu/Open Library, identidade Jikan, login, biblioteca, permissões ou regras administrativas. Não remover controles acessíveis sob pretexto de simplificação.

UI de anexos depende do contrato da change Cloudinary, mas a modernização visual e os carrosséis podem avançar independentemente dela. Medições/metas e otimizações de transporte permanecem em `otimizar-performance-app`; aceite de mutações administrativas permanece em `gerenciamento-website`.

**Rodada atual: análise e planejamento apenas.** Nenhuma funcionalidade implementada, imagem gerada, referência externa de inspiração, publicação, ativação, push ou merge. Os artefatos ficam propostos para aprovação do usuário antes de iniciar qualquer implementação. Changes históricas canceladas/revertidas não são retomadas automaticamente.
