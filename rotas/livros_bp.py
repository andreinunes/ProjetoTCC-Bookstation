from flask import Blueprint
from controladores.livros_controlador import buscar_por_titulo

livros_bp = Blueprint('livros_bp', __name__,template_folder='templates')

livros_bp.route('/buscar_por_titulo', methods=['GET','POST'])(buscar_por_titulo)
