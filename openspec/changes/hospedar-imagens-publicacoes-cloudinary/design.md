## Context

Frontend já normaliza URLs HTTPS, porém post.image é do tipo image no Xano e POST/PUT processam image_upload com storage.create_image. Hospedagem externa precisa de contrato persistente próprio; não basta colar URL no campo image sem validar comportamento. Conta Cloudinary ainda em criação.

## Goals / Non-Goals

Entregar ambiente e transporte prontos para a integração. Não ativar uploads reais, migrar imagens antigas, remover marcas já incorporadas, publicar contrato incompleto ou trocar hospedagem local.

## Decisions

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
