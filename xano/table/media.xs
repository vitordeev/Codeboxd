table media {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    text identity_key
    text external_source
    text external_id
    enum media_type { values = ["movie", "series", "anime", "book"] }
    text title filters=trim|min:1|max:500
    text description?
    text cover_url?
    int year?
    json details?
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "identity_key", op: "asc"}]}
    {type: "btree", field: [{name: "media_type", op: "asc"}]}
  ]
  guid = "UWMBCi6jmk5K-JkaQeSIQ2DW5ds"
}
