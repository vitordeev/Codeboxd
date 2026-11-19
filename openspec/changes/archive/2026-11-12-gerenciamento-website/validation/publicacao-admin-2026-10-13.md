# Publicação e validação administrativa — 13/10/2026

Publicação autorizada pelo usuário após o preview apresentado na rodada anterior.
Tarefas relacionadas: 2.1–2.3, 3.1 e preparação de 9.1/9.2. Checklist permanece
17/34; cenários admin/desativado e persistência ainda não foram comprovados.

## Publicação efetiva

- Antes da alteração: CLI exportou 67 documentos de estrutura remota para
  `.local/xano-before-admin-publication-2026-10-13`, sem `--records`/`--env`.
- Dry-run limitado: uma tabela `report` e nove endpoints novos. Nenhuma mudança
  em `profile`, `media` ou `/likes` foi incluída.
- A primeira importação falhou por ausência de `input` em `admin/dashboard`.
  Depois da falha, o mesmo dry-run continuou indicando os dez objetos novos.
- Corrigido `input` com `page` e `per_page` para atividade recente (padrão seis,
  máximo 100). Os totais continuam agregados; pendências continuam limitadas a
  cinco. A interface atual continua compatível com a lista `recent_posts`.
- Novo preview manteve o escopo; o push confirmou **10 documentos publicados**
  e **10 GUIDs sincronizados** nos arquivos locais.
- Dry-run após publicação: **No changes to push** para os mesmos includes.
- Não foram importados registros, concedidos papéis, suspensas contas ou
  desativadas transações. Nenhum dado existente foi truncado/excluído pelo push.

```powershell
xano workspace push -d xano -w 147717 --dry-run -i 'table/report.xs' -i 'api/codeboxd/admin_*.xs' -i 'api/codeboxd/reports_POST.xs'
```

## Acesso remoto atual

[Resultado após publicação](admin-read-after-publication-2026-10-13.json): GETs de
dashboard, usuários, catálogo e reports retornaram **401 para visitante** e **403
para membro**. Login e identidade das duas contas de teste existentes foram
verificados; papéis `member`, estado `active`. Uma primeira rodada encontrou
429 e ficou parcial; o probe foi adaptado para repetir 429 com espera limitada.
Os oito resultados finais acima passaram. Admin e desativado foram explicitamente
não executados por falta de tokens/contas aprovadas.

O exit code 1 do probe completo indica os cenários faltantes, apesar dos oito
GETs verificados. Não interpretar esse código como validação integral aprovada.
Não houve teste de autorização em mutações administrativas nesta rodada.

## Navegador e limites

O Edge headless verificou redirecionamento de visitante de `/admin` para
`/admin/login`, login comum e bloqueio de membro em `/admin`. A página de login
ficou sem overflow horizontal em 1440 e 390 pixels. Isso não valida os módulos
administrativos autenticados completos: tarefas 6.3/9.2 continuam abertas.

O teste de imagem do feed encontrou defeitos transversais P.5, acompanhados em
[uploads e sessão](../../../validation/uploads-and-session-2026-10-13.md).
Redefinição de senha: [teste negativo P.6](../../../validation/password-reset-negative-2026-10-13.json)
rejeitou código inválido (401) e confirmou senha original funcionando (200), sem
enviar e-mail ou trocar senha; entrega real permanece pendente.

## Credenciais e próximo passo

Conferência sem emitir valores confirmou que `TMDB_READ_TOKEN` atual continua
igual ao token presente no histórico Git. Rotação não foi executada: requer nova
credencial pelo painel do provedor e atualização local de `.env`. Não remover a
credencial atual antes de ter uma substituta funcional. Contas de teste não foram
modificadas. [Auditoria resumida](admin-member-results-2026-10-13.json).

Usuário foi consultado sobre conta administradora e conta controlada para
suspensão/reativação e recuperação de senha. Concessão de admin continua manual,
conforme design. Depois de identificadas as contas, validar autorização em todos
os endpoints, contagens, filtros, relatórios, auditoria e interface completa.
