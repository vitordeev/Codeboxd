// Generate a hashed six-digit reset code, at most once per minute per account.
function "Quick Start/generate_magic_link" {
  input {
    email email filters=trim|lower
  }

  stack {
    var $result { value = null }
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "account_status"]
    } as $user

    conditional {
      if ($user != null && $user.account_status == "active") {
        db.transaction {
          stack {
            // Hold the account row lock until this transaction ends.
            db.edit user {
              field_name = "id"
              field_value = $user.id
              data = {updated_at: now}
            }
            db.get user {
              field_name = "id"
              field_value = $user.id
            } as $locked_user

            conditional {
              if ($locked_user.account_status == "active" && ($locked_user.password_reset_requested_at == null || $locked_user.password_reset_requested_at <= (now|add_secs_to_timestamp:-60))) {
                security.random_number {
                  min = 100000
                  max = 999999
                } as $number
                var $code { value = $number|to_text }

                db.edit user {
                  field_name = "id"
                  field_value = $user.id
                  data = {
                    password_reset: {token: $code, expiration: (now|add_secs_to_timestamp:900), used: false}
                    password_reset_attempts: 0
                    password_reset_requested_at: now
                    password_reset_format: "six_digits"
                  }
                }
                var.update $result {
                  value = {token: $code, email: $locked_user.email}
                }
              }
            }
          }
        }
      }
    }
  }

  // Private function result for the mailer, never a public API response.
  response = $result
  tags = ["xano:quick-start"]
  guid = "Moy1di4xbII1-v2ENoG7OW1EYwc"
}
