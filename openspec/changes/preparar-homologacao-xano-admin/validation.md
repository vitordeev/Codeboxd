# Preparação de homologação — 11/11/2026

## Base e autorização

Usuário escolheu homologação e confirmou que precisava prepará-la. Branch
task/homologacao-xano-20261111, worktree própria, base origin/develop 29d0456.
Nova change criada antes do código porque preparar infraestrutura separada não
estava implementado pelo escopo de administração. Origem protegida 147717.
Pedido cobre obter recurso isolado vazio, sem compra de plano ou alteração da
origem; publicação de contratos exige prévia e aprovação específica posteriores.

## Preparação local concluída

`tools/prepare_homologation.py` gera pacote allowlist local sem rede ou modo apply.
**32 documentos**: 13 tabelas, três funções, dois grupos e 14 queries. Exclui
workspace original, titulos legado, addon/AI, recuperação/envio de e-mail,
tasks/triggers, registros e variáveis privadas. GUID/canonical são removidos para
gerar identidades próprias no destino. Lógica de negócio dos contratos selecionados
preservada; uploads opcionais do POST de publicações não foram exercitados.

Pacote privado em `.local/homologacao-admin-20261111/xano/`, multidoc e manifesto
no mesmo diretório. [Manifesto sem segredos](local-manifest-2026-11-11.json) registra
arquivos/hashes e contagens. SHA-256 do multidoc:
`393b21ce667f42d613100e544cd9ce3a0520217f21d998b03f9523cb0cd940f4`.
Não equivale a dry-run Xano, publicação ou equivalência integral ao workspace real.

Exemplo `homologacao.env.example` separado, placeholders sem credenciais. Git
ignora `homologacao.env`; exemplo aparece no conjunto não ignorado. Nenhum `.env`
atual, perfil global ou processo do aplicativo foi alterado.

Comando de preparação já executado nesta worktree:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.prepare_homologation --output .local/homologacao-admin-20261111
```

Saída existente é preservada: para regenerar após mudanças, escolher outro
diretório privado, sem sobrescrever o pacote revisado.

## Validação local

- Sete testes específicos passaram: pacote real, contagens, ausência de atributos
  herdados/dados/env/envio, preservação de saída, segredos literais e bloqueios de
  destino, incluindo boolean como ID e origem com credenciais/query.
- Primeira execução teve uma falha na fixture por `.local` inexistente em checkout
  novo. Teste ajustado para projeto temporário independente; sete passaram depois.
- Suíte completa: **573 testes passaram em 22,968s**, log privado
  `.local/tests-homologacao-20261111.log`. Não somar às suítes das outras branches.
- `openspec validate preparar-homologacao-xano-admin --type change`: aprovado.
- `git diff --check`: aprovado. Nenhum código Reflex alterado; sem compile/restart.
- CLI @xano/cli 1.2.0: help/version fora do sandbox após erro uv_os_get_passwd no
  ambiente restrito. Nenhuma atualização de CLI ou dependência instalada.

## Tentativas remotas e bloqueio real

1. Sandbox: GET `/api:meta/sandbox/me`, operação que pode provisionar recurso,
   e não leitura pura. Retornou **HTTP 500**, sem identidade de sandbox confirmada.
   [Resumo sanitizado](sandbox-attempt-2026-11-11.json). Nenhum reset, push ou
   importação. Não repetir automaticamente nem afirmar provisionamento concluído.
2. Workspace vazio: nome `codeboxd-homologacao-admin` ausente antes da tentativa;
   um POST de criação retornou **HTTP 403, ERROR_CODE_ACCESS_DENIED**. GET posterior
   confirmou zero workspaces com esse nome. [Resumo](workspace-attempt-2026-11-11.json).
   Origem 147717 não editada, nenhum registro/env copiado, nenhum contrato publicado.

Essa conta/credencial não permitiu obter o destino por esses caminhos. **Não foi
confirmado se a restrição específica é de plano, permissão ou disponibilidade da
funcionalidade**. A documentação de preços e o CLI indicam restrições por plano,
mas não substituem conferência do faturamento/permissões desta conta. Não comprar
plano, criar outra conta ou reaproveitar live como consequência automática.

Fonte primária do comportamento dos comandos: CLI instalado (`sandbox/get` chama
getOrCreateSandbox; workspace/create usa POST). Referências:
[CLI oficial](https://github.com/xano-inc/cli),
[MCP oficial, sandbox](https://github.com/xano-inc/xano-developer-mcp),
[planos Xano](https://www.xano.com/pricing). CLI/MCP e página de preços podem
divergir em elegibilidade; registrar resposta real como evidência desta conta.

## Estado e próximo desbloqueio

**4/8 tarefas**: preparação e verificação de disponibilidade concluídas; recurso
vazio, prévia, publicação e acesso remoto continuam abertos. Homologação ainda
não está disponível para o piloto. Administração permanece com sua pendência 9.2.

O proprietário precisa verificar no painel Xano se pode criar workspace/sandbox
isolado e ajustar a permissão necessária ou disponibilizar outra instância de
homologação. Informar somente identificadores/caminho privado de configuração;
não enviar tokens no chat. Depois retomar com leitura de identidade/estado vazio,
prévia limitada e revisão antes de publicar. Mudança de plano/custo é decisão do
usuário, fora da execução atual. Sem Docker, push Git, merge ou arquivamento.
