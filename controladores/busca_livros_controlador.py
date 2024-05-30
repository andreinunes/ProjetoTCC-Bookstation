from flask import render_template, request
from modelos.busca_livro_modelo import Busca_Livro

html_pagina_busca = "busca_livros.html"

def buscar_por_titulo(nomeLivro, indiceInicial):

  retornoBusca = Busca_Livro.buscar(nomeLivro, indiceInicial,"titulo")
  livros = retornoBusca[0]
  url = retornoBusca[1]
  possuiProximo = retornoBusca[2]
 
  return render_template(html_pagina_busca,
                         livros=livros,
                         url=url,
                         possuiProximo=possuiProximo,
                         indiceInicial=indiceInicial,
                         textoBuscaLivro=nomeLivro,
                         tipoDeBusca='buscarLivrosTitulo',
                         tipoBusca='Titulo')


def buscar_por_autor(nomeAutor, indiceInicial):

  retornoBusca = Busca_Livro.buscar(nomeAutor, indiceInicial,"autor")
  livros = retornoBusca[0]
  url = retornoBusca[1]
  possuiProximo = retornoBusca[2]

  return render_template(html_pagina_busca,
                         livros=livros,
                         url=url,
                         possuiProximo=possuiProximo,
                         indiceInicial=indiceInicial,
                         textoBuscaLivro=nomeAutor,
                         tipoDeBusca='buscarLivrosAutor',
                         tipoBusca='Autor')


def buscar_por_genero(genero):

  retornoBuscaGenero = Busca_Livro.buscar_por_genero(genero,12)
  colecao_genero = retornoBuscaGenero[0]
  livros = retornoBuscaGenero[1]
        
  return render_template(html_pagina_busca, colecao_genero = colecao_genero, livros = livros, generoBuscado = genero)


def buscar_livro_id(id = None):

  if request.args.get('idDoLivro') is None:
    retornoBuscaLivro= Busca_Livro.buscar_livro_id(id)
    return render_template("pagina_livro.html", livro=retornoBuscaLivro[0],existe = retornoBuscaLivro[1], emqueLista = retornoBuscaLivro[2],existeEmFavoritos = retornoBuscaLivro[3], notaLivro = retornoBuscaLivro[4], media_livro = retornoBuscaLivro[5])
  else:
    retornoBuscaLivro = Busca_Livro.buscar_livro_id()
    livro = retornoBuscaLivro[0]
    urlBusca = retornoBuscaLivro[1]
    return render_template("pagina_livro.html",livro=livro,urlBusca=urlBusca,existe = retornoBuscaLivro[2], emqueLista = retornoBuscaLivro[3], existeEmFavoritos = retornoBuscaLivro[4], notaLivro = retornoBuscaLivro[5], media_livro = retornoBuscaLivro[6])