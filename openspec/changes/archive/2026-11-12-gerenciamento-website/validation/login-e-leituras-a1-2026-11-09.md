# A1 — login manual e acesso de leitura, 09/11/2026

Após A0, o usuário autorizou prosseguir com **login manual seguro da conta admin
existente e verificação de sessão/acesso, mantendo somente leituras**. Esta é
autorização limitada de A1; não libera A2–A4, fixtures, escritas administrativas,
decisões, suspensão/reativação ou limpeza. A tarefa 9.2 segue aberta, **33/34**.

## Evidência real

[Resultado sanitizado](a1-session-access-2026-11-09.json): **passed=true**, dez
checks aprovados e sete requisições HTTP 200, com intervalo de 3,1 s. Uma chamada
POST de autenticação e seis GET, sem retry automático ou emissão de token via
Metadata. Não descrever o POST de login como leitura pura; a ausência de mutações
refere-se às operações administrativas sobre dados, não à emissão de sessão.

| Operação | Verificação esperada | Observado |
| --- | --- | --- |
| POST auth /auth/login | Credenciais fornecidas pelo usuário apenas no formulário local | HTTP 200; token recebido somente em memória |
| GET auth /auth/me | Conta aprovada ID 14, role admin e account_status active | Confirmado pelo servidor; sessão aceita |
| GET social /admin/dashboard | Acesso e métricas inteiras não negativas, sem campos secretos | HTTP 200; contrato básico aprovado |
| GET social /admin/users, page=1/per_page=1 | Acesso e contrato paginado sem segredos | HTTP 200; aprovado |
| GET social /admin/catalog, media_type=movie, page=1/per_page=1 | Acesso e contrato paginado sem segredos | HTTP 200; aprovado |
| GET social /admin/reports, status=pending, page=1/per_page=1 | Acesso e contrato paginado sem segredos | HTTP 200; aprovado |
| GET auth /auth/me ao terminar | Sessão ainda da mesma conta admin ativa | Confirmado |

O campo request_count inclui login e todas as leituras. Dez checks não são dez
requisições. Não foram criados dados de teste nem utilizados usuários/reports
existentes como alvos de mutação. Payloads dos registros não foram publicados.

## Limitação do que foi comprovado

O formulário usado é o login local seguro do executor, não a página Reflex
/admin/login. Esta execução comprova autenticação real e acesso API, mas NÃO
valida renderização atual, redirecionamentos da aplicação, membro/visitante/
suspenso, filtros/página 2 ou qualquer alteração administrativa. A leitura com
per_page=1 também não substitui a paginação UI de 25. Evidências antigas de UI
continuam aproveitadas com suas próprias datas/modalidades, sem nova contagem.

## Guardas do adaptador e preservação

Adaptador privado .local/admin_a1_20261109.py, subclasse do Probe existente, com
allowlist rígida de método/base/rota: somente POST auth/login, GET auth/me e
quatro GETs administrativos. Origem HTTPS Xano, auth/social na mesma instância,
teto de 12 chamadas e sem redirects HTTP automáticos. Nenhum executor histórico
de mutação ou limpeza foi chamado. A confirmação da conta é feita pelo servidor,
sem promoção ou alteração de role.

Verificação offline específica do adaptador, antes de concluir o login real:
cinco GETs simulados passaram; PUT de conta, POST de catálogo e DELETE de report
foram rejeitados antes do transporte. Zero rede real nessa verificação; não
confundir com execução dos endpoints de escrita no Xano. Evidência privada:
.local/admin-a1-20261109/offline-check.json.

Credenciais informadas só na janela Validação Codeboxd; nenhuma senha/token salvo
no código ou relatório. Servidor local e navegador encerrados, token descartado
da memória pelo finally do executor. Não se realizou revogação global de sessões.
As alterações locais anteriores e o lockfile foram preservados, sem commits/push.

## Próxima etapa

Acesso do admin confirmado; permanece necessário preparar as guardas locais do
executor integrado e confirmar o destino de homologação. A0 identificou apenas
branch v1/live e fonte live, sem isolamento existente. Antes de A2–A4, obter
aprovação específica de destino/lote, operações e limpeza/retenção. O login
atual não autoriza o conjunto de 239 registros proposto nem a exclusão de nada.
Sem dados descartáveis autorizados, não realizar os cenários negativos que
possam alterar contas, obras ou reports. Nenhum critério integrado amplo de
9.2 foi marcado como concluído por estes checks de API.
