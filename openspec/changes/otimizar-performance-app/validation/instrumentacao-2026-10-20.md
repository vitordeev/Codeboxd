# Instrumentação local e inventário inicial — 20/10/2026

## Autorização e escopo

Usuário aprovou criar instrumento local, testes e registros OpenSpec após a
proposta de contar chamadas, duração e HTTP 429 sem dados pessoais. A execução
desta rodada é exclusivamente simulada. Não houve alteração em `Codeboxd_main/`,
reinício, login real, criação de conta, envio de e-mail ou publicação remota.
Alterações anteriores no working tree foram preservadas.

## Instrumento

`tools/performance_probe.py` oferece `HttpProbe.capture()` como contexto para
um processo de diagnóstico isolado. Envolve temporariamente o envio assíncrono
httpx e restaura a função ao sair, inclusive em erro. Não modifica parâmetros,
resposta ou política de tentativas da aplicação. Não é importado pelo app.

Registra somente: serviço reconhecido, método permitido, rota com palavras
conhecidas e demais segmentos substituídos por `{value}`, status, resultado
genérico, início relativo e duração. Não retém URL original, host da instância,
query string, cabeçalhos, corpos ou mensagens de exceção. Há no máximo 2.000
eventos detalhados por captura; agregados continuam contando os demais.

Execução offline pela raiz:

```powershell
.venv/Scripts/python.exe -B -m tools.performance_probe --demo
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_performance_probe.py -v
```

Integração futura em um executor isolado, somente após aprovar seu cenário:

```python
from tools.performance_probe import HttpProbe

probe = HttpProbe()
with probe.capture():
    await scenario()  # executor define o cenário explicitamente aprovado
report = probe.report()
```

Limites: não se conecta a um servidor já ativo; não captura requests de outro
processo, APIs síncronas, tráfego do navegador ou bibliotecas sem httpx. Cada
`send` é contado; redirecionamentos internos podem envolver mais de um salto
de rede. Duração de resposta com streaming não inclui consumo posterior do corpo.
Contagem inclui retries efetuados pelo chamador, sem inferir quais foram retries.
O instrumento não registra Retry-After nesta versão; sua coleta sanitizada ainda
precisa ser planejada para o diagnóstico real. Não usar capturas sobrepostas ou
em servidor compartilhado. Uma captura por instância. Relatório fica em memória;
a demonstração imprime JSON sem persistir resultados.

## Inventário estático inicial

Fonte: rotas `Codeboxd_main/Codeboxd_main.py`, estados session/social/admin e
formulários existentes. Esta tabela mapeia cargas principais e ações conhecidas;
não comprova cobertura dinâmica de todo componente/evento. Chamadas condicionais,
paginação, cache, falhas e dados podem alterar o volume.

| Tela/rota | Entrada/carga principal | Subfluxos para medir |
| --- | --- | --- |
| `/login` | `SessionState.login`, sem carga on_load de API | Credenciais válidas/inválidas, lembrar sessão, destino por papel |
| `/cadastro` | `SessionState.signup` | Validação, criação, verificação da sessão, destino |
| `/redefinir-senha` | Handlers de solicitação e confirmação | Código, cooldown, senha nova, feedback |
| `/admin/login` | `guard_admin_login` | Sessão existente, login, acesso negado |
| `/` | `visit('home')` | Sessão, mídia Xano, coleções por provedor, busca, categorias, mais resultados, retry |
| `/conta`, `/perfil/[profile_id]` | `visit('profile')` | Sessão, referências mídia/perfis, detalhe, atividade, seguidores, edição/banner, seguir |
| `/obra/[media_id]` | `visit('media')` | Mídia interna, sessão, interação, listas padrão, trailers, streaming, relacionados, críticas |
| `/obra` | `visit('external')` | Detalhe externo, sessão, identidade Xano e mesmos complementos da ficha |
| `/biblioteca` | `visit('library')` | Sessão, referências, interações, nota/status e navegação |
| `/listas` | `visit('lists')` | Sessão, referências, listas padrão/públicas/próprias, itens, criar/editar/remover |
| `/comunidade` | `visit('community')` | Carregamento da home, pessoas, seguidores próprios e denúncia |
| `/feed` | `visit('feed')` | Sessão, referências, feed/posts/likes, discussão sob demanda, post/upload/curtida/comentário/denúncia |
| `/admin` | `load_dashboard` | Sessão/papel, indicadores, recentes e pendências |
| `/admin/users` | `guard_users_page` | Autorização, pesquisa/filtros, páginas, suspensão/reativação |
| `/admin/catalog/movies`, `/series`, `/books`, `/anime` sob `/admin/catalog` | Loaders por tipo | Autorização, filtros, páginas, criar/corrigir obra |
| `/admin/reports` | `load_reports` | Autorização, filtros/páginas, detalhe, decisão e auditoria |
| `/admin/demo` | Página de demonstração | Renderização sintética, sem equivalência com autorização remota |

## Diagnóstico inicial de login

Caminho estático de sucesso para membro, cache vazio e sem páginas extras:

1. POST `/auth/login`.
2. GET `/auth/me` antes do redirecionamento.
3. Em `/conta`, outra GET `/auth/me` pelo carregamento do perfil.
4. GET `/media` e GET `/profiles` em paralelo.
5. GET `/profiles/{value}` somente depois das referências.

Total esperado neste caminho: seis chamadas de aplicação; não é contagem real
observada. `_load_reference` pode buscar páginas extras e aguardar dados que
antecedem a apresentação do perfil. O transporte cria cliente por chamada,
possível custo de conexão a medir. Não remover validação da sessão sem verificar
garantias. Também foi observado GET de recuperação de senha sujeito à política
genérica de retry para GET; efeito colateral precisa de tratamento específico
em intervenção futura aprovada. Nenhuma dessas observações identifica a quota
ou endpoint causador do 429 relatado.

## Validação nesta rodada

Seis testes do instrumento passaram: contagens/status, ausência de segredos,
propagação de erro sem mensagem privada, limite de eventos com agregados,
restauração da função e classificação/sanitização. Demonstração offline contou
duas respostas sintéticas, uma 429 e uma 200. Durações não são benchmark do app.
`openspec validate otimizar-performance-app --strict` e `git diff --check`
passaram; houve somente aviso de fim de linha em lockfile já modificado.

Não houve compilação Reflex: nenhum código do aplicativo foi alterado, e o
instrumento não importa Reflex. O próximo passo é propor executor e cenário
de linha de base, seus arquivos, eventual servidor/reinício e acesso de teste,
pedindo autorização antes de criar ou executar. Tarefas 1.1/1.2 permanecem
abertas: inventário de eventos e autorização completa de medições ainda faltam.

Rollback: remover somente instrumento, seus testes e estes registros se aprovado;
não reverter alterações anteriores do usuário ou de outras rodadas.
