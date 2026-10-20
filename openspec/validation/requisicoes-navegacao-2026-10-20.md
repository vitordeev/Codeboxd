# Reduzir requisições na navegação — 20/10/2026

Complemento ativo de performance/confiabilidade, posterior ao carregamento da
homepage. Relato: navegação e uso de funcionalidades exibem espera de 20 segundos.
O transporte apresenta essa mensagem ao receber HTTP 429 do Xano; endpoint e
limite remoto responsáveis no uso do usuário ainda não foram reproduzidos.

- [x] Inspecionar carregadores e identificar leituras repetidas.
- [x] Reutilizar leituras por 15 segundos no estado privado de cada sessão,
  limitando entradas e separando credenciais/parâmetros/paginação.
- [x] Invalidar antes e depois de gravações e ao limpar identidade; não cachear
  erros, autenticação ou ações de recuperação de senha.
- [x] Validar regressões e compilação local.
- [ ] Confirmar navegação autenticada no navegador e redução de HTTP 429 real.

Não alterar limites remotos nem repetir gravações automaticamente. Dados podem
ficar até 15 segundos atrás de alterações feitas por outra sessão.

Implementação local em `SocialState._call`: whitelist `/media`, `/profiles`,
`/lists` e `/interactions`, máximo de 32 entradas, chave hash de token, caminho,
parâmetros, payload e modo de paginação. Cópias profundas; resposta armazenada
somente após completar as páginas. Autenticação continua consultando o servidor.

Validação: 174 testes locais aprovados e `reflex compile --dry` aprovado.
Quatro regressões verificam cópias/expiração, isolamento, invalidação e erros.
Teste anterior de notas passou a limpar o cache entre cenários independentes.
Chamadas de rede dos testes são simuladas. Não houve publicação remota, medição
autenticada nem reinício de servidor nesta rodada. A mensagem pode persistir se
o volume restante superar o limite remoto; não declarar resolução integral.
Ambos os comandos emitiram aviso preexistente de parse do `.env` na primeira
linha; conteúdo privado não foi exibido nem alterado.
