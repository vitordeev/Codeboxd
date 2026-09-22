# Roadmap e próximos passos

## Fase 0 — Decisões e preparação

- [ ] Escolher entre Streamlit e Reflex.
- [ ] Confirmar o workspace Xano alvo: `Victor's Workspace` (`151345`).
- [ ] Definir convenções de nomes, tipos e enums.
- [ ] Definir as APIs externas de filmes, séries, animes e livros.
- [ ] Definir variáveis de ambiente e nunca armazenar credenciais no repositório.
- [ ] Registrar as decisões nas especificações do OpenSpec.

## Fase 1 — Modelo de dados Xano

- [ ] Revisar o modelo de `user` atual.
- [ ] Adicionar `username` único.
- [ ] Separar os dados públicos em `profile`.
- [ ] Criar `media`.
- [ ] Criar `user_media_interaction`.
- [ ] Criar `user_follow`.
- [ ] Criar `post`.
- [ ] Criar `post_like`.
- [ ] Criar `comment`.
- [ ] Criar `user_list`.
- [ ] Criar `user_list_item`.
- [ ] Criar índices e restrições únicas.
- [ ] Criar dados de teste mínimos.

## Fase 2 — Autenticação e perfis

- [ ] Ajustar cadastro para username, email e senha.
- [ ] Validar campos obrigatórios e duplicidades.
- [ ] Confirmar login e sessão.
- [ ] Implementar logout conforme a estratégia escolhida.
- [ ] Criar leitura e edição do perfil próprio.
- [ ] Proteger alterações de perfil por ownership.
- [ ] Criar consulta pública de perfil e estatísticas.

## Fase 3 — Catálogo e descoberta

- [ ] Implementar adaptadores das APIs externas.
- [ ] Normalizar respostas para o modelo `media`.
- [ ] Criar busca textual.
- [ ] Criar filtros por tipo.
- [ ] Criar detalhes da mídia.
- [ ] Persistir somente a referência e os dados necessários.
- [ ] Tratar resultados vazios e falhas externas.

## Fase 4 — Interações e listas

- [ ] Implementar status de consumo.
- [ ] Implementar nota e review.
- [ ] Implementar atualização da interação existente.
- [ ] Criar listas.
- [ ] Adicionar e remover mídias.
- [ ] Proteger listas por ownership.
- [ ] Impedir duplicações.

## Fase 5 — Rede social

- [ ] Implementar seguir e deixar de seguir.
- [ ] Impedir auto-seguimento e duplicação.
- [ ] Implementar posts.
- [ ] Implementar curtidas.
- [ ] Implementar comentários.
- [ ] Implementar edição e exclusão do próprio conteúdo.
- [ ] Implementar feed de usuários seguidos.

## Fase 6 — Frontend

- [ ] Criar estrutura inicial do frontend.
- [ ] Criar fluxo de cadastro, login e logout.
- [ ] Criar página inicial.
- [ ] Criar busca e resultados.
- [ ] Criar detalhes da mídia.
- [ ] Criar biblioteca e interações.
- [ ] Criar listas.
- [ ] Criar feed.
- [ ] Criar perfil.
- [ ] Tratar carregamento, erros e estados vazios.

## Fase 7 — Validação

- [ ] Testar o fluxo completo de cadastro até perfil.
- [ ] Testar busca até detalhe da mídia.
- [ ] Testar persistência das interações entre sessões.
- [ ] Testar feed com relações de seguidores.
- [ ] Testar listas com todas as categorias.
- [ ] Testar ownership e autorização.
- [ ] Testar duplicação e integridade referencial.
- [ ] Validar as changes com `openspec validate --all --no-interactive`.
- [ ] Executar `xano workspace push --dry-run` antes de publicar alterações.
- [ ] Revisar o workspace após o push.

## Comandos operacionais úteis

```powershell
# Verificar perfil e conta autenticada
xano profile get
xano profile me
xano workspace list

# Exportar o workspace atual para inspeção
xano workspace pull --directory .\tmp\xano-workspace

# Validar as especificações
openspec validate --all --no-interactive

# Sempre simular antes de publicar alterações
xano workspace push --dry-run
```

## Critério de conclusão da fundação

A fundação estará pronta quando:

- O frontend escolhido estiver iniciado.
- O usuário puder se cadastrar, entrar e acessar seu perfil.
- O Xano possuir todas as entidades principais.
- As restrições de unicidade e ownership estiverem ativas.
- Uma mídia puder ser buscada e associada a uma interação.
- Listas e relações sociais puderem ser persistidas.
- O fluxo principal estiver validado ponta a ponta.
