## 1. Configuração e serviço

- [x] 1.1 Configurar chave privada e exemplo vazio; verificar que .env não é rastreado e chave não aparece no diff.
- [x] 1.2 Implementar tradução PT-BR, cache persistente, proteção concorrente e fallback; verificar testes de cache, falhas, português e ausência de chave.

## 2. Integração e validação

- [x] 2.1 Integrar fichas Kitsu/Jikan/Open Library sem mudar identidade e sem traduzir TMDB; verificar testes de integração simulados.
- [x] 2.2 Executar suíte local e smoke remoto limitado com DeepL, incluindo reutilização de cache; registrar resultados e limites sem segredos.
- [ ] 2.3 Validar ficha traduzida no navegador; registrar resultado e eventual limitação de execução.
- [x] 2.4 Atualizar documentos centrais e validar change com openspec validate --strict.

Evidências desta rodada: [implementacao-2026-10-19.md](validation/implementacao-2026-10-19.md).
5/6 tarefas verificadas; revisão no navegador permanece aberta.

21/10: browser público confirmou ficha disponível com sinopse original, mas
DEEPL_API_KEY não está configurada no `.env` atual. Solicitado preenchimento
privado/arquivo local; não concluir 2.3 por fallback. 18 testes pertinentes
passaram. [Retomada e evidências](validation/retomada-2026-10-21.md).
