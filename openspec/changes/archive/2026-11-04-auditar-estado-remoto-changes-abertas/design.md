## Context

Ver proposal.md. A sessão já possui resultados sanitizados de leituras REST e
metadados Xano, sem exportar valores de ambiente nem registros. Há quatro changes
funcionais com 38 tarefas abertas e um scaffold sem artefatos. Reflex, Xano e
provedores TMDB/Kitsu/Open Library permanecem os mesmos; identidades Jikan legadas
não são afetadas.

## Goals / Non-Goals

**Goals:** entregar uma matriz verificável de evidências, lacunas e próximos passos.
**Non-Goals:** executar migrações, escrever dados, disparar recuperação, testar
senhas, conceder papéis, alterar flags, eliminar scaffold ou concluir as changes
funcionais. Navegador autenticado e benchmarks completos continuam fora desta auditoria.

## Decisions

- Usar resultados das consultas em memória e resumos sanitizados; não guardar
  exports brutos ou credenciais na change. Não consultar conteúdo de usuários.
- Distinguir contrato visível no workspace de execução real: guards/índices são
  inspecionáveis; suspensão, entrega de e-mail, auditoria persistida e concorrência
  exigem outros ensaios. GETs públicos/401 não substituem testes admin/membro.
- Registrar flags efetivas somente do processo novo que importa o app; não
  atribuir esses valores a um servidor preexistente sem inspecioná-lo.
- Reutilizar, como evidência anterior desta sessão, os 464 testes/compile
  aprovados sem alterações de código posteriores. Não repetir testes só para
  chamar resultados antigos de uma nova execução.
- Acrescentar referências datadas ao README e PENDENCIAS. Preservar contagens e
  registros históricos, identificando diferenças atuais de forma explícita.
- Não corrigir o scaffold com `skip_specs`: ele não tem escopo documental definido.
  Esta auditoria tem escopo documental próprio e usa essa opção legitimamente.

## Risks / Trade-offs

Contrato sem validação de efeito → manter tarefas funcionais abertas.
Export inclui formato normalizado → diferença textual não prova divergência lógica.
Flag local difere de processo ativo → declarar o escopo exato da inspeção.
Dados/segredos em metadados → pedir env=false/records=false e persistir apenas resumo.

## Migration Plan

Sem migração. Rollback documental remove somente as adições desta change e
suas referências, preservando todo o trabalho anterior. Sem Docker ou reinício.
