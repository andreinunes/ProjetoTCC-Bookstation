from database import db
from passlib.hash import pbkdf2_sha256

class Usuario(db.Model):
  __tablename__ = 'usuario'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  nome = db.Column(db.String(100),nullable = False)
  email = db.Column(db.String(100),nullable = False)
  senha = db.Column(db.String(100),nullable = False)

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