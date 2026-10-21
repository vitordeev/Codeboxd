# Biblioteca paginada: validação Xano real — 20/10/2026

## Resultado

O endpoint `GET /library` foi publicado no workspace Xano `147717`, e o dry-run
posterior confirmou que não há diferenças pendentes. A validação usou o app
Reflex em produção na porta 3031 e um proxy local limitado às rotas de login,
sessão, perfil próprio e biblioteca. O usuário entrou no Edge visível; tokens,
cookies, corpos completos e títulos não foram registrados.

Login, leitura de sessão, perfil e biblioteca responderam HTTP 200. A biblioteca
real retornou 4 itens em uma página, com `has_more=false`, IDs ordenados depois
do cursor, um único proprietário e todos os campos necessários à tela. Não
houve HTTP 429 nem requisições negadas pelo proxy. O relatório sanitizado está
em [JSON](biblioteca-paginada-xano-real-2026-10-20.json). O app normal foi
restaurado em 3030 após o teste.

Uma falha inicial do teste foi corrigida antes do resultado válido: o proxy
bloqueava por engano a leitura do próprio perfil, e a automação navegava à
biblioteca por URL direta em vez do link real da aplicação. Nenhuma dessas
falhas foi causada pelo endpoint publicado. Os registros sanitizados das
tentativas anteriores foram preservados nos respectivos arquivos JSON.

## Ativação local

Após o contrato autenticado passar, `LIBRARY_PAGINATION_ENABLED=true` foi
adicionado somente ao `.env` privado e o app normal foi reiniciado. A build de
produção terminou e `/login` e `/biblioteca` responderam HTTP 200 em `3030`.
O `.env` não foi exibido nem adicionado ao Git. Nenhuma chamada autenticada à
biblioteca foi feita contra o app normal após a ativação; a jornada autenticada
foi executada no servidor temporário com a mesma build e com a flag habilitada.

## Limites ainda abertos

A conta testada contém apenas quatro itens: continuação real, múltiplas
páginas, coleção extensa e isolamento entre contas ainda não foram validados
no Xano. Listas não foram paginadas nem alteradas. O sucesso confirma o contrato
da primeira página e a jornada autenticada desta conta, não a meta de quota do
app nem o encerramento da tarefa 6.2 ou da change geral. Continuação extensa e
falhas/429 permanecem cobertas por testes locais e de navegador com fixtures,
separados desta evidência remota.
