// Request a six-digit code only for an eligible, active account.
query "reset/request-reset-link" verb=GET {
  api_group = "Authentication"
  input {
    email email filters=trim|lower
  }
  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "account_status"]
    } as $reset_account
    precondition ($reset_account != null && $reset_account.account_status == "active") {
      error_type = "notfound"
      error = "Não encontramos uma conta ativa com esse e-mail. Confira o endereço informado."
    }
    function.run "Quick Start/generate_magic_link" {
      input = {email: $input.email}
    } as $token_and_email

    conditional {
      if ($token_and_email != null) {
        // Only generated digits are inserted; no template placeholders in mail.
        var $message {
          value = "<!doctype html>\n<html lang=\"pt-BR\">\n<head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Seu código Codeboxd</title></head>\n<body style=\"margin:0;padding:0;background:#0d0d0f;color:#f4f2ec;font-family:Arial,Helvetica,sans-serif;-webkit-text-size-adjust:100%\">\n<div style=\"display:none;font-size:1px;line-height:1px;max-height:0;overflow:hidden;mso-hide:all\">Seu código para redefinir a senha. Válido por 15 minutos.</div>\n<table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\" style=\"background:#0d0d0f\"><tr><td align=\"center\" style=\"padding:36px 16px\">\n<table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\" style=\"max-width:480px\">\n<tr><td style=\"padding:0 0 24px;font-size:27px;font-weight:800;letter-spacing:-1px;color:#faf8f2\">code<span style=\"color:#f5b300\">boxd</span></td></tr>\n<tr><td style=\"height:4px;background:#f5b300;border-radius:12px 12px 0 0;font-size:1px;line-height:4px\">&nbsp;</td></tr>\n<tr><td style=\"padding:30px 24px;background:#18181b;border:1px solid #303034;border-top:0;border-radius:0 0 12px 12px\">\n<p style=\"margin:0 0 14px;color:#f5b300;font-size:10px;font-weight:700;letter-spacing:2px\">RECUPERAÇÃO DE ACESSO</p>\n<h1 style=\"margin:0 0 12px;font-size:28px;line-height:1.2;letter-spacing:-.7px;color:#faf8f2\">De volta às suas histórias.</h1>\n<p style=\"margin:0 0 24px;font-size:14px;line-height:1.65;color:#b9b6c0\">Use este código na página de recuperação para criar sua nova senha.</p>\n<table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tr><td align=\"center\" style=\"padding:22px 8px;background:#0d0d0f;border:1px solid #4f4324;border-radius:10px\">\n<p style=\"margin:0 0 10px;color:#a6a2ad;font-size:10px;letter-spacing:1.6px\">SEU CÓDIGO</p>\n<p style=\"margin:0;color:#f5b300;font-size:34px;font-weight:700;line-height:1.25;letter-spacing:5px;font-family:Consolas,monospace;white-space:nowrap\">" ~ $token_and_email.token ~ "</p>\n</td></tr></table>\n<p style=\"margin:16px 0 24px;font-size:12px;color:#aaa6b0;text-align:center;line-height:1.6\">Válido por <strong style=\"color:#f4f2ec\">15 minutos</strong> · Uso único</p>\n<p style=\"margin:0;padding-top:20px;border-top:1px solid #303034;color:#92909a;font-size:12px;line-height:1.65\">Não pediu para trocar a senha? Ignore esta mensagem. Sua senha continua a mesma. Nunca compartilhe este código.</p>\n</td></tr>\n<tr><td style=\"padding:22px 0;color:#77737f;font-size:11px;line-height:1.65\">Codeboxd · Suas histórias, no mesmo lugar.<br>Mensagem automática de segurança.</td></tr>\n</table></td></tr></table>\n</body></html>\n"
        }
        var $plain_message {
          value = "Codeboxd - Recuperacao de acesso\n\nSeu codigo: " ~ $token_and_email.token ~ "\n\nUse este codigo na pagina de recuperacao para criar sua nova senha.\nValido por 15 minutos. Uso unico.\n\nSe voce nao solicitou a troca, ignore esta mensagem. Sua senha continua a mesma. Nunca compartilhe este codigo."
        }
        precondition ($env.SENDGRID_API_KEY != null && $env.SENDGRID_API_KEY != "" && $env.SENDGRID_FROM != null && $env.SENDGRID_FROM != "") {
          error_type = "inputerror"
          error = "Não foi possível enviar o código de recuperação. Tente novamente mais tarde."
        }
        var $delivery_accepted { value = false }
        try_catch {
          try {
            api.request {
              url = "https://api.sendgrid.com/v3/mail/send"
              method = "POST"
              params = {
                from: {email: $env.SENDGRID_FROM, name: "Codeboxd"}
                personalizations: [{to: [{email: $token_and_email.email}]}]
                subject: "Seu código de 6 dígitos para recuperar a senha do Codeboxd"
                content: [{type: "text/plain", value: $plain_message}, {type: "text/html", value: $message}]
                tracking_settings: {
                  click_tracking: {enable: false, enable_text: false}
                  open_tracking: {enable: false}
                  subscription_tracking: {enable: false}
                }
              }
              headers = ["Content-Type: application/json", "Authorization: Bearer " ~ $env.SENDGRID_API_KEY]
              timeout = 15
            } as $delivery
            var.update $delivery_accepted {
              value = $delivery.response.status == 202
            }
          }
          catch {
            var.update $delivery_accepted { value = false }
          }
        }
        precondition ($delivery_accepted) {
          error_type = "inputerror"
          error = "Não foi possível enviar o código de recuperação. Tente novamente mais tarde."
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
