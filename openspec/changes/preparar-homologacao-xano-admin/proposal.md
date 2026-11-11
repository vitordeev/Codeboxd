## Why

O aceite administrativo precisa de dados descartáveis e o usuário escolheu
homologação isolada. Hoje só está acessível o workspace compartilhado 147717;
executar mutações nele contrariaria a decisão registrada.

## What Changes

- Preparar pacote de contratos sem registros, segredos, tarefas automáticas ou
  integrações de envio, para um destino Xano isolado e explicitamente aprovado.
- Verificar elegibilidade de sandbox pessoal/workspace separado sem presumir
  que o plano atual suporta recursos adicionais ou autorizar custos.
- Adicionar verificações locais que recusem origem compartilhada como destino,
  perda de isolamento ou importação de dados/env, e documentar ativação por etapas.
- Prover evidências distintas de preparação, criação remota, publicação, verificação
  de isolamento e disponibilidade para o piloto de gerenciamento-website 9.2.

## Capabilities

### New Capabilities

- `isolated-acceptance-environment`: preparação e identificação verificável de
  backend de homologação vazio, com contratos compatíveis e configuração separada.

### Modified Capabilities

Nenhuma. operational-reliability continua protegendo segredos/arquivos locais;
o novo contrato trata isolamento e bloqueio de operações no destino incorreto.

## Impact

Ferramentas locais de preparação/verificação, configuração de exemplo e OpenSpec.
Criação de recurso Xano e publicação somente após prévia e autorização específica,
sem alterar o workspace 147717, credenciais globais ou recursos existentes.
Sem copiar usuários, senhas, tokens, registros, uploads ou env de produção; sem
Docker, aquisição de plano/domínio, push Git, merge ou arquivo de changes.
