## Purpose

Facilitar a leitura e o uso do código de recuperação e informar prontamente o andamento do pedido sem gerar reenvios redundantes.

## ADDED Requirements

### Requirement: Mensagem de recuperação acessível
O e-mail MUST apresentar código contínuo de seis dígitos em destaque, prazo de 15 minutos, uso único e instrução para ignorar pedido desconhecido. MUST oferecer conteúdo HTML e texto simples, sem dependência de imagens externas para leitura.

#### Scenario: Leitura do código
- **WHEN** a pessoa abre o e-mail em cliente HTML ou texto
- **THEN** consegue identificar e copiar o código e ler seu prazo e instruções

### Requirement: Solicitação com feedback e reenvio controlado
A interface MUST apresentar estado de envio antes de aguardar a rede e impedir solicitações repetidas para o mesmo endereço durante o intervalo de 60 segundos após resposta aceita. MUST preservar respostas genéricas e não repetir automaticamente chamadas.

#### Scenario: Envio em andamento
- **WHEN** a solicitação começa
- **THEN** a interface indica envio e bloqueia cliques repetidos antes da resposta

#### Scenario: Reenvio imediato
- **WHEN** a pessoa solicita reenvio para o mesmo endereço antes do intervalo
- **THEN** a interface informa a espera restante sem chamar novamente o backend
