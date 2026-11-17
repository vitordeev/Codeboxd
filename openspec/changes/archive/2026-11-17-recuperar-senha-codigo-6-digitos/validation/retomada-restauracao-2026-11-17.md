# Retomada da restauração — 17/11/2026

Change selecionada por ter a menor pendência: 11/12, falta a restauração da tarefa 3.2.

## Investigação local

O ensaio de 12/11 comprovou recebimento, troca temporária, login novo e rejeição de senha/código/sessão anteriores. A falha posterior ocorreu na chamada POST `/reset/magic-link-login`, antes de obter a credencial de restauração e antes de qualquer escrita para restaurar. HTTP 403 sozinho não demonstra a causa: o relatório sanitizado não contém corpo/diagnóstico remoto suficiente. Não atribuir automaticamente a código errado, expiração ou permissão administrativa.

O executor atual suporta somente retomar um primeiro pedido ainda válido, com menos de 15 minutos e `restoration_needed=false`; não deve importar o relatório antigo de restauração pendente como se esse fosse o caso. Tampouco repetir o fluxo completo que cria outra senha temporária apenas para obter uma restauração.

## Próximo passo necessário

Atualização: usuário respondeu “permitido” à solicitação específica de restauração. Essa autorização substitui a recusa anterior somente para esta retomada: no máximo um novo pedido, restauração supervisionada e confirmação de login, sem repetir troca temporária.

Executor `tools/restore_recovery_account.py` implementado e janela privada aberta. Verifica primeiro se a senha desejada já funciona, confirmando `/auth/me` (ID e e-mail em memória) antes de dispensar novo pedido. Caso login rejeitado, exige código novo para uma única escrita e confirma login/identidade após a restauração. Evidência nova vinculada ao SHA-256 do ensaio anterior, sem alterar seu resultado histórico. Nenhuma senha/código/endereço é gravado na evidência; não há retries. Se escrita tiver resultado incerto, manter pendência e investigar sem repetir automaticamente.

Validação: seis testes novos com transporte simulado aprovados (restauração, senha já válida sem envio/escrita, código rejeitado, timeout sem retry, identidade divergente e entrada inválida sem rede), além dos 19 testes existentes do executor. Aguardando operação da janela e resultado real em `restauracao-autorizada-2026-11-17.json`; preparação/testes não concluem 3.2.

Estado real observado após operação da janela: senha desejada não aceita no login inicial; um único pedido novo aceito HTTP 200, `phase=awaiting_restore_code`, duas chamadas totais (login e solicitação), sem consumo de código ou escrita de senha até essa observação. O relatório preserva uma rejeição anterior de entrada local (`confirm_same_account_and_valid_matching_password`), que ocorreu antes da rede e não significa falha do pedido posterior aceito. Aguarda exclusivamente o novo código na janela privada, sem reenvio. Validação OpenSpec da change e `git diff --check` aprovados.

Validação local desta retomada: `.venv/Scripts/python.exe -m unittest discover -s tests -p test_recovery_acceptance.py -q`, **19 testes aprovados**, usando transporte simulado; não é nova validação real de restauração.

A autorização anterior de 17/11 cobria um único pedido para medir entrega, explicitamente sem trocar senha. O recebimento desse pedido não autoriza consumir seu código ou restaurar senha. Foi solicitada autorização específica para novo pedido e restauração da mesma conta em janela privada. A recusa histórica permanece válida para restauração até resposta explícita.

Após autorização: identificar a mesma conta privadamente, confirmar a senha que o usuário quer restaurar e sua política antes de consumir código, usar uma credencial nova de recuperação e confirmar login com a senha restaurada. Não copiar senha/código/token/endereço para evidências. Não obter código por acesso administrativo, reutilizar código expirado, contornar as guardas, repetir escrita/envio após timeout ou republicar contratos sem diagnóstico. Manter recibo sanitizado separado, vinculado ao ensaio original sem alterá-lo.

Se o usuário já restaurou a conta manualmente, uma confirmação dessa operação e de login pode ser registrada como evidência manual, distinguindo-a da execução automatizada; não assumir que ocorreu. Nenhuma operação remota, novo envio ou troca de senha nesta retomada. 3.2 permanece aberta.
