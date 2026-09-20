# Publicação com domínio

A aplicação está preparada para um servidor Linux com Docker Compose. Reflex roda em modo de produção em uma única porta interna; o Caddy recebe o tráfego público e fornece HTTPS, incluindo a conexão WebSocket. Xano continua armazenando os dados. Não é uma aplicação exclusivamente estática.

## Preparar o servidor

1. Disponibilize o projeto no servidor com Docker e Compose instalados.
2. Copie `deploy/production.env.example` para `.env.production` na raiz.
3. Configure `APP_DOMAIN` com o domínio real e as URLs Xano e o token TMDB no arquivo local do servidor. Não envie esse arquivo ao Git. O contexto Docker usa uma lista de arquivos permitidos e exclui credenciais, testes locais e imagens de referência.
4. Aponte o registro DNS A para o IPv4 do servidor. Só configure AAAA se houver IPv6 funcionando. Libere as portas TCP 80 e 443.
5. Na raiz, execute:

```sh
docker compose --env-file .env.production config --quiet
docker compose --env-file .env.production up -d --build
docker compose --env-file .env.production logs --tail=100 app proxy
```

O primeiro início compila o frontend e precisa de acesso à internet para instalar dependências frontend. Aguarde o healthcheck ficar saudável. O Caddy inicia depois e emite o certificado quando o DNS e as portas estiverem corretos. Os certificados ficam em volumes persistentes.

## Verificação após publicar

- Abra `https://SEU-DOMINIO/ping` e a página inicial.
- Confirme no navegador que a conexão `/_event` usa WSS no mesmo domínio, sem referências ao localhost.
- Valide cadastro, login, recarga da sessão e logout; busque um filme e uma série, abra detalhes e confira as capas.
- Salve uma avaliação, crie/edite uma lista e uma publicação e confirme o resultado após recarregar.
- Confira em celular as páginas inicial, perfil, feed e listas.

O compose usa um único processo de aplicação. Não aumente réplicas/workers sem configurar o gerenciamento de estado compartilhado do Reflex. Reinícios podem interromper formulários em andamento; os dados já gravados permanecem no Xano.

## Atualizar

Depois de enviar o código atualizado ao servidor, repita `docker compose --env-file .env.production up -d --build`. Não use `down -v`, pois remove os volumes de certificados. Para voltar a uma versão anterior, restaure o código dessa versão e reconstrua a imagem.

## Estado de validação

A publicação e a emissão do certificado dependem do servidor e domínio que serão escolhidos. O Docker Engine não estava disponível na máquina de desenvolvimento; a imagem ainda precisa de build e teste em Linux antes da publicação. Os testes locais do Reflex não substituem essa validação.

Referências: [self-hosting Reflex](https://reflex.dev/docs/hosting/self-hosting/) e [HTTPS Caddy](https://caddyserver.com/docs/quick-starts/https).
