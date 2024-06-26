from flask import Blueprint
from controladores.usuarios_controlador import cadastrar,login,logout, checar_senha,checar_email,pagina_usuario,buscar_lista_usuario, atualizar_preferencias_usuario

usuarios_bp = Blueprint('usuarios_bp', __name__,template_folder='templates')

usuarios_bp.route('/cadastrar', methods=['GET','POST'])(cadastrar)
usuarios_bp.route('/login', methods = ['GET', 'POST'])(login)
usuarios_bp.route('/logout')(logout)
usuarios_bp.route('/checar-senha', methods=['GET'])(checar_senha)
usuarios_bp.route('/checar-email', methods=['GET'])(checar_email)
usuarios_bp.route('/paginausuario', methods=['GET'])(pagina_usuario)
usuarios_bp.route('/paginausuario/<string:tipoLista>', methods=['GET'])(buscar_lista_usuario)
usuarios_bp.route('/atualizarPreferencias', methods = ['GET', 'POST'])(atualizar_preferencias_usuario)