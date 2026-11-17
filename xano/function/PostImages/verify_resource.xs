function "PostImages/verify_resource" {
  input {
    json reservation
    int user_id filters=min:1
    int version filters=min:1
  }
  stack {
    api.lambda {
      code = "const r = $input.reservation; return !!r && r.user_id === $input.user_id && r.cloud && /^[A-Za-z0-9_-]+$/.test(r.cloud) && new RegExp('^codeboxd/posts/u' + $input.user_id + '/[a-f0-9]{32}$').test(r.public_id) && ['reserved','verified','reconciliation_required'].includes(r.state);"
    } as $valid_reservation
    precondition ($valid_reservation && $input.reservation.cloud == $env.CLOUDINARY_CLOUD_NAME && $env.CLOUDINARY_API_KEY != null && $env.CLOUDINARY_API_SECRET != null) {
      error_type = "accessdenied"
      error = "A reserva da imagem não pôde ser verificada."
    }
    api.lambda {
      code = "return encodeURIComponent($input.reservation.public_id);"
    } as $encoded_id
    var $credentials { value = ($env.CLOUDINARY_API_KEY ~ ":" ~ $env.CLOUDINARY_API_SECRET)|base64_encode }
    var $lookup { value = null }
    try_catch {
      try {
        api.request {
          url = "https://api.cloudinary.com/v1_1/" ~ $input.reservation.cloud ~ "/resources/image/upload/" ~ $encoded_id
          method = "GET"
          headers = ["Authorization: Basic " ~ $credentials]
        } as $provider_response
        conditional {
          if ($provider_response.response.status == 200) {
            var.update $lookup { value = $provider_response.response.result }
          }
        }
      }
      catch {
        var.update $lookup { value = null }
      }
    }
    api.lambda {
      code = "const r=$var.lookup, expected=$input.reservation; if (!r || r.public_id !== expected.public_id || r.resource_type !== 'image' || r.type !== 'upload' || r.version !== $input.version || typeof r.asset_id !== 'string' || !r.asset_id || !['png','jpg','jpeg','webp','gif'].includes(r.format)) return null; if (['width','height','bytes','version'].some(k=>!Number.isInteger(r[k]) || r[k]<=0) || r.bytes>5242880) return null; const url='https://res.cloudinary.com/' + expected.cloud + '/image/upload/v' + r.version + '/' + expected.public_id + '.' + r.format; if (r.secure_url!==url || (expected.asset_id && expected.asset_id!==r.asset_id) || (expected.version && expected.version!==r.version)) return null; return {public_id:r.public_id,asset_id:r.asset_id,version:r.version,format:r.format,bytes:r.bytes,width:r.width,height:r.height,url};"
    } as $verified
    precondition ($verified != null) {
      error_type = "inputerror"
      error = "A imagem ainda não pôde ser confirmada. A operação permanece pendente."
    }
  }
  response = $verified
  guid = "CBPostImageVerifyResource20261117"
}
