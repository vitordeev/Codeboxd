# Carregamento e proposta de robôs

## Implementação local

Criado `Codeboxd_main/loading.py` com `loading_status`, `loading_icon` e `skeletons`. Integrações nos ramos de flags já existentes de home/coleções, busca inicial, ficha, biblioteca, perfil, comentários, feed e administração, além dos botões de autenticação. Conteúdo já disponível segue a política anterior; biblioteca e busca com resultados recebem indicador inline/sem skeleton substitutivo. Erros e ações de repetição foram preservados. Não há percentual fictício, overlay, novo estado, temporizador, polling ou chamada de API. CSS isolado em `cb-loading`/`cb-skeleton`, placeholders decorativos, texto anunciado educadamente e animações desativadas com movimento reduzido.

## Validações

- `.venv/Scripts/python.exe -m reflex compile --dry`: primeira compilação aprovada em 15,570s; segunda compilação executada após ajuste da mensagem de carregamento inicial da home.
- `.venv/Scripts/python.exe -m unittest discover -s tests -q`: 497 testes aprovados em 77,063s. Mensagens de falhas simuladas de provedores fazem parte da suíte.
- `.venv/Scripts/python.exe -c "import runpy; runpy.run_path('.local/check_loading_ui.py')"`: 13 verificações aprovadas no Edge headless, com markup gerado a partir dos próprios componentes Reflex e CSS real, variantes inline/cards/rows em 360/1440px, movimento normal/reduzido e transição simulada de erro/tentativa/sucesso. Confirmados um status por componente, anúncio educado, placeholders ocultos de leitores de tela e ausência de controles focáveis/overflow. Evidência `validation/loading-browser.json`; capturas `validation/loading-360.png` e `validation/loading-1440.png`.
- `.venv/Scripts/python.exe .local/check_robot_board.py`: quatro verificações aprovadas, temas claro/escuro em 360/1440px, sem overflow ou erro JavaScript. XML válido, IDs únicos, sem gradientes/filtros/raster; prancha SVG de 10.790 bytes. Evidência `validation/style-board.json`. O primeiro ensaio de escrita do relatório não encontrou a pasta validation; a pasta foi criada e o verificador repetido com sucesso.
- Validação OpenSpec estrita executada após atualização das tarefas/evidências.

## Ilustração candidata — aguardando aprovação

Proposta **Lume**: evolução do robô cinematográfico, com visor arredondado, cabeça de aproximadamente 1/3 da altura, carretel lateral como assinatura, corpo simples, olhos em pontos e boca em traço. Paleta candidata: marca #f5aa32, preto #171411, off-white #fff0d5, neutro #8f897c, acento #d9c86a; cores via `--illu-*`, traço 2px e sombra plana de 12%. Prancha contém três poses, três expressões e seis objetos. Produção original diretamente em SVG, sem geração raster ou referência a personagem externo. Layout local de prévia reaproveita apenas a estrutura de apresentação do estudo anterior; o personagem e a proposta são novos.

Arquivos para revisão: `review/style-board.svg`, `review/style-board.png`, `review/index.html` e capturas claras/escuras. Esses arquivos são propostas da change e não assets distribuídos pelo app. A prancha Dobra da change cancelada não foi retomada; logo e design geral atual foram preservados. Os bonecos atuais permanecem até aprovação e integração da nova família.

## Limites e próximo passo

O navegador verificou componentes locais e uma transição de fixture; não foi executada nesta rodada uma jornada Reflex autenticada de ponta a ponta nem validação remota. Não houve publicação ou reinício da instância normal. Testes funcionais existentes não comprovam aprovação estética. A skill `ilustracao-com-identidade` exige apresentar a prancha e registrar aprovação explícita antes das oito cenas. Essa aprovação ainda não existe; tarefas 2.2 e 2.3 permanecem abertas. SVGO e retirada de assets antigos pertencem à integração futura, após o aceite. Sem Docker.

## Preparação da continuidade

Conferidos estado da change (5/7 tarefas), consumidores atuais dos bonecos e ausência de SVGO instalado no frontend local. Roteiro de integração registrado em `implementation-plan.md`, com mapeamento das oito cenas, preservação de estados e limites de 404/500/offline. Nenhuma cena nova foi desenhada nem aplicada nesta preparação. A confirmação da prancha Lume foi solicitada; não presumir aprovação enquanto não houver resposta. A change `refresh-frontend-visual-identity` excluída não foi recriada.

