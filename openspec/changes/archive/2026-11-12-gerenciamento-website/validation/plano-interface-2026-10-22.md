# Validação local da interface administrativa

Escopo autorizado: tarefas 6.2 e 6.3. Exercitar as páginas reais `/admin`,
usuários, quatro tipos de catálogo e reports, com login administrativo fictício
e APIs locais. Verificar busca, filtros, paginação, espera, vazio, falha e
recuperação visual em 1440px e 390px. Corrigir defeitos pertinentes antes de
encerrar os critérios. Registrar screenshots e resultado estruturado.

Execução em produção isolada, `.venv`, sem Docker, sem alterar o servidor
habitual ou dados Xano. O utilitário reutiliza o ciclo de vida isolado de
`tools/feed_lists_browser.py`; todas as respostas administrativas são fictícias.
As tarefas de persistência/autorização remota e 9.2 continuam abertas: navegador
com fixtures não comprova integração com dados reais de desenvolvimento.
