# Descoberta, cards e busca geral — 22/09/2026

## Mudanças

- Busca textual sempre consulta filmes, séries, animes e livros, independentemente da categoria usada antes. Botões de categoria ficam separados do formulário e abrem catálogos navegáveis.
- A home usa a página completa dos populares: 20 filmes e 20 séries verificados no TMDB, em vez do corte anterior em 10 de cada. “Ver mais” abre a categoria e “Carregar mais resultados” acrescenta páginas sem duplicar identidades.
- A paginação preserva o termo efetivamente enviado, mesmo após editar o campo sem enviar outra pesquisa. Uma falha parcial não impede a exibição de resultados das outras fontes.
- Cards reservam proporção 2:3 para as capas, com carregamento lazy e alternativa para URL ausente ou imagem com erro. Banners usam a imagem horizontal quando disponível.
- Consultas iniciais de populares e comunidade executam em paralelo. Uma seção popular que falhou pode ser tentada novamente na próxima carga, mesmo quando a outra já carregou.
- Resultados de busca não aparecem misturados aos cards da comunidade. Busca sem resultados permanece na área de resultados.

## Verificação

| Verificação | Resultado |
| --- | --- |
| Suíte Python completa | 54 testes passaram, incluindo 6 novos testes de descoberta |
| Reflex compile --dry | Passou |
| OpenSpec validar definir-fundacao-codeboxd | Passou |
| Home no Edge headless | 20 filmes e 20 séries |
| Capa real e falha HTTP 404 controlada | Imagem carregou; falha mostrou alternativa sem mudar a altura do card |
| Botão Filmes e carregar mais | Categoria abriu com 22 itens (20 do provedor e 2 do catálogo salvo); próxima página aumentou a quantidade |
| Pesquisa Batman após selecionar Filmes | Retornou filmes e outros tipos de mídia; cards da comunidade não aparecem na pesquisa |
| Viewports 1440 e 390 pixels | Sem overflow horizontal da página |
| Exceções JavaScript da rodada final | Nenhuma |

Saídas: [testes Python](discovery-unit-results.txt), [compilação](discovery-compile-results.txt), [browser](discovery-browser-results.json). Testes reproduzíveis em `tests/test_discovery.py` e [discovery_browser.py](discovery_browser.py).

```powershell
venv\Scripts\python.exe -m unittest discover -s tests -q
venv\Scripts\reflex.exe compile --dry
openspec validate definir-fundacao-codeboxd --type change
venv\Scripts\python.exe openspec\changes\definir-fundacao-codeboxd\validation\discovery_browser.py
```

O teste de browser exige a versão atual em `http://localhost:3013` e acesso aos provedores. A instância foi iniciada em produção com `reflex run --env prod --single-port --frontend-port 3013`. Log local: `.local/discovery-production.log`. Capturas: `.local/discovery-fixed-desktop.png` e `.local/discovery-fixed-mobile.png`; a capa ausente do primeiro card na captura desktop é a falha 404 provocada pelo teste.

## Limites e diagnóstico das tentativas

O sandbox inicialmente bloqueou o acesso aos provedores e às imagens; as verificações finais usaram acesso de rede autorizado. Uma simulação inicial de evento de erro com propagação indevida acionou `window.onerror` do Reflex; o teste foi corrigido para gerar uma resposta de imagem HTTP 404, como ocorre em uso real. Também foi ajustada a espera das asserções de browser para carregamento externo.

As verificações confirmam busca geral e resultados de tipos diferentes; não comprovam disponibilidade contínua de todos os provedores nem a existência de capa para todo título. A falha de uma fonte continua exibindo aviso. Nenhuma credencial foi adicionada a estes arquivos, e nenhuma alteração foi publicada no backend.
