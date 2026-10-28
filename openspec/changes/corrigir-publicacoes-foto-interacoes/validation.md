# Implementação e validação — 28/10/2026

## Alterações

Foto anexada passa a ser a imagem principal do post. Obra associada usa cartão
com miniatura 44×62, título/link e placeholder quando falta capa. Mantidos
posts sem foto, sem obra e os controles de autoria.

Curtidas usam coração preenchido e cor ativa com aria-pressed, contagens
disponíveis e bloqueio durante requisição. Comentários saem do fim do feed e
abrem em diálogo Reflex com foco/escape, loading, erro local, vazio, avatares,
edição/exclusão próprias e composer controlado. Contratos Xano existentes.

Leituras fixam post, geração e sessão; respostas antigas são descartadas.
Escritas de comentário são serializadas; token de formulário recusa replay
de envio confirmado. Falha de escrita mantém o rascunho. Falha de refresh após
escrita confirmada informa que foi salvo e não repete o POST. Fallback de
/likes ausente permanece sob demanda, sem leitura por post ao carregar feed.

## Testes locais

- Skills reflex-docs/setup-python-env/reflex-process-management verificadas;
  ambiente existente `.venv`, Reflex 0.9.11.post1. Sem reinstalação ou Docker.
- Referência: [diálogo Reflex](https://reflex.dev/docs/library/overlay/dialog/).
- `.venv/Scripts/python.exe -B -m reflex compile --dry`: aprovado em 6,620 s
  no primeiro incremento. Build de produção isolado posterior também compilou
  os componentes finais.
- Suíte completa final: **432 testes aprovados**, em 52,665 s. Inclui onze
  testes novos de interações e adaptação do teste legado de likes ao evento
  com atualização progressiva. Foram cobertos concorrência, post/conta antigos,
  fechamento, ownership, falha e rascunho, replay e payload inválido.

## Navegador

Primeira tentativa `validation/browser-2026-10-28`: falhou antes dos cenários
por timeout de pré-render em /admin/catalog/books. Resultado preservado;
não representa validação visual do feed.

Segunda tentativa `validation/browser-client-prod-2026-10-28`: processo em
produção com REFLEX_SSR=false apenas no executor isolado. Build aprovado
(31 s), servidor de teste em 3031; código do app e dados sociais reais não
foram substituídos. A configuração do servidor normal não foi alterada.
O teste usa dados fictícios e imagem de fixture, não upload/curtidas/comentários
em conta real. Resultados visuais finais serão registrados após os cenários.

O executor anterior aguardou /login e expirou na prontidão; o harness agora
permite escolher a raiz como endereço de prontidão de SPA, mantendo /login como
padrão para os demais executores. `browser-spa-2026-10-28` chegou à publicação,
mas falhou porque as imagens fictícias HTTP foram corretamente recusadas por
catalog.safe_url. Fixtures corrigidas para HTTPS e interceptadas no navegador,
sem afrouxar o filtro do produto. Cada tentativa foi preservada separadamente.

## Limites

Sem publicação Xano, migração, gravações de negócio remotas ou reinício do
servidor normal. As changes administrativas e de performance foram preservadas.

## Resultado final

- [Resultado do navegador](validation/browser-final-2026-10-28/result.json):
  **8/8 cenários aprovados**, quatro variantes em 1440/390px: foto+obra,
  obra sem foto, foto sem obra e obra sem capa/título longo. Sem overflow
  horizontal ou erros JavaScript. Conferidos miniatura até 60×85, foto com
  largura superior a três miniaturas, link da obra, curtir/descurtir e contagens,
  vazio, criar/editar comentário, rascunho após 503, retry manual e Escape.
- Inspeção das capturas revelou contraste insuficiente herdado do tema claro
  e aviso geral persistente após 503 recuperado. Corrigidos com cores explícitas
  no diálogo e erro local para falhas transitórias; 401/403 continuam passando
  pelo tratamento de sessão. A execução final verifica cor computada do texto
  e ausência do aviso geral após recuperação.
- Build final isolado: compilação em 5 s, produção em 30 s; cenário final
  manteve REFLEX_SSR=false somente no executor. Não altera rxconfig.py.
- Suíte completa depois desses ajustes: **432 testes aprovados em 37,450 s**.
- Alteração incidental de formato/faixas de reflex.lock/package.json gerada
  pelo compilador foi removida depois de conferir que somente `^` e formatação
  divergiam do arquivo original. Sem mudança solicitada de dependências.
- `openspec validate corrigir-publicacoes-foto-interacoes --type change` e
  `git diff --check` aprovados. Checklist **6/6**, sem sincronização/arquivo.

Capturas de revisão: [feed no celular](validation/browser-final-2026-10-28/feed-390-1.png)
e [comentários no desktop](validation/browser-final-2026-10-28/comments-1440-1.png).
A instância normal em produção não foi reiniciada; requer recarga do processo
para servir o código novo. Nenhum teste interagiu com contas ou posts reais.
