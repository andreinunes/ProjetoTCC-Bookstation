from flask import render_template, request
from modelos.busca_livro_modelo import Busca_Livro

def buscar_por_titulo(nomeLivro, indiceInicial):

  retornoBusca = Busca_Livro.buscar(nomeLivro, indiceInicial,"titulo")
  livros = retornoBusca[0]
  url = retornoBusca[1]
  possuiProximo = retornoBusca[2]
 
  return render_template("busca_livros.html",
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

  return render_template("busca_livros.html",
                         livros=livros,
                         url=url,
                         possuiProximo=possuiProximo,
                         indiceInicial=indiceInicial,
                         textoBuscaLivro=nomeAutor,
                         tipoDeBusca='buscarLivrosAutor',
                         tipoBusca='Autor')


def buscar_por_genero(genero):

  retornoBuscaGenero = Busca_Livro.buscar_por_genero(genero)
  colecao_genero = retornoBuscaGenero[0]
  livros = retornoBuscaGenero[1]
        
  return render_template("busca_livros.html", colecao_genero = colecao_genero, livros = livros, generoBuscado = genero)


def buscar_livro_id(id = None):

  if request.args.get('tituloLivro') is None:
    retornoBuscaLivro= Busca_Livro.buscar_livro_id(id)
    return render_template("pagina_livro.html", livro=retornoBuscaLivro)
  else:
    retornoBuscaLivro = Busca_Livro.buscar_livro_id()
    livro = retornoBuscaLivro[0]
    urlBusca = retornoBuscaLivro[1]
    return render_template("pagina_livro.html",livro=livro,urlBusca=urlBusca)
