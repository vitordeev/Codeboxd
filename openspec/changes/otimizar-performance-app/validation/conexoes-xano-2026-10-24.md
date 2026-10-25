# Transporte Xano — 24/10/2026

## Plano antes da implementação

Usuário confirmou app mais fluido após pooling público e autorizou continuar.
Incremento transversal de requisições e medições 2.4/6.4/7.4/9.1/9.3; não mudar
funcionalidades, design, autorização, cache ou retry. Estado inicial **14/37**.
Preservar alterações anteriores e exclusão preexistente do package-lock.

Diagnóstico: `services/api.py` cria um AsyncClient por chamada Xano, inclusive
leituras consecutivas de perfil/biblioteca/feed e validação de sessão. Pooling
TCP não deve reutilizar identidade, headers, cookies ou conteúdo entre contas.

Implementar um cliente por loop no lifespan, separado do catálogo e de uploads.
Sem headers de autorização/default de usuário; token explicitamente por chamada,
cookies bloqueados e respostas nunca cacheadas pelo transporte. Manter timeout
10/connect 3, métodos, payloads, mensagens e número de tentativas. Fallback por
chamada fora do lifespan. Não tocar contratos remotos nem configurar permissões.

Arquivos: API, registro do lifespan, testes de isolamento/transporte e executor
de comparação real de leitura. Reusar padrão do catálogo sem refatoração ampla.
Validar duas contas intercaladas/concorrentes, visitante após membro, 401/403,
cookies, fechamento, loops e mutações sem retry. Suíte e compilação isolada.

Comparação real: login manual de membro em formulário loopback já existente;
três leituras (perfil próprio, primeira página da biblioteca e feed), cinco
pares com ordem alternada sem cache da aplicação, intervalo 3 s. Limite 40
requisições físicas incluindo login/validação; parar em falha/429. Sem mutações
ou acesso de metadados. Token/senha e payloads somente em memória, relatório
sanitizado de tempos/status/contagens. Não pedir credenciais pelo chat.

Se não houver login, manter medição remota aberta e concluir trabalho local
independente. Não atribuir ganho remoto a simulação. Após validações, build
isolado e troca somente do launcher normal identificado, com rede autorizada;
validar catálogo/rotas preservados. Rollback: remover lifespan/seleção de cliente
da API e reiniciar processo próprio, preservando pool do catálogo.

## Implementação e testes locais

`api_connection_pool` registrado no lifespan do app, com cliente separado do
catálogo. `_api_client` reutiliza apenas no mesmo loop e mantém fallback por
chamada. Timeout 10/connect 3 preservado; Authorization e Accept por chamada,
cookies recusados e nenhum cache novo. Multipart continua em transporte separado.

Sete regressões novas aprovadas: contas concorrentes e visitante, cookies,
token rejeitado sem contaminar outro, ausência de cache de resposta, grupos/
métodos/payloads, limites de retry/efeitos colaterais, fallback, encerramento e
isolamento de loops. Três regressões do comparador verificam 30 leituras físicas
em cinco pares, nenhum payload/token exportado, orçamento e propriedade.
O primeiro teste do contador usava patch do construtor HTTPX que ocultava o
instrumento; corrigido para substituir somente a fábrica local de clientes.
Sem chamadas remotas nesses testes.

`.venv/Scripts/python.exe -m unittest discover -s tests -q`: **374 testes
aprovados**, 34,332 s. Compile seco isolado com
`.local/compile-xano-pool-20261024`: **aprovado**, 11,533 s.

Executor `tools.xano_connections_measurement` iniciado em janela Edge temporária,
aguardando login manual de membro. Não acessa `.xano/credentials.yaml` nem API
de metadados; sem mutações. Comparação usa API real do produto, contabiliza
tentativas físicas e subtrai apenas as esperas deliberadas de 3 s do tempo ativo.
Tempo total inclui criação/fechamento dos clientes. O número máximo inclui login.
Hash de conteúdo somente em memória; relatório exporta apenas igualdade.

Build de produção em frontend próprio `.local/frontends/xano-pool-20261024`
em preparação, preservando app normal e o frontend do catálogo. Métricas remotas,
troca de servidor e browser serão registrados separadamente. Estado **14/37**.

## Comparação real concluída

Login manual aceito: tentativa inicial retornou 400, seguida de login 200 e
`/auth/me` 200. Não atribuir causa ao 400 sem evidência; sequência preservada.
Foram **33 requisições físicas totais**, incluindo autenticação, dentro do
orçamento de 40. As **30 leituras comparadas retornaram 200**, nenhum 429.
Cinco pares de igualdade aprovados, com ordem dos modos alternada.

| Modo | Mediana ativa das três leituras | Pior amostra | Chamadas por amostra |
| --- | --- | --- | --- |
| Cliente por requisição | 3.366,243 ms | 4.039,014 ms | 3 em todas as cinco |
| Pool Xano | 1.337,623 ms | 3.272,126 ms | 3 em todas as cinco |

Redução de **60,26% na mediana** das leituras perfil/biblioteca/feed neste
cenário. Tempos excluem somente pausas intencionais de 3 s; incluem criação e
fechamento de clientes. Não são tempos de página/navegador nem promessa de ganho
idêntico em toda ação. Mesmo conteúdo confirmado em cada par; hashes e payloads
não foram exportados. [Resultado bruto](conexoes-xano-real-2026-10-24.json).

Token descartado, formulário local/Edge da ferramenta encerrados pelo executor.
Não houve mutações, acesso de metadados ou mudanças de privilégio. Isolamento
real entre duas contas e jornada completa ainda não são comprovados por esse
cenário de membro único; os testes de múltiplos tokens são locais.

## Aplicação no app normal

Export de produção do frontend independente `xano-pool-20261024` aprovado,
build reportou 44 s. Log `.local/xano-pool-build-20261024.log`.
Conectividade real confirmada antes de encerrar somente launcher normal PID
16476 com horário de criação exato. Novo launcher oculto **10856** iniciado em
3030, produção com `.venv`/npm e frontend próprio. Logs privados
`.local/normal-xano-pool-20261024-stdout.log` e `-stderr.log`.
Build do run aprovado em 26 s, além da preparação de dependências; esse tempo
não integra a métrica de navegação. HTTP final `/`, `/login`, `/listas` e
`/biblioteca`: **200** seguindo normalização de rota. Isso comprova entrega HTML,
não autorização de visitante para dados privados.

Navegador público real: **três fileiras TMDB com 20 cards cada**.
[Resultado](conexoes-xano-browser-2026-10-24.json). Pool do catálogo preservado;
Open Library ainda registrou ConnectTimeout, mantendo limite conhecido da home.
Não foi executada jornada autenticada completa de navegador nesta rodada.

Manifest/lock gerados pelo build preservados em `.local/xano-pool-generated/`.
Diferenças de manifest verificadas como formatação/prefixos `^`, sem mudança das
versões; restaurado original e mantida ausência preexistente do lock. Nenhuma
atualização de dependência integra a entrega. Servidor permanece ativo com ambos
os pools; código novo aplicado, sem aguardar reinício. Estado **14/37**.

Fechamento: `openspec validate otimizar-performance-app --type change` e
`git diff --check` **aprovados**, somente avisos LF/CRLF em arquivos gerados.
