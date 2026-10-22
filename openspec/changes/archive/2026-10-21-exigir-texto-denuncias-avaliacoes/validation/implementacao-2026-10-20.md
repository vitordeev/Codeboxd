# Texto obrigatório — implementação e pendências — 20/10/2026

Pedido: impedir denúncias e avaliações sem conteúdo escrito. A change própria
preserva o histórico e não altera a contagem de tarefas de performance.

## Implementado

- Modal de denúncia exige detalhes em todos os motivos; formulário de avaliação
  exige crítica. HTML required/min_length e validação Python com strip.
- Ausente, null, vazio, espaços, tabs, quebras de linha e NBSP são rejeitados
  antes da gravação, com mensagem e manutenção do formulário aberto.
- Atalho com nota positiva também exige crítica. Organização de status sem nota
  continua válida; não é envio do formulário de avaliação.
- POST reports exige description com trim/min:1/max:2000. PUT interactions
  rejeita nota positiva sem review. Registros antigos não foram alterados.

## Evidência local

Seis novos testes em test_required_submission_content.py e adequação do teste
de denúncia válida antiga para incluir descrição. **269 testes passaram**;
**reflex compile --dry passou**. Preservadas as validações anteriores de envio
único, identidade, falha/retry e proteção de rascunhos.

## Publicação real

Dry-run limitado: apenas interactions PUT e reports POST, duas atualizações.
Backup privado de 78 documentos em .local/xano-before-required-content-20261020,
sem registros nem variáveis de ambiente. Publicação aprovada dos dois endpoints;
export posterior em .local/xano-after-required-content-20261020 comparado por hash.
Somente esses dois contratos diferem; total de 78 documentos preservado.
[Resumo sanitizado](publicacao-2026-10-20.json).

O CLI emitiu aviso de referências não incluídas no push. Export pós-publicação
confirmou db.get/db.add/db.add_or_edit e as referências de tabela preservadas,
sem placeholders. Não foram enviados schemas ou registros nesse push.

Falta testar rejeições autenticadas na API real. O arquivo de conta controlada
citado nos scripts históricos não existe atualmente; nenhuma conta foi criada,
senha extraída do histórico, token de usuário gerado ou privilégio concedido.
Publicação/export não equivalem a execução autenticada.

## Navegador e transição

tools/required_content_browser.py prepara casos de vazio/espaços/texto válido
para os quatro tipos em 1440/390px com dados fictícios. A execução falhou antes
de qualquer caso (0/12) porque o build de produção encerrou com timeout de
prerender da rota /. O fallback de restauração também falhou nessa etapa;
o relatório contém normal_restored=false e a evidência foi preservada.
[Falha de inicialização](browser-2026-10-20/result.json).

Usuário pediu retomar análise de otimização. Recuperação operacional e situação
da execução normal ficam na revisão de performance desta rodada. Não declarar
browser aprovado, nem encerrar esta change: estado 3/5 tarefas.
