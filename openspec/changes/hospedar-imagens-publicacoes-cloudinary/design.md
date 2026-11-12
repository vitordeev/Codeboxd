# Design — conclusão planejada em 11/11/2026

## Context

Esta revisão atualiza o escopo existente de 2.1/2.2; não cria outra change nem
implementa funcionalidades. Proposta/specs/tasks são candidatos à aprovação do
usuário. As evidências anteriores são históricas, não operações desta rodada.

Conferido no código local: posts ainda usam `image_upload` multipart e
`storage.create_image` no Xano; `post` não tem os campos externos propostos.
`save_post/remove_post` e o feed funcionam com imagens legadas. O adaptador
Cloudinary local já valida assinatura, versão, URL canônica e namespace por dono,
mas gera sua própria identidade depois de iniciar a chamada e não é usado pelos
posts. O helper de payload não comprova autoria perante a API Xano sozinho.

[Ensaio real isolado](ensaio-real-2026-11-11.md): PNG 2×2 enviado, recuperado e
excluído com HTTP 200 e bytes iguais, antes desta rodada. Foi outro executor,
não um post. [Validação local anterior](contrato-integracao-2026-11-11.md):
632 testes, inclusive endurecimento posterior do adaptador. Plano Free e 0/25
créditos foram observados antes do ensaio; não tratar esse consumo como atual.

Mantêm-se `.venv` e Reflex 0.9.11.post1; Xano é autoridade de persistência,
autoria e sessão. TMDB/Kitsu/Open Library/Jikan não mudam. Homologação isolada
continua indisponível na evidência existente; nenhum aceite remoto pode ser
inferido de fixtures ou do teste de transporte Cloudinary.

## Goals / Non-Goals

**Goals:** concluir o fluxo de imagem do post de forma recuperável e compatível,
com associação verificável por usuário/publicação e exclusão supervisionada.

**Non-Goals:** migrar imagens antigas, remover marcas já incorporadas, alterar
avatar/banner, redesenhar o feed, criar atividade de listas, mudar provedores,
comprar plano/domínio ou publicar/ativar nesta rodada de planejamento.

## Decisions

### 1. Reserva durável e validação independente

Reservar antes de subir o arquivo. Nova tabela candidata `post_image_asset`,
com identidade exclusiva por cloud/public_id e vínculo obrigatório ao usuário
derivado de sessão atual válida. Para edição, vincular também ao post autorizado
e à revisão esperada de imagem. Essa reserva é a chave de idempotência.

Depois evoluir o adaptador para usar **exatamente** a identidade reservada,
`overwrite=false`. Não aceitar dono do formulário ou gerar outro ID no retry.
Fixar sessão, editor e operação durante awaits; troca de conta/editor impede
commit no contexto novo. Dúvida sobre upload deve deixar uma referência durável,
não somente um objeto de estado Reflex ou arquivo temporário de processo.

O commit Xano verifica reserva/dono/estado/versão e a assinatura Cloudinary de
`public_id`/`version`. Essa assinatura **não cobre** URL, asset_id, MIME ou tamanho.
Uma leitura server-side restrita do recurso no Cloudinary confirma asset_id,
versão, formato e metadados, no cloud configurado, antes de associar. Sem URL
arbitrária como origem de consulta e sem consulta genérica/listagem de assets.
O resultado verificado pode ser reutilizado na mesma reserva, sem confiar no
cliente ou compartilhá-lo como autorização entre contas.

URL de exibição é construída/validada pelo backend usando cloud configurado,
identidade, versão e formato permitido; não gravar URL livre. Rejeitar receipt
forjado, ID de outro dono, replay em outro post, recurso desaparecido ou versão
divergente. Verificar tipo real e bytes; manter limite de entrada de **5 MiB**
(5×1024², historicamente chamado 5 MB) e PNG/JPEG/WebP/GIF. Assinatura válida não
substitui validação do arquivo, de autoria ou de estado da reserva.

