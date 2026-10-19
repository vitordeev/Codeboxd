# Retorno à descoberta — 19/10/2026

Vínculo: P.13 em PENDENCIAS.md. Ajuste visual solicitado para fichas de filmes e
séries, que compartilham o componente de ficha com os demais tipos de obra.

Plano: substituir seta textual e link cinza por controle compacto arredondado,
superfície escura, borda discreta e ícone com destaque amarelo. Preservar semântica
de link e destino `/`, foco visível e área de toque mínima de 44px. Conferir
compilação e navegador em desktop/celular sem modificar dados remotos.

## Resultado

Implementação em `Codeboxd_main/pages/social.py` e `assets/codeboxd.css`: link com
ícone Lucide arrow-left decorativo, círculo amarelo discreto e borda arredondada.
Hover com contraste maior e pequeno movimento da seta, desativado quando o
usuário prefere movimento reduzido. Foco visível e destino `/` preservados.

- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado.
- `git diff --check` nos arquivos de implementação: aprovado.
- Edge headless, aplicação real em produção em http://localhost:3033: quatro
  verificações passaram. Controle mede aproximadamente 190×46px em 1440 e 390px,
  sem ultrapassar a viewport; foco visível e Enter retornando à descoberta.
- [Resultado estruturado](voltar-descoberta-browser-2026-10-19.json).
- Capturas locais inspecionadas: `.local/back-link-390-2026-10-19.png` e
  `.local/back-link-1440-2026-10-19.png`.

Sem testes unitários novos para este ajuste visual. Nenhuma escrita remota.
Instância de validação 3033 reiniciada; instância anterior 3000 não reiniciada.
