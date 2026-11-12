# Controles reutilizáveis e retorno de foco — 11/11/2026

## Estado conferido e recorte

Branch `task/ui-rails-acceptance-20261111`, worktree
`.local/worktrees/ui-foundations-20261111`. Fetch confirmou origin/develop
`7d32dc2`, sem divergência de commits. As seis alterações locais da rodada de
carrosséis foram preservadas. Usada a change existente, sem novo escopo ou
alteração das specifications aprovadas: tarefa 2.2 e requisitos de consistência,
feedback, teclado/foco e responsividade.

## Implementação de produto

- `pages/social.py`: campos e áreas de texto compartilham `ui-control`; botões
  recebem variante secundária explícita. Cancelar, editar avaliação e remover
  anexo/obra deixam de competir visualmente com a ação principal. Eventos,
  permissões, conteúdo e nomes das ações foram mantidos.
- Feedback compartilhado para avisos do shell/editor e estado vazio do grid.
  Erro usa alert; informação/sucesso usam status. Não se infere sucesso/erro a
  partir do texto de mensagens de negócio: o consumidor escolhe o tom.
- CSS: cores existentes via tokens, borda legível, foco de 2px, controles com
  área mínima de 44px, texto quebrável, estado vazio sem caixa tracejada e
  diálogos limitados à largura/altura da viewport, com rolagem própria.
- `assets/ui-dialog-focus.js`, carregado pelo head existente: corrige perda de
  foco em editor aberto programaticamente. Guarda até 32 elementos focados,
  associa cada diálogo ao elemento anterior e restaura somente se o foco ficou
  no body, o elemento continua conectado/habilitado e não há outro modal
  incompatível. Não sobrescreve o retorno nativo Radix. Limpa referências
  desconectadas e evita instalação duplicada; não envia eventos ao servidor.

A perda de foco foi reproduzida no navegador antes da correção e deixou de
ocorrer depois. Não foram alterados SocialState, serviços, contratos Xano,
autenticação, lógica de rascunho ou flags. Nenhuma funcionalidade foi removida.
Marca, fonte, tema escuro e amarelo permanecem; sem referências externas novas.

## Verificação

**632 testes Python aprovados**, suíte completa final em 41,195s, exit 0.
Compilação do app normal: `reflex compile --dry`, aprovada em **5,451s**, sem
registrar rotas/estado da fixture. Logs em `.local/controls-compile-final.log`.
Logs da suíte em `.local/controls-unit-final.log`. As primeiras
tentativas da fixture precisaram de setter explícito e registro do estado em
módulo canônico antes do app; foram corrigidas antes do aceite. A falha de foco
do editor foi corrigida no produto, sem retirar a asserção do teste.

[Matriz de controles](controles-2026-11-11.json): cinco cenários em
320/390/768/1024/1440px, Edge headless, todos aprovados:

- Rótulos acessíveis, alteração de campo e colagem real via clipboard do browser.
- Submissão com falha simulada, alerta contextual e rascunho preservado.
- Transição carregando/desabilitado → disponível, vazio, sucesso e falha parcial.
- Editor com Tab contido, Escape e retorno ao botão de origem.
- Confirmação destrutiva cancelada com retorno ao gatilho nativo.
- Foco visível, alvo secundário ≥44px, ausência de overflow e zero erros JS.
- Contraste computado nos campos: texto **17,15:1**, borda **3,55:1**.

[Regressões de Home/ficha](carrosseis-apos-controles-2026-11-11.json): quatro
cenários 320/390/768/1440px passaram novamente com as alterações de produto,
preservando paginação 12→24, esgotamento, identidade e capa indisponível.
Não equivale a comparação quantitativa de performance com baseline.

[Captura controlada, 390px](capturas/controles-fixture-390.png): galeria de
componentes reais com dados fictícios, não referência oficial de uma nova tela.
Essa rota e o estado de simulação existem somente no módulo de teste escolhido
explicitamente por REFLEX_APP_MODULE_IMPORT; não são registrados pelo app normal.

O backend da fixture bloqueia HTTP externo e o browser bloqueia hosts externos;
somente mensagens locais de teste e capas fictícias são utilizadas. Nenhum
usuário, e-mail, token ou asset real foi utilizado. A instância do usuário não
foi reiniciada. Sem Docker, push, merge, PR, arquivamento ou ativação Cloudinary.

## Limites e próximos passos

Aceite de **2.2** limitado à família piloto de componentes compartilhados e às
regressões descritas; não comprova os fluxos de negócio de todas as páginas.
Auditoria manual com leitor de tela, demais famílias e aceite transversal
continuam em 6.x/7.x. O script de foco acrescenta um asset local pequeno; não há
nova biblioteca. Comparações completas de bytes/tempos e cenários de diálogos
aninhados ainda pertencem ao aceite transversal, não foram inferidas daqui.

3.2 continua aberta por aparelho físico e 3.3 por baseline quantitativo. 1.2/2.3
permanecem abertas para revisão concreta do shell antes de condensar destinos.
Cloudinary e performance preservam seus próprios checklists.
