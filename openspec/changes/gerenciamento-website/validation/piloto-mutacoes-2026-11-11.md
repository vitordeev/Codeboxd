# Preparação do piloto de mutações — 11/11/2026

Vínculo: 9.2, gerenciamento-website, 33/34. Continuação após leituras reais
aprovadas; ainda sem autorização específica de escrita/limpeza. Branch própria
task/admin-readiness-20261111. Não publicar, criar fixtures ou excluir registros.

## Plano antes da implementação local

Implementar planejador offline e guardas de limpeza do primeiro subconjunto do
plano completo existente. Sem rede, .env, credenciais, CLI de apply ou transporte
real. Não habilitar o executor histórico que exclui event_log. Preparar exemplo
determinístico de recursos e testar IDs alheios, deriva e dependências antes de
propor qualquer escrita. Reconciliar também simulação de updated_at de user com
o contrato existente; jamais liberar alteração de identidade/papel por esse motivo.

## Primeiro subconjunto, sem reduzir o aceite final

- Duas contas member R/B, dois perfis e quatro listas do cadastro: oito registros.
- Oito obras sintéticas de seed (duas por tipo), entre as 96 do plano completo.
- Uma publicação textual de R, sem imagem.
- Oito reports de R (quatro message, dois post, dois media), os oito destinados
  a revisão em duas larguras no plano completo.

Total: **25 registros de domínio**, além de auditoria normal. R/B nunca admin;
conta A existente é somente ator e nunca alvo. Sem e-mails, uploads ou provedores
de catálogo. Seed usa source=test, não identidades públicas artificiais de provedor.

Piloto cobre E1/E2/E3/E5 e parte de E6/E7; não cobre sozinho E4 nem a segunda
página com 25+1 linhas da UI. Restante do plano continua obrigatório: mais 24
contas, 88 obras seed, oito criações pela UI e 22 reports. Somados aos 25 do
piloto, respeitam o teto histórico de 239; não marcar 9.2 completa pelo piloto.

## Política de limpeza proposta

Reter R/B, seus perfis/quatro listas e oito reports revisados: **16 registros**,
mais todos os eventos. Desativar apenas R/B ao final, com auditoria, após
autorização. Remover somente as oito obras seed e o post do próprio lote
(nove registros), após verificar identidades, snapshots e referências externas.
Se houver referência de terceiros ou política de cascata não confirmada,
interromper; não ampliar silenciosamente retenção ou exclusão.

Nenhum event_log é candidato a remoção. ID retornado deve ser novo em relação
ao baseline; prefixo sozinho não comprova autoria. Antes de limpar, comparar
todos os originais e registros próprios, e verificar relações de outras tabelas.
O preview offline não comprova cascatas publicadas, execução remota, auditoria
real ou autorização. Limpeza A4 não pode ser inferida de aprovação de leituras.

## Dependências para aplicar

Confirmar destino isolado ou aceitar nominalmente efeitos visíveis no workspace
compartilhado 147717/v1/live; reler contratos/referências/cotas; preparar executor
real de provisionamento e integração da UI com allowlist do manifesto e journals;
obter A2/A3/A4 com contagens/retencão/limpeza explícitas. Apenas depois criar lote.
Não apresentar um comando remoto ainda inexistente como pronto para uso.

## Resultado local

Criados `tools/admin_fixture_lifecycle.py` e 12 testes. Plano concreto em
[piloto-plano-2026-11-11.json](piloto-plano-2026-11-11.json): 25 registros,
16 retidos e nove candidatos a limpeza, sem execução remota. Prefixo não basta:
guardas comparam recibos exatos, snapshots, baseline de originais, identidade,
donos, inventário completo e referências revisadas. Verificam R/B desativados e
member, reports terminais, revisor e evento final de auditoria de cada alvo.
Referências externas ou deriva bloqueiam o preview inteiro. Preview não executa
DELETE, não emite permissão reutilizável e não valida sozinho cascatas do Xano.

O recebimento do inventário e dos recibos é fronteira de confiança: eles precisam
vir de coleta completa/provisionamento independente. Flags de revisão não provam
paginação ou ausência de relações não inspecionadas. O módulo não é executor de
provisionamento/limpeza real e não carrega configurações ou credenciais.

