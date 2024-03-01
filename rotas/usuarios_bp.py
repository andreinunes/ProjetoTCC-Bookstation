from flask import Blueprint
from controladores.usuarios_controlador import cadastrar,login,logout

usuarios_bp = Blueprint('usuarios_bp', __name__,template_folder='templates')

usuarios_bp.route('/cadastrar', methods=['GET','POST'])(cadastrar)
usuarios_bp.route('/login', methods = ['GET', 'POST'])(login)
usuarios_bp.route('/logout')(logout)