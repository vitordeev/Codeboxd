# Design

## Context

Rodada de **planejamento**, sem execução do app ou alteração funcional. Base local
`task/cloudinary-limites-20261111`, HEAD `faa655f`; alterações Cloudinary anteriores
estão não commitadas. O schema é spec-driven, CLI 1.14.3. README e documentação
central foram lidos; `docs/project-overview.md` e `docs/domain-model.md` não existem
nesta worktree. Domínio conferido nos contratos Xano e specs consolidadas.

Reflex instalado 0.9.11.post1. Fontes principais: `Codeboxd_main/Codeboxd_main.py`,
`pages/social.py`, `pages/login.py`, `pages/account.py`, `pages/admin.py`,
`state/social.py`, `assets/codeboxd.css`, tabelas e APIs Xano. O arquivo de rotas
é a autoridade: `index()` e `account_page()` legados não estão registrados como
as páginas atuais. Home/catálogo/busca de obras compartilham `/`; edição do perfil
é um diálogo em `/conta`, avaliações ficam na ficha e nas atividades/biblioteca.
Não inventar páginas já existentes separadas ou reconstruir esses fluxos.

### 1. Diagnóstico visual e evidências disponíveis

| Referência local | Uso na proposta | Limite |
| --- | --- | --- |
| `Imagens/HomePage.png` e `Imagens/MoviePage.png` | Marca preta/amarela, símbolo, proporções de capas e organização cultural; ambas visualizadas | Referências antigas, não capturas atuais nem contrato para duplicar cartões/placeholders |
| `Imagens/Captura de tela 2026-09-17 230510.png` | Recorte histórico da Home, visualizado | Nove imagens foram localizadas em Imagens; não se presume que todas representem telas implementadas |
| `assets/codeboxd-logo.svg`, helper `_logo_icon` | Preservar símbolo geométrico amarelo e wordmark code/boxd | SVG inspecionado; não redesenhar marca |
| `assets/mascot.png`, `_mascots_svg` do login | Mascotes ativos; PNG visualizado e consumidores conferidos | Não gerar substitutos nesta change |
| `openspec/changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/validation/owner-groups-final/groups-2-390.png` | Autoria ao lado do avatar e diretório público agrupado, captura visualizada | Histórico com fixtures, não ensaio novo |
| `gerenciamento-website/validation/multiagente-browser-2026-10-28/dashboard-partial-390.png` | Leitura administrativa em celular e falha parcial preservada, captura visualizada | Histórico, sem conferir dados ou permissões atuais |
| `melhorar-mascotes-carregamento/validation/integration-21268/login-1440.png` | Apenas identificar a diferença histórica, captura visualizada | Lume foi revertido: a proposta e tasks daquela change prevalecem sobre ARTWORK antigo |

Arquivos anexados fora do repositório não foram disponibilizados nesta rodada.
Não se buscaram referências externas de inspiração nem se geraram imagens.
Não há evidência visual nova de todas as telas, tablet/320px, leitor de tela ou
gesto real; os diagnósticos abaixo combinam fonte atual e capturas históricas,
sem declarar falhas no navegador quando só há um risco inferido do código.

### 2. Identidade a preservar e sistema visual proposto

Paleta efetiva: `--yellow: #f5c810`, fundo social `#0d0d0d`, superfícies
`#121215`/`#111114`, texto `#f6f5f2`, secundários `#a2a0a8`/`#939199` e bordas
`#38383c`. Login/cadastro ainda usam `#F5B300` e preto puro; isso explica parte
da inconsistência sem implicar que uma nova cor seja necessária. Inter já é
carregada em HEAD_COMPONENTS; manter família e fallbacks, sem baixar outra fonte.

Propor tokens semânticos para fundo/superfície/borda/texto/ação/foco e estados,
tomando `#f5c810` como destaque principal. Harmonizar o amarelo do login na revisão
visual, sem recolorir os mascotes. Texto escuro sobre botão amarelo; amarelo para
ação principal, seleção e foco, não para todas as legendas ou painéis inteiros.
Vermelho/verde/âmbar têm semântica e texto/ícone, nunca informação só por cor.

