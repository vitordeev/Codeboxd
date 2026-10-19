# Catálogos verticais e relevância da busca — 22/09/2026

## Problema reproduzido

A pesquisa real por `homen aranha` devolvia livros como `Provérbios 11`, `Provérbios 30` e `Uma Nova Criatura`, enquanto o TMDB não encontrava filmes com essa grafia. Com `homem aranha`, o TMDB encontrava os títulos corretos, mas a busca ampla da Open Library ainda incluía livros sem relação. A home mostrava os populares em prateleiras horizontais.

## Correção

- Populares em grades verticais: cinco colunas no desktop, três em telas intermediárias e duas no celular. Mantidos 20 filmes e 20 séries iniciais. “Carregar mais filmes/séries” acrescenta páginas abaixo, na própria seção, sem remover a outra.
- Consulta de livros pelo campo `title`, conforme a [documentação da Open Library](https://openlibrary.org/dev/docs/api/search), incluindo títulos das edições para preservar traduções relevantes.
- Normalização explícita da grafia comum `homen` → `homem` na consulta aos provedores, sem alterar o texto visível digitado.
- Correspondência de todas as palavras significativas com o título, título original ou de edição; normalização de acentos, caixa e pontuação, prefixos e tolerância limitada a pequenas diferenças. Títulos exatos vêm primeiro. Autoria, assunto e descrição não qualificam um resultado sozinhos.
- A mesma regra vale para dados do catálogo salvo e páginas adicionais. Livros relacionados continuam aparecendo; não existe bloqueio por tema religioso ou por categoria.

## Evidências

- 61 testes Python passaram, incluindo relevância, títulos originais/traduzidos, erro de grafia, preservação de livros relacionados, paginação vertical, deduplicação e repetição de página após falha de provedor.
- Compilação Reflex e validação OpenSpec passaram.
- Edge headless na instância de produção `http://localhost:3013`: seções iniciais com 20 cards distribuídos em várias linhas, sem rolagem horizontal; “Carregar mais filmes” passou para 40 e preservou os 20 de séries.
- Celular de 390 pixels: duas colunas e conteúdo continuando para baixo, sem overflow horizontal da página.
- `homen aranha` e `homem aranha` retornaram 37 títulos relacionados, incluindo filmes, séries e livros. Nenhum dos livros bíblicos sem relação apareceu. Listas completas e avisos estão no JSON abaixo.
- Nenhuma exceção JavaScript na rodada final.

Arquivos: [script de browser](discovery_relevance_browser.py), [resultados do browser](vertical-relevance-browser-results.json), [testes locais](vertical-relevance-unit-results.txt). Testes automatizados: `tests/test_search_relevance.py`, `tests/test_discovery.py`. Capturas locais: `.local/vertical-home-desktop.png`, `.local/vertical-home-mobile.png`, `.local/spiderman-search-desktop.png`.

```powershell
venv\Scripts\python.exe -m unittest discover -s tests -q
venv\Scripts\reflex.exe compile --dry
openspec validate definir-fundacao-codeboxd --type change
venv\Scripts\python.exe openspec\changes\definir-fundacao-codeboxd\validation\discovery_relevance_browser.py
```

## Limites

Jikan ficou indisponível nas duas pesquisas reais; o aviso de anime permaneceu visível, e as outras fontes responderam. A validação não comprova disponibilidade contínua dos provedores. A correção automática de grafia é limitada à palavra documentada; não constitui um corretor ortográfico universal. Este registro substitui o comportamento de prateleiras horizontais descrito na rodada anterior.
