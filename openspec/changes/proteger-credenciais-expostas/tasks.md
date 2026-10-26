## 1. Inventário e contenção

- [x] 1.1 Auditar arquivos atuais, índice e histórico disponível com saída sanitizada; registrar categorias, ocorrências, consumidores e limites de cobertura, sem valores ou dados pessoais.
- [x] 1.2 Classificar exposição confirmada e itens não verificados; definir ordem por privilégio/alcance, mecanismos de revogação e acessos necessários com evidência por item.

## 2. Rotação e contas

- [x] 2.1 Substituir credenciais de serviço expostas e atualizar todos os consumidores identificados; comprovar funcionamento autorizado, registrando por item o que não foi validado.
- [x] 2.2 Revogar credenciais anteriores e registrar evidência sanitizada do provedor ou rejeição autenticativa inequívoca; manter abertos itens sem comprovação.
- [x] 2.3 Trocar senhas de contas de teste afetadas e verificar/tratar sessões e tokens anteriores; comprovar preservação de acesso legítimo e invalidação conforme mecanismo disponível.

## 3. Prevenção

- [x] 3.1 Implementar verificação reproduzível do conteúdo preparado para commit e arquivos privados conhecidos, com saída sem valores; validar detecção, código de saída e ausência de vazamento usando fixtures sintéticas.
- [x] 3.2 Conferir ignore, exemplos de configuração e instruções de uso do verificador; validar placeholders, URLs públicas e exclusão dos arquivos privados sem apagar cópias locais.

## 4. Evidências e fechamento

- [x] 4.1 Executar checks locais relevantes e smoke seguro das integrações alteradas; separar evidências locais/remotas e registrar limitações sem tratar testes simulados como rotação real.
- [x] 4.2 Reconciliar P.1 e documentos centrais com o inventário final, resultados por item e pendências; validar a change e manter abertas tarefas sem evidência.

## Evidência de planejamento — 26/10/2026

Git estava limpo antes da criação. `openspec list --json` mostrou três changes ativas, nenhuma cobrindo rotação de credenciais; propostas conferidas. P.1 e operational-reliability foram lidas. Criados proposta, design, delta de spec e checklist. Nenhuma rotação, auditoria de valores ou validação remota foi executada nesta etapa. Resultado da validação documental registrado em validation.md.

## Evidência de inventário — 26/10/2026

Tarefa 1.1: [inventário e limites](inventory.md), [ocorrências sanitizadas](inventory.json) e [triagem de contas](account-triage.json). Auditores executados com exit 0; comparação em memória confirma token TMDB atual no histórico, cinco registros de conta com senha e dois campos de token em quatro JSON históricos. Checagem de privacidade dos artefatos passou. Nenhuma chamada remota, rotação ou alteração da configuração privada. Tarefa 1.2 e demais continuam abertas.

Tarefa 1.2, rodada seguinte: [plano e classificação](rotation-plan.md), [consulta Xano sanitizada](access-audit.json), [validação TMDB](tmdb-check.json). TMDB exposto aceito com 200; três contas Xano identificáveis são member/active. Duas contas e mecanismos efetivos de revogação de sessão continuam não verificados; limitações e acessos necessários documentados. Nenhuma credencial alterada. Rotação depende do acesso à conta emissora; não confundir preparação com entrega de 2.1–2.3.

Após o usuário informar atualização do .env: verificador repetido confirmou current_matches_exposed=true e autenticação 200 para o valor exposto. Não foi detectado token substituto; rotation_verified=false. Tarefas 2.1/2.2 continuam abertas, conforme validation.md.

Atualização posterior confirmada: token novo diferente, autenticação HTTP 200; token TMDB exposto rejeitado com HTTP 401. Leituras movie/popular e tv/popular com novo token retornaram 200 e resultados. Tarefa 2.2 concluída para o segredo de serviço cuja exposição foi confirmada (C.01). Contas/sessões seguem na 2.3, aberta. 2.1 permanece aberta até comprovar recarga dos consumidores/processo da aplicação; teste GET direto não comprova navegador nem servidor já iniciado. Evidência atual em tmdb-check.json e validation.md.

## Continuação autorizada — 26/10/2026

- 2.1: aplicação iniciada em produção com .venv na porta 3030 após compilação aprovada; primeira tentativa teve timeout de prerender, repetição sem alteração de código passou. Navegador público real comprovou três fileiras de filmes e uma de séries com 20 obras cada; reloaded-browser.json.
- 2.3 parcial: account-preview.json comprovou quatro logins históricos válidos de membros; account-rotation.json comprova quatro trocas de senha com login novo/identidade 200 e antigo 403. A.02 já retornava 403, sem troca. Dois tokens expostos retornam 401. Sessões emitidas antes da troca continuam 200, portanto a tarefa permanece aberta. Novas senhas somente em .local/credential-rotation/account-*.json; não versionadas.
- 3.1: tools/check_staged_secrets.py, quatro testes sintéticos aprovados; 818 arquivos do índice examinados, sem achados. Conteúdo novo/modificado conferido adicionalmente por verify_change_files.py, sem segredos conhecidos ou padrões detectados.
- 3.2: .xano/ acrescentado ao ignore; .env, .aws, .local e arquivos privados de substituição ignorados. Exemplos públicos sem valores reais; comandos e limites em prevention.md. Nenhum hook instalado.
- 4.1: compilação, navegador real, checks remotos de senhas/tokens e testes sintéticos separados em validation.md. Limitação de revogação de sessões registrada, sem alterar política de autenticação.
- 4.2: documentos centrais e P.1 reconciliados com o resultado e a única tarefa aberta. Change não pronta para arquivar; correção de política de sessões depende de planejamento próprio.

## Fechamento — dependência de sessões concluída

2.3 concluída pela change revogar-sessoes-apos-troca-senha: política publicada em 39 rotas autenticadas, tokens legados/anteriores rejeitados, outra conta preservada e recuperação isolada. Quatro contas existentes com senhas substituídas e acesso preservado; quinta identidade histórica confirmada ausente por leitura de metadados, sem apagar usuários. Evidências: ../revogar-sessoes-apos-troca-senha/remote-validation.json (29 checks), unusable-account-inspection.json, browser-validation.json e validation.md (392 testes locais). As marcações anteriores de pendência preservam as etapas históricas. Agora 9/9, sem commit/push ou arquivamento automático.