Escala candidata: corpo 16px/1,5; metadados 13–14px; títulos de seção 20–24px e
título de página 28–36px responsivo. Pesos 400/500/600/700, 800 reservado à marca
ou destaque. Espaçamentos 4/8/12/16/24/32/48px; controles 8–12px de raio e painéis
12–16px, exceções justificadas para hero/avatars. Um nível de superfície por
bloco, borda quando organiza leitura; sombras discretas apenas em sobreposição.
Manter imagens de obras e um destaque editorial; gradiente só quando necessário
para legibilidade sobre imagem, sem novos brilhos, emojis ou enfeites de template.

Cálculo local de pares sólidos declarados: `#595959` sobre `#030303` = 2,94:1;
`#77757d` sobre `#0d0d0d` = 4,28:1; candidatos a correção para texto pequeno.
`#7e7e7e` sobre preto = 5,17:1 e amarelo sobre `#0d0d0d` = 12,17:1.
São cálculos sRGB de declarações, não certificação do contraste composto de
imagens, opacidades ou todas as telas. Revalidar tokens nos fundos reais.

### 3. Auditoria das páginas e redundâncias

| Área e evidência no código | Comportamento atual / problema | Melhoria proposta e preservação | Prioridade |
| --- | --- | --- | --- |
| Shell, `shell` | Perfil no menu e Meu perfil na ação da conta apontam a `/conta`; Biblioteca/Comunidade ficam no rodapé | Manter um acesso reconhecível ao próprio perfil no menu da conta; levar Biblioteca ao menu principal, mantendo links antigos | P1 visual/navegação |
| Home/Buscar/Catálogo, `discovery_page` | Busca e categorias moram em `/`; não há escopos Pessoas/Listas; banner editorial, textos e CTA de biblioteca disputam a primeira dobra | Home editorial mais compacta, entrada Buscar explícita e resultados em rota estável; manter filtros de categorias separados da consulta textual | P1; consultas novas P2 |
| Catálogo, `catalog_shelf` | Setas 34×34 e trilho focável já existem; não há arrasto de mouse implementado | Evoluir uma prateleira, ampliar área interativa e preservar carregamento por lote | P1 interação |
| Detalhes, `media_page` | Ficha, dados técnicos, trailer, streaming, nota, crítica, status e listas coexistem; várias caixas e avisos ocupam a hierarquia | Um bloco de ação principal de avaliação, status distinto de listas; secundários em grupos claros. Não fundir nota, progresso e lista como se fossem a mesma regra | P2 visual |
| Filmes/séries/animes/livros | Mesmo template, detalhes técnicos variam por provedor; resposta complementar pode chegar depois | Reutilizar template, revelar campos pertinentes ao tipo, manter hero e obra identificados durante falha parcial | P2 visual |
| Avaliações, `rating_picker` | Estrelas de meia nota e seletor numérico coexistem | Reagrupar sem eliminar alternativa acessível, manter incrementos de 0,5 e notas dos visitantes locais diferenciadas das persistidas | P2 visual |
| Biblioteca, `library_page` | Atividades com status/nota e paginação/flag já existem; CTA Descobrir no fim e navegação principal distante | Dar acesso direto, densidade consistente e estado vazio contextual; não reimplementar biblioteca paginada nem alterar status | P1 navegação/P2 visual |
| Minhas listas, `lists_page` | H1 Listas, subtítulo, H2 Suas listas, dois seletores e CTA antes dos itens; detalhe aparece abaixo do diretório | Compactar introdução, CTA único por contexto; manter gerenciamento em `/listas` e abrir detalhe endereçável separado | P2 visual/rota |
| Listas públicas, `public_list_group` | Diretório agrupado por dono e títulos padrão repetidos; sem pesquisa ou detalhe compartilhável | Conservar diretório; buscar listas individuais com criador/descrição curta. Nunca ocultar títulos iguais de donos diferentes | P1 descoberta/P2 Xano |
| Feed, `feed_page/post` | Sidebar tem Criar publicação, sugestões e atalho à comunidade; notices globais e de diálogo podem coexistir | Um CTA principal contextual, sugestões secundárias; foto/obra compacta e comentários sob demanda preservados. Não refazer likes/discussão | P2 visual |
| Perfil, `profile_page` | Nome/@, bio, estatísticas em cards e três seções longas; edição usa diálogo com banner, nome e URL de avatar | Hierarquia de identidade/conteúdo/conexões, estatísticas compactas e seções acessíveis; reusar links de âncora e seguir/denunciar | P2 visual |
| Edição de perfil | Banner tem upload e avatar URL; forms/feedback diferem do editor social | Padronizar rótulos, ajuda e erro por campo, preservar os mecanismos atuais; mudança de storage de avatar/banner não faz parte de Cloudinary-posts | P2 visual |
| Login/cadastro | Marca e mascotes existentes, amarelos divergentes, slogan extra em caixa, erros sem padrão entre páginas | Preservar composição/mascotes, harmonizar campos e contraste, subordinar slogan sem esconder cadastro, recuperação ou acesso admin | P1 contraste/P2 visual |
| Recuperação | Fluxo de duas etapas com progresso já implementado; Voltar e Voltar para entrar podem coexistir | Reutilizar duas etapas, condensar navegação redundante após revisão; preservar resend, alterar e-mail, confirmação, mensagens e regras de segurança | P2 visual |
| Administração | Sidebar/feedback/paginação próprios, densidade e grids de usuários/catálogos/reports; indicadores indisponíveis não são zero | Compartilhar tokens/inputs sem trocar guards ou modelo; preservar confirmação, auditoria, estados parciais, demonstração e rotas | P3 visual, aceite próprio |

