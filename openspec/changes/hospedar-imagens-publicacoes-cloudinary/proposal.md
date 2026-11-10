## Why

O usuário escolheu avançar com Cloudinary e pediu preparar o ambiente enquanto cria a conta. Hoje anexos passam por storage.create_image do Xano; para evitar esse processamento, imagens futuras devem ser hospedadas externamente e referenciadas por URL.

## What Changes

- Preparar configuração privada e adaptador de upload assinado Cloudinary, desativado até credenciais e contrato remoto estarem prontos.
- Testar transporte e tratamento de falhas com respostas simuladas, sem depender de conta criada.
- Registrar integração posterior dos posts: salvar URL HTTPS e identificadores, controlar autoria e limpeza/substituição dos assets, preservar imagens legadas.

## Capabilities

### New Capabilities

- `external-post-images`: Hospedagem externa de anexos com assinatura privada e persistência de URL/identificadores.

### Modified Capabilities

Nenhuma spec principal alterada nesta preparação.

## Impact

.env privado, .env.example, serviço Python e testes, documentação OpenSpec. Nesta rodada não alterar SocialState ou publicar esquema/endpoints Xano. Uso da .venv sem Docker; httpx existente, sem nova dependência.
