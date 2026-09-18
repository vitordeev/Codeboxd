// Query all titulos records
query titulos verb=GET {
  api_group = "Titulos"

  input {
  }

  stack {
    db.query titulos {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "86znymP5RlsFr9dbcspCD0m5J2w"
}