from database import db
from funcoes_auxiliares import getDicionarioGeneros



class Usuario_Preferencia(db.Model):
  __tablename__ = 'usuarios_preferencias'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  usuario_id = db.Column(db.Integer,
                         db.ForeignKey('usuario.id'),
                         nullable=False)
  nome_genero = db.Column(db.String(100),nullable = False)
  estado_preferencia = db.Column(db.String(3),nullable = False)

  def __init__(self, usuario_id, nome_genero,estado_preferencia):
    self.usuario_id = usuario_id
    self.nome_genero = nome_genero
    self.estado_preferencia = estado_preferencia

  def __repr__(self):
    return "usuario_id: {}".format(self.usuario_id)


  @staticmethod
  def gerar_preferencias_usuario(usuario_id):
    DicionarioGeneros = getDicionarioGeneros()
    for genero in DicionarioGeneros:
      preferencia = Usuario_Preferencia(usuario_id,DicionarioGeneros[genero],"I")
      db.session.add(preferencia)
      db.session.commit()
    return 0

  @staticmethod
  def atualizar_preferencias_usuario(usuario_id,stringPreferencias):
    listaPreferenciasUsuario = Usuario_Preferencia.query.filter_by(
      usuario_id=usuario_id).count()
    if listaPreferenciasUsuario == 0:
      Usuario_Preferencia.gerar_preferencias_usuario(usuario_id)
    
    listaPreferenciasAtualizacao = stringPreferencias.split('#')
    for preferenciasAtualizacao in listaPreferenciasAtualizacao:
      preferencia = Usuario_Preferencia.query.filter_by( usuario_id=usuario_id,nome_genero=preferenciasAtualizacao).first()
      if preferencia is None:
        preferenciaAdicionar = Usuario_Preferencia(usuario_id,preferenciasAtualizacao,"I")
        db.session.add(preferenciaAdicionar)
        db.session.commit()
      
    listaPreferenciasUsuario = Usuario_Preferencia.query.filter_by(
      usuario_id=usuario_id).all()
    for preferencia in listaPreferenciasUsuario:
      if preferencia.nome_genero in listaPreferenciasAtualizacao:
        preferencia.estado_preferencia = "A"
      elif preferencia.nome_genero not in listaPreferenciasAtualizacao:
        preferencia.estado_preferencia = "I"
      db.session.commit()
    
    return listaPreferenciasUsuario

  @staticmethod
  def get_preferencias_usuario(usuario_id):
    listaPreferenciasUsuario = Usuario_Preferencia.query.filter_by(
      usuario_id=usuario_id, estado_preferencia = "A" ).all()
    listaPreferencias = []
    stringPreferencias = ''
    for preferencia in listaPreferenciasUsuario:
      listaPreferencias.append(preferencia.nome_genero)
      stringPreferencias = '#'.join(listaPreferencias)
    return stringPreferencias
    
    

  
    
