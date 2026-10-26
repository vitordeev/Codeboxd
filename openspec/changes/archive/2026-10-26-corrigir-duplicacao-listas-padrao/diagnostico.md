# Diagnóstico — 26/10/2026

## Xano real, somente leitura

Consulta GET paginada à Metadata API, workspace 147717, tabela user_list 895415, fonte live. Credencial selecionada pelo domínio configurado do aplicativo; nenhum segredo ou dado pessoal registrado. Conferidas contagem total e unicidade dos IDs.

- 19 listas, pertencentes a 8 proprietários.
- 16 listas padrão, em 16 combinações únicas de proprietário/título.
- Zero grupos duplicados de listas padrão por proprietário, normalizando espaços externos e caixa.
- Todas as 16 listas padrão são públicas.
- Nenhuma escrita remota, login ou exclusão executados.

## Código local

`SocialState.load_lists`, em `Codeboxd_main/state/social.py`, consulta GET /lists/public e GET /lists e junta ambos por ID. As listas públicas de outros perfis entram na mesma coleção das próprias. Cada proprietário tem IDs distintos, portanto a união por ID mantém todos os títulos iguais. Esse comportamento explica o relato, sem duplicação persistida por perfil na amostra completa atual.

`_ensure_default_lists` verifica títulos antes de criar; POST /lists local usa inserção simples. Existe risco potencial de concorrência e de consulta incompleta por paginação, mas ele não comprova ocorrência no banco. A hipótese inicial de duplicação persistida não foi confirmada.

## Limites e próximos passos

Não houve inspeção da sessão do navegador do usuário nem comparação do contrato publicado com o local. A correção principal deve separar a coleção pessoal da descoberta pública. Não há justificativa atual para limpar registros remotos. A defesa contra concorrência é prevenção, com validação própria, sem alegar que foi a causa observada.

As tentativas iniciais de acesso falharam por perfis múltiplos e restrição de rede; a consulta final com perfil selecionado pelo domínio e permissão de rede concluiu. A ausência de PyYAML não afetou a consulta final.
