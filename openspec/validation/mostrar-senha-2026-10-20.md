# Mostrar e ocultar senha — 20/10/2026

Complemento ativo de autenticação e da change `recuperar-senha-codigo-6-digitos`.
Pedido do usuário: permitir visualizar a senha digitada.

- [x] Adicionar controle independente aos campos de login, cadastro e redefinição.
- [x] Iniciar oculto, alternar ícone/descrição acessível e usar botão sem submit.
- [x] Validar compilação e testes locais.
- [ ] Validar interação no navegador em todas as páginas (login verificado em 20/10).

Componente compartilhado `Codeboxd_main/password_input.py` com ComponentState:
apenas a visibilidade é estado; a senha continua sendo enviada pelo formulário.
Cada campo tem controle independente. O login administrativo já possuía o recurso
e foi preservado. Estilo com área de toque de 44px e foco visível.

Referência consultada: https://reflex.dev/docs/api-reference/componentstate/
Não houve alteração de contratos Xano nem publicação remota.

Validação local: `.venv/Scripts/python.exe -m reflex compile --dry` passou;
`unittest discover -s tests -q` passou com 148 testes; `git diff --check`
passou. A suíte existente cobre regressões de autenticação, mas não comprova
a interação visual do novo botão. Revisão no navegador ainda pendente.

Complemento em 20/10: login abriu sem erro JavaScript e o botão “Mostrar senha”
alternou o campo para `text`; o formulário foi enviado com dados sintéticos.
O erro de configuração do login foi investigado e corrigido em
[evidência própria](login-configuracao-2026-10-20.md). Cadastro e redefinição
ainda não tiveram a interação dos botões conferida no navegador.
