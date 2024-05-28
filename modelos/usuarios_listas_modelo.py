from modelos.listas_livros_modelo import Lista_Livro
from modelos.livros_generos_modelo import Livro_Genero
from database import db
from funcoes_auxiliares import realizar_request_api, remove_html_tags, verificar_ISBNs, converter_data
import operator

API_KEY = 'AIzaSyBJSFy6VtqvSEJeHk9h8tCgWpgJSht00ac'


class Usuario_Lista(db.Model):
  __tablename__ = 'usuarios_listas'
  usuario_id = db.Column(db.Integer,
                         db.ForeignKey('usuario.id'),
                         nullable=False)
  lista_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True,
                       nullable=False)
  tipo_lista = db.Column(db.String(5), nullable=False)

  def __init__(self, usuario_id, tipo_lista):
    self.usuario_id = usuario_id
    self.tipo_lista = tipo_lista

  def __repr__(self):
    return "lista_id: {}".format(self.lista_id)

  @staticmethod
  def criar_listas_novos_usuarios(usuario_id):

    Livros_Lidos = Usuario_Lista(usuario_id, "LL")
    db.session.add(Livros_Lidos)
    db.session.commit()

    Lendo = Usuario_Lista(usuario_id, "LM")
    db.session.add(Lendo)
    db.session.commit()

    Futuras = Usuario_Lista(usuario_id, "LF")
    db.session.add(Futuras)
    db.session.commit()

    Abandonados = Usuario_Lista(usuario_id, "LA")
    db.session.add(Abandonados)
    db.session.commit()

    Favoritos = Usuario_Lista(usuario_id, "FAV")
    db.session.add(Favoritos)
    db.session.commit()

  @staticmethod
  def get_lista_livros(usuario_id, tipoLista,stringPreferencias):
    if tipoLista == "REC":
      livros = Usuario_Lista.get_lista_livros_recomendados(usuario_id)
      return livros
    elif tipoLista == "RECPREF":
      livros = Usuario_Lista.get_lista_livros_recomendados_preferencias(usuario_id,stringPreferencias)
      return livros
    else:
      lista_livros = Usuario_Lista.query.filter_by(
          usuario_id=usuario_id, tipo_lista=tipoLista).first()
      if lista_livros is None:
        return None
      else:
        lista_livros = Lista_Livro.query.filter_by(
            lista_id=lista_livros.lista_id).all()
        livros = []
        jsondata = ""
        for item in lista_livros:
          url = 'https://www.googleapis.com/books/v1/volumes/' + item.livro_id + '?key=' + API_KEY
          jsondata = realizar_request_api(url)
          dict_livro = Usuario_Lista.gerar_dicionario(jsondata)
          livros.append(dict_livro)
        return livros

  @staticmethod
  def verificar_livro_lista(usuario_id, tipoLista, idLivro):
    livros_lidos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                 tipo_lista="LL").first()
    lendo_momento = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                  tipo_lista="LM").first()
    leituras_futuras = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                     tipo_lista="LF").first()
    livros_abandonados = Usuario_Lista.query.filter_by(
        usuario_id=usuario_id, tipo_lista="LA").first()
    livros_favoritos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                     tipo_lista="FAV").first()

    existeEmLista = 0
    emQualListaExiste = ''
    existeEmFavoritos = 0
    notaLivro = -1
    if Lista_Livro.query.filter_by(lista_id=livros_lidos.lista_id,
                                   livro_id=idLivro).count() != 0:
      existeEmLista = 1
      emQualListaExiste = 'Livros Lidos'
      notaLivro = Lista_Livro.buscar_nota_livro(livros_lidos.lista_id,usuario_id,idLivro)

    if Lista_Livro.query.filter_by(lista_id=lendo_momento.lista_id,
                                   livro_id=idLivro).count() != 0:
      existeEmLista = 1
      emQualListaExiste = 'Lendo no Momento'
      notaLivro = Lista_Livro.buscar_nota_livro(lendo_momento.lista_id,usuario_id,idLivro)

    if Lista_Livro.query.filter_by(lista_id=leituras_futuras.lista_id,
                                   livro_id=idLivro).count() != 0:
      existeEmLista = 1
      emQualListaExiste = 'Leituras Futuras'
      notaLivro = Lista_Livro.buscar_nota_livro(leituras_futuras.lista_id,usuario_id,idLivro)

    if Lista_Livro.query.filter_by(lista_id=livros_abandonados.lista_id,
                                   livro_id=idLivro).count() != 0:
      existeEmLista = 1
      emQualListaExiste = 'Livros Abandonados'
      notaLivro = Lista_Livro.buscar_nota_livro(livros_abandonados.lista_id,usuario_id,idLivro)

    if Lista_Livro.query.filter_by(lista_id=livros_favoritos.lista_id,
                                   livro_id=idLivro).count() != 0:
      existeEmFavoritos = 1

    return [existeEmLista, existeEmFavoritos, emQualListaExiste,notaLivro]

  @staticmethod
  def adicionar_livro_lista(usuario_id, tipoLista, idLivro):
    lista_livros = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                 tipo_lista=tipoLista).first()
    if lista_livros is None:
      return 1
    else:
      verificarexiste = Usuario_Lista.verificar_livro_lista(
          usuario_id, tipoLista, idLivro)
      if verificarexiste[0] == 0 and tipoLista != 'FAV':
        livro = Lista_Livro(lista_livros.lista_id, idLivro)
        db.session.add(livro)
        db.session.commit()
        return 0
      elif verificarexiste[0] == 0 and tipoLista == 'FAV':
        return 1
      elif verificarexiste[0] == 1 and tipoLista != 'FAV':
        return 1
      elif verificarexiste[0] == 1 and tipoLista == 'FAV' and verificarexiste[
          1] == 0:
        livro = Lista_Livro(lista_livros.lista_id, idLivro)
        db.session.add(livro)
        db.session.commit()
        return 0
      else:
        return 1

  @staticmethod
  def remover_livro_lista(usuario_id, idLivro):
    verificarexiste = Usuario_Lista.verificar_livro_lista(
        usuario_id, '', idLivro)
    lista_com_o_livro = verificarexiste[2]
    if verificarexiste[0] == 1 and lista_com_o_livro != '':
      siglaLista = ''
      if lista_com_o_livro == 'Livros Lidos':
        siglaLista = "LL"
      elif lista_com_o_livro == 'Lendo no Momento':
        siglaLista = "LM"
      elif lista_com_o_livro == 'Leituras Futuras':
        siglaLista = "LF"
      elif lista_com_o_livro == 'Livros Abandonados':
        siglaLista = "LA"

      lista_livro = Usuario_Lista.query.filter_by(
          usuario_id=usuario_id, tipo_lista=siglaLista).first()
      idDaLista = lista_livro.lista_id

      Lista_Livro.query.filter_by(lista_id=idDaLista,
                                  livro_id=idLivro).delete()
      db.session.commit()
      if verificarexiste[1] == 1:
        Usuario_Lista.remover_livro_lista_favorito(usuario_id, idLivro)
        return 0
      else:
        return 0
    else:
      return 1

  @staticmethod
  def remover_livro_lista_favorito(usuario_id, idLivro):
    lista_livro = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                tipo_lista="FAV").first()
    idDaLista = lista_livro.lista_id
    Lista_Livro.query.filter_by(lista_id=idDaLista, livro_id=idLivro).delete()
    db.session.commit()
    return 0

  @staticmethod
  def gerar_dicionario(livro):
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
        ISBN.append({
            'ISBN': ISBNs['type'],
            'Identificador': ISBNs['identifier']
        })
    if 'pageCount' in livro['volumeInfo']:
      numeroPaginasLivro = livro['volumeInfo']['pageCount']

    generosDoLivro = Livro_Genero.buscar_genero_webscrapper(
        idDoLivro, categoriasDoLivro)
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

  @staticmethod
  def get_lista_livros_recomendados(usuario_id):
    livros_lidos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                 tipo_lista="LL").first()
    lendo_momento = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                  tipo_lista="LM").first()
    lista_livros_lidos = Lista_Livro.query.filter_by(
        lista_id=livros_lidos.lista_id).all()
    lista_livros_momento = Lista_Livro.query.filter_by(
        lista_id=lendo_momento.lista_id).all()
    merge_lista_livros = lista_livros_lidos + lista_livros_momento

    lista_generos = []

    listaExclusao = []

    for item in merge_lista_livros:
      lista_generos = lista_generos + Livro_Genero.buscar_genero_webscrapper(
          item.livro_id)
      listaExclusao.append(item.livro_id)

    contador_generos = {i: lista_generos.count(i) for i in lista_generos}
    lista_ordenada_generos = dict(
        sorted(contador_generos.items(),
               key=operator.itemgetter(1),
               reverse=True))
    quantidade_lista_ordenada = len(lista_ordenada_generos)
    livros_recomendados = []

    if quantidade_lista_ordenada == 1:
      livros_recomendados = Livro_Genero.getColecaoGenerosRecomendacao(
          list(contador_generos.keys())[0], listaExclusao, 18)

    elif quantidade_lista_ordenada == 2:
      livros_recomendados = livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
          list(contador_generos.keys())[0], listaExclusao, 9)
      for item in livros_recomendados:
        listaExclusao.append(item.id_livro)
      livros_recomendados = livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
          list(contador_generos.keys())[1], listaExclusao, 9)

    elif quantidade_lista_ordenada >= 3:
      livros_recomendados = livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
          list(contador_generos.keys())[0], listaExclusao, 6)
      for item in livros_recomendados:
        listaExclusao.append(item.id_livro)
      livros_recomendados = livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
          list(contador_generos.keys())[1], listaExclusao, 6)
      for item in livros_recomendados:
        listaExclusao.append(item.id_livro)
      livros_recomendados = livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
          list(contador_generos.keys())[2], listaExclusao, 6)
    livros = []
    jsondata = ""
    for item in livros_recomendados:
      url = 'https://www.googleapis.com/books/v1/volumes/' + item.id_livro + '?key=' + API_KEY
      jsondata = realizar_request_api(url)
      dict_livro = Usuario_Lista.gerar_dicionario(jsondata)
      livros.append(dict_livro)
    return livros



  @staticmethod
  def quantidade_livro_lista(usuario_id):
    livros_lidos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                 tipo_lista="LL").first()
    lendo_momento = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                  tipo_lista="LM").first()
    leituras_futuras = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                     tipo_lista="LF").first()
    livros_abandonados = Usuario_Lista.query.filter_by(
        usuario_id=usuario_id, tipo_lista="LA").first()
    livros_favoritos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                     tipo_lista="FAV").first()

    quantidade_ll = Lista_Livro.query.filter_by(lista_id=livros_lidos.lista_id).count()
    quantidade_lm = Lista_Livro.query.filter_by(lista_id=lendo_momento.lista_id).count()
    quantidade_lf = Lista_Livro.query.filter_by(lista_id=leituras_futuras.lista_id).count()
    quantidade_la = Lista_Livro.query.filter_by(lista_id=livros_abandonados.lista_id).count()
    quantidade_fav = Lista_Livro.query.filter_by(lista_id=livros_favoritos.lista_id).count()
    
    return [quantidade_ll, quantidade_lm, quantidade_lf, quantidade_la, quantidade_fav]


  @staticmethod
  def get_id_lista(usuario_id, idLivro):
    livros_lidos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                 tipo_lista="LL").first()
    lendo_momento = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                  tipo_lista="LM").first()
    leituras_futuras = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
                                                     tipo_lista="LF").first()
    livros_abandonados = Usuario_Lista.query.filter_by(
        usuario_id=usuario_id, tipo_lista="LA").first()


    emQualListaExiste = ''
    if Lista_Livro.query.filter_by(lista_id=livros_lidos.lista_id,
                                   livro_id=idLivro).count() != 0:
      emQualListaExiste = livros_lidos.lista_id

    if Lista_Livro.query.filter_by(lista_id=lendo_momento.lista_id,
                                   livro_id=idLivro).count() != 0:
      emQualListaExiste = lendo_momento.lista_id

    if Lista_Livro.query.filter_by(lista_id=leituras_futuras.lista_id,
                                   livro_id=idLivro).count() != 0:
      emQualListaExiste = leituras_futuras.lista_id

    if Lista_Livro.query.filter_by(lista_id=livros_abandonados.lista_id,
                                   livro_id=idLivro).count() != 0:
      emQualListaExiste = livros_abandonados.lista_id

    return emQualListaExiste


  @staticmethod
  def get_lista_livros_recomendados_preferencias(usuario_id,stringPreferencias):
    listaPreferencias = stringPreferencias.split('#')
    contadorListaPreferencias = len(listaPreferencias)
    lista_livros_recomendados = []
    
    livros_lidos = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
       tipo_lista="LL").first()
    lendo_momento = Usuario_Lista.query.filter_by(usuario_id=usuario_id,
        tipo_lista="LM").first()
    leituras_futuras = Usuario_Lista.query.filter_by(usuario_id=usuario_id, tipo_lista = "LF").first()
    leituras_abandonadas = Usuario_Lista.query.filter_by(usuario_id=usuario_id, tipo_lista = "LA").first()
    
    
    lista_livros_lidos = Lista_Livro.query.filter_by( lista_id=livros_lidos.lista_id).all()
    lista_livros_momento = Lista_Livro.query.filter_by(
    lista_id=lendo_momento.lista_id).all()
    lista_livros_futuros = Lista_Livro.query.filter_by(
      lista_id=leituras_futuras.lista_id).all()
    lista_livros_abandonados= Lista_Livro.query.filter_by(
      lista_id=leituras_abandonadas.lista_id).all()
    merge_lista_livros = lista_livros_lidos + lista_livros_momento + lista_livros_futuros + lista_livros_abandonados
    listaExclusao = []
    for item in merge_lista_livros:
      listaExclusao.append(item.livro_id)

    if contadorListaPreferencias == 1:
      lista_livros_recomendados = Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[0], listaExclusao, 18)

    elif contadorListaPreferencias == 2:
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[0], listaExclusao, 9)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[1], listaExclusao, 9)
      
    elif contadorListaPreferencias == 3:
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[0], listaExclusao, 6)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[1], listaExclusao, 6)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[2], listaExclusao, 6)

    elif contadorListaPreferencias == 4:
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[0], listaExclusao, 4)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[1], listaExclusao, 4)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[2], listaExclusao, 5)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[3], listaExclusao, 5)

    elif contadorListaPreferencias == 5:
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[0], listaExclusao, 4)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[1], listaExclusao, 4)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[2], listaExclusao, 4)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[3], listaExclusao, 3)
      for item in lista_livros_recomendados:
        listaExclusao.append(item.id_livro)
      lista_livros_recomendados = lista_livros_recomendados + Livro_Genero.getColecaoGenerosRecomendacao(
        listaPreferencias[4], listaExclusao, 3)

    
    livros = []
    jsondata = ""
    for item in lista_livros_recomendados:
      url = 'https://www.googleapis.com/books/v1/volumes/' + item.id_livro + '?key=' + API_KEY
      jsondata = realizar_request_api(url)
      dict_livro = Usuario_Lista.gerar_dicionario(jsondata)
      livros.append(dict_livro)
    return livros
