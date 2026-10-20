# Isolar avaliação por obra — 20/10/2026

Correção ativa posterior a `avaliacao-envio-unico-2026-10-20.md`. Relato:
avaliação de Cara de Barro aparece ao abrir A Odisseia.

Causa confirmada: GET público `/media` com identity_key inexistente retornou
HTTP 200 e 12 registros, demonstrando que a versão remota não respeita esse
filtro. `_load_external_interaction` confiava em `found[0]`, atribuindo o ID de
uma obra diferente à ficha. A nova consulta foi introduzida na rodada anterior.

- [x] Aceitar somente correspondência exata de identidade na resposta.
- [x] Limpar estado da avaliação entre obras e remontar formulário por identidade.
- [x] Validar identidade interna antes de escrever e rejeitar submit de outra obra.
- [x] Testar busca sem filtro efetivo, ausência de correspondência e troca de obra.

Não apagar ou mover avaliações existentes com base apenas no relato: sem acesso
à conta e à avaliação não é possível inferir com segurança o vínculo pretendido.
Nenhum dado pessoal foi consultado no diagnóstico; apenas catálogo público.

Validação local: 170 testes e compilação Reflex `--dry` passaram; diff sem erros.
Cinco novas regressões cobrem resposta com várias obras e correspondência fora
da primeira posição, nenhum match sem herdar crítica/ID, ficha interna sem
avaliação, formulário atrasado de outro filme e ID antigo incorreto antes de
persistir a obra certa. Pedidos privados e gravações foram simulados.

A API pública remota continua sem filtrar identidade nesta instância; o cliente
agora filtra explicitamente a resposta paginada. Nenhuma publicação remota ou
alteração de avaliações existentes. Conferência autenticada no navegador e
reparo de dados antigos pendentes de identificar a conta/avaliação do usuário;
nome de usuário solicitado sem senha/token.
