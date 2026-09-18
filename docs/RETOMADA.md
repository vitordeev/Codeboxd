# Ponto de retomada — CodeBoxd

## Pedido e escopo

Implementar a rede social prevista nas changes `definir-fundacao-codeboxd` e `criar-modelo-dados-xano`, com Reflex e Xano. O usuário pediu encerrar esta etapa com o trabalho salvo para continuar no dia seguinte. Não interpretar este checkpoint como conclusão das 117 tarefas.

## Aplicado e verificado localmente

- Skills oficiais reflex-docs, setup-python-env e reflex-process-management instaladas em `C:/Users/victo/.codex/skills`.
- Ambiente existente: `venv`, Python 3.14.6, Reflex 0.9.11.post1.
- Designs completos e referências a Streamlit substituídas por Reflex; as duas changes passaram no `openspec validate`.
- Autenticação ativa usa `state/session.py`; `auth_state.py` é um alias de compatibilidade.
- Login por submit (incluindo Enter e validação HTML), sem senha como variável sincronizada de estado. Cookie de 24 horas para lembrar sessão e SessionStorage caso contrário.
- Identidade/papel confirmados por `/auth/me`, acesso ao admin condicionado ao papel e guard de carregamento, tratamento distinto para credenciais e falhas de serviço.
- Rotas conectadas: `/`, `/login`, `/cadastro`, `/conta`, `/admin`. Login redireciona admin para `/admin` e demais usuários para `/conta`.
- CSS personalizado conectado; removido carregamento duplicado de Tailwind por CDN. O plugin TailwindV4 existente continua responsável pelas classes.
- Cadastro tem formulário e validação, mas permanece bloqueado quando `XANO_SOCIAL_URL` está ausente. O endpoint antigo publicado não garante username/perfil. NÃO configurar a variável como se a migração já estivesse publicada.
- `.env.example` documenta configuração; `.gitignore` protege ambientes, segredos e `.local/`.

Validações executadas:

```powershell
python -m reflex compile --dry
python -m unittest discover -s tests -v
openspec validate definir-fundacao-codeboxd
openspec validate criar-modelo-dados-xano
```

Resultado: compilação OK, 12 testes OK, duas changes válidas. Os testes usam respostas simuladas; não validam um login real ou publicação Xano. O módulo `state/social.py` foi importado com sucesso, mas seus fluxos não foram testados nem conectados a páginas.

## Preparado, ainda não finalizado

- `services/api.py`: transporte assíncrono Xano, normalização de URL e erros.
- `services/catalog.py`: busca/detalhes TMDB, Jikan e Open Library; precisa de testes dos adaptadores e `TMDB_READ_TOKEN` para filmes/séries.
- `state/social.py`: rascunho de biblioteca, perfis, seguidores, feed, posts, comentários, curtidas e listas. Ainda precisa de revisão, testes e telas. Não faz parte das rotas ativas.
- `xano/table/`: nove tabelas sociais adicionadas em arquivos XanoScript.
- `xano/api/codeboxd/`: 30 endpoints preparados, canonical proposto `codeboxd`.
- Correções Xano locais: autorização dos writes de titulos, registro de logs sem objetos de usuário, cadastro transacional com perfil, bloqueio de contas desativadas.

## Estado remoto

**Nenhuma alteração foi publicada no Xano.**

- CLI autenticado no perfil default; workspace identificado: Pedro's Workspace, ID 147717.
- Exportação remota sem registros/segredos em `.local/xano-remote/`, incorporada aos arquivos locais para preservar os campos já existentes.
- Remoto tem `titulos`, campos adicionais de user e papel moderator; preservar tudo. Games do legado não devem ser convertidos em séries.
- `xano sandbox get` falhou: sandbox não está disponível no plano Free.
- Dry-run executado: 9 tabelas criadas, 1 grupo criado, 30 endpoints criados e 9 endpoints atualizados. Dry-run é prévia de alterações, NÃO prova de compilação ou execução do XanoScript.
- Não usar truncamento, importação de registros, exclusão de objetos ausentes ou sobrescrever variáveis remotas.

## Próximos passos

1. Ler este documento, `AGENTS.md`, os designs e tasks das duas changes; preservar alterações locais e remotas da equipe.
2. Revisar/validar os XanoScripts antes de publicar: sintaxe, retorno de variáveis em condicionais/transações, unicidade sob concorrência, limites/paginação, validação backend de username/URLs, autorização e privacidade. Rever a recuperação de senha legada e revogação de sessões.
3. Construir páginas sociais que usem `SocialState`, com estados vazios/erro/carregamento, paginação e confirmação para exclusões. Tratar recarregamento das páginas e evitar dados de outro usuário após logout/login.
4. Testar adaptadores externos, falhas parciais, normalização, sessões e ownership com dois usuários. Configurar TMDB somente pelo `.env` local.
5. Comparar novamente o remoto, apresentar a prévia final e aplicar migração revisada no workspace autorizado. Não declarar tarefas remotas concluídas com base somente nos arquivos.
6. Configurar a URL social publicada, liberar cadastro e executar fluxo real de cadastro/login/perfil, interações, feed e listas. Não publicar credenciais ou registrar senhas/tokens em relatórios.
7. Atualizar checkboxes somente conforme a evidência. Arquivar OpenSpec apenas depois da implementação completa.

Os arquivos estão salvos no diretório de trabalho. Não foi criado commit; o projeto já tinha diversos arquivos não rastreados antes desta implementação.
