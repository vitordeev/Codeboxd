query "profiles/{user_id}" verb=GET {
 api_group = "Codeboxd"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100
int user_id
 }
 stack {
db.query profile {
 where = $db.profile.user_id == $input.user_id
 return = {type: "single"}
} as $profile
precondition ($profile != null) {
  error_type = "notfound"
  error = "Perfil não encontrado."
}
db.query user_media_interaction {
 where = $db.user_media_interaction.user_id == $input.user_id
 sort = {user_media_interaction.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $interactions
db.query user_follow {
 where = $db.user_follow.followed_id == $input.user_id
 sort = {user_follow.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $followers
db.query user_follow {
 where = $db.user_follow.follower_id == $input.user_id
 sort = {user_follow.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $following
 }
 response = {profile: $profile, interactions: $interactions, followers: $followers, following: $following}
 guid = "KN99IAk_SICbNLL9IZnwXi_oBCU"
}
