from flask import render_template, redirect, url_for, request, abort,flash, jsonify
import requests
import urllib.request, json
from urllib.parse import quote 
import re

API_KEY = 'AIzaSyBJSFy6VtqvSEJeHk9h8tCgWpgJSht00ac'

def buscar_por_titulo_e_autor():
  if request.method == 'GET':
    return redirect(url_for('indice'))
  elif request.method == 'POST':
    textoBuscaLivro = request.form['buscaLivro']


    textoBuscaLivro = re.sub(r"[^\w\s]", '', textoBuscaLivro)

    textoBuscaLivro = re.sub(r"\s+", '+', textoBuscaLivro)

    textoBuscaLivro = urllib.parse.quote(textoBuscaLivro)

    selectBuscaLivro = request.form.get('selectBusca')

    indiceInicial = 0
    livros = []

    if selectBuscaLivro == 'Titulo':
      url = 'https://www.googleapis.com/books/v1/volumes?q="' + textoBuscaLivro + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY
    elif selectBuscaLivro == 'Autor':
      url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"' + textoBuscaLivro + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)

    while 'items' in jsondata:
      
      for livro in jsondata['items']:

        tituloDoLivro = ""
        autoresDoLivro = []
        subtituloDoLivro = ""
        linkCapaDoLivro = ""

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
            

        livros.append({
           "titulo": tituloDoLivro,
          "subtitulo": subtituloDoLivro,

           "autores": autoresDoLivro,
           "linkCapa": linkCapaDoLivro
                     })
      indiceInicial += 40
      
      if selectBuscaLivro == 'Titulo':
        url = 'https://www.googleapis.com/books/v1/volumes?q="' + textoBuscaLivro + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY
      elif selectBuscaLivro == 'Autor':
        url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"' + textoBuscaLivro + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY
        
      resposta = urllib.request.urlopen(url)
      dados = resposta.read()
      jsondata = json.loads(dados)
      
    return render_template("busca_livros.html", livros = livros, url = url, tamanho = len(livros))


def buscar_por_autor(autor):
  autor = re.sub(r"[^\w\s]", '', autor)
  
  autor = re.sub(r"\s+", '+', autor)

  autor = urllib.parse.quote(autor)
  
  indiceInicial = 0
  livros = []
  url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"' + autor + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY
  
  resposta = urllib.request.urlopen(url)
  dados = resposta.read()
  jsondata = json.loads(dados)
  
  while 'items' in jsondata:
  
    for livro in jsondata['items']:
  
      tituloDoLivro = ""
      autoresDoLivro = []
      subtituloDoLivro = ""
      linkCapaDoLivro = ""
  
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
  
  
      livros.append({
         "titulo": tituloDoLivro,
        "subtitulo": subtituloDoLivro,
  
         "autores": autoresDoLivro,
         "linkCapa": linkCapaDoLivro
                   })
    indiceInicial += 40
    url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:"' + autor + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY
  
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
  
  return render_template("busca_livros.html", livros = livros, url = url, tamanho = len(livros))



def buscar_por_genero(genero):
  genero = re.sub(r"[^\w\s]", '', genero)

  genero = re.sub(r"\s+", '+', genero)

  indiceInicial = 0
  livros = []
  url = 'https://www.googleapis.com/books/v1/volumes?q=subject:"' + genero + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY

  resposta = urllib.request.urlopen(url)
  dados = resposta.read()
  jsondata = json.loads(dados)

  while 'items' in jsondata:

    for livro in jsondata['items']:

      tituloDoLivro = ""
      autoresDoLivro = []
      subtituloDoLivro = ""
      linkCapaDoLivro = ""

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


      livros.append({
         "titulo": tituloDoLivro,
        "subtitulo": subtituloDoLivro,

         "autores": autoresDoLivro,
         "linkCapa": linkCapaDoLivro
                   })
    indiceInicial += 40
    url = 'https://www.googleapis.com/books/v1/volumes?q=subject:"' + genero + '"&startIndex=' + str(indiceInicial) + "&maxResults=40&printType=books&langRestrict=pt&orderBy=relevance&key=" + API_KEY

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)

  return render_template("busca_livros.html", livros = livros, url = url, tamanho = len(livros))
  
  
  
