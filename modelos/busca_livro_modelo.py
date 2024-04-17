from flask import request
from modelos.livros_generos_modelo import Livro_Genero
from funcoes_auxiliares import remove_html_tags, formatar_palavra_busca, verificar_prioridade, realizar_request_api,verificar_ISBNs,converter_data

API_KEY = 'AIzaSyBJSFy6VtqvSEJeHk9h8tCgWpgJSht00ac'

class Busca_Livro():

  @staticmethod
  def buscar(busca, indiceInicial,tipoBusca):

    textoAntesFormatacao = busca
    busca = formatar_palavra_busca(busca)
    livros = []
    url = ''
    urlSeguinte = ''
    if tipoBusca == 'titulo':
      
      url = 'https://www.googleapis.com/books/v1/volumes?q="{0}"&startIndex={1}&maxResults=20&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(busca,indiceInicial,API_KEY)
  
      urlSeguinte = 'https://www.googleapis.com/books/v1/volumes?q="{0}"&startIndex={1}&maxResults=2&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(busca,indiceInicial+20,API_KEY)

    if tipoBusca == 'autor':
      url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"{0}"&startIndex={1}&maxResults=20&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(busca,indiceInicial,API_KEY)

      urlSeguinte = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"{0}"&startIndex={1}&maxResults=2&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(busca,indiceInicial+20,API_KEY)
  
    jsondata = realizar_request_api(url)
    jsondataSeguinte = realizar_request_api(urlSeguinte)
  
    possuiProximo = 0
    if 'items' in jsondataSeguinte:
      possuiProximo = 1
    else:
      possuiProximo = 0
  
    if 'items' in jsondata:
      for livro in jsondata['items']:
        dict_livro = Busca_Livro.gerar_dictionary_livro(livro)
        generosDoLivro = Livro_Genero.buscar_genero_webscrapper(dict_livro['id'],
                                                   dict_livro['categorias'])
        dict_livro['categorias'] = generosDoLivro
        prioridade = verificar_prioridade(dict_livro, textoAntesFormatacao)
        if prioridade == 1:
          livros.append(dict_livro)
        elif prioridade == 0:
          livros.insert(0, dict_livro)

    return [livros,url,possuiProximo]
  
  @staticmethod
  def buscar_por_genero(genero):
  
    page = request.args.get('page',1,type = int)
    per_page = 15
    colecao_genero = Livro_Genero.getColecaoGeneros(genero,page,per_page)
    livros = []
    jsondata = ""
    for item in colecao_genero.items:
      url = 'https://www.googleapis.com/books/v1/volumes/' + item.id_livro + '?key=' + API_KEY
      jsondata = realizar_request_api(url)
      dict_livro = Busca_Livro.gerar_dictionary_livro(jsondata)
      livros.append(dict_livro)

    return [colecao_genero,livros]
  
  @staticmethod
  def buscar_livro_id(id = None):
  
    if request.args.get('tituloLivro') is None:
      url = "https://www.googleapis.com/books/v1/volumes/" + str(id) + '?key=' + API_KEY
      jsondata = realizar_request_api(url)
      livro = Busca_Livro.gerar_dictionary_livro(jsondata)
      return livro
    else:
      autorLivro = request.args.get('autorLivro')
      generoLivro = request.args.get('generoLivro')
  
      if autorLivro is None:
        autorLivro = "#"
      if generoLivro is None:
        generoLivro = "#"
  
      livro = {
        "titulo": request.args.get('tituloLivro'),
        "subtitulo": request.args.get('subtituloLivro'),
        "autores": autorLivro.split('#'),
        "linkCapa": request.args.get('linkCapa'),
        "descricao": request.args.get('descricaoLivro'),
        "id": str(request.args.get('idDoLivro')),
        "categorias": generoLivro.split('#'),
        "dataPublicacao": converter_data(request.args.get('dataPublicacaoLivro')),
        "ISBN10": request.args.get('ISBN10'),
        "ISBN13": request.args.get('ISBN13'),
        "editora": request.args.get('editoraLivro'),
        "numeroPaginas": str(request.args.get('numeroPaginasLivro'))
      }
      return [livro,request.args.get('urlAtual')]
  
  @staticmethod
  def gerar_dictionary_livro(livro):
    tituloDoLivro = ""
    autoresDoLivro = []
    subtituloDoLivro = ""
    linkCapaDoLivro = ""
    descricaoLivro = ""
    idDoLivro = ""
    dataPublicacaoLivro = ""
    ISBN = []
    editoraLivro = ""
    numeroPaginasLivro = ""
    categoriasDoLivro = []
  
    if 'title' in livro['volumeInfo']:
      tituloDoLivro = livro['volumeInfo']['title']
    if 'subtitle' in livro['volumeInfo']:
      subtituloDoLivro = livro['volumeInfo']['subtitle']
    if 'imageLinks' in livro['volumeInfo']:
      linkCapaDoLivro = livro['volumeInfo']['imageLinks']['thumbnail']
    if 'authors' in livro['volumeInfo']:
      maximoAutores = 0
      for autores in livro['volumeInfo']['authors']:
        autoresDoLivro.append(autores)
        maximoAutores += 1
        if maximoAutores == 3:
          break
    if 'description' in livro['volumeInfo']:
      descricaoLivro = remove_html_tags(livro['volumeInfo']['description'])
    if 'id' in livro: idDoLivro = livro['id']
    if 'categories' in livro['volumeInfo']:
      for categoria in livro['volumeInfo']['categories']:
        categoriasDoLivro.append(categoria)
    if 'publishedDate' in livro['volumeInfo']:
      dataPublicacaoLivro = livro['volumeInfo']['publishedDate']
    if 'publisher' in livro['volumeInfo']:
      editoraLivro = livro['volumeInfo']['publisher']
    if 'industryIdentifiers' in livro['volumeInfo']:
      for ISBNs in livro['volumeInfo']['industryIdentifiers']:
        ISBN.append({ 'ISBN': ISBNs['type'], 'Identificador': ISBNs['identifier']})
    if 'pageCount' in livro['volumeInfo']:
      numeroPaginasLivro = livro['volumeInfo']['pageCount']
  
    generosDoLivro = Livro_Genero.buscar_genero_webscrapper(idDoLivro, categoriasDoLivro)
    ISBN = verificar_ISBNs(ISBN)
  
    dict_livro = {
        "titulo": tituloDoLivro,
        "subtitulo": subtituloDoLivro,
        "autores": autoresDoLivro,
        "linkCapa": linkCapaDoLivro,
        "descricao": descricaoLivro,
        "id": str(idDoLivro),
        "categorias": generosDoLivro,
        "listacategoria": '#'.join(generosDoLivro),
        "listaautores": '#'.join(autoresDoLivro),
        "dataPublicacao": converter_data(dataPublicacaoLivro),
        "ISBN10": ISBN['ISBN10'],
        "ISBN13": ISBN['ISBN13'],
        "editora": editoraLivro,
        "numeroPaginas": str(numeroPaginasLivro),
    }
    return dict_livro
