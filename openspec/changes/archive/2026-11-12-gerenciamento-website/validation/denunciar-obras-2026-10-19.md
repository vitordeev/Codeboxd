# Correção do envio de denúncia de obra — 19/10/2026

Pedido do usuário: botão de denunciar obra não conclui e mostra muitas requisições.
Vínculo: tarefas 5.1, 5.4 e 9.1–9.2 da change gerenciamento-website.

## Investigação e plano

Código atual repete requisições HTTP 429 até três vezes e limita Retry-After a
três segundos. O modal não exibe `notice`, que recebe o erro atrás do overlay.
Obras externas podem abrir denúncia com target_id zero, incompatível com o
endpoint que exige ID persistido. Confirmar logs reais antes de atribuir a causa
do 429. Corrigir retorno no modal, preservar formulário e impedir reenvios durante
o prazo informado; resolver ID da obra ao enviar. Testar regressões e compilar.

## Correção implementada

- Modal mostra erro com `role=alert`, mantém motivo/descrição e feedback de envio.
- POST não é repetido automaticamente em 429. Leituras só repetem se a espera
  informada pelo servidor for de até três segundos, respeitando seu valor.
  Ausência/valor inválido usa 30 segundos; HTTP-date também é suportado.
- APIError carrega retry_after; envio de denúncia guarda prazo e bloqueia nova
  chamada antes dele. Ao expirar, usuário pode reenviar sem perder o rascunho.
- Sessão já identificada envia diretamente à rota protegida no Xano, evitando
  GET /auth/me redundante. A autorização continua no servidor remoto.
- Obra externa sem ID pode abrir modal; ao enviar, a identidade é persistida por
  /media e o ID retornado é usado no report. Alvos já persistidos não são recriados.

## Diagnóstico remoto

Consulta de histórico via Metadata API retornou 200: entre 100 chamadas recentes,
11 tinham status 429. As únicas chamadas de reports nessa janela eram os GETs
administrativos da validação anterior (401/403); nenhum POST de denúncia apareceu.
Isso confirma limitação real recente, sem comprovar qual chamada causou o erro
relatado. A tentativa de ampliar per_page para 1000 foi rejeitada com HTTP 400;
não foi usada como evidência de ausência de requisições mais antigas.

## Validação local

- `.venv/Scripts/python.exe -m unittest discover -s tests -q`: **143 testes passaram**.
- Regressões novas: POST único em 429, Retry-After longo/curto/data, preservação
  do rascunho, cooldown, reenvio após prazo, envio em andamento, falha 404 e
  persistência da identidade externa sem validação de sessão redundante.
- `.venv/Scripts/python.exe -m reflex compile --dry`: compilação aprovada.
- `git diff --check` nos arquivos de implementação/testes alterados passou.

## Validação Xano real

Uma denúncia de obra criada com conta controlada existente. Resposta HTTP 200,
status pending e snapshot da obra persistido pelo servidor. Conteúdo da obra
comparado antes/depois, sem alterações. Denúncia criada removida por ID após
verificar ator e marcador exatos; nenhuma denúncia de outro usuário foi alterada.
[Resultado](report-remote-2026-10-19.json).

## Navegador real

Edge headless com aplicação em produção na porta 3033 e Xano real: modal abriu,
viewport 390 sem overflow da página, envio com confirmação visível e fechamento
do modal. Persistiu exatamente uma denúncia do marcador de teste, removida ao
final. [Resultado](report-browser-2026-10-19.json), seis verificações aprovadas.
Capturas privadas em `.local/report-dialog-{desktop,mobile}-2026-10-19.png`.

Servidor inicial sem rede no sandbox foi encerrado e reiniciado com acesso
autorizado; primeira tentativa do browser antes de iniciar falhou, repetição após
prontidão passou. Servidor atualizado disponível em http://localhost:3033, log
`.local/reflex-report-validation-2026-10-19.log`. Instância anterior na porta 3000
não foi reiniciada. Nenhum contrato Xano precisou ser republicado nesta correção.

## Limites

O 429 foi reproduzido nos testes simulados, sem provocar saturação no ambiente
real. O browser validou o caminho de sucesso, não a ocorrência real de limite.
Limites da plataforma continuam vigentes; não afirmar que 429 nunca ocorrerá.
Validação de moderação administrativa completa e dos outros tipos de alvos
continua pendente; tarefas 5.1, 5.4 e 9.1–9.2 mantidas abertas, contagem 17/34.
