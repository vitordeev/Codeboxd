# Avaliações com meias estrelas — 19/10/2026

Pedido: permitir meia estrela e decimais como 1,5 nas avaliações.

## Implementação

- Estado social normaliza vírgula/ponto com Decimal, somente finitos, escala
  0,5–5 em passos de 0,5; zero significa sem nota. Sem arredondamento/truncamento.
- Seleção e restauração de visitante aceitam meias estrelas, decimais legados e
  limpeza da nota. LocalStorage continua isolado; não publica nota de visitante.
- Cinco estrelas possuem dez metades acionáveis, preenchimento 0/50/100%, nomes
  acessíveis com vírgula e aria-pressed. Cada alvo mede 24×48px. Controle nativo
  adicional oferece todas as opções com rótulos 0,5 / 5, 1,5 / 5 etc.
- Controle compartilhado entre conta e visitante. Trocar nota não remonta mais
  o formulário, preservando a crítica ainda não salva. Biblioteca mostra vírgula.
- Xano já tinha campo decimal e validação de passo 0,5; nenhuma migração ou
  publicação de endpoint foi necessária. Contratos arquivados não foram alterados.

## Testes locais

- `.venv/Scripts/python.exe -m unittest discover -s tests -q`: **148 passaram**.
- Cinco novas regressões cobrem todos os passos, vírgula/ponto, limites, valores
  não finitos, restauração visitante/conta, limpeza e envio numérico de 1,5.
- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado.
- `git diff --check` nos arquivos alterados: aprovado.
- `openspec validate avaliar-meias-estrelas --strict`: aprovado.

## Navegador e Xano real

Edge headless, aplicação em produção na porta 3033 e conta de teste controlada
existente. [Resultado final](browser-xano-2026-10-19.json): nove checks aprovados.

1. Visitante seleciona 0,5.
2. Nota 1,5 exibe uma estrela completa e uma metade (larguras 48/24/0/0/0).
3. Nota decimal do visitante volta após recarga.
4. Estrelas cabem na viewport de 390px; desktop em 1440px também verificado.
5. Limpeza da nota restaura zero após recarga.
6. Troca por estrela e por seletor mantém a crítica em edição.
7. Xano persiste valor numérico **1.5**, associado à conta de teste.
8. Nota e crítica da conta retornam após recarga da ficha.
9. Interação criada foi removida por ID, após conferir usuário, obra e marcador.

Escolhida obra sem interação anterior dessa conta; nenhuma avaliação existente
precisou ser sobrescrita. Apenas a nova interação de teste foi removida. Capturas
inspecionadas em `.local/half-stars-{desktop,mobile}-2026-10-19.png`.

## Limites e tentativas anteriores

A [primeira tentativa](browser-xano-primeira-tentativa-2026-10-19.json) teve erro
429 no GET /interactions usado para conferir o salvamento; a interação criada
foi removida. Outra tentativa encontrou 429 na leitura inicial de /media, antes
de qualquer avaliação. A verificação final usou metadados para conferir persistência
e respeitou esperas de leituras/recarga; não repetiu o salvamento automaticamente.

Nenhum teste provocou saturação intencional. Limites da plataforma continuam
vigentes. Instância 3033 reiniciada e atualizada; instância 3000 não reiniciada.
Não há validação de hospedagem ou Docker. Changes de administração e tradução
mantêm suas pendências próprias; esta entrega não encerra esses escopos.
