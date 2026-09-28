from pathlib import Path
p=Path('xano/api/codeboxd/media_POST.xs'); s=p.read_text(encoding='utf8')
a=s.index('conditional {\n if ($existing == null)')
b=s.index('\n }\n response = $result',a)
s=s[:a]+'''api.lambda {
 code = "const i = $input; const mal = String((i.details || {})['MyAnimeList ID'] || ''); return i.external_source === 'kitsu' && /^[0-9]+$/.test(mal) ? 'jikan:anime:' + mal : i.external_source + ':' + i.media_type + ':' + i.external_id;"
} as $legacy_key
db.get media {
 field_name = "identity_key"
 field_value = $legacy_key
} as $legacy_existing
conditional {
 if ($existing != null) {
  var $result { value = $existing }
 }
 else {
  conditional {
   if ($legacy_existing != null) {
    var $result { value = $legacy_existing }
   }
   else {
    db.add media {
     data = {identity_key: $key, external_source: $input.external_source, external_id: $input.external_id, media_type: $input.media_type, title: $input.title, description: $input.description, cover_url: $input.cover_url, year: $input.year, details: $input.details}
    } as $result
   }
  }
 }
}''' + s[b:]
p.write_text(s,encoding='utf8')
