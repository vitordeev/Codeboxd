table post_image_asset {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    timestamp updated_at?=now
    int user_id
    int? post_id?
    text operation_key filters=trim|min:32|max:32
    enum operation { values = ["create", "replace"] }
    enum state?="reserved" { values = ["reserved", "verified", "attached", "reconciliation_required", "cleanup_pending", "deleted"] }
    int expected_image_revision?=0 filters=min:0
    text cloud filters=trim|max:80
    text public_id filters=trim|max:200
    text? asset_id? filters=trim|max:200
    int? version?
    text? format? filters=trim|max:10
    int? bytes?
    int? width?
    int? height?
    timestamp? retain_until?
    text? last_error_code? filters=trim|max:80
    int attempt_count?=0 filters=min:0
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "cloud", op: "asc"}, {name: "public_id", op: "asc"}]}
    {type: "btree|unique", field: [{name: "user_id", op: "asc"}, {name: "operation_key", op: "asc"}]}
    {type: "btree", field: [{name: "post_id", op: "asc"}]}
    {type: "btree", field: [{name: "state", op: "asc"}, {name: "retain_until", op: "asc"}, {name: "id", op: "asc"}]}
  ]
  guid = "CBPostImageAsset20261117"
}