Alternativas rejeitadas: salvar só URL; confiar em prefixo/recibo no frontend;
usar somente Python como guarda da API; apagar por asset_id ou URL não verificados;
upload sem reserva seguida de limpeza em memória. Cada uma perde segurança ou
reconciliação quando há chamadas diretas, concorrência ou falha de rede.

### 2. Contratos de persistência candidatos

| Entidade/campo | Contrato proposto |
| --- | --- |
| `post.image` | Manter legado, sem migração/reprocessamento de arquivos existentes |
| `post.image_provider` | Nulo/legado ou cloudinary; só backend decide ao confirmar vínculo |
| `post.image_public_id`, `image_version`, `image_url` | Metadados verificados, anuláveis para posts antigos e sem imagem |
| `post.image_asset_record_id` | Vínculo ao registro durável próprio, não ID arbitrário do cliente |
| `post.image_revision` | Inteiro inicial 0, incrementado em replace/remove; checagem atômica evita substituição concorrente |
| `post_image_asset.id`, `user_id`, `post_id` | Reserva única, dono obrigatório; post nulo antes de criação, depois vínculo consistente |
| `cloud`, `public_id`, `asset_id`, `version`, `format`, `bytes`, `width`, `height` | Identidade reservada e metadados confirmados server-side; asset_id não autoriza excluir por si |
| `operation`, `state`, `expected_image_revision` | create/replace, estado permitido, revisão esperada quando aplicável |
| `created_at`, `updated_at`, `retain_until`, `last_error_code`, `attempt_count` | Retenção/reconciliação auditáveis, sem corpo bruto, credencial ou dado secreto |

Índice único de cloud/public_id, índices por dono/post/estado, integridade entre
post e registro. Bloquear exclusão em cascata do journal quando o post é removido.
IDs finais, constraints e paginação devem passar em validação/dry-run do Xano
antes de qualquer publicação. Assets assinados são evidência operacional privada;
não expor recibos/assinaturas/chaves em feed público, logs ou repr.

### 3. Contratos HTTP aditivos, não publicados

| Operação candidata | Entrada/resposta e garantias |
| --- | --- |
| `GET /post-image-capabilities` | Contrato v1 e disponibilidade de escrita; sem segredos. O cliente não ativa caminho externo apenas pela flag local |
| `POST /post-image-uploads` | Sessão válida; create ou replace, post e revisão quando edição. Retorna reserva/public_id esperado e estado; não fornece API secret |
| `GET /post-image-uploads/{id}` | Só dono ou operador autorizado, informa estado/post confirmado para reconciliar resultado incerto; não lista arquivos alheios |
| `POST /posts` / `PUT /posts/{id}` | Campos existentes preservados; contrato v1 acrescenta `image_action=keep|replace|remove`, reserva, recibo e revisão esperada. Campos ausentes em edição significam keep, nunca remoção |
| `DELETE /posts/{id}` | Autoria validada; transação remove post/filhos como hoje e deixa asset em fila durável. Não chama destroy antes de confirmar remoção |
| Leituras `/posts`, `/feed` | Projetar somente URL e metadados públicos necessários; não expor journal/assinaturas. Preservar paginação/formato consumidos hoje |
| Ferramenta supervisionada de reconciliação/limpeza | Prévia por IDs próprios e lote limitado, aprovação vinculada à prévia, releitura antes da exclusão; sem scheduler obrigatório |

Na API, keep não aceita simultaneamente reserva/novo arquivo; replace exige
reserva própria válida e não aceita imagem legada em paralelo; remove exige
post existente, autoria e revisão. Envio contraditório resulta em erro, sem
escolha silenciosa de um campo. POST sem imagem não depende de credenciais
Cloudinary nem de reserva. Formatos antigos de resposta continuam compatíveis;
dados operacionais novos usam contrato versionado/documentado.

