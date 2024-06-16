from flask import request
import os
import urllib.error
from modelos.livros_generos_modelo import Livro_Genero
from modelos.usuarios_listas_modelo import Usuario_Lista
from modelos.listas_livros_modelo import Lista_Livro
from flask_login import current_user
from funcoes_auxiliares import formatar_palavra_busca, realizar_request_api,verificar_busca_caracteres_especiais

auxiliar_chamada_api = '?key='
API_KEY = str(os.getenv("API_KEY"))


class Busca_Livro():

  @staticmethod
  def buscar(busca, indiceInicial, tipoBusca):
      
    verificacao_caracteres_especiais = verificar_busca_caracteres_especiais(busca)
    busca = formatar_palavra_busca(busca)
    livros = []
    url = ''
    urlSeguinte = ''
    possuiProximo = 0
    if not verificacao_caracteres_especiais:
        if tipoBusca == 'titulo':
    
          url = 'https://www.googleapis.com/books/v1/volumes?q="{0}"&startIndex={1}&maxResults=20&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(
              busca, indiceInicial, API_KEY)
    
          urlSeguinte = 'https://www.googleapis.com/books/v1/volumes?q="{0}"&startIndex={1}&maxResults=2&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(
              busca, indiceInicial + 20, API_KEY)
    
        if tipoBusca == 'autor':
          url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"{0}"&startIndex={1}&maxResults=20&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(
              busca, indiceInicial, API_KEY)
    
          urlSeguinte = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"{0}"&startIndex={1}&maxResults=2&printType=books&langRestrict=pt&orderBy=relevance&key={2}'.format(
              busca, indiceInicial + 20, API_KEY)
    
        jsondata = realizar_request_api(url)
        jsondataSeguinte = realizar_request_api(urlSeguinte)
    
        possuiProximo = 0
        if 'items' in jsondataSeguinte:
          possuiProximo = 1
        else:
          possuiProximo = 0
    
        if 'items' in jsondata:
          for livro in jsondata['items']:
            dict_livro = Usuario_Lista.gerar_dicionario(livro)
            generos_livro = Livro_Genero.buscar_genero_webscrapper(
                dict_livro['id'], dict_livro['categorias'])
            dict_livro['categorias'] = generos_livro
            livros.append(dict_livro)

    return [livros, url, possuiProximo]

  @staticmethod
  def buscar_por_genero(genero, per_page):

    page = request.args.get('page', 1, type=int)
    colecao_genero = Livro_Genero.getColecaoGeneros(genero, page, per_page)
    livros = []
    jsondata = ""
    for item in colecao_genero.items:
      url = 'https://www.googleapis.com/books/v1/volumes/' + item.id_livro + auxiliar_chamada_api + API_KEY
      jsondata = realizar_request_api(url)
      dict_livro = Usuario_Lista.gerar_dicionario(jsondata)
      livros.append(dict_livro)

    return [colecao_genero, livros]

  @staticmethod
  def buscar_livro_id(id=None):

    try:
        livroExisteLista = 0
        emQueLista = ''
        verificarexiste = []
        existeEmFavoritos = 0
        notaLivro = -1
        if request.args.get('idDoLivro') is None:
          url = "https://www.googleapis.com/books/v1/volumes/" + str(
              id) + auxiliar_chamada_api + API_KEY
          jsondata = realizar_request_api(url)
          livro = Usuario_Lista.gerar_dicionario(jsondata)
          if current_user.is_authenticated:
            verificarexiste = Usuario_Lista.verificar_livro_lista(
                current_user.id, '', str(id))
            if verificarexiste is not None:
              livroExisteLista = verificarexiste[0]
              existeEmFavoritos = verificarexiste[1]
              emQueLista = verificarexiste[2]
              notaLivro = verificarexiste[3]
          media_livro = Lista_Livro.buscar_media_livro(str(id))
          return [
              livro, livroExisteLista, emQueLista, existeEmFavoritos, notaLivro,
              media_livro
          ]
        else:
          url = "https://www.googleapis.com/books/v1/volumes/" + str(
              request.args.get('idDoLivro')) + auxiliar_chamada_api + API_KEY
          jsondata = realizar_request_api(url)
          livro = Usuario_Lista.gerar_dicionario(jsondata)
          if current_user.is_authenticated:
            verificarexiste = Usuario_Lista.verificar_livro_lista(
                current_user.id, '', str(request.args.get('idDoLivro')))
            if verificarexiste is not None:
              livroExisteLista = verificarexiste[0]
              emQueLista = verificarexiste[2]
              existeEmFavoritos = verificarexiste[1]
              notaLivro = verificarexiste[3]
          media_livro = Lista_Livro.buscar_media_livro(
              str(request.args.get('idDoLivro')))
    
          return [
              livro,
              request.args.get('urlAtual'), livroExisteLista, emQueLista,
              existeEmFavoritos, notaLivro, media_livro
          ]
    except urllib.error.HTTPError:
        return [None, None, None, None, None, None, None]
