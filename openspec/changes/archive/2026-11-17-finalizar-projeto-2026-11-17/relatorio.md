# Auditoria e plano de conclusão — 17/11/2026

## Resultado e limite

Sete changes funcionais: **51/111 tarefas concluídas, 60 abertas**. Não é percentual de conclusão do produto. `modernizar-ui-ux-codeboxd` já estava em 7/26 antes desta rodada; os quatro avanços desde o quadro de 14/11 não são entregas novas desta sessão. Duas changes documentais ficam fora desse total. Preservadas todas as alterações locais preexistentes de busca/listas e seus testes.

A aplicação compila e a suíte local passa. Ainda não é possível declarar o projeto inteiro finalizado hoje: há trabalho de implementação além dos bloqueios externos, principalmente Cloudinary, propagação visual e medições integradas. O plano abaixo define a ordem de conclusão e os critérios para decidir liberação, sem substituir aceite por simulação.

## Incoerências verificadas

1. **Resumos defasados:** os documentos centrais informavam 47/111 e UI 3/26, enquanto CLI/checklists atuais mostram 51/111 e UI 7/26.
2. **Frontend e contrato de busca divergentes:** `/buscar` envia `q`, `creator_id`, `search_in` e espera envelope paginado; os GETs locais de perfis/listas ainda ignoravam esses parâmetros e devolviam arrays. Implementação candidata preparada nesta sessão; publicação não executada.
3. **Contagem de listas padrão:** itens dessas listas vêm de `user_media_list_status`, não de `user_list_item`. A nova projeção escolhe a contagem correta pela chave e pelo proprietário.
4. **Planejamento pronto não significa produto entregue:** `openspec status` informa artefatos completos, mas `instructions apply` e os checklists mantêm tarefas funcionais abertas.
5. **Histórico e presente misturados:** documentação inclui referências antigas a Resend, ausência de credenciais Cloudinary e administração pendente; as evidências posteriores registram SendGrid, ensaio Cloudinary e administração arquivada para leitura. Preservar datas, sem reutilizar os registros antigos como diagnóstico atual.
6. **Dependências efetivamente abertas:** Cloudinary não tem ciclo de vida integrado dos posts; domínio autenticado e entrega comparada de e-mail não foram comprovados; ambiente administrativo isolado permanece indisponível no último ensaio. Não concluir por flag ou HTTP 200/202.
7. **Aceite de UI incompleto:** foco/teclado do shell, propagação para famílias, leitor de tela, dispositivo touch físico e comparações de performance ainda têm critérios abertos.

## Plano para hoje, por ordem de execução

Estimativas são de esforço adicional e dependem dos acessos; não são horário prometido. Não cabem todos os 60 critérios restantes numa única homologação sem implementação adicional.

| Ordem | Entrega e change responsável | Critério de conclusão | Dependência / estimativa |
| --- | --- | --- | --- |
| 1 | Baseline, correções de contrato e plano — esta change + UI 5.1 | Suíte, compile, OpenSpec e prévia dos contratos limitados | Rodada local executada; restante da busca exige aceite Xano |
| 2 | Busca/listas UI 5.1–5.4 | Termos/coringas, ranking estável, totais, paginação, visitante/dono/outra conta, privada=inexistente, mudança de visibilidade, links antigos e limpeza | Backup/prévia do lote e destino identificados; cerca de 2–4 h após acesso e ajustes necessários |
| 3 | Recuperação 3.2 + SendGrid 3.1 + experiência do e-mail | Restauração da conta, replay/sessões, recebimento e comparação real de entrega | Usuário: decisão sobre retomar recuperação, caixa controlada e DNS; 1–2 h de execução, propagação DNS sem prazo garantido |
| 4 | Shell/controles/UI 1.2, 2.2, 2.3, 6.x, 7.x | Teclado/foco, rotas e guards, 320/390/768/1024/1440, erros/rascunhos, regressões e revisão visual | Mais implementação e navegador por família; estimativa 4–8 h, além de leitor de tela e touch físico |
| 5 | Cloudinary 2.1.1–2.1.10 e 2.2 | Reserva durável, verificação independente, commit idempotente, edição/exclusão, fila/reconciliação, autoria e legados, ensaio descartável antes de ativar | Trabalho de código/backend ainda amplo; estimativa inicial 1–2 dias, revisar após desenho detalhado. Não é apenas fornecer uma chave |
| 6 | Performance 1.3/1.5 e aceites 2.4–9.3 | Cinco amostras equivalentes por cenário, metas aprovadas e jornada completa; distinguir mocks e rede real | Contas/dados controlados e metas; 3–6 h de medições, correções adicionais conforme resultado |
| 7 | Homologação Xano admin 2.2/3.x | Destino separado vazio, importação sem dados/segredos, guardas de isolamento e disponibilidade | Usuário: ambiente elegível; cerca de 1–2 h após acesso, sem usar live como substituto |
| 8 | Revisão de liberação | Critérios acima atendidos, evidências, rollback, specs sincronizadas só quando prontas | Não arquivar changes funcionais incompletas; publicação e hospedagem têm escopo próprio |

