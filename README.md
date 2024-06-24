
# Bookstation

Projeto de criação de um website para organização e recomendação de livros. O website utiliza a API do Google Livros para requisitar os dados dos livros. Aplicação feita em Python, utilizando o microframework Flask como Backend.




## Tópicos

- [Estrutura do Projeto](#estrutura-do-projeto-design-mvc-model-view-controller)

- [Funcionalidades](#funcionalidades)

- [Observações](#observações)

- [Tecnologias utilizadas](#tecnologias-utilizadas)
  
## Estrutura do Projeto: Design MVC (Model-View-Controller)

O projeto utiliza principalmente um design de arquitetura MVC. E possui também uma "camada" extra para o mapeamento das rotas do Flask.

### Modelos
Responsável pela estrutura das tabelas e as funções de acesso ao banco de dados.

### View (templates e static)
Interface utilizada pelo usuário. Conjunto dos arquivos html, css, javascript e imagens.

### Controladores
Responsável pela ligação entre os comandos realizados pelo usúarios na View e a execução deles nos Modelos.

### Rotas
Mapeamento dos URLs para uma função específica que manipula a lógica desse URL.

## Funcionalidades

- Cadastro e Login
- Busca de livros ( Por título, autor ou gênero)
- Inserção e remoção de livro de listas
- Listas de recomendação (Baseada nas listas e baseada nas preferências)
- Avaliação de livros
- Seleção de preferências


## Observações
- O sistema foi executado utilizando o Replit, que possibilita ligar o projeto com o repositório no Github, por isso a ausência de um tópico sobre como executar o website localmente
- Devido ao uso da API do Google Livros, a aplicação possui um limite de requisições, depois de ser utilizado extensamente, é possível que ele alerte que o limite foi atingido. A contagem de requisições reseta no dia seguinte.
- Quando o deploy é refeito, o banco de dados do sistema reseta. Nisso, não apenas os cadastros e listas são apagadas, como também os gêneros dos livros. Assim, a busca por gênero inicialmente não retornará livros até que esses livros tenham sido pesquisados de outras formas e seus gêneros sejam salvos no banco de dados.
## Tecnologias utilizadas
- Python
- Flask
- HTML
- CSS
- Javascript
- SQLite3
