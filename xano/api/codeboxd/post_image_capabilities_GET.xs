query "post-image-capabilities" verb=GET {
  api_group = "Codeboxd"
  input {
  }
  stack {
    var $enabled {
      value = $env.CLOUDINARY_UPLOADS_ENABLED == "true" && $env.CLOUDINARY_POST_IMAGES_CONTRACT_READY == "true"
    }
  }
  response = {contract_version: 1, uploads_enabled: $enabled, max_bytes: 5242880}
  guid = "CBPostImageCapabilities20261117"
}
