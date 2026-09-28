query media verb=GET {
  api_group = "Codeboxd"

  input {
  }

  stack {
    db.query media {
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "aZXoHM0FsqNrgoEWCGAFZJDnvoE"
}