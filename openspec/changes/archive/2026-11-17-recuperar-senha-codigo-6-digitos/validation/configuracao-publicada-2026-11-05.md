# Conferência da configuração publicada — 05/11/2026

Pedido atual: concluir o projeto, conduzindo as decisões técnicas sem exigir
novo diagnóstico pelo usuário. Nenhum segredo foi exibido ou copiado para
este documento.

Leitura autenticada de `GET /api:meta/workspace/147717/multidoc` com
`env=true&records=false`: **HTTP 200**. As variáveis `RESEND_API_KEY` e
`RESEND_FROM` estão presentes no ambiente exportado do workspace.

Consulta de `GET https://api.resend.com/domains` usando em memória a chave
desse ambiente publicado: **HTTP 401, `restricted_api_key`**. A chave tem
prefixo Resend, corresponde à configuração local e não é máscara/redação.
O código indica permissão restrita para essa consulta; **não comprova chave
inválida ou impossibilidade de enviar e-mail**. O remetente publicado usa o
domínio de testes `resend.dev`. Isto supera a limitação da sondagem de 04/11
que não conferiu a chave publicada, mas não testa envio nem recebimento.

Para concluir 3.4/3.2, continua necessário confirmar envio aceito pelo provedor
e remetente elegível para a caixa de uma conta controlada. Não criar conta em
e-mail de terceiros, ler código no banco como prova de entrega, enfraquecer
a autenticação ou substituir o provedor sem configuração verificável.

Nenhuma variável alterada, endpoint publicado, mensagem enviada ou senha
modificada nesta conferência. **8/10 mantido**, 3.2/3.4 abertas.

## Ajuste planejado do diagnóstico (3.4)

Guardar no executor `resend_readiness` somente o nome de erro conhecido,
por allowlist, além do HTTP. `restricted_api_key` deve indicar restrição de
permissão, sem concluir chave inválida. Descartar mensagens e campos arbitrários,
que podem conter endereços ou segredos. Testar respostas restritas, inválidas,
JSON malformado e nomes não permitidos, sem rede ou envio.

Implementado e validado: três testes novos de `test_resend_readiness`, incluídos
na suíte final de 494 testes aprovados. O instrumento registra nomes por
allowlist e não exporta mensagens arbitrárias. Conferido com a
[referência oficial de erros](https://resend.com/docs/api-reference/errors) e
[permissões das chaves](https://resend.com/docs/api-reference/api-keys/create-api-key).
OpenSpec global estrito 22/22 válido. Entrega real continua não executada.
