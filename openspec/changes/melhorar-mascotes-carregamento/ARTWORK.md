# Lume — origem e manutenção

Personagem e linguagem aprovados pelo usuário com a resposta “aprovo” à prancha Lume. Arte original construída em SVG a partir do estudo aprovado, sem saída raster gerada, personagem de terceiros, pacote de clipart ou recurso gráfico externo. O material de origem dos antigos bonecos permanece apenas em `Imagens/` como referência histórica e não é distribuído como asset de interface. `assets/mascot.png` foi removido depois da migração de seus consumidores.

## Fonte e otimização

O fonte editável das oito cenas é `tools/generate_lume_assets.py`, que contém a geometria do personagem, objetos e composição. Regenerar pela raiz:

```powershell
.venv/Scripts/python.exe tools/generate_lume_assets.py
npx --yes --package=svgo@4.0.0 svgo --folder assets/illustrations/lume --config tools/svgo-lume.config.mjs
```

SVGO é uma ferramenta de otimização; nenhum asset de sua documentação foi incorporado. Configuração preserva IDs de grupos, estrutura e variáveis da paleta. Versão 4.0.0 executada nesta entrega. O acesso inicial ao npm foi bloqueado pelo sandbox; a execução ampliada foi autorizada e concluída. O aplicativo não recebeu dependências npm adicionais.

Manifesto com tamanhos e hashes: `validation/artwork-manifest.json`. O conjunto otimizado soma 23.863 bytes e cada arquivo tem menos de 30 KB. Grupos fundo/personagem/objetos, viewBox 320×240, contorno 2px, paleta de cinco cores e sombra plana de 12%. Não há gradientes, filtros ou imagens raster.

## Consumo

`Codeboxd_main/illustrations.py` carrega somente arquivos locais de uma lista fechada e os monta em componentes SVG nativos. `Illustration(name, size)` aceita tamanhos sm/md/lg; nome desconhecido usa empty. O padrão é decorativo; `label` não vazio torna a imagem informativa. IDs recebem prefixos por instanciação. Cores são herdadas por `--illu-*`; a prévia usa `data-illustration-theme=light` para contorno escuro em fundo claro sem mudar o tema global do app.

A galeria das oito cenas está em `review/scenes.html`. 404 e offline são entregues para o catálogo/prévia sem criar novas rotas nem interpretar todo erro de provedor como falta de conexão. Mensagens, ações de repetição e contratos funcionais permanecem na interface.

Referências técnicas: https://svgo.dev/docs/preset-default/ e https://reflex.dev/docs/library/html/svg/ . São referências de API, não fontes dos desenhos.
