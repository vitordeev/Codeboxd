# Primeiro lote local: fundamentos e carrosséis — 11/11/2026

## Escopo e autorização

O usuário aprovou o prosseguimento após o planejamento das duas frentes.
Este lote aplica a change `modernizar-ui-ux-codeboxd` a fundamentos visuais,
piloto de login e coleções horizontais. Não constitui conclusão da change inteira.

- Branch: `task/ui-foundations-20261111`, base `faa655f`.
- Worktree nova: `.local/worktrees/ui-foundations-20261111` dentro do repositório principal.
- A base contém as integrações anteriores. Nenhum checkout ou desenvolvimento em `main`/`develop` foi realizado.
- O planejamento aprovado foi copiado da worktree Cloudinary para esta branch; o código pendente de Cloudinary não foi copiado nem alterado.
- Nenhum push, merge, sincronização de specs, arquivamento, alteração de credenciais, ativação de provider ou mutação remota.

## O que mudou

O login mantém composição, textos de domínio, logo e robôs ativos. Tokens CSS
`--cb-*` identificam fundos, superfícies, texto, destaque, erro, fonte/fallback,
espaços e raios. O piloto melhora contraste de texto secundário e campos, foco,
feedback de erro com `role=alert` e área dos links. A cor amarela continua sendo
destaque; nenhuma arte, fonte ou referência externa de design foi introduzida.

O helper `horizontal_collection.py` reutiliza marcação nativa para trilho/setas.
Home e recomendações compartilham o comportamento de
`assets/horizontal-collections.js`, carregado uma vez pelo head existente.
Arrasto só começa após intenção horizontal de 8px; avanço por seta/tecla usa
85% da região. Captura, seleção e clique pós-arrasto são tratados localmente,
sem um evento Reflex por movimento. Supressão dura no máximo 350ms e corresponde
ao ponteiro/região do gesto; um clique novo ou ativação por teclado permanece
funcional. Desmontagem, cancelamento, perda de captura, blur e documento oculto
restauram o estado transitório.

Toque/trackpad continuam nativos. Setas têm 44×44px, identificação por coleção
e estados de início/fim/sem overflow. O trilho aceita esquerda/direita e Home/End
quando focado, revela horizontalmente o card focado e respeita movimento reduzido.
Não foram alterados `SocialState`, serviços, caches, paginação ou identidade das obras.
Carregar mais permanece um botão separado. Recomendações vazias não recebem setas
sem uma região correspondente.

Uma falha encontrada no primeiro aceite foi corrigida: o snap alinhava o
primeiro card em `scrollLeft=2`, deixando a seta anterior habilitada. O novo
`scroll-padding-inline:2px` conserva o respiro existente e o extremo correto.

## Evidências e camadas

| Verificação | Resultado observado | Limite |
| --- | --- | --- |
| Suíte Python final, `python -B -m unittest discover -s tests` | **621 testes, OK, 36,295s**, exit 0 | Testes locais da base desta branch |
| `python -B -m reflex compile --dry` final | Sucesso, **3,146s**, Reflex 0.9.11.post1 | Compilação, não aceite de serviço real |
| Servidor fixture em produção | Build e execução na porta 3036 aprovados | Dados fictícios, estado em memória |
| Baseline Home/login/ficha | **15 capturas**, cinco larguras; sem overflow ou erro JS | Estado anterior do lote, fonte externa bloqueada |
| Matriz de navegador após alterações | **20 cenários**, aprovados; zero erros JS | Edge headless, backend fictício |
| Inter já declarada pelo aplicativo | **Cinco verificações adicionais**, aprovadas | Somente os hosts existentes do Google Fonts liberados |
| Controle positivo do contador de eventos, 390px | Rodada complementar aprovada; clique de card detectado e gestos continuam com zero eventos | Confirma que zero não resulta de um contador inoperante |
| Preservação das worktrees anteriores | **1.735 arquivos de código/configuração, cinco worktrees, zero diferenças** | Hashes do inventário anterior; não inclui arquivos privados ignorados |
| OpenSpec 1.14.3, validação estrita | UI/UX e Cloudinary válidas nas respectivas worktrees | Artefatos válidos não significam implementação ou aceite completos |

