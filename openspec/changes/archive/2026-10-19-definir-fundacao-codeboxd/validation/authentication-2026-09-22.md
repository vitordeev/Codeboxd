# Validação de cadastro e login — 22/09/2026

## Resultado

14 testes automatizados locais passaram, 6 verificações de integração com o Xano publicado passaram e a compilação Reflex passou. Nenhuma alteração no código da aplicação foi necessária nesta rodada. Isso não confirma o funcionamento completo dos formulários no navegador: não houve execução de navegador nesta rodada.

Ambiente: Windows, Python 3.14, Reflex 0.9.11.post1, ambiente virtual existente `venv`. Configuração do Xano carregada do `.env`, sem copiar valores para este relatório.

## Evidências

| Camada | Cenários | Resultado |
| --- | --- | --- |
| Estado local, backend simulado | Cookie não concede acesso sozinho; sessão expirada limpa identidade e tokens; indisponibilidade preserva identidade e remove papel administrativo; membro sem acesso administrativo; conta desativada bloqueada | Passaram |
| Login local, backend simulado | Manter conectado ligado/desligado; normalização de e-mail; credenciais inválidas sem sessão; mensagem específica de erro | Passaram |
| Cadastro local, backend simulado | Cadastro bloqueado antes da configuração da migração social | Passou |
| Transporte simulado | Retry em 429; URL e Authorization; erro 500 sem vazamento de resposta; resposta malformada; rejeição de caminho absoluto | Passaram |
| Xano real | `/auth/me` sem token e login inválido rejeitados | Passaram |
| Xano real | Nova conta criada e identidade consultada com o token emitido | Passou |
| Xano real | E-mail repetido com username diferente; username repetido com e-mail diferente | Ambos rejeitados |
| Estado da aplicação com Xano real | Login da conta nova, token persistente selecionado, identidade correta, revalidação e limpeza de identidade/tokens no logout | Passou |
| Compilação | `reflex compile --dry` | Passou |

Saídas completas: [testes locais](auth-unit-results.txt), [integração](auth-live-results.json), [compilação](auth-compile-results.txt). Script reproduzível: [auth_live.py](auth_live.py).

## Reprodução

Executar a partir da raiz do repositório:

```powershell
venv\Scripts\python.exe -m unittest discover -s tests -p test_authentication.py -v
venv\Scripts\reflex.exe compile --dry
venv\Scripts\python.exe openspec\changes\definir-fundacao-codeboxd\validation\auth_live.py
```

O último comando usa rede e cria uma conta de teste única por execução. A conta criada nesta rodada permanece no Xano; suas credenciais ficam exclusivamente em `.local/auth-validation-*.json`, ignorado pelo Git. O script não imprime credenciais ou tokens. A primeira tentativa no sandbox falhou por conexão bloqueada; após execução com acesso de rede autorizado, os seis cenários passaram. Falha de conexão inicial não foi classificada como defeito da aplicação.

## Limites e próximos testes

- Não executados nesta rodada: preenchimento e envio no navegador, redirecionamento visual, cookies após recarregar/reabrir navegador, layout e sessão em múltiplas abas.
- Logout verificado no estado Python: identidade e tokens locais ficam vazios. Revogação de token no servidor não foi testada.
- Cadastro real foi exercitado pela API; validações do formulário como confirmação de senha, campos obrigatórios e senha fraca ainda precisam de uma rodada específica pela interface.
- Os testes locais existentes simulam o serviço; seu resultado isolado não comprova integração real.
- As marcações históricas das tarefas não foram alteradas. Esta evidência não substitui a validação final da change nem reproduz necessariamente o erro relatado pelo usuário.
