table post {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    int media_id? { table = "media" }
    image image?
    text body filters=trim|min:1|max:5000
    bool spoiler?
    timestamp updated_at?=now
    text? image_provider? filters=trim|max:20
    text? image_public_id? filters=trim|max:200
    int? image_version?
    text? image_url? filters=trim|max:500
    int? image_asset_record_id?
    int image_revision?=0 filters=min:0
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "media_id", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}, {name: "id", op: "desc"}]}
    {type: "btree|unique", field: [{name: "image_asset_record_id", op: "asc"}]}
  ]
  guid = "yj4R8prcVHksFpDqZrhTa7L6j3g"
}
