## 1. Levantamento e contratos administrativos

- [x] 1.1 Mapear endpoints, esquemas Xano, campos editáveis do catálogo e regras atuais de papéis/estados de conta; registrar a matriz de operações administrativas em um documento de implementação revisável.
- [x] 1.2 Definir os payloads paginados para indicadores, atividade recente, usuários, catálogo, reports e auditoria; verificar compatibilidade com os modelos existentes e com as quatro specs desta mudança.
- [x] 1.3 Definir limites de acesso e privacidade para snapshots de reports e dados exibidos no dashboard; revisar exemplos de resposta para confirmar que não incluem segredos.

## 2. Autorização e APIs de dashboard

- [ ] 2.1 Implementar verificações de papel admin nos endpoints de leitura e mutação administrativos no Xano, derivando o ator de `$auth.id`; verificar que visitante e membro recebem rejeição também ao chamar os endpoints diretamente.
- [ ] 2.2 Implementar endpoints de totais e atividade recente com paginação e consultas agregadas; verificar as respostas contra contagens conhecidas do ambiente de desenvolvimento.
- [ ] 2.3 Implementar consultas de reports pendentes para alimentar o painel; verificar contagens, paginação e tratamento de lista vazia.

## 3. Gerenciamento de usuários

- [ ] 3.1 Implementar endpoint paginado de busca de usuários por identificador/nome e filtros administrativos; verificar busca sem resultados e ausência de senha, token e dados secretos no payload.
- [ ] 3.2 Implementar suspensão e reativação usando os estados `disabled` e `active`, com ator administrativo obtido da sessão; verificar que uma sessão suspensa não pode continuar usando operações protegidas.
- [ ] 3.3 Persistir auditoria das mudanças de conta com ator, ação, horário e motivo opcional; verificar que o histórico identifica a conta e a ação sem aceitar o ator do payload como fonte de verdade.

## 4. Gerenciamento do catálogo

- [ ] 4.1 Implementar endpoints paginados de catálogo com filtros por filme, série, livro e anime, consulta e busca; verificar que cada filtro retorna apenas seu tipo e que resultados podem ser paginados.
- [ ] 4.2 Implementar correção dos campos administrativos identificados na tarefa 1 sem alterar IDs locais ou referências externas; verificar validação de dados e preservação do registro em caso de erro.
- [x] 4.3 Implementar prevenção de duplicatas pela identidade externa e tipo de obra antes da criação administrativa; verificar que uma identidade existente direciona ao registro atual em vez de criar outro.

## 5. Reports e auditoria de moderação

- [ ] 5.1 Criar estrutura persistente para reports com tipo/ID do alvo, snapshot contextual, motivo, denunciante, status e timestamps; verificar inserção válida e rejeição de campos obrigatórios ausentes.
- [ ] 5.2 Implementar fila paginada e filtros por status, tipo e motivo, protegidos pelo papel admin; verificar acesso negado por chamada direta sem papel autorizado.
- [ ] 5.3 Implementar transições pendente, em análise, resolvido e rejeitado com decisão e trilha de auditoria; verificar que cada transição guarda o ator autenticado e o estado anterior.
- [ ] 5.4 Garantir que criar ou revisar um report não apague nem altere automaticamente o conteúdo alvo; verificar a integridade do conteúdo após o fluxo de denúncia.
- [ ] 5.5 Aceitar reports do tipo mensagem usando snapshot mesmo sem criar mensageria; verificar exibição do snapshot quando o alvo ao vivo não estiver disponível.

## 6. Estrutura da área administrativa

- [x] 6.1 Substituir o placeholder da rota `/admin` por uma estrutura com navegação para Dashboard, Usuários, Filmes, Séries, Livros, Animes e Reports; verificar proteção da rota para admin, membro e visitante.
- [ ] 6.2 Criar componentes reutilizáveis de busca, filtros, tabelas/listas paginadas, estados vazios, carregamento e erro; verificar comportamento com listas vazias e falhas simuladas.
- [ ] 6.3 Aplicar identidade visual do Codeboxd e layout responsivo da área de gerenciamento; verificar navegação e legibilidade em larguras desktop e celular.
- [x] 6.4 Criar a página `/admin/login` com formulário, estado de carregamento, mensagens de erro, link de recuperação e autenticação existente; verificar login de admin e rejeição de credenciais inválidas.
- [x] 6.5 Integrar login administrativo ao estado de sessão, enviar admins autenticados para `/admin` e impedir que membros criem sessão administrativa; verificar os três casos em chamadas de evento.
- [x] 6.6 Atualizar a proteção da rota `/admin` para direcionar visitantes a `/admin/login` e bloquear membros; verificar acesso direto com visitante, membro e admin.

