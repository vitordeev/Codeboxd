# Proposal

## Why

A pendência P.1 registra credenciais e contas de teste no histórico Git, embora o índice atual já tenha sido limpo. Precisamos identificar o alcance da exposição e invalidar os acessos afetados com evidência, preservando a operação local.

## What Changes

- Inventariar credenciais no estado atual e no histórico disponível, registrando somente nomes, categorias, localização e situação, sem valores secretos ou dados pessoais.
- Priorizar credenciais administrativas, de infraestrutura e contas privilegiadas; depois integrações externas, conforme o inventário confirmado.
- Substituir e revogar segredos afetados, atualizar seus consumidores e verificar acessos novos e rejeição dos antigos pelos mecanismos de cada serviço.
- Tratar senhas e sessões de contas de teste expostas e prevenir novo versionamento de segredos.
- Vincular evidências e limitações à P.1, sem declarar rotação ou limpeza remota a partir de verificações locais.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `operational-reliability`: acrescentar critérios de inventário seguro, revogação verificável e prevenção de reincidência de exposição de credenciais.

## Impact

Configuração local privada, consumidores de credenciais no Python e Xano, contas de teste, configuração de provedores e documentação OpenSpec. TMDB, DeepL, Resend, Xano e infraestrutura são candidatos a inventário, não exposições presumidas. URLs públicas não serão tratadas automaticamente como segredos.

Esta rodada cria somente planejamento. Reescrita do histórico Git, force-push, exclusão de contas/dados, hospedagem e Docker estão fora do escopo; eventual saneamento de histórico terá decisão própria após revogação. A change não altera funcionalidades sociais nem conclui as outras changes ativas.