Propostas de condensar, mover ou retirar decoração dependem da aprovação desta
change e da revisão visual da tarefa correspondente. Antes de retirar um
controle, demonstrar ação equivalente e acessível; dados técnicos, spoilers,
direitos de edição, privacidade e alternativas de teclado permanecem.

## Goals / Non-Goals

**Goals:** tornar ações encontráveis, preservar a identidade, reduzir ruído com
rastreabilidade, garantir alternativas a gestos e permitir busca pública segura.

**Non-Goals:** reconstruir app, mudar marca/mascotes, copiar templates, gerar arte,
reescrever regras de notas/listas, reativar Lume, migrar provedores, alterar dados
ou concluir aceitações de administração, autenticação, Cloudinary ou performance.

## Decisions

### 4. Hierarquia e navegação

- Desktop: Início, Buscar, Feed, Biblioteca; conta com Meu perfil/Minhas listas/
  Comunidade/Sair e entrada administrativa existente. Não expor controle admin
  como permissão: guards continuam determinando acesso. Menu da conta é operável
  sem hover e mantém texto identificável.
- Celular/tablet: mesmos destinos em navegação compacta com rótulos; não adicionar
  simultaneamente barra inferior, abas e menu duplicando a mesma ação. Menu
  expansível para secundários; foco visível e conteúdo não encoberto. Validar
  protótipo local antes de fixar layout; não depende de referências externas.
- `/` conserva descoberta editorial e categorias. `/buscar?tipo=obras|pessoas|listas&q=...`
  é rota proposta; consulta submetida e escopo sobrevivem a recarga/voltar. Links
  atuais `/biblioteca`, `/listas`, `/conta`, `/perfil/...`, `/obra...` são mantidos.
- Perfil/biblioteca organizam o próprio acervo; listas não passam a ser posts.

### 5. Componentes a reutilizar

`shell`, `_logo_icon`, `cover_image` (lazy/fallback), `media_card`, `catalog_shelf`,
`person`, `public_list_group`, `interaction`, `post`, `editor`, `confirm`,
`password_input`, `rating_picker`, feedback/paginação administrativos e os
transportes existentes. Eventos de autenticação, identidade Jikan/externa,
cache/gerações e diálogos acessíveis devem ser preservados, não reescritos.

### 6. Componentes a modernizar

Extrair progressivamente tokens e variantes de Button/Field/Feedback/EmptyState,
shell e prateleira reutilizável; começar em uma página de cada família. Sem um
componente novo para cada variação, nem um card para cada linha. Estado vazio,
falha e carregamento continuam diferentes; feedback fica próximo da ação,
com resumo global só quando ajuda. Remover CSS antigo somente após inventário de
consumidores e regressão, nunca por nome que parece legado. Não importar módulos
de `withdrawn-implementation/` para recuperar trabalho revertido.

### 7. Descoberta de listas públicas e relação com feed

Busca começa em Obras (quatro tipos, relevância já existente), com escopos Pessoas
e Listas públicas. Não há aba Todos que dispare todos os provedores a cada tecla.
Pesquisa por submissão; estado independente por escopo. Ao mudar escopo, limpar
resultados incompatíveis e consultar apenas o escopo ativo. Mudança de conta,
consulta, filtro ou página invalida resposta atrasada.

