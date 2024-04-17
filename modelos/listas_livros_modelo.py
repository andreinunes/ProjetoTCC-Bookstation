from database import db

class Lista_Livro(db.Model):
  __tablename__ = 'listas_livros'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  lista_id = db.Column(db.Integer, db.ForeignKey('usuarios_listas.lista_id'),nullable=False)
  livro_id = db.Column(db.String(100),nullable = False)

  def __init__(self, lista_id, livro_id):
    self.lista_id = lista_id
    self.livro_id = livro_id

  def __repr__(self):
    return "lista_id: {}".format(self.lista_id)