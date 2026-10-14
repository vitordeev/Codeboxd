## 1. Contratos de recuperação

- [x] 1.1 Implementar esquema aditivo, geração de seis dígitos, prazo de 15 minutos, cooldown e e-mail; verificar contratos no dry-run e confirmar geração/hash/cooldown em execução controlada.
- [x] 1.2 Implementar validação de formato, conta ativa, prazo, cinco tentativas persistidas, uso único e token temporário de cinco minutos; verificar rejeições, concorrência e consumo no Xano real.

## 2. Interface e testes locais

- [x] 2.1 Ajustar campo e mensagens para seis dígitos e bloquear entradas inválidas sem requisição; verificar testes de formato, troca, falhas e não persistência do token.
- [x] 2.2 Verificar formulário em desktop/celular e código inválido no navegador, preservando a senha; registrar screenshots privados e resumo sem segredos.
- [x] 2.3 Executar suíte, compilação e validação estrita OpenSpec, atualizar P.6/contexto/evidências e registrar os limites das verificações.

## 3. Publicação e entrega real

- [x] 3.1 Exportar estrutura, revisar delta limitado e publicar contratos de reset; verificar dry-run posterior sem mudanças, sem importar registros/segredos.
- [ ] 3.2 Comprovar chegada do e-mail com seis dígitos, troca de senha, novo login e rejeição de reutilização em conta com caixa controlada; registrar resultado e restauração segura da conta de teste.

Evidências e limites: [implementacao-2026-10-14.md](validation/implementacao-2026-10-14.md).
