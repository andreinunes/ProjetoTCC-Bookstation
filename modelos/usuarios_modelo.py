from database import db
from flask_login import login_user
from passlib.hash import pbkdf2_sha256
from modelos.usuarios_listas_modelo import Usuario_Lista

class Usuario(db.Model):
  __tablename__ = 'usuario'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  nome = db.Column(db.String(100),nullable = False)
  email = db.Column(db.String(100),nullable = False)
  senha = db.Column(db.String(100),nullable = False)
  listas = db.relationship('Usuario_Lista', backref='usuario', lazy=True)
  preferencias = db.relationship('Usuario_Preferencia', backref='usuario', lazy=True)

  @property
  def is_authenticated(self):
    return True
    
  @property
  def is_active(self):
    return True
    
  @property
  def is_anonymous(self):
    return False
    
  def get_id(self):
    return str(self.id)
  
  def __init__(self, nome, email, senha):
    self.nome = nome
    self.email = email
    self.senha = pbkdf2_sha256.hash(senha)

  def __repr__(self):
    return "Usuário: {}".format(self.nome)

  @staticmethod
  def busca_usuario(email):
    buscar_usuario = Usuario.query.filter_by(email=email).first()  
    return buscar_usuario
  
  @staticmethod
  def cadastrar_usuario(nome, email, senha):
    usuario = Usuario(nome, email, senha)
    db.session.add(usuario)
    db.session.commit()
    login_user(usuario)
    Usuario_Lista.criar_listas_novos_usuarios(usuario.id)
    return usuario

  @staticmethod
  def login_usuario(form):
    usuario = Usuario.query.filter_by(email=form.email.data.strip()).first()
    if usuario and pbkdf2_sha256.verify(form.senha.data.strip(), usuario.senha):
      login_user(usuario)
      return usuario
    else:
      return '0'


db.create_all()