from flask import render_template, redirect, url_for, request, abort, flash, jsonify
import requests, urllib.request, json, re
from urllib.parse import quote
from controladores.auxiliar_generos import buscar_genero_webscrapper,remove_html_tags


API_KEY = 'AIzaSyBJSFy6VtqvSEJeHk9h8tCgWpgJSht00ac'
url_base = 'https://www.googleapis.com/books/v1/volumes'
url_parte_final = '&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=' + API_KEY
url_Seguinte = '&maxResults=2&printType=books&langRestrict=pt&orderBy=relevance&key=' + API_KEY

def auxiliar_busca():
  if request.method == 'GET':
    return redirect(url_for('indice'))
  elif request.method == 'POST':
    textoBuscaLivro = request.form['buscaLivro']
    selectBuscaLivro = request.form.get('selectBusca')
    retorno = ''

    if selectBuscaLivro == 'Titulo':
      retorno = buscar_por_titulo(textoBuscaLivro, 0)

    elif selectBuscaLivro == 'Autor':
      retorno = buscar_por_autor(textoBuscaLivro, 0)

    return retorno


def buscar_por_titulo(nomeLivro, indiceInicial):

  textoAntesFormatacao = nomeLivro
  nomeLivro = formatar_palavra_busca(nomeLivro)
  livros = []
  url = url_base + '?q="' + nomeLivro + '"&startIndex=' + str(
      indiceInicial) + url_parte_final

  urlSeguinte = url_base + '?q="' + nomeLivro + '"&startIndex=' + str(
    indiceInicial + 40) + url_Seguinte

  jsondata = json.loads(urllib.request.urlopen(url).read())
  jsondataSeguinte = json.loads(urllib.request.urlopen(urlSeguinte).read())

  possuiProximo = 0
  if 'items' in jsondataSeguinte:
    possuiProximo = 1
  else:
    possuiProximo = 0

  if 'items' in jsondata:
    for livro in jsondata['items']:
      dict_livro = gerar_dictionary_livro(livro)
      prioridade = verificar_prioridade(dict_livro,textoAntesFormatacao)
      if prioridade == 1:
        livros.append(dict_livro)
      elif prioridade == 0:
        livros.insert(0, dict_livro)

  return render_template("busca_livros.html",
                         livros=livros,
                         url=url,
                         possuiProximo = possuiProximo,
                         indiceInicial = indiceInicial,
                         textoBuscaLivro=textoAntesFormatacao,
                         tipoDeBusca = 'buscarLivrosTitulo',
                         tipoBusca='Titulo')


def buscar_por_autor(nomeAutor, indiceInicial):

  textoAntesFormatacao = nomeAutor
  nomeAutor = formatar_palavra_busca(nomeAutor)
  livros = []
  url = url_base + '?q=inauthor:"' + nomeAutor + '"&startIndex=' + str(indiceInicial) + url_parte_final

  urlSeguinte = url_base + '?q=inauthor:"' + nomeAutor + '"&startIndex=' + str(indiceInicial + 40) + url_Seguinte

  jsondata = json.loads(urllib.request.urlopen(url).read())
  jsondataSeguinte = json.loads(urllib.request.urlopen(urlSeguinte).read())

  possuiProximo = 0
  if 'items' in jsondataSeguinte:
    possuiProximo = 1
  else:
    possuiProximo = 0

  if 'items' in jsondata:
    for livro in jsondata['items']:
      dict_livro = gerar_dictionary_livro(livro)
      livros.append(dict_livro)

  return render_template("busca_livros.html",
                         livros=livros,
                         textoBuscaLivro=textoAntesFormatacao,
                         possuiProximo = possuiProximo,
                         indiceInicial = indiceInicial,
                         tipoDeBusca = 'buscarLivrosAutor',
                         tipoBusca='Autor',
                        url = url)


def buscar_por_genero(genero, indiceInicial):
  
  genero = formatar_palavra_busca(genero)

  livros = []
  url = url_base + '?q=subject:"' + genero + '"&startIndex=' + str(
      indiceInicial) + url_parte_final
  
  urlSeguinte = url_base + '?q=subject:"' + genero + '"&startIndex=' + str(
      indiceInicial+40) + url_Seguinte

  jsondata = json.loads(urllib.request.urlopen(url).read())
  jsondataSeguinte = json.loads(urllib.request.urlopen(urlSeguinte).read())

  possuiProximo = 0
  if 'items' in jsondataSeguinte:
    possuiProximo = 1
  else:
    possuiProximo = 0

  if 'items' in jsondata:
    for livro in jsondata['items']:
      dict_livro = gerar_dictionary_livro(livro)
      livros.append(dict_livro)

  return render_template("busca_livros.html",
                         livros=livros,
                         url=url,
                         tamanho=len(livros),
                         possuiProximo = possuiProximo,
                         indiceInicial = indiceInicial,
                         textoBuscaLivro=genero,
                         tipoDeBusca = 'buscarLivrosGenero',
                         tipoBusca='Autor',)


def buscar_livro_id(id):

  url = url_base + '/' + id + '?key=' + API_KEY

  jsondata = json.loads(urllib.request.urlopen(url).read())

  livro = gerar_dictionary_livro(jsondata)

  generosDoLivro = buscar_genero_webscrapper(id,livro['categorias'])

  livro['categorias'] = generosDoLivro
  

  return render_template("pagina_livro.html", livro=livro)


def formatar_palavra_busca(palavraBusca):
  palavraBusca = re.sub(r"[^\w\s]", '', palavraBusca)

  palavraBusca = re.sub(r"\s+", '+', palavraBusca)

  palavraBusca = urllib.parse.quote(palavraBusca)

  return palavraBusca


def gerar_dictionary_livro(livro):
  tituloDoLivro = ""
  autoresDoLivro = []
  subtituloDoLivro = ""
  linkCapaDoLivro = ""
  descricaoLivro = ""
  idDoLivro = ""
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


  dict_livro = {
      "titulo": tituloDoLivro,
      "subtitulo": subtituloDoLivro,
      "autores": autoresDoLivro,
      "linkCapa": linkCapaDoLivro,
      "descricao": descricaoLivro,
      "id": idDoLivro,
      "categorias": categoriasDoLivro
  }
  return dict_livro



def verificar_prioridade(dict_livro,textoBusca):
  titulo = dict_livro['titulo']
  subtitulo = dict_livro['subtitulo']
  descricao = dict_livro['descricao']

  if textoBusca.casefold() in titulo.casefold():
    return 0
  elif textoBusca.casefold() in subtitulo.casefold():
    return 0
  
  return 1



