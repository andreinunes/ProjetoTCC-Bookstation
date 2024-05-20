from bs4 import BeautifulSoup
import requests
from database import db
from funcoes_auxiliares import remove_html_tags,getDicionarioGeneros

dicionarioGeneros = getDicionarioGeneros()

class Livro_Genero(db.Model):
  __tablename__ = 'livro_genero'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  id_livro = db.Column(db.String(100),nullable = False)
  nome_genero = db.Column(db.String(100),nullable = False)

 
  def get_id(self):
    return str(self.id)

  def __init__(self, id_livro, nome_genero):
    self.id_livro = id_livro
    self.nome_genero = nome_genero

  def __repr__(self):
    return "id_livro: {}".format(self.id_livro)

  @staticmethod
  def buscar_genero_webscrapper(id,categorias = None, buscaGenero = None):

    buscar_livro = Livro_Genero.query.filter_by(id_livro=id).first() 
    listaGeneroResultado = []

    if buscar_livro:
      listaGeneroResultado = []
      colecaoGenerosLivro = Livro_Genero.query.filter_by(id_livro=id).all()
      for i in range(len(colecaoGenerosLivro)):
        listaGeneroResultado.append(colecaoGenerosLivro[i].nome_genero)
    else:

      headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
      }

      url = f"https://www.google.com.br/books/edition/%7B%7D/{id}?hl=en"
      response = requests.get(url, headers = headers) 
      soup = BeautifulSoup(response.content, 'html.parser')
      retornos = soup.find_all(class_="fl")
      lista = []

      for retorno in retornos:
        lista.append(str(retorno))

      for i in range(len(lista)):
        lista[i] = remove_html_tags(lista[i])

      listaGenerosWebScrapper = ' '.join(str(e) for e in lista)
      listaCategoriasAPI = ' '.join(str(e) for e in categorias)
      stringGeneros = listaGenerosWebScrapper + ' ' + listaCategoriasAPI
      listaGeneroResultado = []

      for chave in dicionarioGeneros.keys():
        if chave.casefold() in stringGeneros.casefold():
          listaGeneroResultado.append(dicionarioGeneros[chave])

      for items in list(set(listaGeneroResultado)):
        livro_genero = Livro_Genero(id, items)
        db.session.add(livro_genero)
        db.session.commit()

    if len(list(set(listaGeneroResultado))) == 0:
      if buscaGenero != None:
        livro_genero = Livro_Genero(id, buscaGenero)
        db.session.add(livro_genero)
        db.session.commit()

    if buscaGenero not in list(set(listaGeneroResultado)):
      if buscaGenero != None:
        livro_genero = Livro_Genero(id, buscaGenero)
        db.session.add(livro_genero)
        db.session.commit()

    return list(set(listaGeneroResultado))

  @staticmethod
  def verificar_genero(genero):
    for chave in dicionarioGeneros.keys():
      if chave == genero:
        return genero
      if genero ==  dicionarioGeneros[chave]:
        return chave
    return "0"

  @staticmethod
  def getGeneroChave(genero):
    return dicionarioGeneros[genero]

  @staticmethod
  def getColecaoGeneros(genero, page, per_page):
    colecaoGeneros = Livro_Genero.query.filter_by(nome_genero=genero).paginate(page=page,per_page=per_page)
    return colecaoGeneros

  @staticmethod
  def getColecaoGenerosRecomendacao(genero, listaExclusao, quantidadeBusca):
    colecaoGeneros = Livro_Genero.query.filter(Livro_Genero.nome_genero == genero, ~Livro_Genero.id_livro.in_(listaExclusao)).limit(quantidadeBusca).all()

    return colecaoGeneros