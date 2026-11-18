## Purpose

Preservar a identidade preta e amarela do Codeboxd enquanto torna suas páginas,
ações e mensagens visualmente coerentes, acessíveis e responsivas.

## ADDED Requirements

### Requirement: Identidade visual preservada
O aplicativo SHALL usar tema escuro por padrão, base preta/escura e amarelo intencional para ações e foco, preservando logo e mascotes ativos. Componentes equivalentes SHALL compartilhar hierarquia de texto, cores, espaços e controles, sem reativar arte revertida.

#### Scenario: Navegar entre famílias de páginas
- **WHEN** uma pessoa alterna entre descoberta, social, autenticação e administração
- **THEN** a marca e o significado visual dos controles SHALL permanecer reconhecíveis, com hierarquia adequada ao contexto

#### Scenario: Uso de referências históricas
- **WHEN** uma referência antiga diverge da identidade ativa ou pertence a trabalho revertido
- **THEN** ela SHALL ser identificada como histórica e não substituir a identidade atual sem aprovação específica

### Requirement: Navegação encontrável e compatível
A navegação SHALL distinguir Início, Buscar, Feed e Biblioteca e manter acesso reconhecível a listas, perfil e comunidade. Rotas existentes SHALL continuar funcionais. Reduzir duplicação visual SHALL preservar ações úteis e alternativas acessíveis.

#### Scenario: Encontrar o próprio acervo
- **WHEN** o usuário quer abrir biblioteca, gerenciar suas listas ou acessar seu perfil
- **THEN** esses destinos SHALL ser alcançáveis pela navegação identificada, sem depender de encontrar conteúdo no feed

#### Scenario: Uso em tela pequena
- **WHEN** a navegação é apresentada em celular ou tablet
- **THEN** ela SHALL oferecer os mesmos destinos essenciais sem ocultá-los atrás de hover ou obstruir o foco e o conteúdo

### Requirement: Hierarquia e recursos preservados
Cada contexto SHALL distinguir ação principal, alternativas e informação secundária. A simplificação SHALL manter informações de domínio, direitos de edição, estado de privacidade e funcionalidades acessíveis, sem confundir notas, progresso, listas e publicações.

#### Scenario: Revisão de uma ficha
- **WHEN** os controles de avaliação e organização são modernizados
- **THEN** o usuário SHALL continuar distinguindo nota, crítica, progresso e inclusão em lista, com acesso aos detalhes técnicos pertinentes ao tipo da obra

#### Scenario: Controle visual redundante
- **WHEN** um controle duplicado é condensado ou movido
- **THEN** a ação equivalente SHALL permanecer identificável, operável por teclado e disponível no contexto revisado

### Requirement: Feedback contextual e recuperável
Carregamento, vazio, sucesso, erro e falha parcial SHALL ter mensagens distintas e compreensíveis. Uma falha SHALL preservar conteúdo utilizável e entrada recuperável, sem indicar sucesso não confirmado ou repetir a mesma mensagem desnecessariamente em vários locais.

#### Scenario: Falha de uma seção
- **WHEN** uma consulta complementar falha enquanto outra seção está disponível
- **THEN** o conteúdo disponível SHALL permanecer utilizável e a seção afetada SHALL informar a falha e ação de recuperação aplicável

#### Scenario: Envio pendente ou recusado
- **WHEN** uma ação está pendente ou falha
- **THEN** o controle SHALL comunicar o estado, impedir duplicação enquanto necessário e preservar o rascunho permitido, com anúncio acessível contextual

### Requirement: Acessibilidade dos fluxos alterados
Os fluxos alterados SHALL atender aos critérios aplicáveis WCAG 2.2 AA, com contraste adequado, nomes/rótulos, teclado, foco visível não encoberto e status acessível. Ações principais e controles de toque SHALL ter área interativa projetada para 44×44 CSS px, respeitando no mínimo 24×24 e exceções normativas justificadas.

#### Scenario: Operar sem mouse
- **WHEN** o usuário navega por teclado, abre diálogo e retorna à página
- **THEN** ele SHALL alcançar as ações, reconhecer o foco e retornar ao gatilho sem armadilha ou perda de contexto

#### Scenario: Informação de estado
- **WHEN** seleção, erro ou confirmação é apresentada
- **THEN** seu significado SHALL ser identificável sem depender apenas de cor, ícone decorativo ou animação

### Requirement: Responsividade e movimento reduzido
A interface SHALL manter leitura e operações em 320, 390, 768, 1024 e 1440 CSS px, zoom de 200% e reflow aplicável, sem rolagem horizontal involuntária do documento. Preferências de movimento reduzido SHALL ser respeitadas.

#### Scenario: Texto longo em largura pequena
- **WHEN** nomes, títulos ou mensagens longas aparecem em 320/390px
- **THEN** o layout SHALL acomodar o conteúdo sem cortar ações essenciais, encobrir foco ou exigir rolagem horizontal da página

#### Scenario: Preferência por menos movimento
- **WHEN** o usuário solicita movimento reduzido
- **THEN** transições não essenciais SHALL ser removidas e informações/ações SHALL permanecer disponíveis sem animação

### Requirement: Apresentação sem regressão funcional ou de tráfego
Mudanças puramente visuais SHALL preservar regras e permissões existentes e não acrescentar chamadas ao backend. Estados indisponíveis SHALL permanecer distintos de valores válidos, inclusive na administração, sem transformar falha em zero ou vazio.

#### Scenario: Atualização visual administrativa
- **WHEN** controles ou indicadores da administração são modernizados
- **THEN** guardas, confirmações, auditoria e paginação SHALL permanecer preservados e indicador indisponível SHALL continuar explícito

#### Scenario: Comparação da mesma jornada
- **WHEN** uma mudança visual é candidata a aceite
- **THEN** suas chamadas, recursos renderizados e resposta de interação SHALL ser comparados em condições equivalentes, investigando regressões antes de concluir
