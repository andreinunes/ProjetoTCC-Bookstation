from flask import Blueprint
from controladores.busca_livros_controlador import buscar_por_titulo, buscar_por_autor,buscar_por_genero,buscar_livro_id

busca_livros_bp = Blueprint('livros_bp', __name__,template_folder='templates')

busca_livros_bp.route('/buscarLivrosTitulo/<string:nomeLivro>/<int:indiceInicial>', methods=['GET'])(buscar_por_titulo)

busca_livros_bp.route('/buscarLivrosAutor/<string:nomeAutor>/<int:indiceInicial>', methods=['GET'])(buscar_por_autor)

busca_livros_bp.route('/buscarLivrosGenero/<string:genero>/', methods= ['GET'])(buscar_por_genero)

busca_livros_bp.route('/paginalivro/<id>', methods=['GET'])(buscar_livro_id)
