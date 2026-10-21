# Tarefas da administração

Revisão em 13/10/2026: 17/34 tarefas próprias concluídas; 17 abertas. IDs originais preservados. Checkbox aberto não significa ausência de código: nos grupos 2–5 os contratos locais existem, mas falta validação remota. A [matriz de evidências](validation/revisao-2026-10-13.md) descreve o que já foi feito e o critério restante.

Os sete itens históricos H.1–H.7 foram transferidos para [HISTORICO.md](../../HISTORICO.md), sem perda de contexto e sem inflar a contagem administrativa. As marcações concluídas abaixo indicam a camada local documentada; não comprovam publicação Xano nem smoke completo.

## 1. Levantamento e contratos administrativos

- [x] 1.1 Mapear endpoints, esquemas Xano, campos editáveis do catálogo e regras atuais de papéis/estados de conta; registrar a matriz de operações administrativas em um documento de implementação revisável.
- [x] 1.2 Definir os payloads paginados para indicadores, atividade recente, usuários, catálogo, reports e auditoria; verificar compatibilidade com os modelos existentes e com as quatro specs desta mudança.
- [x] 1.3 Definir limites de acesso e privacidade para snapshots de reports e dados exibidos no dashboard; revisar exemplos de resposta para confirmar que não incluem segredos.

## 2. Autorização e APIs de dashboard

Revisão em 19/10/2026: endpoints e tabela de reports já existem no workspace 147717. Leituras reais rejeitam visitante e membro; 18 testes locais passaram. Correções locais e prévia restrita de dois endpoints revisadas, sem publicação. Faltam conta de teste admin e validação das operações autorizadas. Detalhes em [validation/backend-review-2026-10-19.md](validation/backend-review-2026-10-19.md); os checkboxes abaixo permanecem abertos até a validação completa.

- [ ] 2.1 Implementar verificações de papel admin nos endpoints de leitura e mutação administrativos no Xano, derivando o ator de `$auth.id`; verificar que visitante e membro recebem rejeição também ao chamar os endpoints diretamente.
- [ ] 2.2 Implementar endpoints de totais e atividade recente com paginação e consultas agregadas; verificar as respostas contra contagens conhecidas do ambiente de desenvolvimento.
- [ ] 2.3 Implementar consultas de reports pendentes para alimentar o painel; verificar contagens, paginação e tratamento de lista vazia.

## 3. Gerenciamento de usuários

Implementado localmente: consulta paginada, alteração de status e registro `event_log` em transação. Falta testar respostas reais, bloqueio da conta suspensa e persistência da auditoria.

- [ ] 3.1 Implementar endpoint paginado de busca de usuários por identificador/nome e filtros administrativos; verificar busca sem resultados e ausência de senha, token e dados secretos no payload.
- [ ] 3.2 Implementar suspensão e reativação usando os estados `disabled` e `active`, com ator administrativo obtido da sessão; verificar que uma sessão suspensa não pode continuar usando operações protegidas.
- [ ] 3.3 Persistir auditoria das mudanças de conta com ator, ação, horário e motivo opcional; verificar que o histórico identifica a conta e a ação sem aceitar o ator do payload como fonte de verdade.

## 4. Gerenciamento do catálogo

Implementado localmente: GET/POST/PUT de catálogo administrativo. Tarefa 4.3 possui teste simulado de reutilização de identidade; 4.1–4.2 aguardam comprovação remota de filtros, paginação e integridade.

- [ ] 4.1 Implementar endpoints paginados de catálogo com filtros por filme, série, livro e anime, consulta e busca; verificar que cada filtro retorna apenas seu tipo e que resultados podem ser paginados.
- [ ] 4.2 Implementar correção dos campos administrativos identificados na tarefa 1 sem alterar IDs locais ou referências externas; verificar validação de dados e preservação do registro em caso de erro.
- [x] 4.3 Implementar prevenção de duplicatas pela identidade externa e tipo de obra antes da criação administrativa; verificar que uma identidade existente direciona ao registro atual em vez de criar outro.

## 5. Reports e auditoria de moderação

Implementado localmente: tabela `report`, criação pública autenticada e endpoints administrativos, snapshots e auditoria. Falta validar persistência, autorização direta e política de transições no Xano real; arquivo local não equivale a tabela publicada.

- [ ] 5.1 Criar estrutura persistente para reports com tipo/ID do alvo, snapshot contextual, motivo, denunciante, status e timestamps; verificar inserção válida e rejeição de campos obrigatórios ausentes.
- [ ] 5.2 Implementar fila paginada e filtros por status, tipo e motivo, protegidos pelo papel admin; verificar acesso negado por chamada direta sem papel autorizado.
- [ ] 5.3 Implementar transições pendente, em análise, resolvido e rejeitado com decisão e trilha de auditoria; verificar que cada transição guarda o ator autenticado e o estado anterior.
- [ ] 5.4 Garantir que criar ou revisar um report não apague nem altere automaticamente o conteúdo alvo; verificar a integridade do conteúdo após o fluxo de denúncia.
- [ ] 5.5 Aceitar reports do tipo mensagem usando snapshot mesmo sem criar mensageria; verificar exibição do snapshot quando o alvo ao vivo não estiver disponível.