POST com reserva é idempotente: dois commits da mesma operação devolvem o
mesmo post. Transação/lock protege reserva e post; segundo vínculo a outro post
é recusado. PUT aplica compare-and-set de image_revision para imagens; edição
de texto preserva os campos de imagem e regras existentes. Política de conflito
de texto não é ampliada silenciosamente por esta change.

### 4. Estados e retenção

Estados propostos: reserved → verified → attached; falhas podem levar a
reconciliation_required; remoção/substituição confirmadas levam o asset anterior
a cleanup_pending; deleted somente após resposta confirmada/reconciliação de
ausência. Cancelar uma reserva sem prova de ausência não apaga a referência.
Transições são verificadas no servidor, não valores editáveis pelo cliente.

Política candidata para aprovação: órfão confirmado e asset substituído recebem
carência mínima de **24 horas** após desvinculação/confirmação antes de entrar
em lote de limpeza. Asset attached não expira; resultado incerto não vence para
exclusão por tempo. Remoção explícita de imagem/post retira o vínculo do produto
imediatamente após a transação; limpeza física pode ocorrer sem carência, mas
continua sujeita à prévia e verificações. Essa distinção evita manter uma imagem
removida visível no app, sem prometer revogação imediata de CDN/backups.

Nenhuma exclusão automática nesta entrega. Executor futuro aceita por padrão
no máximo dez candidatos por prévia, exige autorização para aquele lote e
revalida dono/cloud/namespace/asset_id/versão, ausência de referências atuais,
retenção e estado. Autorização envelhecida ou estado alterado invalida o item.
Falha preserva pendência/auditoria e não destrói a imagem nova ou histórica.
Proposta explícita de retenção/lote não é configuração real já aplicada.

### 5. Matriz dos onze fluxos exigidos

| Fluxo | Comportamento esperado / evidência de aceite |
| --- | --- |
| Criar com imagem | Reservar → upload assinado → verificar → commit atômico; ler o mesmo post e imagem em outra sessão |
| Criar sem imagem | Caminho atual sem Cloudinary, inclusive quando o serviço está desabilitado ou indisponível |
| Consultar com imagem | Preferir vínculo externo verificado; fallback ao image legado; URL sem reprocessamento no Xano |
| Editar texto | Preservar imagem e identidade do post; não reenviar ou limpar asset |
| Substituir | Novo asset único, commit com revisão, anterior legível até confirmação e então fila; conflito não perde imagem antiga |
| Remover imagem | Ação explícita, confirmação/autoria/revisão; post permanece sem imagem; anterior só candidato próprio à limpeza |
| Excluir post | Confirmar transação e filhos; journal sobrevive para limpeza supervisionada; timeout exige reconciliação |
| Falha no upload | Rascunho preservado, sem post com sucesso fictício, reserva recuperável; não repetir a escrita automaticamente |
| Falha em persistir no Xano | Consultar reserva/post antes de compensar; HTTP 5xx/erro de rede sozinho não demonstra ausência de commit |
| Timeout/resposta incompleta Cloudinary | Manter public_id reservado, rejeitar recibo inválido, ler/reconciliar recurso exato e não apagar por suposição |
| Órfãos | Identificação durável, retenção, dono/propriedade/referências/estado revalidados, prévia aprovada e recibo de limpeza |

Imagem legada removida/substituída não é candidata a destroy Cloudinary. Não
apagar uploads antigos do Xano como efeito desta mudança. Deixar explícita no
produto eventual falha de limpeza sem reexibir como anexo um arquivo removido.

### 6. Integração Reflex e limites

Reutilizar staging validado, snapshot de sessão/editor, bloqueio post_saving,
preservação de rascunho, invalidação de cache antes/depois de escrita e feed
existentes. Depois de reserva, upload usa identidade prevista; resposta atrasada
de outra conta/editor não grava nem limpa no contexto novo. Com uploads externos
habilitados, erro externo é explícito, sem fallback silencioso ao Xano.