Listas: título como critério padrão; filtro explícito opcional por criador
(`creator_id` vindo de perfil selecionado) e, em modo avançado, descrição. Não
inventar tags, popularidade ou ranking por seguidores sem dados do domínio.
Ordenação estável por correspondência no título e desempate por ID. Paginação
servidor: 20 itens, máximo 50; total/has_more apenas de listas visíveis. Cada
resultado tem título, criador com perfil, descrição curta e contagem correta de
itens; capa composta só se os dados já vierem no lote, sem N+1.

API candidata: ampliar `GET /lists/public` com parâmetros opcionais `q`,
`creator_id`, `search_in=title|title_description` e ordenação suportada, preservando
chamada antiga sem query. Acrescentar `GET /lists/public/{id}` com resumo/autor e
usar o endpoint de itens existente com paginação. Para detalhe privado do dono,
propor `GET /lists/{id}` autenticado, sem alterar acesso dos itens privados.
Pessoas: estender `GET /profiles` com `q` por username/display_name e paginação,
sem retornar e-mail ou outros campos privados; manter o formato consumido pelos
clientes ou adicionar metadados por contrato versionado, nunca trocar array por
envelope silenciosamente. Catálogo de obras não muda sua semântica multiformato.

Buscar filtra no Xano **antes** de paginar, contar ou calcular previews. Índices
e busca textual devem ser validados com os recursos reais do plano; não carregar
todas as listas/perfis no Reflex para filtrar. Sem SQL concatenado; termos
escapados, limites de comprimento e consultas parametrizadas.

Detalhe proposto `/listas/[list_id]`: rota resolve metadados e depois itens, não
depende de achar a lista na página atual do diretório. Mostra autor/link, título,
descrição, obras e paginação. Editar/adicionar/remover aparece só ao dono; Xano
valida novamente. Link de lista pública pode ser copiado; fallback selecionável
se Clipboard API falhar. Web Share só como aprimoramento, sem nova rede social.
Privada ou removida por URL pública retorna resposta indistinguível de ausente,
sem título/autor/itens/contagem em resposta, HTML, preview ou cache público.
Isso inclui ajustar o endpoint público de itens existente, que hoje distingue
privada (accessdenied) de ausente (notfound), após validar compatibilidade dos
consumidores; a resposta proposta para ambos é 404 genérico sem metadados.
Após mudar pública→privada, limpar estado e caches; validar acesso público de
novo, sem aplicar cache privado de outra conta nem indexar conteúdo privado.

**Feed:** README descreve atividades/listas, mas `save_list` e `lists_POST.xs`
não criam posts no código lido; `feed_GET.xs` lê posts dos seguidos e
`_refresh_posts` combina posts. Origem do relato não foi reproduzida nesta rodada.
Recomendação: descoberta sempre em Buscar; não introduzir autopost de criação de
lista. Se evento legado existir no ambiente, avaliar mantê-lo como atividade
secundária com link estável e privacidade atualizada; remoção exige decisão
específica após reproduzir. Não apagar eventos/posts ou desligar handlers por
suposição. Essa decisão não bloqueia entregar busca independente do feed.

### 8. Prateleiras arrastáveis

O código atual usa CSS overflow-x/scroll-snap, `shelf_arrow` com scrollBy de 85%
do viewport e trilho `tab_index=0`. A distribuição instalada tem `rx.scroll_area`
(wrapper Radix de rolagem nativa); não foi localizado Carousel nos arquivos da
distribuição Reflex consultada. ScrollArea oferece scrollbar/rolagem, não comprova
arrasto de cards por mouse. Preferir evoluir `catalog_shelf` e adaptar
`.media-shelf` ao mesmo componente; não adicionar biblioteca de carrossel agora.

Proposta: comportamento pequeno no cliente, com Pointer Events e scrollLeft.
Mouse primário: após 8 CSS px de deslocamento predominantemente horizontal,
iniciar arrasto, capturar ponteiro, aplicar grab/grabbing e impedir seleção local.
Antes do limiar, click normal; após arrasto, suprimir somente o click associado
à sequência, inclusive no card, sem engolir Enter/Space ou cliques posteriores.
pointercancel/lost capture/desmontagem restauram seleção/captura, sem listener
duplicado após rerender. Não interferir em botões de ação internos.

