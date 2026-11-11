# Conta validada e prévia do ensaio — 11/11/2026

Atualização posterior: ensaio autorizado e executado com sucesso.
[Resultado real e limites](ensaio-real-2026-11-11.md). As seções abaixo preservam
a prévia revisada antes da execução; não são autorização para repetir o teste.

## Verificação real de leitura

Após o usuário informar que preencheu o `.env`, as três variáveis foram
encontradas. `CLOUDINARY_UPLOADS_ENABLED` permanece false. Uma única chamada
GET /usage retornou HTTP 200: plano Free, 0/25 créditos, zero recursos e zero
uso de armazenamento, tráfego e transformações reportados pelo provedor.
Os números podem atualizar com atraso. Não foram listados assets nem realizados
uploads, exclusões ou consultas ao Xano nesta verificação. Credenciais e cloud
name não foram registrados no Git. Resumo privado em
`.local/cloudinary-usage-read-20261111.json` na raiz da máquina original.

A confirmação substitui o bloqueio de credenciais registrado na rodada anterior.
Permanecem os bloqueios de contrato persistente, integração e aceite real.

## Limite de vinte

A referência do widget documenta vinte chamadas simultâneas no backend, não
vinte arquivos totais na conta. Envio serial ou concorrência limitada respeita
esse limite; não remove cotas de armazenamento/tráfego/processamento.
[Referência oficial](https://cloudinary.com/documentation/upload_widget_reference).

## Executor local preparado

`tools/cloudinary_acceptance_probe.py`, sem executar por padrão:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.cloudinary_acceptance_probe
```

Prévia executada: um upload, um download, uma exclusão do próprio asset,
zero chamadas Xano, zero retries e zero alterações na configuração do aplicativo.

Escopo para autorização específica: PNG sintético 2×2 gerado em memória; public_id
novo em `codeboxd/acceptance/<uuid>`, overwrite=false; recuperar a URL HTTPS
Cloudinary validada e comparar bytes; destruir somente esse asset após resposta
confirmar identidade e metadados esperados. Nenhum arquivo de usuário é lido.
O arquivo é público temporariamente, sem dados pessoais; a invalidação de cache
não é instantânea. Pequeno consumo de armazenamento/tráfego é esperado.

Journal privado exclusivo criado antes de enviar. Timeout/retorno ambíguo de
upload não dispara repetição ou exclusão cega: manter referência privada para
reconciliação específica. Falha no download ainda tenta limpar o asset próprio
confirmado. Falha/timeout de limpeza não é sucesso nem dispara retry automático.
O critério de limpeza é a resposta `result=ok` do provedor; não comprova remoção
imediata de cópias em CDN/backups.

Comando preparado, **ainda não executado remotamente**:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.cloudinary_acceptance_probe --execute --approval-reference 'autorizacao-usuario-ensaio-descartavel' --config 'D:/Repositorios GIT/Codeboxd/.env' --output .local/cloudinary-acceptance-20261111.json
```

Se saída já existir, escolher outro nome; não sobrescrever journal anterior.
Esse teste exercita acesso/transporte isolados, não integra o adaptador de posts,
não prova renderização no navegador, persistência Xano ou autoria de usuários.
Não concluir 2.1/2.2 por aprovação desse ensaio. A flag permanece false.

Fontes: [assinaturas](https://cloudinary.com/documentation/authentication_signatures),
[upload/destroy](https://cloudinary.com/documentation/image_upload_api_reference),
[consulta de uso](https://cloudinary.com/documentation/admin_api#usage).

## Testes e limites

Seis testes MockTransport aprovados: prévia sem rede; fluxo assinado completo;
rejeição de asset/URL estranhos; timeout sem retry; limpeza após download inválido;
limpeza incerta sem falso sucesso. O ensaio real exige autorização específica,
conforme instrução original do usuário para operações remotas de escrita/exclusão.
Nenhum código Reflex, contrato Xano ou processo do app foi alterado.
