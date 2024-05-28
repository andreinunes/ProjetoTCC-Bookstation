from flask import Flask, render_template, session,g,send_file
from flask_migrate import Migrate
from flask_login import LoginManager,current_user
from database import db
from rotas.usuarios_bp import usuarios_bp
from rotas.busca_livros_bp import busca_livros_bp
from rotas.crud_livros_bp import crud_livros_bp
from modelos.usuarios_modelo import Usuario
from modelos.busca_livro_modelo import Busca_Livro


from datetime import timedelta

def create_app(database_uri = 'sqlite:///weblivros.db'):
  app = Flask(__name__, static_url_path='/static')
  app.config.from_object('config')
  app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
  db.init_app(app)
  migrate = Migrate(app, db)
  lm = LoginManager()
  lm.init_app(app)
  app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
  app.register_blueprint(busca_livros_bp, url_prefix='/livros')
  app.register_blueprint(crud_livros_bp, url_prefix='/crud_livros')
  
  
  @lm.user_loader
  def load_user(id):
      return Usuario.query.filter_by(id=id).first()
  
  @app.route('/')
  def indice():
    buscaLivrosFantasia = Busca_Livro.buscar_por_genero("Fantasia",4)
    buscaLivrosBiografia = Busca_Livro.buscar_por_genero("Biografia",4)
    buscaLivrosDrama = Busca_Livro.buscar_por_genero("Drama",4)
    livrosFantasia = buscaLivrosFantasia[1]
    livrosBiografia = buscaLivrosBiografia[1]
    livrosDrama= buscaLivrosDrama[1]
    return render_template('indice.html', livrosFantasia = livrosFantasia, livrosBiografia = livrosBiografia, livrosDrama = livrosDrama )
  
  @app.route("/imagem_indisponivel.png") 
  def imagem_indisponivel(): 
    return send_file("imagens/imagem_indisponivel.png", mimetype="image/png")
  
  @app.errorhandler(404)
  def not_found_error(error):
      return render_template('erro.html', erro = 404), 404
  
  @app.errorhandler(500)
  def internal_error(error):
      db.session.rollback()
      return render_template('erro.html',erro = 500), 500
  
  @app.before_request
  def before_request():
      session.permanent = True
      app.permanent_session_lifetime = timedelta(minutes=30)
      session.modified = True
      g.user = current_user
  
  return app

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run(host='0.0.0.0',port=81)