## 7. Interface do dashboard e usuários

- [x] 7.1 Conectar os indicadores reais e atividade recente do dashboard aos endpoints agregados; verificar correspondência com os dados retornados e estados de falha parcial sem valores fictícios.
- [x] 7.2 Criar busca e consulta de usuários com paginação e estados vazios; verificar filtros, abertura de detalhes e ausência de campos secretos na interface.
- [x] 7.3 Adicionar ações de suspender/reativar com confirmação, feedback de sucesso/erro e motivo opcional; verificar cancelamento sem mutação e atualização após confirmação.

## 8. Interface do catálogo e moderação

- [x] 8.1 Implementar seções de filmes, séries, livros e animes com busca, filtros e paginação conectadas às APIs; verificar que cada seção mantém seu tipo ao navegar e filtrar.
- [x] 8.2 Implementar formulário de correção de campos administrativos existentes com validação e confirmação de resultado; verificar erro de validação sem perda dos dados exibidos.
- [x] 8.3 Implementar fila de reports com filtros, contexto do alvo, snapshot e estados de revisão; verificar reports de mensagem sem alvo ao vivo e os demais tipos suportados.
- [x] 8.4 Implementar registro de decisão e mudança de status com feedback; verificar que a UI reflete o histórico e que nenhuma ação ocorre apenas ao abrir um report.

## 9. Validação integrada

- [ ] 9.1 Adicionar testes de unidade e integração para autorização, paginação, filtros, transições, snapshots e auditoria; verificar cenários de admin, membro, visitante e dados inválidos.
- [ ] 9.2 Validar a interface completa com dados reais de desenvolvimento, estados vazios, erros parciais e tamanhos móveis; registrar resultados e defeitos encontrados.
- [x] 9.3 Compilar a aplicação Reflex e validar os contratos/endpoints Xano em dry-run; verificar que não há alterações remotas publicadas automaticamente nem credenciais expostas no cliente.
- [x] 9.4 Documentar as migrações, os novos endpoints, a concessão manual do papel admin e o procedimento de rollback; verificar que outra pessoa consegue seguir as instruções em ambiente de desenvolvimento.

## Histórico concluído antes desta mudança

Estas tarefas registram trabalho anterior no projeto para dar contexto às próximas conversas. Elas não fazem parte da implementação da área administrativa descrita acima.

- [x] H.1 Corrigir o fluxo de recuperação de senha para solicitar e enviar por e-mail o código de uso único do Xano, validar o código e atualizar a senha; verificado pela implementação do endpoint de envio e do fluxo de redefinição no estado de autenticação.
- [x] H.2 Trocar a associação de obra no compositor do feed por pesquisa de filmes, séries, livros e animes, com seleção de resultado; verificado pela implementação do seletor e dos eventos de pesquisa/seleção.
- [x] H.3 Implementar upload de imagem como arquivo multipart para o campo de imagem do post no Xano, com validação, prévia e leitura da imagem no feed; verificado pela implementação e pelos contratos Xano atualizados.
- [x] H.4 Impedir envios duplicados de publicação enquanto a primeira solicitação está em andamento; verificado pela trava no handler de salvamento e pela compilação sintática do estado.
- [x] H.5 Ajustar o alinhamento dos controles de pesquisa e upload, o card de publicação e os botões de cancelar/confirmar exclusão; verificado pelos estilos responsivos e classes do diálogo.
- [x] H.6 Atualizar e publicar no workspace Xano o campo de imagem e os endpoints POST/PUT de publicação; verificado pelo dry-run sem alterações pendentes e pela análise de 68 arquivos Xano sem erros.
- [x] H.7 Compilar a aplicação Reflex após as mudanças do feed; verificado com `reflex compile --dry`.

O fluxo de upload e exibição da imagem ainda não foi validado com uma publicação real no navegador. A entrega de e-mail também depende da configuração e do funcionamento do provedor no workspace Xano.
