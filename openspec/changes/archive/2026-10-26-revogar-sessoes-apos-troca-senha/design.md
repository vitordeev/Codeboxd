## Context

Ver proposal.md e evidências de proteger-credenciais-expostas: quatro senhas rotacionadas, mas sessões anteriores ainda 200. O usuário autorizou continuar até finalizar e fará commit/push manualmente. Esta é uma dependência de implementação daquela change, conduzida pelo workflow apply, não uma rodada restrita a proposta.

## Goals / Non-Goals

Invalidar tokens anteriores após troca de senha em todas as APIs autenticadas sem alterar papéis, ownership ou dados sociais. Não criar refresh tokens, apagar contas, modificar logout global, usar Docker ou reescrever Git. Provedores TMDB/Kitsu/Open Library/DeepL/Resend e identidades legadas Jikan permanecem inalterados.

## Decisions

- user.session_version inteiro com default zero; leituras antigas nulas equivalem a zero. Tokens recebem session_version e purpose=session ou password_reset. Tokens sem claims válidas são rejeitados; não há janela de compatibilidade que permita sessões expostas.
- Função compartilhada compara versão estrita, conta ativa e finalidade. Cada query auth=user a chama no início; recuperação só é admitida no endpoint de alteração de senha. As verificações originais de papel/propriedade continuam em seguida. Custo: uma leitura adicional da conta por chamada protegida, sem round-trip HTTP adicional no cliente.
- Alteração de senha usa transação, bloqueia a linha por edição, relê versão e revalida a credencial sob bloqueio antes de salvar senha/versão+1. Evita que dois usos da mesma credencial ganhem atualizações concorrentes. Login captura a versão da leitura usada na checagem de senha, portanto corrida com reset produz token antigo e rejeitável.
- Recuperação captura a versão da conta sob a transação de consumo do código, preservando cooldown, tentativas, envio Resend e uso único existentes. Não ler versão nova após o consumo para promover credencial antiga.
- Publicação deve partir do export remoto sem env/records, fazer delta por GUID/nome e preservar modificações remotas de outras changes. Só user, função nova e queries relacionadas podem mudar; sem delete. Backup privado local e dry-run com lista de operações, sem expor respostas/segredos.

## Risks / Trade-offs

- Tokens legados deixam de funcionar → comunicar necessidade de novo login, publicar emissores/guardas de forma coordenada e validar duas contas.
- Parser/contrato Xano divergente → validar dry-run e export publicado; nunca tratar arquivo local como publicação.
- Rate limit → consultas espaçadas; não repetir automaticamente mutações em falha de rede, preservar estado privado e evidência.
- Regressão de dados → comparar contagens/referências e testar negação antes de mutações com payload inválido.

## Migration Plan

Inventariar rotas autenticadas remotas; gerar patch mínimo e testes; export/dry-run; publicar delta revisado; validar tokens legados, login novo, troca, token anterior rejeitado, outra conta preservada, papel/ownership e finalidade de recuperação. Usar contas de teste já autorizadas, sem criar contas incidentalmente. Novas senhas/tokens só em .local privado; resultados sanitizados no OpenSpec.

Rollback operacional preserva coluna aditiva e dados. Não restaurar aceitação de tokens expostos: corrigir e republicar guardas/emissores; em indisponibilidade, manter rejeição de credenciais inseguras. Backups são evidência para reparo revisado, não comando de restauração global.

## Sources

[Xano: auth extras](https://www.xano.com/learn/all-about-authentication-in-xano/), [transações](https://www.xano.com/learn/database-transaction/), documentação/contratos Xano atuais e validação de parser na instância.
