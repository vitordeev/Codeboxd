query profiles verb=GET {
  api_group = "Codeboxd"

  input {
  }

  stack {
    db.query profile {
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "UgGkVqSec1JtB7reKdgaBw6U3Zo"
}