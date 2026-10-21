# Biblioteca e listas no navegador — 20/10/2026

## Escopo e execução

Usuário autorizou reiniciar e validar biblioteca/listas no navegador com dados
fictícios. Criado `tools/library_lists_browser_validation.py`, usando Edge
headless, Reflex de produção em 3031, serviço local de fixtures em 3040 e estado
temporário em memória. URLs Xano substituídas só no processo filho; browser
bloqueia recursos externos. Nenhuma conta real ou endpoint remoto foi utilizado.

O executor reutiliza identificação/parada dos processos do projeto e restauração
normal já existentes na instrumentação. Helper de restauração passou a aceitar
nome de log específico, evitando colisão com logs anteriores. Sete testes dessa
instrumentação e verificação sintática passaram antes da execução. O app já
tinha 217 testes e compilação aprovados na intervenção anterior.

```powershell
.venv/Scripts/python.exe -B -m tools.library_lists_browser_validation
```

## Resultado de navegador

22 cenários passaram: em 1440×900 e 390×900, biblioteca e listas com dados
pequenos, perfis indisponíveis, catálogo lento (2 s), catálogo em 429 e coleções
grandes; mais listas padrão ausentes em cada largura. Conta de fixture é
injetada como cookie sintético e verificada pelo handler real de sessão.

Verificações:

- Ciclo on_load iniciado/concluído em todos os casos, com estado de espera
  visível quando catálogo lento e removido ao terminar.
- Zero GET de pessoas em todos os cenários, mesmo com esse endpoint configurado
  para 429. Nenhum bloqueio pela dependência removida.
- 429 de catálogo continua exibindo aviso de 20 segundos, sem sucesso fictício.
- Bibliotecas pequenas com cinco cards; listas pequenas com 12 linhas, públicas
  e privadas. Grandes começam com 20 e passam a 40 ao clicar “Mostrar mais”,
  sem chamada adicional (comportamento atual, não paginação remota nova).
- Abertura de lista própria preserva obra e opções do seletor (cinco obras mais
  opção sem obra); abertura de lista pública de outra conta não mostra esse
  formulário de edição.
- Ausência de padrões cria duas listas somente no fixture em memória; dados
  reais não alterados.
- Nenhum pageerror JavaScript nem overflow horizontal nos 22 casos.

Contagens observadas incluem toda a ação de teste: biblioteca pequena faz três
chamadas; listas pequenas fazem cinco porque abrir uma lista acrescenta uma
consulta de itens às quatro da carga inicial. Casos grandes: sete na biblioteca
e 11 nas listas, incluindo abertura. Padrões ausentes: oito nas listas, incluindo
dois POST fictícios e abertura de itens. Não comparar essas contagens estendidas
diretamente com o diagnóstico que media apenas a entrada na tela.

[Resultado final](biblioteca-listas-browser-2026-10-20.json).
Capturas por seção, largura e caso em `biblioteca-listas-<seção>-<largura>-<caso>.png`.
Inspecionadas visualmente listas abertas em
[desktop](biblioteca-listas-lists-1440-ready.png) e
[largura de celular](biblioteca-listas-lists-390-ready.png).

Primeira tentativa passou nove casos, mas parou por TimeoutError do executor:
no diretório grande, tentou clicar numa lista padrão fora das primeiras linhas
visíveis. Corrigido somente o teste para abrir uma lista pública visível nesse
caso; nenhuma mudança adicional no produto. A tentativa anterior foi preservada
em [biblioteca-listas-browser-primeira-tentativa-2026-10-20.json](biblioteca-listas-browser-primeira-tentativa-2026-10-20.json).

## Limites e restauração

Resultados cobrem integração frontend/backend com serviços fictícios; não
comprovam latência real, quota Xano, autorização remota ou aparelho físico.
Tempos individuais no JSON incluem inicialização do browser e custo da máquina;
não são SLA, benchmark remoto nem comparação controlada com antes.

Ao fim dos casos, instância de teste e fixture foram encerrados e iniciado build
da instância normal em 3030, com log `normal-restored-after-library-lists.log`.
Build concluído; `normal_restored=true`, GET `/login` com HTTP 200, env gerado
em 3030 e portas 3031/3040 fechadas. Instância normal atualizada disponível.
Aviso preexistente
de parse de `.env` permaneceu; arquivo privado não alterado ou exibido.

Tarefas amplas de paginação e validação real continuam abertas. Próxima
intervenção candidata é carregar somente as informações necessárias à primeira
tela e buscar continuação sob demanda, com proposta/aprovação antes de editar.
