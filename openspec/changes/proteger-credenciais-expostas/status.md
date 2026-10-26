# Resultado da rodada de segurança — 26/10/2026

Planejamento e implementação completos, 9/9 tarefas concluídas. A dependência revogar-sessoes-apos-troca-senha foi publicada e validada; manter as changes disponíveis para revisão, sem arquivamento automático.

| Área | Resultado comprovado | Limite restante |
| --- | --- | --- |
| TMDB | Novo token 200, exposto 401; aplicação recarregada e quatro fileiras reais com 20 obras no navegador | Sem pendência de troca identificada nesta cobertura |
| Senhas Xano | A.01/A.03/A.04/A.05 alteradas; login novo e identidade 200, antigo 403; A.02 confirmada ausente na tabela atual | Nenhuma senha histórica utilizável identificada nesta cobertura |
| Tokens Xano | Dois tokens históricos e quatro tokens legados capturados rejeitados; troca de senha revoga sessões anteriores, com isolamento entre contas | Logout global permanece fora do escopo |
| Prevenção | Verificador de blobs do índice, quatro testes sintéticos e revisão adicional dos arquivos novos/modificados | Verificação manual; não há hook automático, nem garantia sobre formatos desconhecidos |
| Git | Regras para .env/.aws/.xano/.local e arquivos gerados, sem apagar cópias locais | Histórico não reescrito; segredos anteriormente versionados não desaparecem do Git |

Aplicação local iniciada em produção em http://localhost:3030, sem Docker. PID do listener observado: 13172; isso é evidência desta rodada, não garantia de execução futura. Nenhum servidor estava escutando antes da inicialização. Compilação Python aprovada; primeira exportação teve timeout de prerender, repetição sem alteração de código passou. Logs privados em .local/credential-rotation/reflex-*.log.

As quatro senhas substitutas estão exclusivamente nos arquivos privados .local/credential-rotation/account-01.json, account-03.json, account-04.json e account-05.json. Não copiar para o OpenSpec ou chat. Nenhuma conta, conteúdo ou relação social foi apagada; houve somente alteração das senhas e registros normais das chamadas de autenticação no Xano.

A primeira tentativa de rotação encontrou HTTP 429 após a primeira conta. A retomada preservou a troca concluída e o substituto pendente, espaçou as requisições e pararia diante de novo 429, sem repetição automática de mutação. account-rotation-attempt-1.json preserva a tentativa anterior.

**Decisão implementada:** após autorização do usuário para continuar, a change específica revogar-sessoes-apos-troca-senha planejou, publicou e validou a política de versões. Foram aprovados 29 checks remotos, navegador autenticado e 392 testes locais. As observações de sessões ainda válidas acima descrevem a linha de base antes dessa dependência, não o estado final. Ver [validação](../revogar-sessoes-apos-troca-senha/validation.md).
