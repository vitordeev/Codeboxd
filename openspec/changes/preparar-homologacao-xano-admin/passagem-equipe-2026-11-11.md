# Continuação em outra máquina — 11/11/2026

## Branch de trabalho compartilhada

Branch principal desta passagem: **handoff/retomada-20261111**, baseada na
develop integrada 29d0456. Consolida os incrementos de e-mail, Cloudinary,
administração e preparação de homologação que estavam em worktrees separadas.
O pedido posterior do usuário autoriza commit/publicação para permitir que outro
colaborador baixe e continue. As restrições anteriores de não publicar eram
anteriores a esse pedido. Não há merge automático em develop/main.

Para obter o trabalho em outro clone, com alterações próprias já preservadas:

```powershell
git fetch origin
git switch --track origin/handoff/retomada-20261111
git pull --ff-only
```

Se a branch já existir localmente, usar `git switch handoff/retomada-20261111`
antes do pull. Um pull na develop não muda para esta branch nem integra o trabalho.

## Trabalho de performance preservado separadamente

Branch **wip/performance-preservada-20261111**, base a21c806, salva o trabalho
pré-existente da worktree task/performance-20261109. É WIP, não integrado à base
atual: não fazer merge cego ou sobrescrever arquivos desta passagem com os dele.
Preserva código de Home/social, testes, medições e lockfiles tal como estavam no
checkpoint. A origem de alterações de lockfiles com ranges ^ não foi determinada;
revisar antes de integrar. A worktree original de performance não foi alterada.

## Ambiente na nova máquina

Ler AGENTS.md e seguir as skills Reflex antes de executar/editar. Usar `.venv`
local e dependências de requirements.txt; não usar Docker. Configuração privada,
credenciais de teste/Metadata e capturas com dados reais não estão no Git.
Preencher configuração privada própria a partir dos exemplos, sem mandar tokens
no chat ou copiar credenciais do colaborador. Não esperar que caminhos absolutos
de worktrees/venvs desta máquina existam na outra: ajustar cwd e caminho do Python.

Para preparação de homologação, o gerador reproduzível está em
`tools/prepare_homologation.py`; exemplo separado em `homologacao.env.example`.
Ele gera pacote local de 32 contratos, não cria ambiente ou publica código.

```powershell
.venv/Scripts/python.exe -B -m tools.prepare_homologation --output .local/homologacao-admin-nova-maquina
```

Saída existente não é sobrescrita. Não apontar homologação ao workspace protegido
147717, não copiar registros/env, não usar o app local como prova de isolamento.

## Onde paramos

- Usuário confirmou recebimento do código, troca da senha, novo login com senha
  nova e persistência do cadastro. Evidências e limites na change de recuperação.
- SendGrid teve atrasos reais 421/4.7.32; domínio não autenticado. Usuário não
  possui domínio próprio. Não afirmar redução de latência ou alinhamento corrigido.
- Leituras admin reais passaram em 1440/390px: sete áreas, cinco buscas vazias
  por largura, tratamento de 503 local, zero 429. Sem mutações administrativas.
- Piloto offline prevê 25 registros, 16 retidos e nove candidatos próprios à
  limpeza, com auditoria preservada; não fecha o plano completo de 239 registros.
- O usuário escolheu homologação isolada e autorizou prepará-la. Tentativa de
  obter sandbox retornou 500; criar workspace vazio retornou 403/ACCESS_DENIED,
  ausência confirmada após tentativa. Não houve publicação, cópia de dados,
  alteração de plano ou mudança na origem. Restrição de plano/permissão não confirmada.

Próximo desbloqueio: o proprietário verificar permissões/disponibilidade no painel
Xano ou disponibilizar outra instância de homologação. Com o destino identificado,
verificar identidade/estado vazio e produzir prévia limitada antes de publicar.
Não usar live como fallback, não adquirir plano, não resetar sandbox existente.

## Checklists que continuam abertos

| Frente | Estado | Critérios restantes |
| --- | --- | --- |
| preparar-homologacao-xano-admin | 4/8 | Recurso isolado, dry-run, publicação aprovada e acesso |
| gerenciamento-website | 33/34 | Mutações/permissões/auditoria e UI integrada; A2–A4 não executadas |
| recuperar-senha-codigo-6-digitos | 9/11 | Demais critérios do ciclo completo e reconciliação da antiga tarefa Resend |
| integrar-sendgrid-recuperacao | 4/5 | Vínculo com critérios restantes do ciclo, sem concluir só pelo recebimento |
| melhorar-email-recuperacao | 4/5 | Comparação real de chegada antes/depois |
| hospedar-imagens-publicacoes-cloudinary | 3/5 | Credenciais, persistência/ciclo de assets e ativação real |
| otimizar-performance-app | 17/37 | Metas/medições e jornadas restantes; WIP separado |

Não arquivar/sincronizar specs, publicar contratos ou efetuar mutações reais sem
escopo autorizado. O executor administrativo histórico que apaga event_log não é
seguro para reuso. O executor atual de ensaio continua restrito a MockTransport.

## Evidências e validação

Ler validation.md desta change, resultado-leituras-2026-11-11.md da administração,
aceite-usuario-2026-11-11.md da recuperação e os respectivos tasks.md. Relatórios
datados anteriores preservam seus estados históricos. JSONs de tentativas
interrompidas continuam incompletos; não transformar seu passed em true por relato.

Suítes anteriores por worktree: e-mail 585, admin 583, homologação 573. A validação
do conjunto consolidado e as verificações de publicação são registradas em seguida
neste documento; não somar contagens de execuções como se fossem testes únicos.

O ponto de retomada local anterior e seu ZIP são privados e não são necessários
para continuar neste clone. Arquivos publicados de fonte/testes/OpenSpec permitem
reproduzir a preparação sem o cache/frontends/venv daquela máquina.

Validação da passagem: suíte consolidada com 609 testes aprovados; suíte da
branch WIP de performance com 509 testes aprovados. `openspec validate --all`
na consolidação: 31 itens aprovados, nenhum erro; avisos sobre requisitos longos
preexistentes permanecem. Esses resultados não substituem os aceites remotos
pendentes descritos acima.
