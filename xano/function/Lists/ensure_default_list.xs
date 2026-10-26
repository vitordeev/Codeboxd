function "Lists/ensure_default_list" {
  input {
    int user_id
    text default_kind filters=trim
  }
  stack {
    precondition ($input.user_id > 0 && ($input.default_kind == "planned" || $input.default_kind == "completed")) {
      error_type = "inputerror"
      error = "Lista padrão inválida."
    }
    var $key { value = $input.user_id ~ ":" ~ $input.default_kind }
    db.get user_list {
      field_name = "default_key"
      field_value = $key
    } as $result
    conditional {
      if ($result == null) {
        api.lambda {
          code = "return $input.default_kind === 'planned' ? {title:'Quero ver / ler', description:'Obras para descobrir depois.'} : {title:'Já assisti / li', description:'Obras que você já terminou.'};"
        } as $defaults
        try_catch {
          try {
            db.add user_list {
              data = {user_id: $input.user_id, default_key: $key, title: $defaults.title, description: $defaults.description, is_public: true, updated_at: now}
            } as $result
          }
          catch {
            // A competing request may have inserted the unique key first.
            db.get user_list {
              field_name = "default_key"
              field_value = $key
            } as $result
          }
        }
      }
    }
    precondition ($result != null && $result.user_id == $input.user_id && $result.default_key == $key) {
      error_type = "standard"
      error = "Não foi possível preparar sua lista padrão."
    }
  }
  response = $result
  guid = "Waq6O0hSEgPjZrB9CivK4X2fM"
}
