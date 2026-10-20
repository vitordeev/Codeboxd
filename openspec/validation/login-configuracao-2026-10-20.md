# Login sem configuração local — 20/10/2026

Vínculo: manutenção operacional posterior à change `corrigir-erros-operacionais`.
Usuário relatou erro ao tentar entrar após a inclusão do botão de visibilidade.

- [x] Reproduzir no navegador e identificar a causa.
- [x] Restaurar `.env` ignorado com endereços públicos dos grupos Xano.
- [x] Verificar conectividade e o formulário após carregar a configuração.

Na reprodução em `http://localhost:3000/login`, foi usado somente um endereço
fictício `example.invalid` e uma senha sintética. Mostrar senha alternou o tipo
para `text`. O envio exibiu “Este serviço ainda não está disponível. Tente
novamente mais tarde.”. Não houve erro JavaScript na carga inicial.

O `.env` não existia; `XANO_AUTH_URL`, `XANO_SOCIAL_URL` e `XANO_BASE_URL`
estavam ausentes no ambiente de diagnóstico. Os endereços foram recompostos
a partir do hostname das evidências locais e dos canonical IDs dos grupos
em `xano/api/`. Nenhuma chave de TMDB/DeepL ou credencial de conta foi
recuperada do histórico. Esses provedores opcionais continuam sem chave local.

A limpeza anterior removeu somente bytecode `__pycache__`; a evidência disponível
não permite atribuir a ela a ausência do `.env`.

Validação: a primeira consulta HTTP foi bloqueada pelo sandbox (WinError 10013);
a repetição autorizada fora dele retornou HTTP 401 em `GET /auth/me` sem token,
comprovando alcance do grupo de autenticação. Os três grupos resolvem URL local.
O servidor existente de desenvolvimento recarregou após atualização do timestamp
de `services/api.py`, sem alteração de conteúdo. Nova submissão no navegador
com dados fictícios retornou “E-mail ou senha inválidos.”, substituindo o erro de
configuração ausente. A conta real do usuário não foi acessada ou modificada.
`git check-ignore .env` confirmou exclusão do Git e `git diff --check` passou.
