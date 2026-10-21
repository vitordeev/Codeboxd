## Why

A revisão encontrou arquivos privados/gerados rastreados no Git, ambiente `.venv` sem dependências, mensagens de upload com escapes literais. A conferência do Reflex também identificou URL de banner construída como expressão de frontend dentro do backend.

## What Changes

- Proteger arquivos locais e retirar do índice os privados/gerados, preservando cópias locais.
- Verificar histórico remoto sem imprimir segredos; registrar necessidade de rotação quando houver exposição.
- Padronizar `.venv`, instalar as dependências e documentar comandos reproduzíveis.
- Corrigir mensagens de upload e a URL de banner enviada ao Xano.
- Manter execução local sem Docker, conforme decisão do usuário; reverter os ajustes de Docker desta rodada.
- Reconciliar documentação e verificar regressões locais, mantendo evidências reais pendentes explícitas.

## Capabilities

### New Capabilities

- `operational-reliability`: Proteção de arquivos locais, execução reproduzível, mensagens de upload legíveis e armazenamento persistente de imagens.

### Modified Capabilities

Nenhuma. As correções mantêm os contratos funcionais já entregues.

## Impact

`.gitignore`, índice Git, requisitos/ambiente, serviço de upload, estado de perfil, testes e documentos de retomada. Sem reescrever histórico Git, revogar credenciais automaticamente, publicar Xano ou hospedar a aplicação. Administração continua acompanhada em sua change própria.
