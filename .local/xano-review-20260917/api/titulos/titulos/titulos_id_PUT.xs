// Update titulos record
query "titulos/{titulos_id}" verb=PUT {
  api_group = "Titulos"

  input {
    int titulos_id? filters=min:1
    dblink {
      table = "titulos"
    }
  }

  stack {
    db.edit titulos {
      field_name = "id"
      field_value = $input.titulos_id
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
  guid = "c7eNodCwO1bJZMVQ3vFUPkkxFrM"
}