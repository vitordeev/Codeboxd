# Biblioteca paginada — implementação local, 20/10/2026

## Autorização e estado

Usuário respondeu “continue” à proposta de preparar novo contrato somente de
leitura, estado/tela da biblioteca, testes e OpenSpec. Publicação no Xano,
ativação, reinício e navegador não fazem parte desta autorização.

`LIBRARY_PAGINATION_ENABLED=false` por padrão; `.env` privado intacto.
O aplicativo em execução continua no fluxo anterior. Nenhum endpoint remoto
foi publicado, nenhuma conta/dado real foi utilizado nesta rodada.

## Contrato candidato

Arquivo: `xano/api/codeboxd/library_GET.xs`, GET `/library?after_id=0`, auth user.
Ator obtido de `$auth.id`; rejeita usuário inexistente/desativado. Sem input
de outro usuário e sem mutações. Consulta interações desse ator com ID maior
que o cursor, ordem crescente de ID, join de mídia por chave primária.
Projeta apenas ID/usuário/mídia/status/nota/crítica/spoiler e título/tipo/capa/ano.
Consulta até 21 registros para devolver até 20 e informar `has_more` com exatidão,
inclusive quando há exatamente 20. Resposta `{items: [...], has_more: bool}`.
Não executa consulta individual por obra nem contagem integral de registros.

Cliente usa último ID da interação como próximo cursor; não usa ID da mídia
nem offset. Excluir item anterior não desloca o próximo lote. Inclusões novas
com ID maior podem aparecer na continuação; atualizar a página reinicia a leitura.
Não há snapshot transacional de toda a navegação nem total global exibido.

Referências primárias consultadas: [database operations](https://docs.xano.com/xanoscript/function-reference/database-operations),
[array slice](https://docs.xano.com/xanoscript/filter-reference/array) e
[Reflex yield](https://reflex.dev/docs/events/yield-events/).
Sintaxe baseada nessas referências e nos contratos existentes do repositório;
não houve execução/validação do XanoScript em um runtime Xano nesta rodada.

## Implementação e testes locais

- Com flag habilitada, carga inicial lê somente um lote via `/library` com
  `paginate=False`. Não baixa `/media`, `/interactions` ou `/profiles`.
- Mostrar mais busca um lote adicional, indica carregamento e bloqueia envio
  concorrente. Mantém cards e cursor se a página falhar; tentativa é manual.
- Resposta inválida não é aplicada parcialmente. Valida formato, limite,
  proprietário, IDs crescentes e continuação. IDs de mídia repetidos não
  duplicam cards; cursor continua pelo ID da interação.
- Resposta atrasada após troca de credencial, conta, rota ou reset é ignorada.
  401/403 descartam cards privados; 429 bloqueia novas leituras dessa biblioteca
  pelo prazo informado. Transporte geral/retries preexistentes não foram alterados.
- Carregamento/erro inicial não mostra mensagem falsa de biblioteca vazia.
  Título ausente recebe “Obra indisponível” preservando o link por media_id.
- Flag desligada mantém loader legado, incluindo cache e Mostrar mais local.

`tests/test_library_pagination.py`: 12 testes com fixtures fictícias. Coleção de
250 itens: primeiro lote com 20 cards e uma leitura de dados; acesso aos 250 em
13 leituras de dados (0,20,…,240), sem duplicatas, sem catálogo integral. Esses
números excluem validação de sessão, que foi simulada separadamente do transporte;
não são medição de latência nem contagem real do Xano. Cenários cobrem vazio,
20 exatos, falha/retry, cooldown, concorrência, formato inválido, deduplicação,
autorização rejeitada, respostas atrasadas e compatibilidade com flag desligada.

Verificação final: `python -m unittest discover -s tests` pela `.venv`: 229
testes aprovados (12 novos). `python -m reflex compile --dry`: sucesso em
4,551 s. `openspec validate otimizar-performance-app --strict`: válido.
`git diff --check`: sem erros. Aviso preexistente do dotenv na linha 1 continua;
arquivo privado não foi alterado. Sem reinício ou validação de navegador.

## Antes de publicar/ativar — aprovação separada

Revisar delta de um único endpoint, backup e nomes/esquema reais, validar
XanoScript no ambiente apropriado e conferir projeção, lookahead/has_more,
cursor, autorização de visitante/membro/desativado e isolamento entre contas.
Verificar particularmente que o join preserva interação com mídia ausente;
fixture de título nulo não prova o comportamento real do join. Se não preservar,
ajustar o contrato antes da publicação/ativação, sem aceitar omissão silenciosa.
Avaliar plano da consulta/índice existente para volume real; não foi criada migração.

Depois, publicar somente com autorização específica, validar endpoint real,
habilitar flag e reiniciar mediante aprovação; testar navegador em desktop/celular,
falhas, navegação e comparação real de requisições/tempo. 6.2 e 6.4 permanecem abertas.
Rollback: desligar flag e reiniciar, preservando endpoint legado e dados.
