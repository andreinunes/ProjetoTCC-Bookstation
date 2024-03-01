from re import DEBUG
from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager
from database import db
from rotas.usuarios_bp import usuarios_bp
from modelos.usuarios_modelo import Usuario

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
  
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=81)