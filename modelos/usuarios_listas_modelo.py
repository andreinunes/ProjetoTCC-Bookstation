from modelos.listas_livros_modelo import Lista_Livro
from flask_sqlalchemy import SQLAlchemy
from database import db


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
  def get_lista_livros_lidos(usuario_id):
    lista_livros_lido = Usuario_Lista.query.filter_by(usuario_id=usuario_id, tipo_lista="LL").first()
    livros_lista_lido = Lista_Livro.query.filter_by(lista_id=lista_livros_lido.lista_id).all
    return livros_lista_lido