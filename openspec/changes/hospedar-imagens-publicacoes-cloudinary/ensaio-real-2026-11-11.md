# Ensaio real Cloudinary — 11/11/2026

## Autorização e execução

Usuário respondeu `prossiga` à prévia específica de um upload de PNG sintético
2×2, recuperação por HTTPS e exclusão somente do próprio arquivo. Executor
`tools/cloudinary_acceptance_probe.py`, na branch
`task/cloudinary-limites-20261111`, configuração privada da raiz, flag do app false.
Nenhuma chamada Xano, publicação, usuário ou arquivo existente foi envolvido.

Comando executado uma única vez:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.cloudinary_acceptance_probe --execute --approval-reference 'usuario-prossiga-ensaio-descartavel-20261111' --config 'D:/Repositorios GIT/Codeboxd/.env' --output .local/cloudinary-acceptance-20261111.json
```

O journal privado contém a referência exata do asset para reconciliação; não
publicar esse arquivo nem credenciais. Esta evidência omite URL/identificadores.

## Resultados comprovados

| Etapa | Resultado |
| --- | --- |
| Upload assinado sem sobrescrita | HTTP 200, identidade e metadados do asset próprio confirmados |
| Recuperação HTTPS | HTTP 200, bytes idênticos ao PNG enviado |
| Limpeza do asset próprio | HTTP 200, `result=ok` do provedor |
| Resultado do executor | `passed=true`, saída 0 |
| Chamadas ao Xano | Zero |
| Repetições de escrita | Zero |

SHA-256 da imagem sintética enviada e recuperada:
`27ce4cd0859ffa137ec951b62df9ba8c19d37ac07d2c166a4ab6a2a3be1e9ae8`.
O resultado confirma limpeza na API; invalidação de CDN/backups não foi verificada
e não deve ser inferida como imediata. A igualdade dos bytes confirma que este
arquivo sintético não sofreu alteração; não é aceite visual do feed.

## Limites e continuidade

Preparação continua **3/5**. O ensaio usa um executor independente, não o fluxo
de posts nem o adaptador de produção. Não comprova persistência Xano, autoria,
substituição, exclusão integrada ou renderização no navegador. Tarefas 2.1/2.2
continuam abertas; configuração/processo do app não foram alterados.

Próxima etapa: detalhar contrato aditivo de metadados e prova de autoria do asset,
implementar integração e regressões locais preservando imagens legadas e
reconciliação de falhas incertas. Publicação Xano e ensaio de publicações exigem
prévia e autorização próprias; esta autorização cobre somente o PNG deste teste.

Validações locais da ferramenta: 13 testes Cloudinary já aprovados (sete do
adaptador e seis do executor). Após registrar esta evidência, validar a change
OpenSpec e conferir o diff; nenhum produto foi alterado por esta rodada.