Toque/trackpad mantêm overflow nativo, pan horizontal/vertical e zoom; não usar
preventDefault global nem touch-action:none/pan-x que bloqueie a página. Não
emular arrasto de mouse em touch, nem impedir pointerdown antes da intenção estar
clara. Sem loop infinito/autoplay; movimento sem overshoot artificial.

Setas continuam disponíveis, com rótulos por coleção, aria-controls e estados
de início/fim. Trilho suporta teclas esquerda/direita e Home/End quando seu
foco é o contêiner, sem capturar teclas de formulários; Tab alcança cards/setas,
Enter abre o card. Ao focar item fora da área, revelá-lo sem deslocar verticalmente
a página. Rolagem reduzida usa deslocamento imediato; sem animation frame por
movimento enviado ao estado Python. Carregar mais continua ação separada.

### 9. Acessibilidade e responsividade

Aplicar WCAG 2.2 AA nos fluxos alterados: contraste de texto 4,5:1 (grande 3:1),
controles/estados relevantes 3:1, teclado sem armadilha, foco visível e não oculto,
reflow e alternativas a arrasto. Mapear 1.4.3/1.4.10/1.4.11, 2.1.1/2.1.2,
2.4.3/2.4.7/2.4.11, 2.5.1/2.5.2/2.5.7/2.5.8 e 4.1.2/4.1.3 no aceite.
Alvos de pelo menos 24×24 CSS px conforme exceções da norma; meta do produto
44×44 para ações principais, setas e menus no toque. Isso não implica trocar
o glifo de 19px: ampliar a área de interação e seu espaçamento.

Testar 320/390/768/1024/1440px, zoom 200% e reflow equivalente a 320 CSS px,
teclado, nomes longos, mensagens compridas, foco em diálogo e retorno ao gatilho.
Nenhum overflow horizontal do documento; trilho/tabela podem ter região própria
identificada sem esconder ações críticas. Rótulos persistentes, autocomplete,
mensagens por campo e anúncios de status contextual; loading não substitui erro.
Respeitar prefers-reduced-motion, não bloquear zoom, colagem ou gerenciadores de
senhas; manter show/hide acessível. Não alegar conformidade completa só com axe.

### 10. Performance visual

Nenhuma requisição ou atualização de estado Reflex por pointermove/scroll do
trilho. Sem nova biblioteca de carousel/fonte/arte pesada ou autoplay. Manter
lazy loading, dimensões/aspect-ratio e fallback de capas; o placeholder PNG atual
tem 1.934.942 bytes, candidato a avaliar com performance, não a substituir nesta
rodada. Reutilizar URL/cache, não criar variante de transformação para cada pixel.

Busca consulta só o escopo submetido, paginação por domínio, sem N+1 de autores
ou de capas e sem buscar todos os tipos apenas para contadores. Limitar DOM a
lotes existentes; medir antes de propor virtualização. Preservar carregamento
progressivo da Home/P0, gerações, cache, pools e isolamento já implementados.

Baseline/comparação: mesmo commit-base, dataset, viewport, cache e rede; medir
cinco pares, mediana/pior, requests/DOM/bytes e métricas de interação quando
disponíveis. Não mudar metas existentes. Zero chamadas novas em mudança puramente
visual e zero chamadas por gesto são critérios rígidos; qualquer regressão
observada de tempo/CLS deve ser investigada antes do aceite. Valores ausentes
não viram zero. Metas amplas/429 e aceite global ficam em `otimizar-performance-app`.

### 11. Dependências e riscos

| Dependência/risco | Tratamento |
| --- | --- |
| Mudança em lists/profiles/detalhes Xano | Contratos/testes locais primeiro, backup/dry-run e autorização por lote antes da publicação |
| Homologação Xano indisponível | UI/gestos com fixtures podem avançar; não inferir aceite real nem usar workspace compartilhado sem autorização própria |
| `SocialState` e CSS compartilhados com performance/Cloudinary | Branch/worktree por lote na implementação, revisar diff comum antes de integrar; preservar trabalho não commitado |
| Relevância por lista quebra agrupamento obrigatório do diretório | Delta explícito `user-lists`, mantendo agrupamento no diretório e autoria em cada resultado |
| Templates antigos/Lume revertido confundem fonte | Código ativo e status de reversão prevalecem; registros antigos são referências históricas |
| Clique involuntário/scroll vertical bloqueado | Limiar/intenções, cancelamento e matriz real de mouse/touch/teclado |
| Interface limpa esconde recursos | Inventário atual→novo, links antigos e alternativa acessível antes de retirar elemento |
| Feed de listas divergente no ambiente | Investigar/reproduzir em leitura autorizada depois; nenhuma remoção automática |
| Rollback após mudança de privacidade | Guardas no servidor permanecem; nunca reabrir acesso privado ao reverter UI |

