# Preparação Cloudinary — 10/11/2026

## Entrega desta rodada

- `.venv/Scripts/python.exe` disponível; `pip check` retornou “No broken requirements found”. httpx/python-dotenv já existentes; nenhuma dependência instalada ou requisito alterado.
- Criadas somente variáveis ausentes no `.env` privado: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET e CLOUDINARY_UPLOADS_ENABLED=false. Verificações booleanas confirmaram campos presentes e flag false; nenhum valor secreto impresso. Exemplos vazios em .env.example.
- Adaptador server-side `services/cloudinary_uploads.py` pronto: assinatura SHA-256 dos campos ordenados, public_id exclusivo por proprietário, overwrite=false, arquivo multipart, limite 5MB e tipos aceitos, timeout sem retry/redirect e erros sanitizados. Configuração desativada/incompleta falha antes da rede. Representação da configuração oculta key/secret; retorno limitado aos metadados validados de asset e URL HTTPS da conta Cloudinary esperada.
- Adaptador não é chamado por SocialState nesta rodada. Fluxo atual de publicação não alterado. Sem esquema/endpoints Xano publicados ou uploads reais.

## Verificações

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_cloudinary_uploads.py -q`: 7 testes passaram, com transporte HTTP simulado. Cobertura de assinatura/transporte sem envio do secret, configuração ausente/desativada, proprietário/tamanho/tipo inválidos, falha de rede, erros do provedor sem retry, JSON inválido e URLs/metadados não confiáveis.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_uploads.py -q`: 4 regressões do transporte atual passaram.
- `git check-ignore .env`: `.env`, confirmando exclusão do arquivo privado.
- `openspec validate hospedar-imagens-publicacoes-cloudinary --type change` e `git diff --check`: aprovados.
- `.venv/Scripts/python.exe -B tools/check_staged_secrets.py`: aprovado, mas **zero arquivos no índice**. Não há validação dos arquivos ainda não adicionados nem dos commits anteriores; executar novamente após preparar o commit. `git status --short` mostrou modificações e arquivos novos sem staging; nenhum commit/push realizado pelo agente.

## Pendências e limites

Conta/credenciais ainda em criação. Não comprovado upload Cloudinary, recebimento/exclusão de asset, feed sem marca ou contrato Xano para URL/IDs. Tarefas 2.1/2.2 abertas: detalhar/publicar contrato aditivo após backup/prévia e integrar criação/edição/exclusão/compensação, preservar imagens legadas e fazer ensaio real com limpeza antes da ativação.

Assinatura e API conferidas na [documentação oficial](https://cloudinary.com/documentation/authentication_signatures). Configuração do usuário em [setup.md](setup.md). Execução local continua com .venv, sem Docker. Nenhum envio de mensagem, conta remota criada ou dado externo modificado nesta preparação.
