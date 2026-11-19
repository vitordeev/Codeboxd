# Aceite incremental de dados dos carrosséis — 11/11/2026

Branch `task/ui-rails-acceptance-20261111`, base origin/develop `7d32dc2`.
Continuação autorizada da task 3.3; nenhuma alteração funcional do aplicativo.
A worktree de UI foi reutilizada limpa, mantendo os commits anteriores e as
worktrees de performance/Cloudinary preservados.

## Alterações e resultados

A fixture anterior devolvia os mesmos 12 itens para qualquer página. Ela agora
mantém a página inicial idêntica, fornece IDs distintos na página 2 e esgota na
página 3. Isso permite testar o comportamento real de `more_popular` sem chamar
provedores. O módulo continua bloqueando HTTP externo no backend.

Nova ferramenta `tools/ui_rails_data_browser.py`, executada no Edge headless
contra a fixture Reflex em produção na porta 3036, com quatro cenários aprovados
em **320, 390, 768 e 1440 CSS px**:

- Home inicia com 12 cards de filmes; End/rolagem não acrescenta itens.
- Carregar mais acrescenta outros 12, sem duplicação e preservando ordem/títulos da primeira página.
- A coleção de séries permanece intacta.
- A terceira consulta esgota os resultados, oculta o botão e conserva 24 cards.
- Foco revela o primeiro card; uma falha real de transporte da imagem remove a imagem, conserva o título e mantém a altura do card (tolerância 1px).
- Enter continua abrindo a ficha; documento sem overflow horizontal e zero erros JavaScript nos quatro cenários.

Resultados: [JSON de execução](carrosseis-dados-2026-11-11.json).
O servidor realizou compile e build de produção com sucesso. Não houve nova
execução da suíte completa; os 632 testes da integração anterior são históricos.
A primeira tentativa da ferramenta comparava innerText com textContent,
misturando título e placeholder; essa asserção foi corrigida para comparar o
título h3. A falha inicial e logs permanecem privados em `.local`.
O servidor registrou avisos de delta para cliente desconectado ao encerrar
contextos; os quatro cenários terminaram com exit 0. OpenSpec estrito, sintaxe
Python e `git diff --check` aprovados. Fixture encerrada após o ensaio; a
instância do usuário não foi reiniciada.

Como a fixture compartilha a URL de capa entre obras, o cache de falha existente
atinge essas capas compartilhadas; não foi simulado um asset real de usuário.
O browser só permite localhost e responde capas fictícias com o PNG existente;
os demais hosts são bloqueados. Sem Xano real, uploads, exclusões ou ativação
Cloudinary. Não foram usadas novas referências visuais.

## Limites e continuação

**3.3 permanece aberta:** os casos de carregar mais/falha de capa agora estão
comprovados, mas falta a comparação quantitativa DOM/requests com baseline
equivalente. Esta rodada não mede tempos, bytes ou chamadas do backend real.
**3.2 permanece aberta:** nenhum aparelho físico foi utilizado. Não há aumento
da contagem global: UI/UX continua **3/26**.

Para repetir, iniciar explicitamente `tools.ui_foundations_fixture` conforme o
[procedimento anterior](fundamentos-carrosseis-2026-11-11.md) e executar:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.ui_rails_data_browser
```

A ferramenta escreve `.local/rails-data-result.json`; preserve o arquivo anterior
antes de uma repetição. Não executar contra um servidor com dados reais.
