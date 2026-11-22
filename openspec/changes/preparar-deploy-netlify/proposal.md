## Why

O Codeboxd precisa de um pacote organizado para publicar o frontend na Netlify, sem misturar credenciais, caches e dados locais. A preparação também precisa deixar explícito o requisito do backend Reflex público para que o deploy não pareça completo quando ainda não puder funcionar.

## What Changes

- Documentar o fluxo Netlify para o frontend estático Reflex e o backend Python hospedado separadamente.
- Criar a configuração de build da Netlify e um empacotador de ZIP com lista permitida de arquivos.
- Ajustar o `.gitignore` para saídas de deploy e artefatos gerados sem ocultar arquivos-fonte relevantes.
- Validar o conteúdo do ZIP contra `.env`, dados locais, builds e diretórios Git.
- Manter a exportação final do frontend condicionada à URL pública do backend.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- Nenhuma. O escopo é tooling e documentação de publicação, sem mudar requisitos funcionais do aplicativo; `skip_specs: true` é aplicado.

## Impact

Afeta `.gitignore`, arquivos de configuração/documentação de deploy, ferramentas locais para build e empacotamento, e a saída ZIP em `dist/`. O frontend é publicado na Netlify; o backend Reflex e suas variáveis privadas permanecem em um host Python compatível com WebSockets.
