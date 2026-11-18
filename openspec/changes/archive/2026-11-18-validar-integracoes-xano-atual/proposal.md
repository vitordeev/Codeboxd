## Why

O usuário informou que não consegue criar outro ambiente Xano e pediu reformular as dependências e continuar. Exigir workspace adicional bloqueia validações que podem ser realizadas com testes locais, leituras e lotes controlados no ambiente existente.

## What Changes

- Substituir a estratégia de ambiente separado por uma matriz de testes locais, leitura/prévia no workspace atual e futuro piloto mutável limitado a fixtures comprovadas.
- Preservar `preparar-homologacao-xano-admin` como estratégia supersedida, com tarefas não realizadas abertas e histórico intacto; não converter cancelamento em entrega.
- Implementar ferramenta local que produz e valida plano de lote no Xano atual, vinculando destino, manifesto, baseline, recibos, conteúdo exato, prazo e política de limpeza.
- Reformular planejamento e acompanhamento de Cloudinary, UI e performance sem diminuir critérios de autorização, privacidade, concorrência, persistência e limpeza.
- Distinguir autorização de estratégia de autorização de publicação/mutações concretas. Nesta rodada executar código/testes locais e prévias; um plano não executa chamadas remotas.
- Atualização autorizada em 17/11: executar o piloto limitado `cbshared_74089c52e9bb` já apresentado e aprovado pelo usuário, incluindo provisionamento, verificação e limpeza estritamente enumerados na prévia; sem publicação de contratos.

## Capabilities

### New Capabilities

- `controlled-shared-acceptance`: planejamento verificável de validações no Xano existente com proteção de registros anteriores e aprovação vinculada ao lote.

### Modified Capabilities

Nenhuma spec principal precisa mudar. A estratégia isolada era uma capability da change ativa anterior, não foi consolidada como obrigação do produto.

## Impact

Ferramenta e testes em `tools/` e `tests/`; planejamento/evidências e documentos centrais em `openspec/`. Preservar APIs e guardas históricos, `.venv` sem Docker, dados e flags atuais. Sem provisionar ambiente, compras, publicação, reset de conta, mensagens, importação de dados/env ou limpeza remota nesta rodada.
