# Preparação local de leituras administrativas — 11/11/2026

Vínculo: gerenciamento-website 9.2, 33/34, schema spec-driven. Base develop
29d0456 em branch própria task/admin-readiness-20261111. Changes de e-mail e
Cloudinary ficam em suas worktrees; performance não tocada.

## Plano antes da implementação

Tornar ferramentas existentes portáveis entre worktrees: `admin_reads_remote`
receberá caminho opcional de configuração sem mudar o default; `admin_browser_real`
propagará o mesmo caminho para autenticação e proxy de leitura. Não copiar .env,
tokens ou senhas para a worktree nem mudar URLs remotas. Testar passagem do caminho
com dobres locais e conferir regressões do leitor. Preparar frontend isolado e
compilar com a .venv existente; preservar lockfiles da branch byte a byte.

Não repetir a bateria visual fictícia histórica de 68 cenários nem declarar
aprovação nova por essas evidências. Sem escrita Xano, seed ou limpeza; guardas
de mutação atuais continuam restritas a MockTransport. Sem login remoto até
aprovação específica da etapa administrativa A1. Preparação local não fecha 9.2.

## Ensaio proposto para aprovação

Conta admin existente fornecida pelo operador em janela privada de navegador.
API auth/social do .env Codeboxd/workspace histórico 147717. Somente POST inicial
de autenticação e GET auth/me/admin/dashboard/users/catalog/reports; proxy da UI
recusa demais métodos/rotas. Não permitir suspensão, edição, decisão ou exclusão.

Frontend/backend de teste em produção local, porta 3035, diretórios gerados e
capturas privadas isolados; app do usuário não reiniciado. Navegação de Dashboard,
Usuários, quatro tipos de Catálogo e Reports em 1440/390px; buscas vazias e erro
503 somente no proxy local, preservando servidor remoto. Intervalo 3,1s entre
leituras do proxy; parar em 429/erro de contrato. Não provocar indisponibilidade
real, não publicar snapshots privados. Nenhum dado original usado como alvo.

Essa etapa não substitui mutações e auditoria integradas de A2–A4, que continuam
sem aprovação e sem execução. Somente propor conclusão de 9.2 após evidência de
todos os critérios aplicáveis, sem arquivar automaticamente.

## Resultado da preparação local

- `admin_reads_remote.main` e CLI aceitam `--config`, preservando default.
  BrowserProbe recebe o caminho e o proxy carrega exatamente a mesma configuração.
  Configuração privada não copiada, dados de sessão só em memória.
- Dois testes novos verificaram configuração de login/proxy antes de abrir rede,
  sockets ou navegador; 12 regressões de admin_reads_remote passaram. Todas locais.
- Suíte completa desta branch: **568 testes passaram em 37,079s**. Esta branch
  não contém os testes novos do executor de recuperação da branch de e-mail;
  não confundir 568 aqui com os 585 daquela branch nem somar execuções.
- Frontend independente preparado em `.local/frontends/admin-readonly-20261111`,
  cópia privada de arquivos/pacotes, sem compartilhar diretório gerado em uso.
- `.venv` existente do repositório principal, `reflex compile --dry` com frontend
  isolado: **aprovado em 5,245s**. URLs de compilação apontaram para loopback sem
  serviço; sem validação remota. Variáveis locais específicas desse processo.
- Três lockfiles existentes preservados byte a byte; zero lockfiles novos.
  Relatório privado `.local/compile-admin-summary-20261111.json`; logs de compile
  e testes na `.local` desta worktree. App normal não reiniciado ou modificado.

Nenhum browser/login admin remoto nesta preparação. Não houve correção do
aplicativo: somente portabilidade das ferramentas para o isolamento solicitado.

`openspec validate gerenciamento-website --type change` e `git diff --check`
aprovados; aviso preexistente de requisito longo preservado. Porta 3035 livre
na conferência local. Git: três arquivos modificados e dois novos (teste e
relatório), sem commit, push ou merge na branch própria.

## Comando pronto, somente após aprovação A1

Na worktree `D:/Repositorios GIT/Codeboxd/.local/worktrees/admin-readiness-20261111`:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.admin_browser_real --config 'D:/Repositorios GIT/Codeboxd/.env' --output 'openspec/changes/gerenciamento-website/validation/browser-leituras-2026-11-11.json' --frontend-workdir '.local/frontends/admin-readonly-20261111' --private-dir '.local/admin-readonly-browser-20261111'
```

A janela de autenticação é no navegador local, conta admin existente fornecida
pelo operador, sem promoção de papéis. Não reutilizar senha da caixa ou token
histórico. Roteiro atual pode consumir minutos com leituras ritmadas; parar em
falha e preservar relatório. Não executar se porta 3035 estiver ocupada; não
encerrar processo que não pertença a este ensaio. Saída/capturas já existentes
impedem reutilização silenciosa. Sem push, merge, arquivo ou A2–A4.

## Execução autorizada iniciada

Usuário aprovou explicitamente abrir navegador, autenticar conta admin existente
e validar somente leituras. Comando acima iniciado fora do sandbox. Navegador
local aberto aguardando preenchimento privado; nenhuma credencial coletada pelo
chat. A aprovação não inclui A2–A4, criação/suspensão/edição/decisão/exclusão.
Resultado de API/browser será registrado após execução; início não é aceite.

Na conferência final observou-se defeito apenas de evidência no runner: o resumo
do proxy sobrescreve a lista inicial de autenticação e request_count continua
contando só chamadas do Probe. Preparar correção local preservando requests
iniciais, separando proxy_requests e contando upstream independentemente dos
503 locais. Testar resumo com dados fictícios; preservar JSON bruto desta
execução e publicar apuração separada, sem repetir leituras remotas já aprovadas.