Flag desliga novas operações externas, não leitura das imagens já persistidas
nem reconciliação do journal por operador autorizado. Campos de imagem/controles
do editor devem coordenar-se com UI/UX sem alterar catálogo, likes ou comentários.
Backend possui chave de desativação própria para recusar reservas novas quando
contrato/cota não está disponível; cliente verifica versão antes do novo fluxo.

Cloudinary: 25 créditos compartilhados no plano Free observado; tamanho,
armazenamento, tráfego, transformações e Admin API têm limites. Verificar
consumo antes de ensaio/ativação, restringir consultas de reconciliação por lote,
respeitar Retry-After e não automatizar compras. Receber 429 não autoriza retry
de upload/commit/destroy. Alertas de 70%/85% de créditos são proposta operacional,
sem prometer contadores em tempo real ou custo zero. Não fazer teste de carga real.

### 7. Autorização e dependências reais

| Ação | Condição para executar depois |
| --- | --- |
| Código/modelos/tests locais | Aprovação das duas changes e início explícito da implementação |
| Inspeção remota/backup de contratos | Destino identificado e acesso autorizado; sem exportar registros/env privados em evidências públicas |
| Publicar tabela/journal/campos/endpoints Xano | Prévia exata, compatibilidade/dados preservados, rollback revisado e autorização específica de publicação |
| Configurar segredo/verificador no Xano | Autorização específica de configuração, valor por canal privado e escopo mínimo; não copiar todo o .env |
| Upload/commit/edição/exclusão de posts de teste | Conta/assets descartáveis identificados, cenário/volume/limpeza aprovados; autorização antiga do PNG não se estende a posts |
| Limpeza física de assets | Prévia restrita + autorização daquele lote e verificação novamente na execução |
| Ativar flag no app/backend | Contratos/ensaio completos, aprovação específica e janela/rollback; não habilitar por existir uma chave |

Falta de homologação isolada mantém aceite remoto pendente. Não usar live como
fallback automático nem pedir compra de plano como etapa obrigatória. UI pode
avançar com fixtures, mas não fecha Cloudinary pela aparência do feed.

## Risks / Trade-offs

- Assinatura incompleta → verificar recurso/versão no backend, projeção pública mínima.
- Mais uma leitura Admin API por asset → checagem restrita, verificação durável
  por reserva, lote limitado e nenhuma leitura por renderização de card.
- Reserva vence sem resultado conhecido → estado de reconciliação, nunca exclusão
  automática por idade; app informa retomada/novo envio só depois de resolver.
- Limpeza fica pendente sem scheduler → ferramenta supervisionada e relatório;
  não atribuir suporte a jobs ao plano atual do Xano.
- Rollback com posts externos → compatibilidade de leitura é mantida, não
  desfazer schema apagando dados nem eliminar journal de pendências.
- Imagem pública/cache → explicar limites de remoção física e validar invalidação;
  URLs externas públicas não viram armazenamento privado por essa change.

## Migration Plan

1. Após aprovação: implementar contratos locais/journal/idempotência e testes com
   transporte simulado; adaptar upload ao ID reservado e validar permissões.
2. Revisar backup e dry-run do destino, sem registros/env/delete/truncate; obter
   autorização separada para schema/rotas e para configuração privada necessária.
3. Publicar aditivamente, conferir tipos/índices/guards/projeção e que dados
   legados continuam legíveis. Manter uploads desativados.
4. Ensaiar com conta/asset descartáveis cada fluxo, duas contas e falhas
   controladas. Relatórios separam API, navegador, simulação e limpeza real.
5. Ativar somente após aceite e autorização, verificando consumo e rollback.
   Reverter flags/caminho de novas escritas se necessário; conservar leitura,
   journal, metadados, legado e auditoria. Não apagar schema ou assets no rollback.

## Histórico da preparação — preservado

