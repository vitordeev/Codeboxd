function "Lists/default_list_status" {
  input {
    int user_id filters=min:1
    text? default_key?
  }
  stack {
    var $planned { value = $input.user_id ~ ":planned" }
    var $completed { value = $input.user_id ~ ":completed" }
    precondition ($input.default_key == null || $input.default_key == $planned || $input.default_key == $completed) {
      error_type = "inputerror"
      error = "Identidade da lista padrão inválida."
    }
    api.lambda {
      code = "if ($input.default_key === $var.planned) return 'want_to_watch'; if ($input.default_key === $var.completed) return 'watched'; return null;"
    } as $status
  }
  response = $status
  guid = "CBDefaultListStatus20261103"
}
