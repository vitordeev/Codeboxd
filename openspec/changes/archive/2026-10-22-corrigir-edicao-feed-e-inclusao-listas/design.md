## Context

SocialState decide POST/PUT depois de yield, validação da sessão e persistência
de obra. Fechar o diálogo ou resetar estado limpa edit_post_id; decidir o método
depois dessas operações permite transformar edição em criação. O PUT Xano local
usa db.edit com verificação de autoria. A causa exata no navegador ainda deve
ser verificada; o risco de perda de contexto é observável no código.
Listas usam seletor do catálogo já carregado; ficha tem só duas listas base.

## Goals / Non-Goals

**Goals:** editar o mesmo ID, associação opcional, buscar e adicionar aos quatro
tipos de obra e às listas próprias. **Non-Goals:** performance global, limpeza
de posts históricos duplicados, mudança de papéis, e-mail, Docker ou novos provedores.

## Decisions

- Capturar identidade do post antes de qualquer suspensão, incluir ID no
  formulário, validar coerência/sessão e nunca fazer fallback de edição para
  POST. Bloquear fechamento/reset do editor enquanto salva e preservar rascunho
  em falhas. Manter envio único e imagens no caminho JSON/multipart existente.
- Busca específica de listas reutiliza TMDB/Kitsu/Open Library, ranking e
  persistência/deduplicação de identidade existentes. Escolha explícita antes
  da inclusão; mostrar vazio, busca, erro parcial e confirmação. Resultados
  tardios não podem sobrescrever consulta/lista/conta nova.
- A ficha abre seletor carregado de GET /lists autenticado e filtrado por
  autoria, incluindo privadas. Persistir obra externa só após confirmar destino.
  Proteções capturam conta, ficha e lista; sem status/nota implícitos ao adicionar
  em lista personalizada. Preservar atalhos atuais das listas base.
- Mudanças no backend só se necessárias; arquivos locais não comprovam contrato
  publicado. Testes de lógica, compilação e navegador com backend fictício são
  separados de operações remotas com conta controlada.

## Risks / Trade-offs

Respostas lentas → geração e contexto antes de aplicar resultados.
Lista alheia → filtro local e autorização Xano existente.
Duplicação → envio único no cliente e identity_key no backend.
Erro após escrita → não repetir automaticamente; confirmar estado recarregado.

## Migration Plan

Sem migração de dados. Validar regressões e compilar na .venv. Usar frontend
isolado para navegador, preservando servidor existente; produção conforme skill.
Rollback reverte somente estado/páginas/estilos desta change. Não excluir posts
ou listas existentes para ocultar a duplicação histórica.
