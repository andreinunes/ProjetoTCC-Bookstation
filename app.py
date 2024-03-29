from re import DEBUG
from flask import Flask, render_template, request, redirect, url_for, session,g,send_file
from flask_migrate import Migrate
from flask_login import LoginManager,current_user
from database import db
from rotas.usuarios_bp import usuarios_bp
from rotas.livros_bp import livros_bp
from modelos.usuarios_modelo import Usuario
import requests
import random

from datetime import timedelta


app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
lm = LoginManager()
lm.init_app(app)
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(livros_bp, url_prefix='/livros')


@lm.user_loader
def load_user(id):
    return Usuario.query.filter_by(id=id).first()

@app.route('/')
def indice():
    return render_template('indice.html')

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
    app.permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True
    g.user = current_user
  
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=81)