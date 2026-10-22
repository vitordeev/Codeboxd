# Relatório de melhorias — 20/10/2026

Comparação com 19/10/2026, a partir do histórico Git e das evidências OpenSpec.
Relatório documental: não foram executados novos testes, navegador ou serviços
para produzi-lo. Resultados abaixo pertencem às respectivas rodadas registradas.

## Base entregue ontem — 19/10

- **Avaliações com meias estrelas:** notas de 0,5 a 5, suporte a vírgula/ponto,
  restauração da nota e preservação da crítica ao trocar a seleção. Navegador
  desktop/celular e persistência real de 1,5 no Xano foram verificados.
- **Tradução de descrições:** integração DeepL para livros e animes, cache
  persistente e retorno ao original em falha. Tradução real e reutilização do
  cache verificadas; integração visual completa continuava pendente.
- **Denúncias de obras:** feedback dentro do modal, preservação de rascunho,
  respeito ao prazo do 429 e resolução da identidade de obras externas.
- **Administração:** publicação de correções nas buscas de usuários, catálogo
  e denúncias, preservando autorização. A suíte administrativa completa com
  conta adequada permanecia pendente.
- **Navegação e organização:** ajustes de retorno à descoberta e regularização
  do histórico após resolução de conflitos entre branches.

Referências: commits `bc26305`, `9468d3b`, `d91a2bb`;
[meias estrelas](changes/archive/2026-10-21-avaliar-meias-estrelas/validation/implementacao-2026-10-19.md),
[DeepL](changes/archive/2026-10-21-traduzir-descricoes-deepl/validation/implementacao-2026-10-19.md),
[denúncias](changes/gerenciamento-website/validation/denunciar-obras-2026-10-19.md)
e [buscas administrativas](changes/gerenciamento-website/validation/publicacao-buscas-admin-2026-10-19.md).

## Melhorias adicionadas hoje — 20/10

| Área | Melhoria | Benefício |
| --- | --- | --- |
| Senhas | Controle de mostrar/ocultar senha nos formulários | Facilita conferir a digitação |
| Recuperação | IDs distintos nos dois campos de e-mail | Elimina conflito que fazia a primeira etapa ler o campo vazio da segunda |
| Avaliações | Identidade vinculada à obra e proteção contra envio repetido | Evita nota associada à ficha errada e gravações duplicadas |
| Home e catálogo | Carregamento progressivo, cache público e concorrência por provedor | Conteúdo disponível antes de terminar todas as consultas |
| Sessão e leituras sociais | Cache curto de identidade, reaproveitamento de leituras equivalentes e invalidação após gravação | Reduz consultas redundantes preservando isolamento entre credenciais |
| Limites da API | Cooldown e tratamento de Retry-After; recuperação de senha sem retry automático | Evita repetir operações e pressionar serviços durante o bloqueio |
| Busca e fichas | Cache de busca, descarte de respostas antigas e publicação progressiva da ficha | Navegação mais consistente mesmo com complementos lentos |
| Biblioteca e listas | Remoção de consulta de pessoas desnecessária; biblioteca em lotes de 20 | Reduz dependências e prepara acesso a coleções maiores |
| Conteúdo obrigatório | Denúncia exige descrição; avaliação exige crítica; Xano exige crítica para nota positiva | Impede envios vazios; atalhos de organização sem nota permanecem válidos |
| Comunidade | Removida a chamada de carregamento integral da home | Abrir perfis não dispara categorias e provedores de catálogo |
| Ferramentas | Inventário de rotas, instrumentos de medição e isolamento de frontends | Melhora diagnóstico e reduz interferência entre execuções |

O problema de rede do TMDB foi identificado e corrigido em uma rodada do dia:
o processo havia herdado restrições de rede. Quatro endpoints responderam com
20 itens e três fileiras exibiram 20 cards cada no navegador. Posteriormente,
as tentativas de build falharam; isso não comprova disponibilidade ao encerrar o dia.

## Resultados registrados

- **Home, amostra local:** categorias disponíveis na primeira visita passaram
  de 26,42 s para 15,32 s; na recarga, de 9,40 s para 1,43 s. O título do destaque
  passou de 26,38 s para 10,94 s na primeira visita, mas a recarga desse título
  variou de 1,12 s para 1,27 s. São amostras históricas locais, sem garantia geral.
- **Perfil, medição real:** dez visitas, nove chamadas Xano e nenhum 429;
  oito revisitas sem nova chamada. Mediana de 454,5 ms nas revisitas aquecidas.
  Não representa toda a aplicação.
- **Biblioteca real:** primeira página autenticada validada com quatro itens.
  Continuação de 250 itens foi validada com dados fictícios no navegador;
  paginação real extensa e isolamento entre duas contas continuam pendentes.
- **Regressões:** última suíte completa do dia com **274 testes aprovados**;
  compilação Reflex `--dry` aprovada. O último ajuste do preparador de frontend
  também teve seus dois testes específicos aprovados.

Referências: [home](validation/carregamento-home-2026-10-20.md),
[perfil real](changes/otimizar-performance-app/validation/resultado-login-real-apos-cache-2026-10-20.md),
[biblioteca](changes/otimizar-performance-app/validation/biblioteca-paginada-xano-real-2026-10-20.md),
[comunidade](changes/otimizar-performance-app/validation/comunidade-sem-home-2026-10-20.md)
e [conteúdo obrigatório](changes/archive/2026-10-21-exigir-texto-denuncias-avaliacoes/validation/implementacao-2026-10-20.md).

## Situação ao encerrar

- **Otimização ainda aberta: 11/37 tarefas integralmente concluídas.** Há código
  implementado parcialmente relacionado a outras tarefas; não equivale a atender
  seus critérios completos.
- O build padrão de produção continua falhando no prerender de `/`. Um build
  direto por Node passou, mas a causa não foi confirmada. A execução em 3030
  terminou sem recuperação comprovada; compilação não equivale a build completo.
- Faltam comparações com metas aprovadas, jornada integral autenticada,
  administração, testes entre contas e conclusão da validação remota dos
  formulários de conteúdo obrigatório.
- A entrega real do e-mail de recuperação e a troca completa da senha continuam
  pendentes de uma caixa controlada.

Referência operacional: [diagnóstico do build](changes/otimizar-performance-app/validation/isolamento-build-2026-10-20.md).

## Registro Git

Cinco commits em 20/10, após `d91a2bb`:

1. `a7dcda6` — Adicionando botao Verificar Senha.
2. `c045cec` — fix: corrigir avaliações por obra e melhorar carregamento do catálogo.
3. `1300b1b` — Configuracao Inicial do Recuperar Senha.
4. `61de9bb` — perf: otimiza carregamento e paginação social.
5. `c2665f3` — perf: reduz consultas na comunidade e melhora isolamento dos testes.

Antes de criar este relatório, `git status --short` estava vazio: as alterações
anteriores estavam commitadas. Este relatório e sua referência no README são
alterações documentais posteriores ao último commit.
