from flask import Blueprint
from controladores.usuarios_controlador import cadastrar

usuarios_bp = Blueprint('usuarios_bp', __name__,template_folder='templates')

usuarios_bp.route('/cadastrar', methods=['GET','POST'])(cadastrar)