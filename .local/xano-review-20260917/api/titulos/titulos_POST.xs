// Add titulos record
query titulos verb=POST {
  api_group = "Titulos"

  input {
    dblink {
      table = "titulos"
    }
  }

  stack {
    db.add titulos {
      enforce_hidden_fields = false
      data = {
        created_at: $input.created_at
        nome      : $input.nome
        categoria : $input.categoria
        sinopse   : $input.sinopse
        ano       : $input.ano
        genero    : $input.genero
        status    : $input.status
        capa      : $input.capa
        updated_at: $input.updated_at
      }
    } as $model
  }

  response = $model
  guid = "Ti-cLy33B4PwDXWnz7a6YHZx_SA"
}