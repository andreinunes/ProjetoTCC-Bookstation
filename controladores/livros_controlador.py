from flask import render_template, redirect, url_for, request, abort, flash, jsonify
import requests, urllib.request, json, re
import time
from urllib.parse import quote
from controladores.generos_controlador import buscar_genero_webscrapper, verificar_genero, getGeneroChave,getColecaoGeneros
from funcoes_auxiliares import remove_html_tags, formatar_palavra_busca, verificar_prioridade, realizar_request_api,verificar_ISBNs,converter_data

API_KEY = 'AIzaSyBJSFy6VtqvSEJeHk9h8tCgWpgJSht00ac'
url_base = 'https://www.googleapis.com/books/v1/volumes'
url_parte_final = '&maxResults=20&printType=books&langRestrict=pt&orderBy=relevance&key=' + API_KEY
url_Seguinte = '&maxResults=2&printType=books&langRestrict=pt&orderBy=relevance&key=' + API_KEY

def buscar_por_titulo(nomeLivro, indiceInicial):

  textoAntesFormatacao = nomeLivro
  nomeLivro = formatar_palavra_busca(nomeLivro)
  livros = []
  url = url_base + '?q="' + nomeLivro + '"&startIndex=' + str(
      indiceInicial) + url_parte_final

  urlSeguinte = url_base + '?q="' + nomeLivro + '"&startIndex=' + str(
      indiceInicial + 20) + url_Seguinte

  jsondata = realizar_request_api(url)
  jsondataSeguinte = realizar_request_api(urlSeguinte)

  possuiProximo = 0
  if 'items' in jsondataSeguinte:
    possuiProximo = 1
  else:
    possuiProximo = 0

  if 'items' in jsondata:
    for livro in jsondata['items']:
      dict_livro = gerar_dictionary_livro(livro)
      generosDoLivro = buscar_genero_webscrapper(dict_livro['id'],
                                                 dict_livro['categorias'])
      dict_livro['categorias'] = generosDoLivro
      prioridade = verificar_prioridade(dict_livro, textoAntesFormatacao)
      if prioridade == 1:
        livros.append(dict_livro)
      elif prioridade == 0:
        livros.insert(0, dict_livro)

  return render_template("busca_livros.html",
                         livros=livros,
                         url=url,
                         possuiProximo=possuiProximo,
                         indiceInicial=indiceInicial,
                         textoBuscaLivro=textoAntesFormatacao,
                         tipoDeBusca='buscarLivrosTitulo',
                         tipoBusca='Titulo')


def buscar_por_autor(nomeAutor, indiceInicial):

  textoAntesFormatacao = nomeAutor
  nomeAutor = formatar_palavra_busca(nomeAutor)
  livros = []
  url = url_base + '?q=inauthor:"' + nomeAutor + '"&startIndex=' + str(
      indiceInicial) + url_parte_final

  urlSeguinte = url_base + '?q=inauthor:"' + nomeAutor + '"&startIndex=' + str(
      indiceInicial + 20) + url_Seguinte

  jsondata = realizar_request_api(url)
  jsondataSeguinte = realizar_request_api(urlSeguinte)

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
                         possuiProximo=possuiProximo,
                         indiceInicial=indiceInicial,
                         tipoDeBusca='buscarLivrosAutor',
                         tipoBusca='Autor',
                         url=url)


def buscar_por_genero(genero):


  page = request.args.get('page',1,type = int)
  per_page = 15
  colecao_genero = getColecaoGeneros(genero,page,per_page)
  livros = []
  jsondata = ""
  for item in colecao_genero.items:
    url = url_base + '/' + item.id_livro + '?key=' + API_KEY
    jsondata = realizar_request_api(url)
    dict_livro = gerar_dictionary_livro(jsondata)
    livros.append(dict_livro)
        
  return render_template("busca_livros_genero.html", colecao_genero = colecao_genero, livros = livros, genero = genero, jsondata=jsondata)


def buscar_livro_id(id = None):

  tituloLivro = request.args.get('tituloLivro')
  subtituloLivro = request.args.get('subtituloLivro')
  autorLivro = request.args.get('autorLivro')
  generoLivro = request.args.get('generoLivro')
  linkCapa = request.args.get('linkCapa')
  descricaoLivro = request.args.get('descricaoLivro')
  editoraLivro = request.args.get('editoraLivro')
  idDoLivro = request.args.get('idDoLivro')
  dataPublicacaoLivro = request.args.get('dataPublicacaoLivro')
  ISBN10 = request.args.get('ISBN10')
  ISBN13 = request.args.get('ISBN13')
  numeroPaginasLivro = request.args.get('numeroPaginasLivro')
  urlBusca = request.args.get('urlAtual')

  if tituloLivro is None:
    
    url = url_base + '/' + id + '?key=' + API_KEY
    jsondata = realizar_request_api(url)
    livro = gerar_dictionary_livro(jsondata)
    return render_template("pagina_livro.html", livro=livro)

  if autorLivro is None:
    autorLivro = "#"
  if generoLivro is None:
    generoLivro = "#"

  livro = {
    "titulo": tituloLivro,
    "subtitulo": subtituloLivro,
    "autores": autorLivro.split('#'),
    "linkCapa": linkCapa,
    "descricao": descricaoLivro,
    "id": str(idDoLivro),
    "categorias": generoLivro.split('#'),
    "dataPublicacao": converter_data(dataPublicacaoLivro),
    "ISBN10": ISBN10,
    "ISBN13": ISBN13,
    "editora": editoraLivro,
    "numeroPaginas": str(numeroPaginasLivro)
  }
  return render_template("pagina_livro.html",livro=livro,urlBusca=urlBusca)

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

  generosDoLivro = buscar_genero_webscrapper(idDoLivro, categoriasDoLivro)
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
