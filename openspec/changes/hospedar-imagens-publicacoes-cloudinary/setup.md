# Configuração privada do Cloudinary

Preparação local concluída; integração com publicações e ativação real ainda pendentes.

## Ao terminar de criar a conta

No painel Cloudinary, obtenha o Cloud name do ambiente e suas credenciais em Settings/API Keys. Preencha somente no `.env` privado da raiz:

```dotenv
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_UPLOADS_ENABLED=false
```

Não envie API Secret pelo chat nem o inclua em commit, print ou relatório. Preserve as demais variáveis do projeto. Após preencher, basta informar que estão salvas; uma verificação posterior pode confirmar presença sem imprimir valores.

Mantenha a flag false: o adaptador está pronto, mas os posts ainda usam o fluxo Xano. Antes de ativar, concluir tarefas 2.1/2.2: persistência de URL/IDs no Xano, autoria, ciclo de vida de assets, integração e teste real. Alterações do ambiente requerem recarga do processo backend conforme skill reflex-process-management.

Não é necessário criar preset unsigned nem instalar SDK para o transporte preparado. A assinatura SHA-256 é gerada no servidor e o API Secret não vai no corpo do upload.

Documentação oficial: [assinaturas](https://cloudinary.com/documentation/authentication_signatures), [upload](https://cloudinary.com/documentation/upload_images).

## Continuação local — 17/11/2026

O fluxo do editor e os contratos candidatos agora incluem reserva, verificação independente, commit idempotente, revisão e fila durável; ver [implementação e limites](implementacao-2026-11-17.md). A flag permanece false. O Xano também exigirá `CLOUDINARY_POST_IMAGES_CONTRACT_READY=false` por padrão: esse gate é exclusivo do backend e só poderá passar a true após a implantação e o aceite completos. Publicar a prévia não ativa o serviço nem configura as credenciais do verificador.

## Git

O `.env.example` possui apenas nomes de variáveis e defaults; o `.env` privado é ignorado. Não usar git add -f no `.env`. O push leva código/exemplos/planejamento, não configura credenciais em outra máquina ou hospedagem.