RehearsalExecutor preservado exclusivamente em MockTransport/origem .invalid.
Verificador de status ajustado ao updated_at do contrato user: permite somente
timestamp numérico positivo/finito, sem regressão em relação ao anterior; mantém
papel e demais campos protegidos. Dois testes novos verificam sucesso com timestamp
e interrupção sem retry para valor inválido. Não houve alteração de endpoint ou
de política do produto. Catálogo/Reports continuam com suas regras próprias.

Validação pertinente: **24 testes do executor, 26 guardas e 12 do ciclo de vida
passaram** (62 locais). Nenhuma rede real nesses testes. Essa contagem não se
soma à suíte completa para representar testes únicos adicionais. Não repetido
o navegador real de leitura já aprovado. Sem novo login, seed, mutação, limpeza,
publicação, push ou arquivo nesta preparação. 9.2 continua aberta.

Suíte completa após essas alterações: **583 testes passaram em 25,373s**,
log privado `.local/tests-admin-pilot-20261111.log`. Reflex/app não alterados;
não repetir compile/build de leitura apenas por novos helpers Python offline.

## Pré-voo de leitura atual

[Evidência](piloto-preflight-2026-11-11.json): 11 GET Metadata com intervalo
mínimo de 3,1s, todos 200. Workspace 147717 confirmado; listagem com uma branch
marcada live e uma única fonte de dados. Não há isolamento adicional demonstrado.
Sete esquemas de tabelas foram lidos sem registros, env ou segredos.

Os detalhes recebidos não expõem as chaves de política de exclusão pesquisadas;
isso NÃO prova que cascatas estão desativadas nem que excluir seja seguro.
Comportamento efetivo de exclusão continua não confirmado. Nenhum teste de
DELETE/seed foi feito para descobri-lo. Não iniciar lote que exija limpeza sem
destino/retencão decididos e referências/cascatas verificadas.

Antes do executor real, é necessária decisão de destino: homologação isolada
com contratos compatíveis, ou autorização nominal para efeitos visíveis no
workspace compartilhado. A implementação offline não escolhe esse risco pelo
usuário. A escolha de destino não equivale a autorização irrestrita para A2–A4.

## Destino escolhido pelo usuário

Usuário escolheu ambiente de homologação. Essa decisão exclui a alternativa
de executar o piloto no workspace compartilhado atual sem nova decisão explícita.
Não criar source/branch/workspace nem importar contratos como efeito implícito.

[Descoberta de leitura](descoberta-homologacao-2026-11-11.json) encontrou um perfil
configurado e um único workspace acessível, 147717, o já usado pelo app. Nenhum
workspace adicional de homologação identificado nas credenciais existentes.
O pré-voo anterior encontrou uma branch live e uma fonte nesse workspace; não
há isolamento adicional demonstrado. Nomes/URLs/segredos não foram publicados.

Falta identificar workspace/instância/fonte isolados e configuração privada
correspondente, ou planejar criação de homologação vazia em escopo próprio.
Consultar o usuário antes de provisão remota; não copiar usuários ou credenciais
do ambiente atual. Contratos compatíveis e ator admin do destino ainda precisam
ser verificados depois de identificado o destino. Backend local/.venv não isola
automaticamente a base Xano. Nenhuma fixture criada, alterada ou removida.

Continuação: usuário autorizou preparar o ambiente ainda inexistente. Trabalho
de infraestrutura foi separado na change preparar-homologacao-xano-admin,
branch/worktree task/homologacao-xano-20261111. Pacote de 32 contratos preparado,
573 testes da respectiva branch aprovados. Sandbox retornou HTTP 500; criação
de workspace vazio retornou 403/ERROR_CODE_ACCESS_DENIED, nome ausente após a
tentativa. A obtenção de destino isolado segue dependente de permissão/plano
ou instância disponibilizada pelo proprietário; causa específica não confirmada.
Nenhum contrato publicado, seed ou limpeza nesta branch administrativa. Não
trocar automaticamente o destino escolhido por live. Evidências completas na
change nova, sem copiar seus artefatos entre branches antes da integração.
