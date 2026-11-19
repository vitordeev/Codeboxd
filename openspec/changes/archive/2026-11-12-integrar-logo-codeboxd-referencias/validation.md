# Integração da logo — 08/11/2026

## Referências e análise

Foram visualizadas as nove imagens de `Imagens/`. `HomePage.png` e `MoviePage.png` mostram o cubo com `< >` na face esquerda e reprodução na direita, acompanhado do nome codeboxd. `image 3.png` é o mascote, não a logo. Não há arquivo independente da logo na pasta. Foi produzida uma reprodução vetorial manual, transparente, em `assets/codeboxd-logo.svg`; não se trata do arquivo-fonte original do autor. Mantidos os textos e layouts existentes, o mascote e os botões. A change de redesign continua cancelada.

## Implementação

O helper `_logo_icon` mantém todos os consumidores existentes e agora usa o mesmo asset local com hash de versão via `rx.asset`. Ícone decorativo com texto adjacente, dimensões reservadas, `alt` vazio e `aria-hidden`. Seis seletores de tamanho foram adaptados para aceitar imagem; `object-fit: contain` mantém a proporção. O head compilado contém favicon SVG com hash; o `.ico` anterior permanece disponível. Documentação consultada: https://reflex.dev/docs/assets/overview/ . Não foi adicionado pacote ou feita publicação.

## Evidências desta rodada

- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado em 10,016s.
- XML do SVG validado pela biblioteca padrão; sem raster, script ou dependência externa.
- Verificação de componentes no código compilado: `validation/compiled-consumers.json`, incluindo favicon no documento e referências da marca nos módulos de rotas.
- Navegador Edge headless, asset servido somente em localhost e CSS real do projeto com markup de verificação: oito casos aprovados (social, admin, recuperação e login, a 360px/1440px), imagem carregada, dimensões positivas, object-fit contain, decoração não anunciada, sem overflow ou erro JavaScript. Resultado em `validation/browser.json`, capturas `validation/logo-360.png` e `validation/logo-1440.png`; detalhe em `validation/logo-preview.png`.
- Scripts auxiliares executados: `.local/apply_codeboxd_logo.py` e `.local/check_codeboxd_logo.py` (locais/ignorados). O primeiro ensaio do verificador teve conflito no nome da chave `width`; corrigido e repetido com sucesso.
- `openspec validate integrar-logo-codeboxd-referencias --type change --strict`: aprovado após completar a documentação.

## Limites

Navegador verifica renderização local com markup de apoio; não constitui teste de navegação autenticada, screenshot de todas as páginas integradas, validação remota ou publicação. Compilação confirma integração em todas as rotas consumidoras. Nenhum servidor normal foi reiniciado e não foi usado Docker. Não foi executada novamente a suíte funcional por se tratar de substituição de asset/estilos de tamanho sem alteração de eventos ou estado.

Conferência final: dimensões nativas fornecidas por `custom_attrs`, para que estilos inline não anulem os tamanhos responsivos; verificado no JSX real do helper. Recompilação final aprovada em 14,499s. Foram identificados 22 módulos compilados com a referência versionada da marca. O verificador de consumidores foi ajustado para incluir arquivos `.jsx`, além de `.js`.
