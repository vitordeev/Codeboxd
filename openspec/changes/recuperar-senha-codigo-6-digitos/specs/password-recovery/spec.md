## Purpose

Permitir recuperar o acesso à conta Codeboxd por um código numérico de seis
dígitos recebido no e-mail cadastrado, com prazo e uso controlados.

## ADDED Requirements

### Requirement: Código de seis dígitos por e-mail
O sistema MUST gerar e enviar ao e-mail cadastrado de uma conta ativa um código
de exatamente seis dígitos ASCII, sem incluí-lo na resposta pública ou nos logs.
O sistema MUST apresentar resposta genérica para solicitações de contas
inexistentes/desativadas e guardar o código somente como hash no banco.

#### Scenario: Conta ativa solicita recuperação
- **WHEN** a pessoa informa o e-mail de sua conta ativa
- **THEN** ela recebe um e-mail com código de seis dígitos e instruções para redefinir a senha

#### Scenario: E-mail sem conta ativa
- **WHEN** o e-mail informado não pertence a uma conta ativa
- **THEN** a resposta pública mantém a mensagem genérica e nenhum código é emitido

### Requirement: Expiração e proteção de tentativas
O código MUST expirar em 15 minutos, ser consumido uma única vez e permitir no
máximo cinco tentativas de validação. O sistema MUST limitar geração/envio a uma
vez a cada 60 segundos por conta, invalidar o anterior ao emitir novo código e
serializar validações concorrentes para impedir reutilização ou perda de contagem.

#### Scenario: Código válido
- **WHEN** a pessoa envia o código correto dentro do prazo e limite de tentativas
- **THEN** o sistema aceita a prova e a consome para permitir a troca de senha

#### Scenario: Código inválido, expirado ou usado
- **WHEN** o código é incorreto, expirou, foi consumido ou esgotou cinco tentativas
- **THEN** a senha permanece intacta e o sistema pede um novo código sem revelar dados da conta

#### Scenario: Reenvio imediato
- **WHEN** outro envio é solicitado antes de 60 segundos
- **THEN** a resposta permanece genérica, sem enviar outro e-mail ou invalidar o código atual

#### Scenario: Novo código depois do intervalo
- **WHEN** a conta solicita novo código depois de 60 segundos
- **THEN** o código anterior deixa de funcionar e o novo inicia outro prazo e limite

### Requirement: Formulário e troca de senha
O formulário MUST aceitar apenas seis dígitos e senha/confirmação válidas antes de
enviar a validação. Após a troca, o sistema MUST orientar novo login sem persistir
a credencial temporária de recuperação como sessão normal no navegador.

#### Scenario: Formato incorreto
- **WHEN** a pessoa informa letras, UUID, menos ou mais de seis dígitos
- **THEN** o formulário pede exatamente seis dígitos e não envia a validação

#### Scenario: Senha redefinida
- **WHEN** o código válido é confirmado e as novas senhas atendem às regras
- **THEN** a nova senha funciona no login e a anterior deixa de funcionar