O design abaixo descreve a preparação anterior e suas restrições daquela rodada.
Referências a conta em criação ou nenhuma integração autorizada são históricas;
o planejamento vigente é o texto acima. Evidências de 10/11 e de cada rodada de
11/11 continuam nos arquivos datados, sem reclassificar seus testes como novos.

### Contexto original

Frontend já normaliza URLs HTTPS, porém post.image é do tipo image no Xano e POST/PUT processam image_upload com storage.create_image. Hospedagem externa precisa de contrato persistente próprio; não basta colar URL no campo image sem validar comportamento. Conta Cloudinary ainda em criação.

## Goals / Non-Goals

Entregar ambiente e transporte prontos para a integração. Não ativar uploads reais, migrar imagens antigas, remover marcas já incorporadas, publicar contrato incompleto ou trocar hospedagem local.

## Decisions

Continuação autorizada em 11/11/2026 após configurar credenciais e ensaio isolado:
preparar integração local por etapas, sem ativar nem publicar. Primeiro endurecer
o adaptador: resposta deve ter versão positiva, assinatura válida de public_id e
version, URL canônica do mesmo asset e namespace pertencente ao autor. Exportar
recibo mínimo para futura validação independente no backend. Assinatura não cobre
asset_id/URL/autoria por si: o backend deve verificar assinatura e prefixo do
usuário autenticado e construir sua URL, nunca aceitar esses campos cegamente.
Em seguida detalhar persistência e reconciliação duráveis antes de ligar
SocialState. A restrição de não editar SocialState da proposta descreve a rodada
inicial de preparação; esta etapa ainda não altera seu comportamento.

- Variáveis CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET e CLOUDINARY_UPLOADS_ENABLED=false. Criar somente chaves ausentes no .env; nunca sobrescrever credenciais que o usuário já tenha preenchido. Configuração incompleta/desativada falha antes de rede; verificação mostra apenas presença.
- HTTPX já instalado; upload server-side multipart para api.cloudinary.com/v1_1/<cloud>/image/upload, assinatura SHA-256 dos campos ordenados + secret. Sem SDK ou preset unsigned obrigatório. Secret não vai no corpo nem no frontend. Timeout sem retry de escrita e sem redirects.
- Adaptador recebe bytes já validados pelo fluxo e mantém guarda de tamanho 5MB/tipos PNG/JPEG/WebP/GIF; exige owner_id positivo e gera public_id exclusivo codeboxd/posts/u<id>/<uuid>, overwrite=false. Não aceita URL remota como origem do upload.
- Retornar apenas URL HTTPS do host res.cloudinary.com/conta configurada, public_id, asset_id e dimensões/tamanho/formato validados. Não devolver corpo bruto ou credenciais. Rejeitar resposta inválida com erro sanitizado.
- Integração posterior manterá limite de arquivo e autoria no servidor, metadados do asset no post e limpeza compensatória de upload conhecido se gravação falhar de forma definitiva. Falha incerta exige reconciliação para não apagar asset possivelmente referenciado. Credenciais e contrato remoto precedem ativação da flag.
- Imagens antigas continuam usando seus metadados Xano. Reenvio do original é necessário para versões sem marca já incorporada. Remoção/substituição precisa distinguir asset próprio de imagem legada e nunca apagar por URL arbitrária.

## Risks / Trade-offs

Conta/cotas e validação real permanecem pendentes; mocks não comprovam upload, renderização ou ausência de marca em produção. Não há fallback silencioso para Xano depois de ativação. Nesta preparação nenhum fluxo de post usa o adaptador, portanto flag isolada não conclui migração.

## Migration Plan

Preparar env/serviço/testes agora. Com credenciais, inspecionar configuração real, detalhar contrato aditivo de post (URL/IDs/provedor), preparar backup/dry-run e integrar criar/editar/excluir com reconciliação de assets. Só ativar após publicação e ensaio descartável com limpeza. Rollback desliga flag mantendo URLs/legados legíveis; não apagar assets já usados.
