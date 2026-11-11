# Plano de análise e medição — 09/11/2026

Vínculo: otimizar-performance-app, 1.3/1.5/4.4/6.4/7.1; manter 17/37.
Usuário autoriza análise, medições reais e registros; nenhuma otimização,
administração remota, gravação de conteúdo, push, merge ou exclusão.
Conta comum será fornecida por login local, credenciais apenas em memória.

Reusar os instrumentos e medições anteriores. Primeiro Home; depois biblioteca,
listas, leitura de avaliação/ficha e social. Não repetir escritas funcionais de
05/11 ou os testes administrativos. Não criar conta/dados para completar amostras.

Confirmada ausência de servidor nas portas 3030/3035. Preparar servidor isolado
de produção em 3032, frontend próprio copiado de fontes/dependências locais e
recompilado, sem reiniciar outros processos. Executar com a .venv existente do
diretório original apenas como runtime; código e cwd da worktree de performance.
Não criar .env nem copiar credenciais: configuração do original passada somente
em memória ao processo. Registrar versões efetivas; setup de novo projeto não
é necessário. Preservar/restaurar somente bytes do lock reescrito pelo compilador.

Instrumentação temporária fora do produto: HTTP Python sanitizado, WebSocket
(somente tempos/bytes/flags), DOM e performance do navegador. Bloquear escritas
Xano antes do transporte, exceto login normal, e todas as rotas administrativas.
Parar em 429, orçamento excedido, falha ou tentativa de escrita; não repetir
mutações. Teto 500 HTTPs Python; não testar carga concorrente.

Cinco pares por viewport 1440x900/390x900 quando possível. Home fria: contexto
novo e caches públicos Python limpos em instância isolada; quente: mesmo contexto,
recarga, caches públicos preservados. Pool mantido; frio não significa TCP frio.
Medir primeiro conteúdo, fim do handler, imagens visíveis, bytes/requisições,
erros e atividade de estado. HTTP 200 não comprova renderização; aguardar ciclo
busy e conteúdo esperado. Leituras privadas condicionadas a login member ativo;
não presumir cache privado aquecido em recarga, registrar chamadas observadas.
Pausas entre pares/rotas para respeitar quota ficam fora dos tempos e impedem
concluir navegação habitual sem pausas. Sem throttling: celular é viewport,
não hardware/rede móvel. Não inferir p95 a partir de cinco amostras.

Metas adicionais serão propostas numericamente, ainda sem aprovação. Não marcar
1.5 concluída por proposta, nem 1.3 por cobertura parcial. Se build/login/API
impedirem execução, guardar a falha real e manter critérios abertos.
