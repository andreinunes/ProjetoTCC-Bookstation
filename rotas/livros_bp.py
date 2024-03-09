from flask import Blueprint
from controladores.livros_controlador import buscar_por_titulo_e_autor,buscar_por_autor,buscar_por_genero

livros_bp = Blueprint('livros_bp', __name__,template_folder='templates')

livros_bp.route('/buscarLivros', methods=['GET','POST'])(buscar_por_titulo_e_autor)
livros_bp.route('/buscarLivros/<autor>')(buscar_por_autor)
livros_bp.route('/buscarLivrosGenero/<genero>')(buscar_por_genero)
