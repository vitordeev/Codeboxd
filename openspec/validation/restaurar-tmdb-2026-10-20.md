# Restaurar seleções TMDB — 20/10/2026

Complemento ativo de confiabilidade operacional e descoberta. Usuário relatou
que “Agora nos cinemas”, “Filmes muito bem avaliados” e “No radar: próximos
filmes” não carregavam. A alternativa com catálogo salvo não cobre essas listas.

- [x] Confirmar ausência da configuração TMDB no ambiente local.
- [x] Recuperar somente TMDB_READ_TOKEN da configuração anterior para `.env`.
- [x] Conferir as três consultas reais no TMDB.
- [x] Verificar as três fileiras no navegador.

Recuperação feita localmente a partir do histórico Git, sem imprimir/copiar
o valor para relatórios, logs ou arquivos rastreados. Outras credenciais não
foram recuperadas. A rotação histórica já registrada continua pendente: esta
restauração reutiliza a configuração anterior, não constitui rotação da chave.

Consultas remotas autorizadas: `movie/now_playing`, `movie/top_rated` e
`movie/upcoming`, com `language=pt-BR`, `region=BR`, página 1, retornaram
HTTP 200 e 20 obras cada. Servidor de desenvolvimento existente recarregado
com atualização do timestamp de `services/catalog.py`, sem alterar código.
Nenhuma escrita Xano, mudança de conta ou implantação foi realizada.

Navegador Edge headless no servidor local: 20 cards em cada uma das três
fileiras. O primeiro script de verificação usou `.media-card` por engano;
a conferência válida usou `.shelf-card`, classe real das fileiras.
`.env` confirmado como ignorado pelo Git; diff documental sem erros.
Sem mudança de código, não foi necessário repetir a suíte/compilação já aprovadas.
