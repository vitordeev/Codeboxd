# Limites, alternativas e prontidão — 11/11/2026

## Escopo desta revisão

Usuário autorizou continuar Cloudinary e pediu conferir limites e alternativas.
Branch `task/cloudinary-limites-20261111`, base `origin/main` em `faa655f`, após
integração da PR #33. A develop remota continua em `29d0456`; usar somente ela
descartaria a preparação já integrada. Nenhuma branch existente foi reescrita.
Revisão vinculada a 1.3 e às dependências de 2.1/2.2; mantido **3/5**.

## Estado local verificado

Atualização posterior: usuário confirmou preenchimento e a leitura encontrou as
três variáveis. GET /usage autenticado confirmou Free, 0/25 créditos e nenhum
recurso, mantendo flag false. [Prévia e evidência atual](preflight-cloudinary-2026-11-11.md).
Os parágrafos seguintes preservam a investigação antes do preenchimento.

O usuário informou ter preenchido as credenciais. A leitura booleana dos `.env`
na raiz e nas worktrees registradas não encontrou os três valores Cloudinary;
somente a raiz possui esse arquivo. Flag da raiz permanece false. Solicitado
somente o caminho do arquivo usado pelo usuário, sem valores no chat.
Isso não prova ausência em outra máquina/pasta. Sem credenciais localizadas,
não foi consultado plano, consumo ou validade da chave da conta Cloudinary.

O adaptador assinado existe, mas nenhum fluxo de posts o chama. SocialState
envia `image_upload`; os contratos locais POST/PUT ainda usam
`storage.create_image`. Leitura compatível com URL não demonstra persistência
externa nem substituição/exclusão funcionando. Não houve nova consulta remota
da estrutura Xano nesta rodada.

## Cotas públicas Cloudinary

O plano gratuito de Image and Video APIs oferece **25 créditos**, compartilhados
entre recursos, não três franquias independentes. Referência típica de imagens:
um crédito equivale a 1 GB armazenado, 1 GB entregue ou 1.000 transformações
comuns. Derivadas e backups também ocupam armazenamento. Não confundir esse
plano com o trial do produto DAM.

Armazenamento mede o total atual; tráfego e transformações do Free usam janela
móvel de 30 dias. Reutilizar uma derivada não repete sua transformação, mas a
entrega continua consumindo tráfego. Cota não é garantia de uso ilimitado.

Fontes oficiais consultadas em 11/11/2026:
[plano](https://cloudinary.com/pricing),
[medição e períodos](https://cloudinary.com/documentation/billing_and_plans).
O painel/contrato da conta deve confirmar sua franquia específica.

Exemplo apenas ilustrativo: 5 GB armazenados + 10 GB entregues + 2.000
transformações comuns resultariam aproximadamente em 17 créditos. Não é medição
do Codeboxd, capacidade garantida de usuários nem previsão de custos.

## Alternativa avaliada

**Cloudflare R2 Standard:** franquia mensal de 10 GB-mês, um milhão de operações
classe A e dez milhões classe B. Saída para internet sem tarifa de egress.
Além da franquia: US$ 0,015/GB-mês, US$ 4,50/milhão classe A e US$ 0,36/milhão
classe B, observadas unidades de arredondamento. Armazenamento/operações não
são gratuitos ilimitados; camadas como Workers podem ter custos próprios.
[Preços oficiais](https://developers.cloudflare.com/r2/pricing/).

R2 não é substituição imediata do adaptador Cloudinary. Requer upload assinado,
URLs/controle de acesso, ciclo de vida e processamento de imagens próprios.
O acesso público `r2.dev` tem limite de requisições e é destinado a desenvolvimento;
a opção direta de produção usa domínio próprio. Como o usuário informou não ter
domínio, isso adiciona uma dependência; outra camada de entrega precisaria ser
planejada e ter seus limites verificados.
[Entrega pública oficial](https://developers.cloudflare.com/r2/buckets/public-buckets/).

Não foi identificado serviço que possa ser recomendado como gratuito e sem
limites de armazenamento, tráfego e operações para este aplicativo. Hospedagem
própria também depende de disco, banda, backups, disponibilidade e manutenção;
não foi proposta nem criada infraestrutura adicional.

## Recomendação e medidas propostas

Manter Cloudinary como candidato para a primeira integração: adaptador existente,
CDN e endereço de entrega sem depender de domínio próprio. Decisão condicionada
à localização das credenciais e à leitura do plano/consumo reais. Considerar R2
se o tráfego justificar a implementação e a configuração de entrega adicionais.
Nenhuma troca de provedor, compra ou nova conta foi executada.

Para reduzir consumo, propor compressão/redimensionamento antes do envio,
miniaturas com poucas dimensões fixas, carregamento de imagens sob demanda e
acompanhamento de créditos. O limite atual de entrada é 5 MiB; isso não significa
que comprima a imagem. As medidas são propostas, não implementações desta rodada.
Qualquer limpeza futura exige comprovar autoria e ausência de referências;
não remover automaticamente imagens antigas ou assets após timeout incerto.

Próximos passos: localizar configuração privada; leitura do consumo sem listar
assets; detalhar contrato aditivo e ciclo de vida; revisar backup/prévia antes
de qualquer publicação Xano. Upload e limpeza descartáveis exigem autorização
específica. Nenhuma imagem real acessada, alterada ou excluída nesta rodada.

## Validação local

Na nova worktree, com Python da `.venv`, sem Docker:

- `unittest discover -s tests -p test_cloudinary_uploads.py -q`: 7 aprovados.
- `unittest discover -s tests -p test_post_interactions.py -q`: 11 aprovados.
- `unittest discover -s tests -p test_uploads.py -q`: 4 aprovados.
- `openspec validate hospedar-imagens-publicacoes-cloudinary --type change`: válido.

Total: 22 testes locais; transporte Cloudinary simulado. Não houve ensaio real,
ativação, mudança de configuração, alteração funcional ou reinício do app.
