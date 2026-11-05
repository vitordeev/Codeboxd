# Validação — 05/11/2026

## Reprodução e correção

Instrumento `tools/media_detail_layout_browser.py`, CSS real do projeto e
markup fictício da ficha, sem Xano/provedores. Edge headless, quatro tipos
e placeholder em 320/390/640/1440px, título e descrição longos.

- `before.json`: 20 cenários, **15 reprovaram** por interseção da capa com texto
  nas três larguras móveis. Desktop aprovado.
- `after.json`: **20/20 aprovados**, sem interseção ou overflow horizontal.
- Screenshots antes/depois examinados em 390px, privados em
  `.local/project-final-20261105/layout-before` e `layout-after`.

Comando de reprodução (usar destinos novos para preservar histórico):

```
.venv/Scripts/python.exe -B -m tools.media_detail_layout_browser --output <novo-relatorio.json> --screenshots .local/<nova-pasta>
```

## Integração

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -q`: **494 testes OK**.
- `.venv/Scripts/python.exe -B -m reflex compile --dry`: aprovado, 58 unidades.
- Build de produção concluído em 23s; aplicação atualizada em porta 3030.
  Log privado `.local/project-final-20261105/app-updated.log`.
- Nenhuma publicação Xano, alteração de dados ou mudança de dependências por
  esta correção de CSS. As contas descartáveis da validação funcional pertencem
  à change de performance e serão limpas por seu journal.

A matriz usa conteúdo fictício para isolar geometria, não prova disponibilidade
de capas/metadados de provedores externos. Não substitui benchmarks ou teste
da recuperação por e-mail.