## 6. Estrutura da área administrativa

Existem componentes e CSS responsivo. 6.2–6.3 continuam abertas porque reutilização/estados e comportamento visual precisam de validação completa desktop/celular. `/admin/demo` é sintética e somente de leitura.

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

Complemento de 20/10: abertura das abas sem filtros/página herdados e botão
“Ver todas”, com 150 testes locais e compilação aprovados. Validação autenticada
real pendente; [evidência](validation/catalogo-inicial-2026-10-20.md).

- [x] 8.1 Implementar seções de filmes, séries, livros e animes com busca, filtros e paginação conectadas às APIs; verificar que cada seção mantém seu tipo ao navegar e filtrar.
- [x] 8.2 Implementar formulário de correção de campos administrativos existentes com validação e confirmação de resultado; verificar erro de validação sem perda dos dados exibidos.
- [x] 8.3 Implementar fila de reports com filtros, contexto do alvo, snapshot e estados de revisão; verificar reports de mensagem sem alvo ao vivo e os demais tipos suportados.
- [x] 8.4 Implementar registro de decisão e mudança de status com feedback; verificar que a UI reflete o histórico e que nenhuma ação ocorre apenas ao abrir um report.

## 9. Validação integrada

Há testes locais em `tests/test_admin.py`, autenticação e social; a suíte completa tem 106 testes aprovados na reanálise. 9.1 segue aberta porque testes simulados não verificam auditoria e autorização do Xano real. A validação 9.3 inclui dry-run histórico de setembro e compilação atual, não publicação administrativa atual.

- [ ] 9.1 Adicionar testes de unidade e integração para autorização, paginação, filtros, transições, snapshots e auditoria; verificar cenários de admin, membro, visitante e dados inválidos.
- [ ] 9.2 Validar a interface completa com dados reais de desenvolvimento, estados vazios, erros parciais e tamanhos móveis; registrar resultados e defeitos encontrados.
- [x] 9.3 Compilar a aplicação Reflex e validar os contratos/endpoints Xano em dry-run; verificar que não há alterações remotas publicadas automaticamente nem credenciais expostas no cliente.
- [x] 9.4 Documentar as migrações, os novos endpoints, a concessão manual do papel admin e o procedimento de rollback; verificar que outra pessoa consegue seguir as instruções em ambiente de desenvolvimento.

## Retomada e encerramento

19/10/2026 — denúncia de obra corrigida localmente: modal com erro visível,
rascunho preservado, cooldown/Retry-After e POST sem repetição automática; obra
externa obtém ID antes do envio. 143 testes e compilação passaram; criação real
e navegador com conta controlada comprovaram persistência e confirmação, com
limpeza das denúncias de teste. Escopo parcial de 5.1/5.4/9.1–9.2; 17/34 mantido.
[Evidência](validation/denunciar-obras-2026-10-19.md).

19/10/2026: três correções de GETs publicadas após backup e dry-run limitado;
dry-run final sem delta. 18 testes locais passaram; visitante 401 e membro 403
verificados. Falta token/conta admin aprovada para validar as consultas e a
interface. Tarefas 3.1, 4.1, 5.2 e 9.1–9.2 mantidas abertas; 17/34.
[Evidência desta rodada](validation/publicacao-buscas-admin-2026-10-19.md).

14/10/2026: erros de buscas administrativas confirmados nos logs Xano e corrigidos
localmente em três GETs; 18 testes admin passaram. Publicação e validação admin
da correção ainda pendentes. [Checkpoint para commit](validation/buscas-admin-2026-10-14.md).
Tarefas 3.1, 4.1, 5.2 e 9.1–9.2 continuam abertas; contagem preservada em 17/34.

Publicação posterior autorizada: [publicacao-admin-2026-10-13.md](validation/publicacao-admin-2026-10-13.md). Dez documentos publicados (tabela report + nove endpoints), com delta sincronizado; GETs rejeitaram visitante (401) e membro (403). Dashboard recebeu entrada/paginação compatível. Admin, desativado, mutações, contagens e auditoria permanecem sem validação completa; checkboxes continuam abertos.

Rodada de implementação posterior à revisão: [retomada-admin-2026-10-13.md](validation/retomada-admin-2026-10-13.md). Tarefas 2.1 e 3.1 receberam correções locais de estado ativo e busca vazia/ID exato. Dry-run limitado passou (tabela report + nove endpoints novos); GETs administrativos atuais retornaram 404. Publicação e cenários autenticados continuam pendentes; nenhum checkbox foi encerrado por essas evidências.

Começar pela autorização direta (2.1), depois dashboard, usuários, catálogo e reports. Registrar testes reais e limpeza de objetos temporários antes de marcar checkboxes. Concluir revisão visual e validação integrada por último. [Pendências centrais](../../PENDENCIAS.md) incluem imagem de post, entrega de e-mail, armazenamento e ambiente, fora do checklist administrativo.
