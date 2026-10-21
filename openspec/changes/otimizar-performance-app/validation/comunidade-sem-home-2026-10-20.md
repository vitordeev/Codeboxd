# Comunidade sem dependência da home

Continuação autorizada pelo usuário em 20/10: executar o que falta na otimização.
Inspeção de `community_page` confirmou que a tela usa somente `visible_people`
e `following_ids`, sem consumir categorias, destaques ou obras da home.
O loader, porém, chamava `load_home`, aguardando validação de sessão, `/media`,
buscas de filmes/séries, destaques e todas as coleções dos provedores.

Intervenção em `SocialState.load_community`: validar a sessão diretamente,
consultar pessoas e, para membro, consultar as conexões do próprio perfil.
Não alterar endpoints, permissões, cache, seguir/deixar de seguir ou conteúdo
da tela. Falha tardia de perfis não pode substituir aviso de outra rota.

Matriz esperada de chamadas sociais sem cache: visitante `/profiles`; membro
`/profiles` e `/profiles/{próprio-id}`, além da validação de sessão quando
necessária. Zero consultas de catálogo originadas por esse loader.

Testes dirigidos cobrem visitante, membro com conexões e falha após navegação.
Resultado: 14 testes dirigidos aprovados (comunidade, respostas tardias,
restauração e isolamento) e `reflex compile --dry` aprovado em 16,370 s.
Os tempos do teste simulado não são benchmark de navegação.
Suíte completa após a intervenção: **274 testes aprovados em 56,144 s**.
Não representa comparação remota, paginação social ou conclusão integral de 7.1/7.2.
Rollback: restabelecer a chamada antiga; esta evidência permanece no histórico.
