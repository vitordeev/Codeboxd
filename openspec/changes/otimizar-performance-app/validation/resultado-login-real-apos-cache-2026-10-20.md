# Resultado real após otimizar sessão/perfil — 20/10/2026

## Execução aprovada e concluída

Usuário entrou manualmente na janela Edge após recuperar o frontend gerado.
Executor completou dez visitas ao perfil (cinco em 1440px e cinco em 390px)
sem exceção, sem HTTP 429 e com ciclo de carga confirmado em todas as visitas.
Dados em [login-real-apos-cache-2026-10-20.json](login-real-apos-cache-2026-10-20.json).

Backend local em produção usando estado em memória e proxy de métricas para
Xano real. Uma conta autenticada, sem editar perfil, criar conteúdo, upload ou
gravação social. Não persistidos screenshots, cookies, tokens, senhas, conteúdo
de perfil ou payloads WebSocket nos relatórios. Largura de celular é emulação de
viewport no Edge desktop, não teste em aparelho físico/rede móvel.

## Resultado observado

| Marco | Resultado |
| --- | --- |
| Login até perfil principal visível | 4.203 ms, uma amostra |
| Chamadas remotas totais | 9, todas HTTP 200 |
| GET `/auth/me` | 2: login e renovação após expiração |
| Revisitas atendidas sem chamadas remotas | 8 |
| Perfil principal nas oito revisitas de cache | Mediana 454,5 ms; intervalo 398–612 ms |
| Última visita, com renovação | 4 chamadas; perfil visível em 2.872 ms; ciclo completo em 4.111 ms |
| Ciclos iniciados e concluídos | 10/10 |
| HTTP 429 | Nenhum nesse cenário |

A carga inicial usou cinco chamadas (login, sessão, detalhe do perfil e duas
referências). Oito revisitas reutilizaram dados. Na última visita, a expiração
provocou quatro consultas novas (sessão, perfil, mídia e pessoas), todas 200.
Assim, o teste também observou renovação real, além de cache aquecido.

Na execução anterior, o teste parou no desktop ao receber 429 na 11ª chamada,
com Retry-After de 20 s. Agora dez visitas foram concluídas com nove chamadas.
Isso comprova redução de tráfego no cenário e ausência do aviso nessa execução;
não define a quota exata do provedor ou garante ausência de 429 no app inteiro.

Não calcular percentual de ganho de latência entre as rodadas: a instrumentação
anterior de revisitas aceitava dados antigos antes do novo on_load. A versão
atual exige busy=true, atualização principal e busy=false no ciclo armado e
confere a presença na interface. O campo `cycle_observed` da primeira visita
parte da abertura da janela e inclui espera humana; usar `login_to_primary_ms`
para o marco de login, não `primary_update_ms` desse primeiro ciclo.

Tempos incluem overhead do proxy local e assets externos bloqueados. São
amostras desse ambiente, não benchmark direto de produção, p95 ou meta aprovada.
Não há ainda cinco amostras independentes com cache vazio em cada viewport.

## Restauração e verificação

Executor encerrou instância de teste/proxy, iniciou app habitual em produção
em 3030 e registrou `normal_restored=true`. Verificação posterior confirmou:

- Log `normal-restored-after-cache.log`: build concluído e app em 3030.
- `.web/env.json`: endpoints de frontend/backend em 3030.
- GET local `/login`: HTTP 200.
- Portas de teste 3031/3041: fechadas.

Servidor normal atualizado permanece em execução. A pasta gerada anterior foi
preservada em `.local/web-before-recovery-20261020-121044`; tentativa de startup
que falhou permanece em `login-real-apos-cache-inicializacao-falhou-2026-10-20.json`.
Nenhuma dependência foi atualizada para resolver a recuperação; o frontend foi
recriado com Reflex 0.9.11.post1 instalado. Aviso preexistente de parse de `.env`
continua sem alteração ou exibição do arquivo privado.

## Limites e próximo escopo

Incremento de login/perfil validado localmente, com navegador e Xano real nas
camadas descritas. Testes anteriores: 205 regressões do app; sete testes da
instrumentação corrigida passaram na retomada. Não houve mudança adicional de
código de produto após esses testes.

Permanecem pendentes metas numéricas aprovadas, cobertura completa de jornadas,
cache vazio por viewport, latência sem proxy e diagnóstico da quota remota.
Próximo escopo sugerido: diagnosticar carregamento de biblioteca/listas e
repetições de sessão durante navegação entre telas. Qualquer nova alteração ou
execução autenticada fora do cenário atual deve ser apresentada para aprovação.
