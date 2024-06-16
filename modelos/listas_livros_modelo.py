from database import db

class Lista_Livro(db.Model):
  __tablename__ = 'listas_livros'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  lista_id = db.Column(db.Integer, db.ForeignKey('usuarios_listas.lista_id'),nullable=False)
  livro_id = db.Column(db.String(100),nullable = False)
  nota_livro = db.Column(db.Integer, nullable = True)

  def __init__(self, lista_id, livro_id):
    self.lista_id = lista_id
    self.livro_id = livro_id

  def __repr__(self):
    return "lista_id: {}".format(self.lista_id)

  @staticmethod
  def adicionar_nota_livro(lista_id,livro_id,nota_livro):
    if nota_livro >= 5:
      nota_livro = 5
    if nota_livro <= 0:
      nota_livro = 0
    lista_livro = Lista_Livro.query.filter_by(
      lista_id=lista_id, livro_id = livro_id).first()
    lista_livro.nota_livro = nota_livro
    db.session.commit()
    return 0

  @staticmethod
  def buscar_nota_livro(lista_id,usuario_id,livro_id):
    lista_livro = Lista_Livro.query.filter_by(
      lista_id=lista_id, livro_id = livro_id).first()
    if lista_livro.nota_livro is None:
      return -1
    else:
      return lista_livro.nota_livro

  @staticmethod
  def buscar_media_livro(livro_id):
    lista_livro = Lista_Livro.query.filter_by(livro_id = livro_id).all()
    media_livro = 0
    quantidade_notas = 0
    for item in lista_livro:
      if item.nota_livro is not None:
        media_livro = media_livro + item.nota_livro
        quantidade_notas = quantidade_notas + 1

    if quantidade_notas == 0:
      media_livro = 0
    else:
      media_livro = media_livro / quantidade_notas
    return media_livro