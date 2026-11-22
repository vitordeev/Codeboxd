## Why

O README da raiz é principalmente uma apresentação visual e não permite que uma pessoa compreenda e use o aplicativo sem ajuda. O material acadêmico pede um manual em Markdown que descreva acesso, perfis, jornadas, exemplos e limitações da versão entregue.

## What Changes

- Reorganizar o `README.md` da raiz como apresentação e manual de uso em Markdown.
- Acrescentar ao `.gitignore` saídas locais de IDE, build, teste e conflitos que não são fonte do aplicativo.
- Documentar acesso local e estado do deploy, papéis de visitante, usuário e administrador, funcionalidades, jornadas passo a passo, exemplos e limitações verificadas.
- Incluir capturas apenas se houver imagens existentes e seguras que representem a aplicação; não inventar evidência visual.
- Evitar publicar credenciais, URLs privadas, dados de contas ou afirmar como concluídos recursos ainda não validados.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- Nenhuma. Mudança documental sem alteração do comportamento do aplicativo; `skip_specs: true` é aplicado.

## Impact

Atualiza o `README.md` e `.gitignore` na raiz do repositório e cria evidências documentais nesta change OpenSpec. Não altera código, rotas, dados, configuração de provedores ou deploy.
