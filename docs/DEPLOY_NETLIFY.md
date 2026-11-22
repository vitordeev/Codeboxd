# Publicar Codeboxd na Netlify

## Arquitetura

A Netlify hospeda os arquivos estáticos exportados do frontend Reflex. O backend Python Reflex deve ficar ativo em um serviço público separado, com suporte a WebSocket. Xano, TMDB/Kitsu/Open Library e demais integrações continuam sendo dependências externas da aplicação.

## Antes do build

1. Hospede o backend Reflex em um serviço Python que mantenha o processo ativo e aceite WebSocket. Use as instruções de produção Reflex e configure nele as variáveis privadas descritas em `.env.example`; nunca coloque valores reais nesse arquivo ou no ZIP.
2. Crie o site na Netlify e anote a URL gratuita `https://<site>.netlify.app`.
3. No serviço do backend, configure `REFLEX_DEPLOY_URL` com essa URL Netlify para permitir a origem do frontend.
4. Nas variáveis de ambiente do site Netlify, configure `REFLEX_API_URL` com a URL HTTPS pública do backend.
5. Conecte o repositório ao Netlify ou use Netlify CLI apontando para este projeto. O `netlify.toml` define o comando de build e a pasta publicada.

Não é necessário comprar domínio. O subdomínio `netlify.app` fornecido pelo serviço pode ser usado como origem.

## Build e publicação

O build instala `requirements.txt`, executa `python tools/netlify_build.py` e publica `.web/build/client`. O script recusa `localhost`, HTTP, placeholders e URLs incompletas para evitar gerar frontend que tente conversar com backend local.

Para gerar localmente depois de configurar o backend, defina `REFLEX_API_URL` no ambiente e execute:

```powershell
python -m pip install -r requirements.txt
python tools/netlify_build.py
```

O ZIP criado por `python tools/package_netlify.py` é um pacote-fonte para conectar ao Git/Netlify CLI. Não faça drag-and-drop desse ZIP como se fosse o diretório estático já compilado.

## Variáveis e privacidade

Cadastre no backend as variáveis necessárias para Xano e integrações. Variáveis privadas do Xano, TMDB, DeepL, SendGrid e Cloudinary não devem ser expostas no frontend ou incluídas no pacote. O arquivo `.env.example` contém apenas nomes e placeholders; use as telas privadas dos serviços para configurar valores reais.

## Limites e conferência

- Sem URL pública do backend, o build final do frontend não pode ser gerado de forma funcional.
- Um build bem-sucedido não prova que login, feed, imagens ou uploads estão corretos no ambiente remoto. Confira essas jornadas no endereço Netlify depois do deploy.
- A Netlify publica o frontend; não substitui o processo Python Reflex.
- O pacote não inclui `.env`, `.local`, `.venv`, `.web`, `.states`, uploads, Xano local ou outros dados de execução.