**Corte sugerido para hoje:** consolidar núcleo existente, corrigir/validar busca e listas e resolver recuperação/entrega com ajuda do usuário. O escopo integral de UI + Cloudinary + todas as jornadas de performance continua pendente; não foi removido dos checklists para caber no prazo.

## Validação desta sessão

| Camada | Execução | Resultado |
| --- | --- | --- |
| Estado inicial | `git status --short`, `openspec list --json` | Alterações preexistentes identificadas e preservadas; UI já 7/26 |
| OpenSpec inicial | `openspec validate --all --no-interactive` | 37/37: oito changes e 29 specs, antes da nova change documental |
| Ambiente | `.venv/Scripts/python.exe -m pip show reflex`, `-m pip check` | Reflex 0.9.11.post1; nenhuma dependência quebrada |
| Suíte inicial | `.venv/Scripts/python.exe -m unittest discover -s tests -q` | 669 aprovados |
| Suíte após contratos | Mesmo comando | **675 aprovados**, incluindo seis regressões novas |
| Compilação | `.venv/Scripts/python.exe -m reflex compile --dry` | Aprovada, 4,074 s; contratos Xano não alteram componentes Reflex |
| Código dos contratos | `test_public_search_contracts.py` | Seis testes aprovados; lambdas JavaScript executadas em Edge headless com dados fictícios e guardas estruturais inspecionadas. Não executa banco Xano |
| Prévia Xano | `xano workspace push -d xano -w 147717 -b v1 --dry-run --no-guids` com cinco includes exatos | Aprovada: três addons criados e dois endpoints atualizados na **prévia**. Nenhuma publicação, registro, variável privada ou GUID alterado |
| Navegador desta rodada | `tools/ui_unified_search_browser.py --url http://127.0.0.1:3041 --output .local/ui-audit-search-20261117 --log .local/ui-audit-20261117.jsonl` | **11 casos aprovados, zero erros JavaScript**, Edge headless/390 px e backend fictício; não valida consultas Xano |
| OpenSpec final | `openspec validate --all --no-interactive` | **38/38**, incluindo nove changes ativas e 29 specs; validade estrutural não encerra critérios funcionais |

Os includes foram `api/codeboxd/profiles_GET.xs`, `api/codeboxd/lists_public_GET.xs` e `addon/search_list_{creator,custom_count,default_count}.xs` (os três nomes completos foram passados individualmente). A prévia não comprova execução de filtros/addons/índices no banco.

`pytest` não está instalado e não foi necessário instalar: a suíte usa `unittest`. A tentativa inicial com pytest não executou testes. O CLI Xano restrito falhou com `uv_os_get_passwd/ENOMEM`; fora do sandbox, com aprovação, a prévia funcionou. O build da fixture restrita falhou no acesso ao cache npm; fora dele houve timeout de prerender. Uma terceira execução em produção com `REFLEX_SSR=false` apenas na fixture concluiu o build (54 s), iniciou na porta 3041 e aprovou os 11 casos. Isso não valida prerender de todas as rotas. O processo de teste foi encerrado após a rodada; nenhuma instância normal foi reiniciada. Arquivos rastreados de `reflex.lock/` gerados pelo build foram restaurados ao conteúdo inicial limpo.

## Ajuda necessária

- Informar acesso disponível ao DNS do domínio e ao ambiente Xano isolado. Configurar chaves apenas pelos mecanismos privados existentes, sem enviá-las no chat.
- Decidir se deseja retomar a restauração da conta controlada. A recusa histórica do terceiro pedido continua preservada até nova instrução.
- Disponibilizar teste em aparelho touch físico e revisão manual com leitor de tela para os respectivos critérios.
- Revisar a prévia e o destino de um lote concreto antes de publicação. Não foi feito push Git, merge, archive, alteração DNS ou ativação Cloudinary nesta rodada.
