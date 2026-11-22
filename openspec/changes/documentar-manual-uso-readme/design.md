## Context

Consulte `proposal.md`. O `README.md` atual é uma página de apresentação com HTML, sem o manual solicitado. A aplicação Reflex registra as rotas em `Codeboxd_main/Codeboxd_main.py`; o backend público ainda não foi publicado e as integrações Xano/Cloudinary têm limites registrados nas changes ativas.

## Goals / Non-Goals

**Goals:** tornar o README legível no GitHub e cobrir os sete tópicos da entrega acadêmica com passos consistentes com as telas e rotas atuais.

**Non-Goals:** alterar funcionalidades, fabricar URL de deploy, expor contas/credenciais, afirmar que uma integração foi aceita sem evidência ou criar capturas que não representem a versão entregue.

## Decisions

- Usar Markdown padrão, com índice, títulos claros, listas e uma tabela de perfis; isso melhora navegação em GitHub e leitura por avaliadores.
- Escrever a URL publicada como pendente e fornecer instrução de execução local com endereço/porta informados pelo Reflex, evitando alegar deploy concluído.
- Descrever visitante, membro e administrador separadamente; jornadas e resultados serão baseados nas rotas/telas existentes, com dependências remotas identificadas.
- Não incluir screenshots nesta rodada: não há capturas atuais verificadas do deploy. Registrar essa limitação no README e adicionar imagens quando houver uma sessão visual validada.
- Ignorar saídas de build/teste e configurações estritamente locais de editores, preservando configurações compartilhadas de agentes e arquivos de instrução que já fazem parte do repositório.

## Risks / Trade-offs

- [Documentação pode prometer ações remotas não aceitas] → limitar descrições ao que a interface expõe e identificar as dependências do Xano/Cloudinary.
- [Endereço publicado ainda não existe] → indicar estado pendente e onde inserir o link após a publicação.

## Migration Plan

Substituir o conteúdo de apresentação do `README.md` pelo manual, preservando identidade textual e as informações acadêmicas. Depois da publicação, atualizar o link de acesso e adicionar capturas verificadas sem alterar os demais passos.
