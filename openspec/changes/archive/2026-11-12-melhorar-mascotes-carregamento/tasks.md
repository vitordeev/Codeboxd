## 1. Carregamento

- [x] 1.1 Criar componente de status e esqueletos com anúncio acessível, classes isoladas e movimento reduzido; verificar renderização, ausência de foco em placeholders e CSS.
- [x] 1.2 Integrar os estados existentes em home, busca, ficha, biblioteca, perfil, comentários, feed, autenticação e administração, preservando conteúdo/erros/repetição; conferir ramos condicionais e compile.
- [x] 1.3 Validar componentes no navegador em 360px/1440px, movimento reduzido e estados de carregamento/erro/conclusão; executar regressões adequadas e registrar limites da validação local.

## 2. Ilustrações

- [x] 2.1 Criar prancha original de evolução dos robôs com cinco cores, três poses, três expressões e seis objetos; validar SVG e prévia em dois temas e 360px/1440px.
- [x] 2.2 Apresentar a prancha e registrar aprovação explícita antes de criar cenas; preservar pendência enquanto não houver resposta.
- [x] 2.3 Após aprovação, entregar oito cenas via componente acessível, otimizar com SVGO, confirmar tamanho <30 KB e substituir os bonecos antigos preservando demais assets; validar temas, dimensões e referências.

## 3. Evidências

- [x] 3.1 Registrar comandos, resultados, limitações e pendências no OpenSpec e executar validação estrita sem declarar aceites não executados.

## Evidências da rodada

Carregamento implementado com flags existentes, sem alterações de estado/serviço/API. Componente e CSS real renderizados no navegador em 13 casos locais; 497 testes existentes aprovados em 77,063s; compile inicial aprovado em 15,570s. Prancha Lume entregue em `review/` e validada em quatro casos de tema/largura. A tarefa 2.2 aguarda aprovação explícita do usuário; 2.3 permanece aberta. Resultados/limites em `validation.md`. Não houve substituição dos bonecos no app nem retomada do redesign cancelado.

## Aprovação da direção visual

O usuário respondeu **“aprovo”** à solicitação explícita de aprovação da prancha Lume. Aprovação registrada antes de produzir as oito cenas e iniciar sua integração. A tarefa 2.2 está concluída; a implementação e validação da 2.3 seguem nesta rodada.

## Integração concluída após aprovação

2.3 concluída: oito SVGs Lume otimizados com SVGO 4.0.0 (23.863 bytes no total, maior arquivo 3.432 bytes), componente acessível com fallback e IDs prefixados, uso em login/cadastro/hero, vazios, busca sem resultados, carregamento e feedback de erro/sucesso. Mascote raster antigo removido dos assets ativos; referência de origem em `Imagens/` preservada. As cenas 404 e offline estão disponíveis no catálogo/prévia sem inventar rotas ou diagnósticos de rede.

Evidências: `validation/artwork-manifest.json`, `validation/lume-scenes.json`, `validation/loading-browser.json`, `validation/integration-21268/result.json`; galeria final em `review/scenes.html`. Navegador integrado: nove casos aprovados com backend fictício, sem erros JavaScript; build de produção isolado aprovado, 497 regressões passaram em 69,340s. A instância normal não foi reiniciada e não houve validação remota/publicação. Todos os sete itens desta change têm evidência local; isso não conclui tarefas de outras changes.

## 4. Reversão solicitada pelo usuário

- [x] 4.1 Restaurar bonecos e carregamento anteriores, preservando a integração da logo; conferir diff e referências.
- [x] 4.2 Retirar os novos módulos/assets/executores dos diretórios ativos e registrar a reversão com evidências preservadas.

As tarefas anteriores descrevem a implementação histórica, agora revertida por solicitação do usuário. Arquivos novos preservados em `withdrawn-implementation/`, sem distribuição no app. Não retomar esta change sem novo pedido.
