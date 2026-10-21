# Isolamento de frontend e diagnóstico do build

Continuação autorizada pelo pedido de realizar o restante da otimização.
Primeiro passo: investigar o timeout de prerender sem interferir no servidor
de desenvolvimento existente. O Reflex instalado oferece `REFLEX_WEB_WORKDIR`
(`reflex.utils.prerequisites.get_web_dir`).

`tools/isolated_frontend.py` prepara uma cópia dos arquivos gerados em
`.local/frontends/<nome>`, excluindo build, backend e caches do React Router.
As dependências já instaladas também são copiadas. O experimento inicial usou
junction, mas foi revisado: o Reflex pode decidir reinstalar dependências ao
trocar o executor, o que tornaria o compartilhamento inadequado. A versão final
nunca compartilha os arquivos de pacotes. A `.web` original é preservada.
Não altera configuração permanente, SSR, contratos ou dados remotos.

Verificação prevista: build completo com SSR padrão, disponibilidade HTTP,
conectividade externa e navegador. Até obter os resultados, nenhum critério
de performance ou tarefa ampla será marcado como concluído.

Rollback: encerrar apenas o processo lançado para este teste e deixar de
usar a variável no processo seguinte; arquivos gerados ficam preservados.

## Resultados e limites

- Cópia isolada inicial: compile passou; export falhou novamente em `/`.
  Portanto o compartilhamento da `.web` não explica sozinho o timeout.
- Build direto por Node com instrumentação local de HTTP: todas as rotas e
  fallback SPA foram gerados. A instrumentação observou conexão, entrada no
  servidor e resposta 200. Não constitui validação da inicialização normal.
- Nova execução padrão do Reflex: voltou a falhar por timeout no prerender.
  Não há causa confirmada nem garantia de recuperação por repetir a tentativa.
- Teste da opção oficial `REFLEX_USE_NPM=true`: iniciou instalação de pacotes;
  foi interrompido junto com sua árvore de processos. Como a cópia inicial
  compartilhava dependências, a versão final do preparador passou a copiá-las.
  Não afirmar que o ensaio não tocou pacotes ou que comprovou falha do Bun.
- 14 testes dirigidos passaram, incluindo isolamento dos arquivos de pacotes
  e proteção contra substituir o servidor quando a rede está indisponível.
- `reflex compile --dry` passou. Nenhum browser foi executado nesta rodada;
  o serviço de produção em 3030 permanece sem recuperação comprovada.

Utilitários de navegador agora preparam diretórios próprios e preservam o app
normal se ele continua respondendo; restauração também prepara arquivos próprios
antes de parar processos. O runner de texto obrigatório aceita `--output` para
preservar o resultado antigo. Isso não encerra a validação dos formulários.
