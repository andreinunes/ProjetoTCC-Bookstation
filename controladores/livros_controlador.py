from flask import render_template, redirect, url_for, request, abort,flash, jsonify
import requests
import urllib.request, json

API_KEY = 'AIzaSyBJSFy6VtqvSEJeHk9h8tCgWpgJSht00ac'

def buscar_por_titulo():
  if request.method == 'GET':
    return redirect(url_for('indice'))
  elif request.method == 'POST':
    textoBuscaLivro = request.form['buscaLivro']

    url = "https://www.googleapis.com/books/v1/volumes?q=intitle:" + textoBuscaLivro + "&startIndex=0&maxResults=40&printType=books&langRestrict=pt&key=" + API_KEY

    resposta = urllib.request.urlopen(url)

    dados = resposta.read()

    jsondata = json.loads(dados)

    # return rendered index.html page with random books from Google Books API
    return render_template("busca_livros.html", livros = jsondata['items'])

