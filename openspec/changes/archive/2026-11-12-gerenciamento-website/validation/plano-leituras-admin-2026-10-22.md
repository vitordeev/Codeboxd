# Validação interativa das consultas administrativas

Continuação de 2.1–2.3, 3.1, 4.1, 5.2 e 9.1, sem encerrar critérios incompletos.
Preparar `tools/admin_reads_remote.py` e testes offline antes da execução real.

Login manual em janela Edge temporária e formulário servido em loopback por
caminho aleatório. Encaminhar apenas email/senha ao login configurado; confirmar
ID 14, papel admin e estado active por `/auth/me` antes das consultas. Manter
senha/token e respostas em memória; não salvar screenshots, cookies ou corpos.
Rejeitar origem/Host inesperados, limitar tamanho do formulário e tentativas.

Consultar dashboard, usuários, quatro tipos do catálogo e reports, incluindo
paginação, busca vazia e filtros. Exportar apenas nomes de cenário, status HTTP
e booleanos de contrato. Limitar chamadas e interromper no primeiro 429, sem
repetição automática. Não publicar contratos nem modificar dados de negócio.
Sem reiniciar Reflex ou usar Docker; a ferramenta não depende do servidor app.

Testes offline devem cobrir bloqueio de membro/conta diferente, interrupção por
429, detecção de segredos e formato de paginação. Execução real depende do login
manual solicitado ao usuário. Rollback: remover a ferramenta/testes; nenhuma
migração remota. Registrar resultados e limitações na mesma change.

## Preparação concluída nesta rodada

`tools/admin_reads_remote.py` implementada com limite de 40 chamadas, três
tentativas de login e dez minutos de espera. Janela Edge temporária, servidor
127.0.0.1 com caminho aleatório, restrição de Host/Origin, sem logs de acesso,
sem cache e sem screenshots. Confere identidade e papel por `/auth/me` antes
de consultar. O login e `/auth/me` podem gerar auditoria normal do serviço;
não são executadas mutações administrativas ou criação de fixtures.

Verificações preparadas: totais não negativos, formato de paginação e
continuação quando disponível, ausência de campos secretos, usuário exato,
filtros por papel, busca vazia, catálogo nos quatro tipos e filtros de reports.
Isso não compara totais com inventário remoto independente, não cobre toda a
matriz de filtros e não substitui o navegador da aplicação nem mutações/auditoria.
Nenhuma tarefa ampla será encerrada somente por essa execução.

Validação local:

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_admin_reads_remote.py`:
  **7 testes aprovados**. Cobrem paginação inválida, segredos aninhados, conta
  aprovada/errada/membro/desativada, interrupção por 429 sem retry, exportação sem
  dados privados, loopback/caminho aleatório e jornada de leituras simulada.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_admin.py`:
  **21 testes aprovados**.
- Execução real ainda não realizada: login manual solicitado ao usuário.
  Nenhum servidor Reflex reiniciado, nenhuma dependência instalada.

Comando preparado (usar outro destino se já existir para preservar evidência):

```powershell
.venv/Scripts/python.exe -B -m tools.admin_reads_remote --output openspec/changes/gerenciamento-website/validation/leituras-admin-real-2026-10-22.json
```

A ferramenta exige acesso de rede e abertura de janela gráfica. Credenciais
devem ser digitadas somente na janela local; nunca passadas por argumento/chat.