### 12. Sequência recomendada de implementação

1. Após aprovação: baseline visual atual, inventário de ações e recortes aprovados.
2. Tokens/contraste/inputs/feedback e shell em uma página piloto; validar teclado
   e telas pequenas antes de propagar. Biblioteca/Buscar ganham acesso claro.
3. Prateleira reutilizável e suas regressões de gesto/teclado; adaptar Home e
   recomendações sem mudar carregamentos ou chamadas.
4. Busca com escopos e estado de URL; obras reutilizam o motor atual. Contratos
   paginados de pessoas/listas e páginas de detalhe em lote próprio no Xano.
5. Propagar padrões para fichas/biblioteca/listas/perfis/autenticação e feed por
   famílias; anexos usam contrato de Cloudinary quando pronto, sem acoplar cores
   a provider. Admin vem por último, preservando seu aceite separado.
6. Ensaios integrados/privacidade/performance e revisão visual final com evidências
   por largura, estado e input. Não arquivar nem publicar automaticamente.

## Migration Plan

Mudanças aditivas por família; manter URLs atuais e abertura de listas pelo
diretório durante a transição. Buscar e detalhe novos podem ficar atrás de
configuração de liberação até backend validado; falha de serviço gera erro
explícito, não busca pública em dados privados locais. Reverter apresentação por
lote sem reverter guards, expor listas privadas ou apagar dados. As reservas de
Cloudinary, quando existirem, continuam reconciliáveis mesmo com UI antiga.

## Referências técnicas

Somente documentação técnica externa foi consultada, sem inspiração visual:
[WCAG 2.2](https://www.w3.org/TR/WCAG22/), skill Reflex e código instalado
`reflex_components_radix/themes/components/scroll_area.py`. A URL de documentação
ScrollArea tentada não ficou acessível; o comportamento descrito foi conferido no
wrapper instalado, sem pressupor suporte a drag que ele não declara.

## Primeiro lote local após aprovação — 11/11/2026

O piloto conserva a composição do login, logo, robôs ativos e fonte Inter já
declarada. Tokens `--cb-*` centralizam cores semânticas, fallback tipográfico,
espaços e raios; o login recebe contraste/contornos e alvos maiores. Essa entrega
não reorganiza o shell nem remove destinos ou ações. A validação com fontes
bloqueadas verifica o fallback; outra rodada carrega somente a Inter existente
pelos hosts que o aplicativo já utilizava, sem inspiração ou fonte novas.

`horizontal_collection.py` compõe regiões e controles nativos reutilizados pela
Home e recomendações. O asset JavaScript tem um registro global idempotente,
eventos delegados e observação de dimensões/entrada/saída de regiões; não instala
um handler Python por gesto. Parâmetros: intenção horizontal a partir de 8 CSS px,
cancelamento se a intenção vertical prevalecer, captura somente após o limiar,
avanço de 85% da largura visível e supressão por até 350ms somente do clique do
mesmo ponteiro/trilho após arrasto. Novo pointerdown e clique de teclado não são
suprimidos. Cancelamento, perda de captura, blur, documento oculto e desmontagem
restauram o estado transitório.

Toque/trackpad mantêm rolagem nativa e `touch-action:auto`; setas e Home/End ficam
locais ao trilho focado. O foco em card oculto ajusta apenas seu scroll horizontal.
As setas têm 44×44px e estados de extremo/sem overflow. `scroll-padding-inline`
preserva os 2px de respiro do trilho existente: sem isso, o snap do primeiro card
produzia scrollLeft=2 e deixava a seta anterior habilitada indevidamente.
Recomendações vazias não exibem controles sem alvo.

Não houve alteração de SocialState, caches, paginação, contratos de autenticação
ou serviços. A evidência em [validation/fundamentos-carrosseis-2026-11-11.md](validation/fundamentos-carrosseis-2026-11-11.md)
delimita testes reais de navegador com backend fictício, cancelamento sintético,
toque emulado e verificações ainda abertas. O restante do plano permanece válido.
