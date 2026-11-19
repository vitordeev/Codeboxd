# Proposal

## Why

O usuário solicitou salvar todo o trabalho versionável no repositório remoto e atualizar a branch develop. Existem novas alterações de Cloudinary e UI/UX em worktrees separadas, além de cópias antigas e trabalho de performance que precisam ser conferidos para evitar perda ou regressão.

## What Changes

- Inventariar e preservar as alterações versionáveis das worktrees, distinguindo conteúdo já publicado, diferenças novas e arquivos privados ignorados.
- Criar commits/checkpoints por frente e enviá-los sem force push; preservar trabalho incompleto sem declará-lo aceito.
- Integrar as frentes compatíveis em branch própria baseada no remoto atualizado, resolver conflitos documentais preservando evidências e validar o conjunto.
- Atualizar origin/develop e sua worktree local por avanço seguro, registrando os commits e como continuar em outra máquina.

## Capabilities

### New Capabilities

Nenhuma. Operação Git e documentação de acompanhamento, sem requisito novo de produto. `skip_specs: true`.

### Modified Capabilities

Nenhuma. As mudanças de produto continuam cobertas pelas changes de origem, com suas pendências intactas.

## Impact

Histórico Git, branches/checkpoints remotos, integração e documentação OpenSpec. A autorização atual permite commits, push e atualização de develop; não autoriza ativar Cloudinary, modificar Xano, limpar assets, publicar o aplicativo ou reescrever main. Credenciais e diretórios privados permanecem fora do envio.