Larguras: **320, 390, 768, 1024 e 1440 CSS px**, altura de viewport 900px.
O catálogo da fixture usa 12 obras fictícias por coleção, nomes longos e a capa
padrão que já existe no projeto. A Home conserva **14 prateleiras/168 cards**
antes/depois nas cinco larguras; o inventário de links das três páginas é
registrado nos JSONs. O DOM inteiro, bytes e tempos de cinco pares comparáveis
ainda não foram medidos: não há alegação de conclusão de performance.

A matriz principal bloqueia HTTP externo no browser e qualquer transporte
HTTP real não substituído no backend. A exceção posterior de fonte permite
apenas leitura dos dois hosts já utilizados pela Inter; não acessa Xano ou
Cloudinary. Não usa conta de usuário, tokens de login ou dados reais como fixture.

Nos trilhos da Home e recomendações, os testes mediram **zero requisições HTTP
de aplicação e zero eventos de aplicação Reflex por gesto**; carregamento lazy
da capa fictícia é distinguido desse tráfego. Handshake/ping do transporte não
são eventos de aplicação. Clique normal e Enter continuam abrindo obras.

Casos de interação incluem mouse com captura, clique abaixo do limiar,
seleção durante o arrasto, saída do trilho, cancelamento, Home/End/setas,
foco em card oculto, wheel horizontal, script carregado novamente, controles sem
overflow, substituição/remoção do DOM e controles funcionando após reaparecer.
O teste de idempotência conta uma única operação de scroll após uma tecla.
Os probes de ciclo de vida são elementos nativos fictícios; navegação real
Home→ficha também desmonta e recria regiões. Cancelamento é disparado por DOM:
a harness reproduz a ausência de click que acompanha um cancelamento nativo.

Toque horizontal/vertical é emulado pelo protocolo do browser; zoom foi
verificado com escala de página emulada. Isso **não equivale a ensaio de dedo,
pinça ou trackpad em hardware físico**. A tarefa 3.2 permanece aberta.

No piloto de login, estilos computados e fundos reais produziram contraste
mínimo de **8,13:1** na seleção de textos/ações verificada e **3,55:1** nos
contornos dos campos. Links testados medem 44px de altura; foco tem contorno
visível. Resultado idêntico com Inter carregada e fallback nas cinco larguras.
Isso não é uma auditoria WCAG de todos os textos, estados ou páginas do app.

## Artefatos reproduzíveis

- [Baseline e inventário de links](browser-baseline-2026-11-11.json).
- [Matriz de UI e gestos](browser-fundamentos-2026-11-11.json).
- [Inter existente carregada](browser-inter-2026-11-11.json).
- [Controle positivo do contador de eventos](browser-contador-eventos-2026-11-11.json).
- [Preservação de código/configuração](preservacao-2026-11-11.json).
- [Validação local e hashes dos arquivos do lote](validacao-local-2026-11-11.json).
- [Login antes, 390px](capturas/login-antes-390.png) e [depois, 390px](capturas/login-depois-390.png): capturas controladas com fallback, sem credenciais preenchidas.

Capturas completas das três páginas nas cinco larguras e logs completos estão
no diretório privado `.local` desta worktree. O baseline usa os arquivos
anteriores ao lote, base `faa655f`; os JSONs registram hashes de CSS distintos.

Reprodução, a partir da worktree deste lote, usando a `.venv` já existente:

```powershell
$uiPython = 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe'
$env:REFLEX_APP_MODULE_IMPORT = 'tools.ui_foundations_fixture'
$env:REFLEX_WEB_WORKDIR = "$PWD/.local/frontends/ui-baseline"
$env:REFLEX_STATE_MANAGER_MODE = 'memory'
$env:REFLEX_USE_NPM = 'true'
$env:COOKIE_SECURE = 'false'
$env:XANO_AUTH_URL = 'http://127.0.0.1:9'
$env:XANO_SOCIAL_URL = 'http://127.0.0.1:9'
& $uiPython -B -m reflex compile --dry
& $uiPython -B -m reflex run --env prod --single-port --frontend-port 3036 --backend-port 3036 *> .local/ui-fixture.log
```

O diretório frontend isolado deve estar preparado com as dependências locais
antes de iniciar; não compartilhe `.web` em uso pelo app do usuário. A variável
`REFLEX_APP_MODULE_IMPORT` seleciona a fixture explicitamente; ela não é importada
pelo app normal. Em outro terminal, cada saída deve ser um diretório novo:

