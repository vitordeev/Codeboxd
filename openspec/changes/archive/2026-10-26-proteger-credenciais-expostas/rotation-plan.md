# Classificação e ordem de rotação — 26/10/2026

## Evidência atual

Atualização posterior nesta data: usuário salvou substituto no .env; verificação remota comprovou novo token diferente e aceito (200), anterior rejeitado (401), filmes e séries com resultados (200). A rotação/revogação C.01 está comprovada; a recarga do processo da aplicação e as contas Xano continuam pendentes. Os itens abaixo preservam a linha de base anterior à troca.

- `tmdb-check.json`: GET oficial `/3/authentication` retornou 200 e success=true para o token atual, idêntico ao histórico. Exposição e validade remota confirmadas; nenhuma rotação realizada.
- `access-audit.json`: consulta Metadata API GET na instância do projeto retornou 200. A.01, A.04 e A.05 têm identidade correspondente ao registro histórico, papel member e status active. A.02/A.03 não têm ID numérico nos artefatos, portanto não houve leitura de seus registros ou enumeração ampla de usuários. Esses rótulos seguem a ordem dos registros extraídos pelo auditor; não são IDs do banco.
- O perfil CLI padrão recebeu 403; inspeção local confirmou que ele pertence a outra instância. O auditor foi corrigido para selecionar exclusivamente o único perfil cujo instance_origin corresponde ao host configurado do projeto. A consulta bem-sucedida usa esse perfil, sem alterar as credenciais CLI.
- A credencial de gerenciamento Xano está fora do repositório, em configuração CLI privada. Sua existência e autorização de leitura foram confirmadas; não se presume exposição dessa credencial, escopo de escrita ou acesso ao painel.

## Sequência e critérios por item

| Ordem | Item | Acesso necessário | Ação e critério de validação |
| --- | --- | --- | --- |
| 1 | C.01, TMDB | Conta emissora, configurações API; acesso ainda não confirmado pelo usuário | Obter substituto e revogar o exposto pelo mecanismo disponível no painel; se não houver opção, solicitar revogação ao suporte. Atualizar apenas TMDB_READ_TOKEN no .env privado. Verificar novo aceito e antigo 401; conferir filmes/séries. Não considerar emissão de outra chave como prova de revogação. |
| 2 | C.02/C.03, contas Xano | Gerenciamento da instância com capacidade de alterar senha e examinar as duas identidades ainda sem ID | Confirmar papéis restantes; qualquer admin identificado passa à frente. Trocar senhas de forma individual, entregar/guardar substitutos em canal privado e verificar rejeição das senhas antigas e acesso legítimo. Não excluir contas ou dados. |
| 2, junto às contas | C.03, sessões Xano | Mecanismo de revogação confirmado ou verificação de expiração no ambiente real | Não presumir invalidação pela troca de senha. O contrato local login/signup emite tokens de 86400 segundos, extras vazio, e update_password apenas altera o campo password. Não há etapa explícita de revogação nesse contrato. Expiração e eventual mecanismo do serviço precisam de evidência antes de fechar 2.3. Mudança de esquema ou política de autenticação exige revisar o design antes de implementar. |
| 3, sem rotação obrigatória demonstrada | C.04/C.05, DeepL/Resend | Contas emissoras e configuração privada Xano caso nova exposição seja encontrada | Não foi confirmada exposição dos valores atuais. Preservar e monitorar; se houver motivo para rotacionar, mapear Python e ambiente Xano, atualizar ambos quando aplicável e comprovar revogação. Não enviar e-mail como teste incidental. |
| Investigação complementar | C.06, literais candidatos | Contexto dos scripts/fixtures | Não rotacionar todos os literais heurísticos como se fossem contas reais. Manter classificação de candidatos, inclusive senhas de exemplos/testes e frontend gerado, sem alegar ausência de outros segredos. |

## Consumidores

- TMDB: `services/catalog.py` lê TMDB_READ_TOKEN; ferramentas de browser também consultam a variável. Alterar .env não atualiza automaticamente processos Python já iniciados; reinício validado da aplicação deve seguir a skill de processos Reflex quando houver troca.
- DeepL: `services/translation.py` lê DEEPL_API_KEY.
- Resend: `tools/deploy_recovery_resend.py` lê .env e configura ambiente Xano; endpoint `request_reset_link_GET.xs` referencia variável do workspace. A ferramenta histórica pressupõe uma única credencial CLI, mas existem dois perfis nesta máquina; não executá-la como parte desta rotação.
- Contas históricas: artefatos são de testes de autenticação; nenhum processo dependente das cinco senhas foi confirmado. Não restaurar os JSON privados removidos em diretórios versionados.

## Como verificar TMDB após troca privada

```powershell
.venv/Scripts/python.exe -B openspec/changes/proteger-credenciais-expostas/check_tmdb_credential.py
```

O verificador lê o token atual do .env e o exposto do blob histórico somente em memória. Consulta apenas o domínio oficial TMDB, sem redirects; persiste somente igualdade, HTTP e resultado booleano. `rotation_verified` exige tokens diferentes, novo autenticado e exposto com 401. A prova inicial atual é false.

## Fontes oficiais consultadas

- [TMDB: autenticação de aplicação](https://developer.themoviedb.org/docs/authentication-application): token de leitura nas configurações API da conta e uso como Bearer. A página não comprova um procedimento universal de regeneração; verificar painel atual.
- [TMDB: validar chave](https://developer.themoviedb.org/reference/authentication-validate-key): GET /3/authentication, respostas 200/401.
- [Xano: Metadata API](https://docs.xano.com/xano-features/metadata-api): acesso condicionado a papéis, permissões e escopos do token.
- [Xano: autenticação](https://www.xano.com/learn/all-about-authentication-in-xano/): validade configurável e extras; não é prova de revogação por troca de senha.

## Limites

Somente consultas GET remotas foram executadas, sem login com senhas históricas, envio de e-mail ou alteração de dados. Não foram comprovadas permissões de escrita, rotação ou revogação. O acesso à conta TMDB foi solicitado por pergunta assíncrona e ainda não foi confirmado. Tarefas 2.1–2.3 continuam abertas.