## Aprovação explícita

Usuário respondeu “aprovo” à prancha Lume. A aprovação autoriza a produção e integração da família descrita na change, preservando logo/layout e os demais contratos. Os registros anteriores de aprovação pendente descrevem a etapa anterior.

## Entrega do conjunto aprovado e integração

A aprovação “aprovo” foi registrada antes da produção das cenas. Foram entregues onboarding, empty, not-found, error, success, loading, offline e no-results. Fonte geométrico em `tools/generate_lume_assets.py`; configuração em `tools/svgo-lume.config.mjs`; origem/manutenção em `ARTWORK.md`. O componente `Illustration` aceita nome/tamanho, aplica fallback seguro para nome inexistente, reserva espaço, prefixa IDs e distingue decoração de imagem informativa.

Os consumidores ativos do antigo `assets/mascot.png` foram migrados antes de sua remoção. O SVG antigo de robôs inline foi substituído pelo helper de compatibilidade para o Lume. Referências históricas de origem em `Imagens/` permanecem; logo, capas reais, avatares e uploads não foram substituídos. A skill de ilustração teve somente seu link documental corrigido para a spec desta change, pois a change anterior referenciada foi excluída.

### Verificações finais

- Geração: `.venv/Scripts/python.exe tools/generate_lume_assets.py`.
- Otimização: `npx --yes --package=svgo@4.0.0 svgo --folder assets/illustrations/lume --config tools/svgo-lume.config.mjs`. A tentativa inicial sem acesso ampliado falhou com EACCES no npm; o acesso solicitado foi autorizado e SVGO 4.0.0 foi executado. Sem adicionar dependência ao aplicativo.
- Manifesto: oito arquivos, 23.863 bytes no total, máximo 3.432 bytes, todos <30 KB; paleta de exatamente cinco cores, traço único de 2px, viewBox/grupos preservados, sem gradientes/filtros/raster. Hashes em `validation/artwork-manifest.json`.
- Compilação seca após integração: aprovada em 15,224s. A prévia de produção recompilou após os ajustes finais de apresentação.
- Regressões: 497 testes aprovados em 69,340s. Ajustes finais de apresentação de sucesso/mobile foram compilados e incluídos no build da prévia; não alteram estados ou eventos.
- Componente real renderizado em navegador: quatro combinações de tema/largura e uma verificação de acessibilidade/IDs/fallback, todas aprovadas. Galeria e capturas em `review/scenes*`; relatório `validation/lume-scenes.json`. As 13 verificações locais de carregamento foram repetidas com o componente ilustrativo integrado e passaram.
- Navegação real de Reflex em produção isolada: `.venv/Scripts/python.exe -m tools.check_lume_browser --frontend-workdir .local/frontends/visual-identity-28472`. A primeira tentativa de build foi bloqueada pelo cache npm; repetição com execução ampliada autorizada em `validation/integration-21268/` passou em nove casos. Login e cadastro foram conferidos a 360/1440px, busca sem resultados foi acionada pela interface e biblioteca/feed vazios foram verificados depois de login fictício. Sem erros JavaScript, overflow ou requisição de `mascot.png`; dados e catálogo foram fixtures locais. Compile de produção e build aprovados (build em 33s). Avisos de delta para cliente desconectado aparecem ao navegar entre páginas e não produziram erro JS ou falha dos casos.
- `git diff --check` e validação estrita do OpenSpec aprovados após atualizar tarefas e evidências.

### Estado da entrega

Change com 7/7 tarefas concluídas por evidência local. Oito cenas entregues e aplicações previstas executadas; 404/offline permanecem em catálogo/prévia conforme o roteiro aprovado, sem novo comportamento de backend. Não houve publicação, mutação remota, uso de Docker ou reinício da instância normal. Não confundir a prévia integrada com homologação remota ou aceites de outras changes. As seções anteriores de aprovação e integração pendentes descrevem rodadas anteriores e foram superadas por esta entrega.

## Reversão solicitada pelo usuário

O usuário rejeitou o resultado e pediu retirar as alterações. Restaurados account/admin/social e `assets/mascot.png` a partir de HEAD; login e CSS voltaram ao estado anterior mantendo somente a integração da logo. Módulos, oito cenas e executores novos foram retirados dos diretórios ativos e preservados em `withdrawn-implementation/`. A aprovação e evidências anteriores permanecem históricas; esta entrega não está mais aplicada. Não houve reinício de servidor ou alteração remota.
