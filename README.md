# CodeBoxd — Descubra, organize e compartilhe

O CodeBoxd é uma aplicação web para pessoas que gostam de filmes, séries, animes e livros. Ela reúne descoberta de obras, registros pessoais e recursos sociais para que cada pessoa organize o que acompanha e compartilhe suas opiniões.

## 1. Apresentação

Catálogos culturais costumam ficar separados, enquanto avaliações, listas e conversas ficam espalhadas por vários lugares. O CodeBoxd reúne esses registros em um perfil cultural e aproxima pessoas com interesses semelhantes.

O público principal são leitores e espectadores que querem descobrir obras, acompanhar o que já consumiram e conversar sobre suas experiências. A aplicação também tem uma área administrativa para a equipe responsável pela comunidade.

## 2. Acesso ao aplicativo

### Versão publicada

**Não há uma versão publicada para acessar nesta entrega.** Para conhecer e usar o aplicativo, siga as instruções de execução local abaixo.

### Executar localmente

Na raiz do repositório, com Python 3.12 instalado, abra o PowerShell e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
python -m reflex run
```

Configure no arquivo `.env` as variáveis necessárias para as integrações antes de usar buscas, login e dados remotos. Não compartilhe esse arquivo. O endereço local aparece no terminal quando o Reflex inicia; a porta pode variar conforme o que estiver disponível no computador.

### Principais páginas

| Página | Endereço local | Para que serve |
| --- | --- | --- |
| Descobrir | `/` | Buscar e explorar obras |
| Cadastro | `/cadastro` | Criar uma conta |
| Login | `/login` | Entrar como membro |
| Obra | `/obra/<id>` | Ver detalhes, avaliar e organizar uma obra |
| Biblioteca | `/biblioteca` | Consultar obras registradas |
| Comunidade | `/comunidade` | Encontrar outros perfis |
| Feed | `/feed` | Ver publicações da comunidade |
| Listas | `/listas` | Consultar e organizar listas |
| Meu perfil | `/conta` | Ver ou editar o próprio perfil |
| Administração | `/admin/login` | Entrar na área administrativa, para contas autorizadas |

## 3. Perfis de usuários

| Perfil | O que pode fazer |
| --- | --- |
| Visitante | Explorar e pesquisar o catálogo e abrir páginas de obras. Para salvar registros, publicar ou seguir pessoas, precisa criar uma conta. |
| Membro cadastrado | Manter biblioteca, avaliações e listas; editar o perfil; acompanhar pessoas e participar das áreas sociais disponíveis. |
| Administrador | Acessar o painel restrito, consultar métricas e ferramentas de usuários, catálogo e denúncias. O acesso exige uma conta com papel administrativo concedido pela equipe. |

## 4. Funcionalidades

- **Catálogo:** filmes, séries, animes e livros, com dados obtidos de serviços externos. A disponibilidade de informações, capas e recomendações depende desses serviços.
- **Busca e descoberta:** pesquisa por título e navegação por categoria na página inicial.
- **Detalhes da obra:** descrição e informações disponíveis; algumas obras também exibem trailers, recomendações e opções de onde assistir.
- **Avaliações e biblioteca:** registrar uma nota, escrever uma crítica, indicar spoiler e acompanhar o status de uma obra.
- **Listas:** reunir obras em listas pessoais e escolher a visibilidade pública ou privada.
- **Comunidade e perfis:** encontrar perfis, seguir pessoas e consultar atividades e avaliações.
- **Feed:** acompanhar publicações e interações da comunidade.
- **Moderação:** administradores podem consultar denúncias, analisar o contexto e escolher uma decisão compatível com o tipo de conteúdo reportado.

## 5. Manual de utilização

### Jornada de visitante: descobrir uma obra

1. Abra a página **Descobrir** (`/`).
2. Digite um título no campo de busca ou escolha uma categoria: filmes, séries, animes ou livros.
3. Selecione um resultado para abrir a ficha da obra.
4. Consulte as informações disponíveis e as recomendações.
5. Para salvar uma avaliação na conta, organizar a obra na biblioteca ou participar da comunidade, crie uma conta e entre no aplicativo.

**Resultado esperado:** a obra aparece na página de detalhes. Os dados disponíveis variam conforme o catálogo externo.

### Jornada de membro: registrar uma avaliação

1. Abra `/cadastro`, preencha nome, usuário, e-mail e senha e selecione **Criar conta**. Se já tiver cadastro, use `/login`.
2. Pesquise uma obra em **Descobrir** e abra seus detalhes.
3. Escolha uma nota de meia a cinco estrelas, informe o status da obra e escreva sua crítica.
4. Marque a opção de spoiler quando o texto revelar partes importantes da história.
5. Selecione **Salvar avaliação**.
6. Consulte o resultado em **Biblioteca** (`/biblioteca`) ou no seu perfil (`/conta`).

**Resultado esperado:** a obra e os dados registrados ficam associados à conta, desde que a integração remota esteja disponível. Sem login, a nota escolhida na página da obra fica somente no navegador e não é publicada no perfil.

### Jornada de membro: organizar uma lista

1. Entre na conta e abra **Listas** (`/listas`).
2. Crie uma lista, informe título e descrição e escolha se será pública ou privada.
3. Pesquise obras dentro da lista ou abra uma obra e escolha **Adicionar a outra lista**.
4. Consulte a lista para conferir as obras incluídas.

**Resultado esperado:** a coleção aparece na página de listas com a visibilidade escolhida. A disponibilidade da gravação depende da conexão com o backend.

### Jornada de membro: conhecer a comunidade

1. Abra **Comunidade** (`/comunidade`) e escolha um perfil.
2. Se estiver conectado, selecione **Seguir** para acompanhar a pessoa.
3. Abra **Feed** (`/feed`) para consultar publicações e interações disponíveis.
4. Em **Meu perfil** (`/conta`), use **Editar perfil** para atualizar nome, usuário, bio e foto. O editor também permite enviar um banner.

**Resultado esperado:** o perfil mostra as informações e atividades carregadas pelo serviço. Upload de imagens depende da configuração integrada de armazenamento.

### Jornada de membro: publicar no feed

1. Abra **Feed** (`/feed`) e selecione **Criar publicação**.
2. Escreva o texto. Se quiser, pesquise e associe uma obra e marque **Contém spoilers**.
3. Opcionalmente selecione uma imagem e confira a prévia.
4. Selecione **Publicar**. Em uma publicação existente, use os controles disponíveis para curtir ou abrir os comentários.

**Resultado esperado:** a publicação aparece no feed quando a gravação no backend é confirmada. O envio de imagem tem a limitação descrita na seção 7.

### Jornada administrativa: analisar uma denúncia

1. Acesse `/admin/login` com uma conta administrativa autorizada.
2. No painel, abra **Reports/Denúncias** e use os filtros de status, tipo ou motivo.
3. Leia o contexto da denúncia. Abrir um report, por si só, não remove o conteúdo.
4. Registre uma decisão e sua justificativa. Se a equipe decidir remover o alvo, use a ação correspondente ao tipo: publicação, comentário, avaliação ou obra.

**Resultado esperado:** a decisão fica registrada conforme as permissões e endpoints administrativos disponíveis. A interface separa a revisão da denúncia da remoção do conteúdo.

## 6. Exemplos de utilização

- **Organizar uma sessão de cinema:** pesquise um filme, registre a avaliação depois de assistir e adicione-o a uma lista chamada “Favoritos de ficção científica”.
- **Acompanhar uma série:** marque a obra como “Quero ver / ler” e depois atualize seu registro quando terminar.
- **Compartilhar uma crítica:** escreva uma avaliação no perfil e marque como spoiler se revelar acontecimentos da trama.
- **Moderar conteúdo:** um administrador filtra denúncias de comentários, lê o contexto e decide entre registrar uma decisão ou remover apenas o comentário reportado.

Os exemplos são cenários de uso, não dados ou contas de demonstração. Não há credenciais de teste publicadas neste repositório.

## 7. Limitações conhecidas

- Não há endereço público de produção nesta entrega; o aplicativo deve ser executado localmente e depende da configuração privada das integrações.
- Busca, autenticação, biblioteca, feed, listas e administração dependem de configuração e disponibilidade do Xano e dos provedores externos.
- O cadastro também depende de `XANO_SOCIAL_URL` e do endpoint de cadastro social publicado; sem essa configuração a aplicação informa que o cadastro ainda está em preparação.
- Recursos de imagem em publicações dependem da integração Cloudinary/Xano. A validação integrada e o ciclo de limpeza de imagens ainda têm pendências; não trate esse fluxo como garantido antes de uma conferência no ambiente publicado.
- O catálogo pode não fornecer todos os campos, capas, trailers ou disponibilidade de streaming para cada obra.
- Os controles administrativos aparecem apenas para contas autorizadas; este README não fornece credenciais administrativas.
- Não incluí capturas de tela porque ainda não há imagens atuais verificadas da aplicação em execução.

---

CodeBoxd — projeto acadêmico desenvolvido por uma equipe de três estudantes de Análise e Desenvolvimento de Sistemas.
