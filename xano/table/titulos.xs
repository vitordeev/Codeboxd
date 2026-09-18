// Stores catalog items (movies, anime, games, books) managed by the admin panel.
table titulos {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text nome filters=trim
  
    // Content type: which section of the catalog this item belongs to.
    enum categoria {
      values = ["filme", "anime", "game", "livro"]
    }
  
    text sinopse? filters=trim
    int ano?
    text genero? filters=trim
  
    // Publication status: only "publicado" items should show on the public home page.
    enum status? {
      values = ["rascunho", "publicado"]
    }
  
    image? capa?
    timestamp? updated_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "categoria", op: "asc"}]}
    {type: "btree", field: [{name: "status", op: "asc"}]}
  ]

  tags = ["cubo:admin"]
  guid = "_a-lU-wWDBEmTLNpEEsS_Zf_Ygk"
}