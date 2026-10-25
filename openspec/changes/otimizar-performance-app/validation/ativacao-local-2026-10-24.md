# Ativação do código atualizado — 24/10/2026

## Plano antes da execução

Usuário informou ter fechado todas as instâncias e autorizou a continuidade.
Vinculado à preparação das validações 7.4/9.1/9.3, preservando funcionalidades
e design. Checagem inicial não encontrou listeners em 3030/3031/3040/8000.
Preservar todo o working tree, inclusive exclusão preexistente do package-lock.

Iniciar somente a aplicação normal em produção com `.venv`, porta 3030,
`REFLEX_USE_NPM=true`, reutilizando o frontend isolado
`.local/frontends/feed-lists-15664` cujo processo de teste já foi encerrado.
Não definir `REFLEX_APP_MODULE_IMPORT`, URLs de API fictícias ou segredos em
comandos/logs. O backend deve importar o app normal e carregar a configuração
privada existente. Subprocesso oculto, com logs novos em `.local/`.

Verificar conectividade antes de iniciar para não herdar bloqueio de rede do
agente; se necessário, usar execução com permissão de rede. Aguardar endereço
efetivo nos logs e conferir HTTP local e as três seleções públicas TMDB no
navegador. Não contabilizar HTML 200 como comprovação de catálogo real.

Após ativação, retomar executor já preparado de jornada real com login manual
de membro, somente se a instância estiver saudável. Preservar limites, fixtures
marcadas, snapshots e limpeza restrita existentes; nunca extrair senha ou fabricar
sessão. Falta de login mantém etapas dependentes pendentes. Sem Docker,
publicação de contratos, contas novas ou mudanças de privilégio.

Rollback operacional: encerrar somente a árvore do novo processo se não subir
corretamente; preservar logs e frontend para diagnóstico. Registrar resultados
e limitações antes de atualizar critérios no checklist.

## Ajuste do executor antes da próxima tentativa

App iniciado e seleções TMDB aprovadas na segunda tentativa de navegador.
Executor real parou antes de abrir o Edge: há dois perfis no arquivo privado
do Xano, enquanto o instrumento exigia exatamente uma linha `access_token`.
Zero etapas, chamadas de verificação ou mutações. Não selecionar primeiro token
nem alterar configuração privada para contornar a ambiguidade.

Incremento de instrumentação 1.2/9.1: ler o perfil padrão declarado no formato
simples do CLI, exigir que `instance_origin` corresponda à origem HTTPS do app
e usar somente o token desse bloco. Sem padrão, aceitar somente correspondência
única de origem; rejeitar duplicatas, ausência, host diferente e ambiguidade.
Não instalar dependências ou imprimir perfil/token. Arquivos: executor existente,
testes de salvaguarda e esta evidência/checklist. Testar perfis múltiplos, origem
incorreta, padrão desconhecido e campos duplicados. Rollback: remover somente a
seleção por perfil e retornar à recusa segura anterior. Não altera app em execução.

## Resultados da ativação

- Prova de conectividade restrita falhou; execução autorizada com rede retornou
  `NETWORK_OK`. Nenhuma instância degradada foi iniciada pelo comando restrito.
- Launcher normal iniciado oculto, PID 3764, com `.venv` e frontend
  `.local/frontends/feed-lists-15664`. Logs privados:
  `.local/normal-performance-20261024-stdout.log` e
  `.local/normal-performance-20261024-stderr.log`.
- Build de produção concluído em 31 s. Endereço no log: porta 3030.
- HTTP: `/` 200; `/login` e `/listas` 307 para respectivas rotas com barra final,
  seguidas de **200**. Não interpretar normalização de rota como falha.
- Primeira verificação TMDB de navegador: timeout de 90 s na fileira de próximos
  filmes. Logs também registraram ConnectTimeout em parte de TMDB/Open Library.
  Falha preservada aqui; sem declarar causa de rede/quota comprovada.
- Diagnóstico serial com rede autorizada: `movies_now`, `movies_rated` e
  `movies_upcoming`, **20 itens cada**. Primeira forma do comando tinha erro de
  aspas e não fez consultas; comando corrigido passou.
- Segunda verificação real no navegador: **três fileiras com 20 cards**, aprovada.
  [Resultado](ativacao-tmdb-real-2026-10-24-tentativa-2.json). Não comprova todos
  os provedores/jornadas nem ausência permanente de timeouts.

## Executor autenticado

Primeira tentativa: [relatório](jornada-real-apos-ativacao-2026-10-24.json),
`RuntimeError` antes da janela por dois perfis de metadados. Zero etapas,
zero requisições de verificação, zero mutações. CLI `xano profile --help`
falhou com erro de ambiente `uv_os_get_passwd/ENOMEM`; não foi necessário
alterar CLI, dependências ou arquivos privados para selecionar o perfil.

Seleção de perfil padrão implementada e validada contra a origem do projeto,
sem registrar nomes ou tokens. O parser aceita somente o formato simples do CLI
e rejeita estruturas desconhecidas; não é um leitor YAML genérico. Sete testes
novos e seis salvaguardas existentes: **13/13 aprovados**, 0,146 s. Cobrem padrão,
origem única sem padrão, host incorreto, padrão desconhecido, nome de perfil URL
entre aspas, duplicatas, token ausente e HTTPS obrigatório.

Segunda tentativa iniciada em janela Edge temporária, aguardando login manual
de membro, com saída exclusiva
`jornada-real-apos-ativacao-2026-10-24-tentativa-2.json`. Mensagem
`READY_FOR_MEMBER_LOGIN` confirmada. App normal atualizado permanece em execução;
instrumento corrigido não exige reinício do app. Não encerrar 5.3/6.3/9.1 sem
resultado real e respectivos critérios completos. Estado **14/37**.

Suíte após corrigir a seleção de perfil: **354 testes aprovados**, 17,977 s
(`.venv/Scripts/python.exe -m unittest discover -s tests -q`). Nenhum código
do produto foi alterado após o build normal. A inicialização npm regenerou
manifest/lock globais: diferenças verificadas como formatação/prefixos `^`,
preservadas em `.local/normal-performance-20261024-generated/` e desfeitas
somente nesses arquivos gerados, mantendo o lock previamente ausente.
`openspec validate otimizar-performance-app --type change` e `git diff --check`
aprovados. Servidor normal permanece ativo; aguarda-se login para o executor.

Resultado posterior: usuário autenticou como membro, `/auth/me` respondeu 200.
A pré-verificação de metadados respondeu **403**, antes de qualquer etapa ou
mutação. [Relatório final](jornada-real-apos-ativacao-2026-10-24-tentativa-2.json).
Não aguarda mais login nessa execução: ela foi encerrada sem fixtures. Não
selecionar outro token, conceder privilégios ou contornar o 403. Continuação de
desempenho público e troca posterior do servidor documentadas em
[conexões de catálogo](conexoes-catalogo-2026-10-24.md).
