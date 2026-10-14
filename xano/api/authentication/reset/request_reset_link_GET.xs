// Request a six-digit code without revealing whether an account exists.
query "reset/request-reset-link" verb=GET {
  api_group = "Authentication"
  input {
    email email filters=trim|lower
  }
  stack {
    function.run "Quick Start/generate_magic_link" {
      input = {email: $input.email}
    } as $token_and_email

    conditional {
      if ($token_and_email != null) {
        // Only generated digits are inserted; no template placeholders in mail.
        var $message {
          value = "<!DOCTYPE html><html><body style=\"font-family:Arial,sans-serif;line-height:1.6;color:#333\"><div style=\"max-width:600px;margin:20px auto;padding:20px;border:1px solid #ddd;border-radius:8px\"><h2>Redefinir senha do Codeboxd</h2><p>Seu código de recuperação é:</p><p style=\"padding:18px;background:#080808;color:#f5b300;font-size:28px;font-weight:bold;letter-spacing:4px;text-align:center\">" ~ $token_and_email.token ~ "</p><p>Este código tem 6 dígitos, expira em 15 minutos e só pode ser usado uma vez.</p><p>Informe-o na página de redefinição e escolha sua nova senha. Se você não pediu a recuperação, ignore este e-mail.</p><p>Codeboxd</p></div></body></html>"
        }
        util.send_email {
          service_provider = "xano"
          to = $token_and_email.email
          subject = "Seu código de 6 dígitos para recuperar a senha do Codeboxd"
          message = $message
        }
      }
    }
  }
  response = {
    message: {
      success: true
      message: "Se o e-mail estiver cadastrado, você receberá um código de 6 dígitos."
    }
  }
  tags = ["xano:quick-start"]
  guid = "f3THZ4ZNIuWXhP86ujrorYTZZPs"
}
