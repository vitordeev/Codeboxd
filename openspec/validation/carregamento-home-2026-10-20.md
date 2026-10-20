# Carregamento progressivo da homepage — 20/10/2026

Complemento ativo de descoberta/confiabilidade operacional. Pedido: reduzir
espera ao recarregar e exibir conteúdo necessário mais cedo.

- [x] Identificar espera conjunta de todos os provedores e consultas repetidas.
- [x] Publicar atualizações parciais de destaque/fileiras durante o carregamento.
- [x] Separar limites de concorrência por provedor.
- [x] Adicionar cache público limitado, com expiração e cópias independentes.
- [x] Verificar regressões, compilação e tempos no navegador.

Cache restrito ao catálogo público; autenticação, contas e dados sociais não
participam. Manter seleção de séries, destaque recente e comportamento de falhas.

Implementação: evento de visita envia atualizações conforme os resultados chegam;
limites separados para TMDB (2), livros (2) e animes (1), evitando que um provedor
ocupe todas as vagas. Cache público de cinco minutos/128 entradas por processo,
com chave por URL/parâmetros/credencial usando hash, sem armazenar erros e com
cópias profundas para impedir mutação cruzada. Kitsu mantém seu cache existente.
Tarefas pendentes são canceladas se a atualização for interrompida.

Validação local: 158 testes passaram, incluindo expiração, cópias independentes,
isolamento por credencial, não cachear erros e atualização antes de uma coleção
lenta terminar. Compilação Reflex `--dry` e diff sem erros passaram.

Medição Edge headless, mesmo servidor local e script `.local/measure_home.py`:

| Cenário | Antes | Depois |
| --- | --- | --- |
| Primeira visita: título do destaque visível | 26,38 s | 10,94 s |
| Primeira visita: categorias habilitadas | 26,42 s | 15,32 s |
| Recarregar: título do destaque visível | 1,12 s | 1,27 s |
| Recarregar: categorias habilitadas | 9,40 s | 1,43 s |

São amostras locais com variação de rede/compilação de desenvolvimento, não um
benchmark controlado. O marco de categorias habilitadas não mede download de
todas as imagens. Cache dura somente no processo e é perdido ao reiniciar.

Conferência final no navegador: destaque Street Fighter preservado e séries
Stranger Things, The Boys, Reacher e La casa de papel nos quatro primeiros cards.
