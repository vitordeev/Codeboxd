# Arquitetura alvo

## Fluxo principal

```text
Usuário
   ↓
Frontend
   ↓
API do Xano
   ├── Autenticação
   ├── Dados do CodeBoxd
   ├── Regras de negócio
   └── Integrações com fontes externas
             ↓
      APIs de filmes, séries,
      animes e livros
```

## Frontend

O frontend deverá:

- Exibir páginas de início, busca, detalhes, feed e perfil.
- Gerenciar formulários e interações do usuário.
- Consumir as APIs do Xano.
- Manter o token de autenticação de forma segura.
- Não depender diretamente de várias APIs externas.

## Backend Xano

O Xano deverá:

- Autenticar usuários.
- Persistir perfis, mídias e interações.
- Controlar ownership e autorização.
- Expor endpoints de busca, detalhes e atividades.
- Normalizar dados das fontes externas.
- Evitar duplicação de mídias.
- Servir o feed e as listas.
- Registrar eventos relevantes para auditoria.

## Fontes externas

As fontes externas deverão fornecer dados detalhados de obras. O CodeBoxd não deverá copiar integralmente seus catálogos.

O backend deverá normalizar respostas externas para uma representação comum e preservar:

- Fonte externa.
- Identificador externo.
- Tipo da mídia.
- Dados básicos necessários para exibição e relacionamento.

## Limites de responsabilidade

| Camada | Responsabilidade |
|---|---|
| Frontend | Apresentação, navegação e interação |
| Xano | Autenticação, autorização, persistência e regras |
| Adaptadores externos | Busca e normalização de mídia |
| APIs externas | Dados de catálogo e detalhes das obras |

## Escolha tecnológica pendente

As especificações do OpenSpec mencionam Streamlit com Python, enquanto o `README.md` contém referência a Reflex. Uma única opção deve ser escolhida antes do início do frontend.
