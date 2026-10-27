# Proxy de medição: rejeição local — 27/10/2026

Retomada autorizada pelo usuário para trabalhar nas changes restantes.
Vínculo: instrumento existente da tarefa 1.2 e validação integrada 9.1/9.2.

## Plano antes da edição

Suíte completa falhou duas vezes na rejeição de POST pelo proxy somente de
leitura, com WinError 10053; arquivo isolado passou (10 testes). O handler fecha
a conexão sem consumir o corpo bloqueado, o que pode causar reset TCP no
Windows. Ajuste limitado a `tools/read_only_journey_browser.py`: consumir corpo
de tamanho válido até 8192 bytes antes de responder 403, com timeout curto;
continuar bloqueando antes de qualquer chamada ao serviço. Não encaminhar,
persistir ou interpretar rascunhos. Fechar conexão explicitamente na resposta.

Validar os testes existentes de bloqueio antes da rede, ausência de payload no
relatório, cookies, orçamento e 429; repetir suíte completa após o reparo.
Nenhum servidor do aplicativo reiniciado, publicação ou mudança de produto.
Rollback: reverter somente o tratamento de resposta bloqueada do instrumento.
Manter 14/37 até os critérios amplos das tarefas serem comprovados.

## Resultado

Ajuste implementado no instrumento. Suíte completa:
`.venv/Scripts/python.exe -B -m unittest discover -s tests -q`: **413 testes
aprovados** em 20,742 s. Inclui bloqueio de mutação antes da rede e verificação
de ausência de rascunho no relatório. Não prova ausência universal de
intermitência TCP; a regressão observada passou na suíte que antes falhava.
Nenhum arquivo Reflex, build ou processo normal do app foi alterado.
