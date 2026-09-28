// Request a one-time magic link to reset password
query "reset/request-reset-link" verb=GET {
  api_group = "Authentication"

  input {
    email email?
  }

  stack {
    // Generate a one-time magic link
    function.run "Quick Start/generate_magic_link" {
      input = {email: $input.email}
    } as $token_and_email
  
    // Check that the link exists
    precondition ($token_and_email != null) {
      error = "Magic link could not be created. Try again."
    }

    var $reset_code {
      value = $token_and_email.token
    }
  
    // Send the one-time credential as a code for the CodeBoxd reset form.
    util.template_engine {
      value = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Redefinir senha do CodeBoxd</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2>Redefinição de senha</h2>
            <p>Recebemos um pedido para redefinir a senha da sua conta CodeBoxd.</p>
            <p>Na página de redefinição, informe este código:</p>
            <p style="text-align: center; margin: 30px 0; padding: 18px; background: #080808; color: #f5b300; font-size: 24px; font-weight: bold; letter-spacing: 2px;">
              {{ $var.reset_code }}
            </p>
            <p>O código expira em 60 minutos e só pode ser usado uma vez. Se você não pediu a redefinição, ignore esta mensagem.</p>
            <p>CodeBoxd</p>
          </div>
        </body>
        </html>
        """
    } as $message
  
    // Send the password reset code
    util.send_email {
      service_provider = "xano"
      to = $token_and_email.email
      subject = "Código para redefinir sua senha do CodeBoxd"
      message = $message
    } as $send_email
  }

  response = {
    message: {}|set:"success":true|set:"message":"reset code sent"
  }

  tags = ["xano:quick-start"]
  guid = "f3THZ4ZNIuWXhP86ujrorYTZZPs"
}
