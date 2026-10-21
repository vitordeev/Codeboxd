# Conclusao da traducao no navegador

Validacao real publica no Edge headless contra http://127.0.0.1:3000, sem reiniciar
os processos existentes e sem sessao autenticada. Kitsu anime 1 e Open Library
OL82563W, nas larguras 1440 e 390: quatro de quatro cenarios aprovados.

Sinopses diferem do original, correspondem ao cache persistente PT-BR e continuam
traduzidas apos recarga. Titulos e identidades presentes, sem erros JavaScript
ou overflow horizontal nos cenarios. Capturas de anime desktop e livro celular
inspecionadas visualmente; texto em portugues confirmado. Dados de provedores
reais; nenhum mock utilizado nesta rodada.

[Resultados](browser-chave-restaurada-2026-10-21/result.json).
Oito testes de tests.test_translation aprovados. Chave privada configurada e
smoke DeepL HTTP 200 registrados em retomada-2026-10-21.md. Nao se mediu o numero
de chamadas DeepL do processo servidor; recarga comprova persistencia visual,
e ausencia de chamadas repetidas esta coberta pelos testes do servico.

Limite visual: a captura de livro em 390px mostra capa sobre parte do texto.
A sinopse traduzida esta presente integralmente no DOM; ajuste de layout deve
ser acompanhado separadamente, sem declarar que a responsividade inteira foi
validada. Nao houve alteracao de codigo ou publicacao Xano nesta rodada.
