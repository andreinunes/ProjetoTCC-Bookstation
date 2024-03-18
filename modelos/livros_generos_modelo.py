from database import db

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