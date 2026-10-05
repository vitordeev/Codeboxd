// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name filters=trim|min:1|max:80
    text username filters=trim|lower|min:3|max:30
    email email filters=trim|lower
    text password filters=min:8
  }

  stack {
    api.lambda {
      code = "return /^[a-z0-9_]{3,30}$/.test($input.username);"
    } as $valid_username
  
    precondition ($valid_username) {
      error_type = "inputerror"
      error = "Nome de usuario invalido."
    }
  
    db.query user {
      where = $db.user.email == $input.email || $db.user.username == $input.username
      return = {type: "single"}
    } as $existing
  
    precondition ($existing == null) {
      error_type = "inputerror"
      error = "E-mail ou nome de usuário indisponível."
    }
  
    db.query profile {
      where = $db.profile.username == $input.username
      return = {type: "single"}
    } as $existing_profile
  
    precondition ($existing_profile == null) {
      error_type = "inputerror"
      error = "Nome de usuário indisponível."
    }
  
    db.transaction {
      stack {
        db.add user {
          data = {
            name          : $input.name
            username      : $input.username
            email         : $input.email
            password      : $input.password
            role          : "member"
            account_status: "active"
          }
        } as $user
      
        db.add profile {
          data = {
            user_id     : $user.id
            username    : $input.username
            display_name: $input.name
            bio         : ""
            avatar_url  : ""
          }
        } as $profile
      }
    }
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken, user_id: $user.id}
  tags = ["xano:quick-start"]
  guid = "urY15kLDHVGb4vbbHON3_u2xqTk"
}