# Design

## Context

Ver proposal.md para motivação. P.1 e a change arquivada corrigir-erros-operacionais registram exposição histórica; não comprovam revogação. Nesta rodada foram conferidos git status, lista de changes, propostas ativas e contrato operational-reliability; nenhum valor secreto foi inventariado ou rotacionado.

Consumidores incluem Python/Reflex, Xano e ferramentas locais. TMDB fornece filmes/séries, Kitsu animes e Open Library livros; DeepL é opcional e Resend atende recuperação. Identidades legadas Jikan permanecem inalteradas. Não presumir que todos esses serviços tiveram exposição.

## Goals / Non-Goals

**Goals:** rastrear cada ocorrência até revogação comprovada, preservar dados e operar com .venv sem Docker.

**Non-Goals:** reescrever histórico, force-push, apagar contas, mudar autenticação funcional ou hospedar o projeto.

## Decisions

1. Inventário primeiro: registrar identificador opaco, nome da variável/categoria, provedor, referências de arquivo/commit quando seguras, consumidor e evidência pendente. Examinar conteúdo por processamento local com saída sanitizada; não despejar arquivos privados ou git show bruto em ferramentas. Inventariar apenas referências disponíveis e explicitar cobertura. URLs públicas não são segredos por definição.
2. Prioridade pelo privilégio e alcance: administração/infraestrutura, contas privilegiadas e depois integrações expostas. Inspecionar escopos e uso antes de trocar. Limpar Git primeiro não revoga cópias já obtidas e foi descartado como contenção principal.
3. Rotação por serviço: preparar substituto com menor escopo suficiente, atualizar consumidores privados e validar operação e revogação; exposição com abuso ativo exige revogação imediata. Não colocar chaves na linha de comando, artefatos ou logs. Acesso aos painéis e limitações de cada serviço serão levantados na execução; documentar passo manual quando necessário.
4. Contas: usar identificadores opacos na documentação, trocar senhas e verificar sessões/tokens antigos. Não presumir que mudar senha invalida tokens Xano; confirmar mecanismo e manter a tarefa aberta se não houver comprovação.
5. Prevenção: verificador local reproduzível do conteúdo preparado para commit, incluindo arquivos privados conhecidos e padrões de segredos; saída limitada a arquivo/localização e regra. Usar fixtures sintéticas para detectar vazamento na própria saída. Não introduzir dependência externa sem necessidade demonstrada; limites heurísticos serão documentados. Histórico antigo é inventário separado e não torna a verificação atual permanentemente inválida.

## Risks / Trade-offs

- Troca incompleta interrompe integrações → mapear consumidores e verificar cada um, incluindo configuração Xano quando aplicável.
- Segredo aparece durante auditoria → sanitizar antes da saída e não persistir cópias dos valores no OpenSpec.
- Ferramenta heurística omite formatos → registrar cobertura e complementar com inventário por serviço.
- Acesso externo ausente → manter tarefa aberta com procedimento e evidência requerida.
- Revogação é irreversível → recuperar serviço emitindo outra credencial válida; nunca reativar segredo exposto.

## Migration Plan

Inventariar; definir ordem por risco; executar rotações e tratamento de contas; verificar integrações e invalidação; adicionar prevenção; reconciliar P.1 e registrar evidências locais/remotas separadas. Consultar documentação oficial atual de cada provedor antes de ações remotas. Não executar envio de e-mail, escrita em dados ou teste destrutivo como smoke incidental. Restaurar apenas configuração não secreta em rollback; credencial revogada é substituída por outra nova.

## Open Questions

- Quais credenciais e contas ainda estão válidas e quais consumidores as utilizam?
- Quais painéis e mecanismos de revogação estão acessíveis nesta sessão de execução?

Essas respostas refinam o inventário e a ordem operacional sem alterar o escopo.
