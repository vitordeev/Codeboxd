## Context

Ver proposal.md. post() em pages/social.py usa post-cover de largura integral
antes da foto; feed_page() coloca a discussão após toda a lista. like() consulta
discussion para compatibilidade com /likes ausente, mas não bloqueia duplicação.
discussion() aceita resposta de post antigo; save_comment() não fixa contexto.
Ambiente existente .venv, Reflex 0.9.11.post1; três skills Reflex verificadas.

## Goals / Non-Goals

**Goals:** foto principal, obra compacta, interação reconhecível, acessibilidade
e consistência em desktop/celular. Referência Instagram é de hierarquia/interação,
sem depender da marca ou reproduzir recursos não suportados pelo backend.

**Non-Goals:** novas APIs, redesenho global, replies, curtidas de comentários,
publicação remota, Docker e alteração da autenticação.

## Decisions

- Cartão de obra com capa pequena/título e link em todos os posts associados,
  incluindo sem foto e sem capa; foto pessoal não é substituída pela capa.
- Diálogo Reflex controlado para comentários, com foco/escape e rolagem;
  abertura identifica imediatamente o post e mostra loading/erro/vazio local.
- Avatares e texto em linhas compactas; controles de autoria existentes mantidos.
- Estado de envio/curtida bloqueia cliques enquanto pendente; confirmação só
  após API. Fixar post, sessão e geração em leituras/escritas. Rascunho mantido
  na falha; token de formulário evita replay de submit concluído.
- Preservar fallback por discussion quando /likes está ausente; não introduzir
  consulta por post ao carregar feed. Sem contagem inventada quando não fornecida.

## Risks / Trade-offs

Respostas fora de ordem → geração/post/sessão antes de aplicar. Erro após escrita
confirmada → não repetir mutação para tentar recarregar comentários. Diálogo
móvel → altura limitada, rolagem e formulário acessível. Regressão de uploads/
edições → suíte existente e testes de interação. Rede real não comprovada por fixture.

## Migration Plan

Sem migração. Validar testes, compile seco e navegador com serviços fictícios
em frontend isolado, 1440/390px. Manter app normal e arquivos históricos intactos.
Rollback por reversão dos trechos da change. Evidências distinguem local, browser
com fixtures e validação remota não executada.
