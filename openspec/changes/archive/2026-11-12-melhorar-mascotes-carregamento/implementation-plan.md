> **Prancha Lume aprovada pelo usuário com “aprovo”. Integração das oito cenas autorizada.**

# Preparação da integração dos mascotes

A aprovação explícita da prancha foi registrada. Este documento preserva o roteiro da integração autorizada; resultados da execução estão em `validation.md`.

## Pontos de integração

| Cena | Uso previsto após aprovação | Critério de preservação |
| --- | --- | --- |
| onboarding | ilustração de login, cadastro e hero de descoberta sem destaque | manter formulários, logo, texto e destinos atuais |
| vazio | biblioteca sem obras, listas e feed vazios | exibir somente após terminar a carga e sem erro |
| sem resultados | busca concluída sem resultados e sem falha | manter termo da busca e ação para pesquisar novamente |
| sucesso | prévia do conjunto e mensagens de sucesso já existentes quando houver espaço | texto de confirmação permanece como fonte principal de informação |
| carregando | prévia e regiões ilustradas de espera inicial | preservar indicadores inline dos botões e esqueletos; não adicionar duração artificial |
| 404 | prévia do conjunto; futura integração somente se já houver página contextual compatível | não criar rota nova ou alterar o tratamento de rotas ausentes |
| 500 | prévia e erro de serviço que já possua região apropriada | preservar mensagem e ação de repetição; não traduzir todo erro em HTTP 500 |
| offline | prévia do conjunto, sem novo monitoramento de rede | não presumir offline a partir de qualquer falha de provedor |

## Componente e assets

- Um componente `Illustration(name, size)` com catálogo fechado de oito nomes, SVG inline e `viewBox` fixo para herdar `--illu-*` do documento.
- Tamanhos por classes específicas; reservar largura e altura e permitir redução ao espaço disponível. Prefixar IDs por instância para evitar colisões.
- Modo decorativo oculto da acessibilidade; modo informativo com `role=img` e nome localizado. Mensagens e ações permanecem fora do desenho.
- Contorno de 2px, paleta de cinco papéis, sem gradiente ou brilho, sombra plana a 12%; formas e proporções da prancha aprovada.
- Otimizar as peças finais com SVGO e registrar versão/comando. O executável não foi encontrado em `.web/node_modules/.bin` nesta conferência; resolver a ferramenta na etapa de produção, sem mudar dependências do aplicativo por padrão.
- Remover `assets/mascot.png` e substituir o corpo de `_mascots_svg` somente depois de migrar e verificar todos os consumidores ativos. Preservar a logo, capas, uploads, avatares e referências históricas de origem.

## Verificação após aprovação

Comparar as oito cenas lado a lado e nos temas claro/escuro a 360px/1440px; medir XML, tamanho <30 KB, paleta, traço, IDs, acessibilidade e dimensões estáveis. Compilar a integração Reflex e testar regiões vazias, carregando, resultado e erro, distinguindo prévia local de navegação integrada. A change só fica concluída após essa entrega e evidência; a aprovação já foi registrada e a integração deve ser conferida nas evidências atuais.

## Resultado

Prancha aprovada e integração concluída. As oito cenas, componente, otimização e aplicações previstas têm evidências em `validation.md`; galeria em `review/scenes.html`. As cenas 404 e offline são disponibilizadas em catálogo/prévia conforme o escopo desta tabela.
