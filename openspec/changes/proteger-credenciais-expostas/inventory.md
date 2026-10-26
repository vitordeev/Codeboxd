# Inventário inicial de credenciais — 26/10/2026

Este documento registra a linha de base anterior à rotação. O [resultado atual](status.md) comprova a troca TMDB, quatro senhas substituídas e a pendência de sessões; os resultados iniciais abaixo são preservados como histórico.

## Resultado

Inventário local concluído para a cobertura abaixo. Nenhuma credencial foi trocada, revogada ou testada contra serviço remoto. A pendência P.1 permanece aberta. Valores, identidades pessoais e fingerprints de segredos não fazem parte destes artefatos.

| ID | Categoria | Localização e consumidor | Evidência e situação |
| --- | --- | --- | --- |
| C.01 | TMDB_READ_TOKEN | `.env` atual; histórico `.env`, blob `dd4d283d89a38472f23fab38fd757a6407a09497`, linha 5; consumidor `Codeboxd_main/services/catalog.py` | Correspondência exata entre valor atual e histórico. Exposição confirmada; validade e revogação não verificadas. Prioridade de rotação entre os serviços identificados. |
| C.02 | Senhas de contas de teste Xano | Quatro JSON históricos em `.local/`, relacionados em account-triage.json; consumidores históricos de validação de autenticação | Cinco registros com senha e cinco identidades de e-mail distintas, sem publicar identidades. Não há papel explícito nesses JSON; privilégios e existência atual não verificados. Os quatro caminhos já não existem localmente e não estão no índice. |
| C.03 | Tokens de sessão de contas de teste | `.local/test-accounts.json` histórico, blob `dc8495ee35530ca53b9c3b98985b89ff2169e376`; consumidor histórico de validação | Dois campos de token não vazios, com padrão JWT encontrado nesse arquivo. Validade, expiração e invalidação não verificadas. Tratar junto de C.02, sem presumir que troca de senha invalida sessão. |
| C.04 | DEEPL_API_KEY | `.env` atual; consumidor `Codeboxd_main/services/translation.py` | Configurada localmente. Nenhuma correspondência exata do valor atual no histórico textual examinado. Exposição histórica não confirmada; isso não comprova ausência de exposição fora da cobertura. |
| C.05 | RESEND_API_KEY | `.env` atual; ferramenta `tools/deploy_recovery_resend.py`; referência em `xano/api/authentication/reset/request_reset_link_GET.xs` | Configurada localmente. Nenhuma correspondência exata do valor atual no histórico textual examinado. Configuração real do provedor/Xano não foi consultada. |
| C.06 | Outros literais candidatos | Scripts, testes e frontend gerado históricos, com localizações em inventory.json | Padrões heurísticos de password incluem fixtures, código e possíveis dados de execução; não classificar todos como contas reais. Triagem adicional por contexto permanece para 1.2. |

O commit `aed4810` contém os arquivos privados conforme evidência histórica, e permanece contido nas referências locais `origin/main` e `origin/develop`. `git log --all -- .env` retorna também `669b95c`. Essas referências locais não comprovam o estado remoto atual.

## Cobertura reproduzível

- Histórico alcançável pelas referências locais: 67 commits, clone não raso e 1.444 blobs únicos; 1.248 blobs textuais examinados, 196 ignorados por conteúdo binário ou tamanho superior a 2 MB. O caminho por blob é representativo, não uma enumeração de todas as ocorrências por commit.
- Índice: 662 blobs textuais examinados, 156 ignorados pelo mesmo critério. Nenhuma correspondência dos três segredos atuais foi encontrada no índice. Literais candidatos em testes não equivalem automaticamente a segredos reais.
- Árvore atual: 678 arquivos textuais examinados, 151 ignorados por binário/tamanho; seis arquivos do primeiro nível de `.local` examinados e dois binários ignorados. `.env` foi lido apenas em memória para comparação.
- `.env`, `.aws/credentials` e `.local/` têm regras de ignore confirmadas; isso não prova existência do arquivo AWS nem elimina o histórico. Não foi identificado acesso AWS/GitHub por padrão na cobertura textual; não é atestado de ausência.
- Excluídos ambientes/dependências, diretórios gerados atuais, uploads, imagens de referência, `.states` e árvores internas de build em `.local`. Backups Xano aninhados fora do glob do auditor não foram examinados. Não foi feito fetch, leitura de reflogs/objetos inalcançáveis, arquivos fora do repositório, painéis, CI remoto ou configuração remota Xano.
- O detector busca padrões JWT, AWS, GitHub, Resend, DeepL, chaves privadas e literais de senha, além de comparação exata dos segredos atuais do `.env`. Não detecta todos os formatos, valores fragmentados, codificados ou segredos antigos sem padrão reconhecido.

## Evidências e execução

```powershell
.venv/Scripts/python.exe -B openspec/changes/proteger-credenciais-expostas/audit_inventory.py
.venv/Scripts/python.exe -B openspec/changes/proteger-credenciais-expostas/audit_triage.py
```

`inventory.json` guarda somente categorias, variáveis, locais e referências de objetos Git. `account-triage.json` registra contagens de campos, sem valores. A triagem também verifica que os valores conhecidos de segredos e identidades extraídos não aparecem nos artefatos da change; resultado aprovado. A checagem cobre valores conhecidos, não todo possível dado sensível.

## Próximo passo

Executar 1.2: confirmar privilégios das contas e consumidores adicionais, especialmente configuração Xano, e preparar a sequência de rotação. C.01 exige substituição porque o valor configurado coincide com o exposto; contas privilegiadas eventualmente identificadas em C.02/C.03 podem ter precedência por risco. Não reescrever o histórico antes de tratar os acessos expostos. A validade remota não foi testada nesta rodada.
