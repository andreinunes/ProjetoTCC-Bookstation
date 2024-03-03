from re import DEBUG
from flask import Flask, render_template, request, redirect, url_for, session,g,send_file
from flask_migrate import Migrate
from flask_login import LoginManager,current_user
from database import db
from rotas.usuarios_bp import usuarios_bp
from modelos.usuarios_modelo import Usuario

from datetime import timedelta


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
lm = LoginManager()
lm.init_app(app)
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

@lm.user_loader
def load_user(id):
    return Usuario.query.filter_by(id=id).first()

@app.route('/')
def indice():
    return render_template('indice.html')

@app.route("/logo_provisorio.png") 
def logo(): 
  return send_file("imagens/logo_provisorio.png", mimetype="image/png")

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True
    g.user = current_user
  
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=81)