```powershell
$uiPython = 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe'
& $uiPython -B -m tools.ui_foundations_browser --phase acceptance --output .local/ui-aceite-novo
& $uiPython -B -m tools.ui_foundations_browser --phase existing-font --output .local/ui-inter-novo
```

Não executar esses comandos contra uma instância com backend real. Ao encerrar,
parar somente o processo da fixture e limpar as variáveis de teste antes de rodar
o app normal. Nenhum processo do app do usuário é alvo deste lote.

## Checklist e próximos incrementos

Concluídos **1.1, 2.1 e 3.1: 3/26**. Os demais continuam abertos, incluindo:

1. **3.2 e 3.3:** completar dispositivo físico/movimento normal e ensaios de carregar mais, falha de capa e carregamento comparável; componente aplicado não equivale ao aceite completo dessas tasks.
2. **1.2, 2.2 e 2.3:** revisão concreta do shell/densidade e padrões de feedback/diálogos antes de condensar ações; nenhuma funcionalidade foi retirada no piloto.
3. **4.x/5.x:** busca separada Obras/Pessoas/Listas públicas, URL e detalhes de lista com fixtures e contratos Xano paginados. Publicação exige destino identificado e autorização específica; privacidade permanece requisito do servidor.
4. **6.x/7.x:** propagar por famílias e completar leitores de tela, estados de erro/loading, zoom/reflow, rotas, comparação de performance e aceite integrado.

Cloudinary conserva seu planejamento e trabalho pendente na worktree
`cloudinary-limites-20261111`: marcos originais **3/5**, checklist expandido
**3/17**. Os 632 testes daquela branch não são a suíte desta base de UI.
Upload descartável anteriormente aprovado não comprova persistência de posts.
Reserva durável, validação no servidor, associação ao post/autor, ciclo de vida
e reconciliação precisam ser implementados; publicação Xano, fixtures remotas,
limpeza e ativação dependem das autorizações específicas previstas no plano.
Nenhuma dessas operações foi realizada nesta continuação.

## Revisão e retorno

Os arquivos de produto do lote são o helper de coleção, duas páginas existentes,
CSS e asset JS. As duas ferramentas são exclusivamente de validação. OpenSpec
inclui o planejamento aprovado, progresso, este relatório, JSONs e capturas
controladas; documentos centrais receberam um registro adicional sem apagar
histórico. O lockfile gerado pela compilação foi reposto byte a byte ao HEAD
somente nesta worktree nova, após conferir igualdade de conteúdo JSON.

Arquivos de produto/ferramentas: `Codeboxd_main/horizontal_collection.py`,
`Codeboxd_main/pages/login.py`, `Codeboxd_main/pages/social.py`,
`assets/codeboxd.css`, `assets/horizontal-collections.js`,
`tools/ui_foundations_fixture.py` e `tools/ui_foundations_browser.py`.
Artefatos da change: `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
quatro deltas em `specs/` e este diretório `validation/`. Acompanhamento central:
`openspec/README.md` e `openspec/PENDENCIAS.md`.

`openspec validate modernizar-ui-ux-codeboxd --type change --strict` e
`openspec validate hospedar-imagens-publicacoes-cloudinary --type change --strict`
passaram nas worktrees de cada frente. `git diff --check` também passou.
Os arquivos desta entrega estão salvos localmente e ainda não commitados;
não estarão disponíveis por git pull em outra máquina enquanto não houver uma
etapa de envio autorizada.

Estado Git da worktree deste lote: cinco arquivos rastreados modificados e
21 arquivos novos, nenhum arquivo staged; lockfile sem diff. A verificação de
escopo, sintaxe Python, links locais dos artefatos e whitespace não apontou
problemas. Os processos de navegador da harness e a fixture da porta 3036
foram encerrados ao final; a instância do usuário não foi reiniciada.

Rollback do lote consiste em reverter seus arquivos de apresentação/helper/head
na branch isolada, preservando dados, regras, serviços e as demais worktrees.
Nenhuma migração ou limpeza remota é necessária. A candidata a entrega continua
local e deve ser revisada antes de qualquer publicação autorizada.
