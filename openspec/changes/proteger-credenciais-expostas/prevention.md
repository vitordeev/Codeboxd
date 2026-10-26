# Prevenção de novos segredos em commits

Antes de cada commit, executar com o Python da .venv:

```powershell
.venv/Scripts/python.exe -B tools/check_staged_secrets.py
```

O comando lê os blobs do índice Git, não os arquivos modificados depois de git add. Não modifica o índice nem faz chamadas de rede. Retorna 0 se aprovado, 1 se houver achado e 2 em erro de execução. A saída contém apenas caminho sanitizado, regra e linha quando aplicável, nunca trechos ou valores encontrados. Arquivos removidos do índice não são examinados como adições.

Para verificar todo o índice, incluindo arquivos sem alteração preparada:

```powershell
.venv/Scripts/python.exe -B tools/check_staged_secrets.py --all-index
```

Nenhum hook foi instalado automaticamente: é uma verificação manual reproduzível. Deve ser repetida depois do último git add; um resultado anterior não cobre conteúdo preparado depois. Não desabilitar uma regra para aceitar um segredo real.

## Cobertura e limites

- Rejeita arquivos .env privados, diretórios .aws/.xano/.local, ambientes e gerados conhecidos.
- Detecta padrões de tokens JWT/JWE parciais, AWS, GitHub, Resend, DeepL e chaves privadas; compara também os valores secretos configurados no .env privado, inclusive em blobs binários.
- Exemplos .env.example e production.env.example são permitidos como caminhos, mas continuam tendo o conteúdo examinado; devem ter placeholders ou valores públicos. URLs Xano públicas não são segredos por definição.
- Não é prova de ausência de todo segredo: formatos desconhecidos, fragmentação e dados fora do índice exigem inventário e revisão. Submódulo ou índice com conflito produz falha explícita em vez de aprovação sem cobertura.
- O histórico exposto permanece histórico; segredos de serviço revogados não são restaurados. Não executar reescrita Git ou force-push por causa deste verificador.
- As novas senhas de teste ficam somente em .local/credential-rotation/account-*.json, ignoradas pelo Git. Não mover esses arquivos para a change nem copiar valores para relatórios.

## Evidências

Quatro testes sintéticos em tests/test_staged_secrets.py verificam padrões, ausência de valores na saída, detecção em binário, sanitização de caminho, placeholders e a diferença entre índice e árvore de trabalho, incluindo remoções. Execução documentada em validation.md. A primeira verificação completa leu 818 arquivos do índice sem achados; os novos arquivos não rastreados exigem verificação adicional antes de um futuro commit.
