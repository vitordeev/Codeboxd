---
name: ilustracao-com-identidade
description: Use ao criar, substituir ou revisar ilustrações, personagens, mascote ou estados vazios e de erro do Codeboxd. Mantém um conjunto original em SVG na paleta laranja e preto, sem clipart genérico ou saída crua de IA.
---

# Ilustração com identidade

As ilustrações do Codeboxd devem parecer desenhadas por uma pessoa com ponto de vista. Esta skill registra a direção fornecida pelo usuário e complementa o contrato de ilustrações do OpenSpec. O contrato vigente das ilustrações está em [character-illustrations](../../../openspec/changes/melhorar-mascotes-carregamento/specs/character-illustrations/spec.md), na change ativa `melhorar-mascotes-carregamento`. A antiga change de redesign foi excluída; não a recriar nem usar seus caminhos como referência. Conferir a change ativa antes de editar e registrar decisões, origem dos assets e evidências em `openspec/`.

## Evitar aparência amadora ou genérica

- Não variar proporções, traço ou estilo entre cenas.
- Não usar cores, gradientes ou brilhos fora da paleta.
- Evitar rostos e mãos detalhados, anatomia estranha e objetos aleatórios sem narrativa.
- Evitar contornos com espessuras diferentes, sombras sem coerência e pessoas sem rosto em cores pastel sobre um laptop.

## Regras do conjunto

- **Paleta fechada:** laranja da marca, preto quente, off-white, mais um neutro e um acento. Exatamente esses cinco papéis, via variáveis `--illu-*` com valores adequados aos temas claro e escuro.
- **Formas:** círculos, retângulos arredondados e arcos, poucos pontos e curvas limpas.
- **Traço:** escolher um para todo o conjunto: sem contorno ou contorno único de 2px. A direção vigente da change escolhe **contorno único de 2px**.
- **Personagem:** cabeça aproximadamente 1/3 do corpo, mãos e pés simplificados, olhos em ponto e boca em um traço. Sem detalhes anatômicos. Um detalhe de assinatura reconhecível e proporções constantes.
- **Sombra:** uma forma plana com 10–15% de opacidade, sem degradê.
- **Fundo:** uma ou duas formas orgânicas simples, blob ou arco, em laranja suave.
- **Grão:** opcional, sutil e igual no conjunto.

## Fluxo

1. **Prancha primeiro:** antes de qualquer cena, criar uma prancha com paleta, traço, um personagem em três poses, três expressões e seis objetos de apoio. Apresentar a prancha e registrar aprovação explícita do usuário no OpenSpec. Não produzir as cenas antes dessa aprovação; um pedido genérico de implementação não aprova uma prancha ainda não apresentada.
2. **Mascote opcional, recomendado:** criar personagem original, simples e reconhecível, com forma-base clara e um detalhe de assinatura. Não derivar de personagens, mascotes ou marcas existentes.
3. **Uma cena, uma ideia:** personagem, um ou dois objetos e fundo. Simplificar se a ideia depender de legenda para ser entendida. Manter mensagem e ação da interface independentes da imagem.
4. **Oito cenas mínimas:** onboarding, vazio, 404, 500, sucesso, carregando, offline e sem resultados. Integrar aos estados existentes e mostrar as oito na prévia, sem inventar novos contratos de backend.
5. **SVG:** viewBox fixo, grupos nomeados de personagem/fundo e cores `var(--illu-*)`. Usar identificadores únicos por instância. Preferir SVG inline no componente para herdar variáveis CSS; `<img src="arquivo.svg">` não herda automaticamente as variáveis do documento.
6. **SVGO:** otimizar, registrar versão e comando e manter cada SVG abaixo de 30 KB. Preservar viewBox, variáveis, grupos necessários e acessibilidade.
7. **Componente `Illustration`:** aceitar `name` e `size`, reservar dimensões e oferecer fallback seguro para nomes desconhecidos. Quando decorativa, `aria-hidden="true"`; quando informativa, `role="img"` e `aria-label` localizado.
8. **Validar:** mostrar o conjunto lado a lado, testar em temas claro e escuro e nas larguras 360px e 1440px. Uma prévia isolada pode demonstrar os dois temas sem adicionar tema claro global ao aplicativo. Conferir dimensões estáveis durante carregamento e falha.
9. **Retirar antigos:** após integrar o conjunto aprovado, conferir consumidores e remover do repositório de trabalho os bonecos e assets ilustrativos substituídos. Preservar histórico Git, capas reais, uploads, avatares e marca. Não apagar arquivos apenas por parecerem antigos.

## Se houver geração de imagens ou vetores

Usar a prancha aprovada como referência. Solicitar formas simples, cores chapadas, fundo transparente e ausência de texto. Tratar a saída como rascunho: redesenhar em SVG no mesmo grid, ajustar proporção, cortar detalhes e forçar a paleta. Nunca publicar a saída crua. Escolher variações pela consistência com o conjunto.

## Originalidade e direitos

Criar personagens e cenas originais. Não reproduzir personagens, mascotes, logotipos ou obras existentes, nem estilos que identifiquem um artista específico. Usar fontes, ícones e assets com licença compatível e registrar origem e licença de qualquer item de terceiros no OpenSpec.

## Checklist de revisão

- [ ] Prancha apresentada e aprovada antes das cenas?
- [ ] Todas as cenas parecem do mesmo conjunto lado a lado?
- [ ] Somente cores da paleta, sem gradiente nem brilho?
- [ ] Traço e sombra idênticos em todas?
- [ ] Cada cena comunica uma ideia em dois segundos?
- [ ] Rostos e mãos simples, sem anatomia estranha?
- [ ] As oito cenas mínimas foram entregues?
- [ ] Funciona nos temas claro e escuro, com aria-hidden ou nome acessível correto?
- [ ] SVG otimizado com SVGO, abaixo de 30 KB e sem deslocamento de layout?
- [ ] Bonecos antigos efetivamente substituídos foram removidos e não há referências quebradas?
- [ ] Autoria e licenças registradas no OpenSpec?
