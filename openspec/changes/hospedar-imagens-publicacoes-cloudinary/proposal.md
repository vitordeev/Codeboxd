## Why

O adaptador Cloudinary e um ensaio descartável já existem, mas os posts ainda enviam imagens ao processamento do Xano. Concluir o escopo de publicações já previsto nesta change exige persistência verificável, autorização no servidor e reconciliação durável, preservando imagens antigas.

## What Changes

- Reutilizar o adaptador assinado existente, sua validação de recibos e os testes; mantê-lo desativado até aceite e autorização de ativação.
- Reservar uploads no Xano antes do envio, vinculados ao usuário autenticado e à operação, com identidade e estado duráveis.
- Persistir metadados e vínculo com o post, verificando recibos e recursos no backend; não confiar em URL, dono ou identificador vindos do formulário.
- Integrar criação com/sem imagem, leitura, edição de texto, substituição, remoção da imagem e exclusão de post, com compatibilidade legada e gravação idempotente.
- Reconciliar falhas e resultados incertos sem retry cego, preservando rascunho, eventos e assets potencialmente referenciados.
- Propor retenção explícita e limpeza supervisionada apenas de arquivos próprios, sem referências e aprovados na prévia; respeitar cotas do provedor.
- Separar implementação local, publicação Xano, ensaio integrado e ativação. A rodada atual altera somente planejamento; aguardar aprovação das duas changes antes de implementar.

## Capabilities

### New Capabilities

- `external-post-images`: hospedagem externa, autorização, persistência, compatibilidade e ciclo de vida dos anexos. Capacidade já declarada nesta change ativa; ampliada em seu mesmo arquivo de spec, sem duplicação.

### Modified Capabilities

Nenhuma spec consolidada é reescrita nesta rodada. `social-feed`, `data-social-content` e os contratos de sessão permanecem compatíveis; a nova capacidade complementa seus comportamentos sem duplicar likes, comentários ou autoria dos posts.

## Impact

Na implementação futura: `services/cloudinary_uploads.py`, fluxo `save_post/remove_post` de SocialState, leitura de imagens no feed, contratos Xano de posts e nova reserva de assets, testes de integração e configuração privada do verificador no backend. A apresentação do compositor/feedback deve coordenar-se com `modernizar-ui-ux-codeboxd`; busca e listas não dependem do armazenamento de anexos.

Agora: somente OpenSpec. Sem código, ativação, mutação remota, push, merge, migração destrutiva ou descarte de trabalho local. Execução posterior com `.venv`, sem Docker. Publicação de tabelas/rotas, configuração de segredos, upload/limpeza reais e ativação exigem prévia e autorização específica; aprovação deste planejamento não as substitui.

## Estado comprovado e histórico

- Preparação original de 10/11: tarefas 1.1–1.3 concluídas, conforme [validation.md](validation.md); criação de conta era então pendente.
- Ensaios de 11/11: conta Free aceita em GET /usage, upload/download/exclusão do PNG descartável com HTTP 200 e bytes idênticos, conforme [evidência real](ensaio-real-2026-11-11.md). O ensaio usou ferramenta independente e não validou posts nem o adaptador endurecido posteriormente.
- Código local não commitado: recibo/versão/URL e payload por autor; [contrato candidato e 632 testes históricos](contrato-integracao-2026-11-11.md). Nesta rodada de planejamento esses testes não são reapresentados como nova execução.
- Marcos originais **3/5**, com 2.1/2.2 abertos. Desdobrar o trabalho em subtarefas não representa progresso funcional novo. Flag permanece desativada no último estado verificado; nenhum acesso remoto é necessário nesta rodada.
- Os relatórios datados anteriores permanecem preservados e descrevem suas próprias rodadas. A restrição inicial a SocialState foi da preparação; esta proposta planeja a conclusão já reservada em 2.1/2.2, sem iniciar implementação.
