from flask import Blueprint
from controladores.livros_controlador import buscar_por_titulo, buscar_por_autor,buscar_por_genero,buscar_livro_id,auxiliar_busca

livros_bp = Blueprint('livros_bp', __name__,template_folder='templates')

livros_bp.route('/busca_livros', methods=['GET','POST'])(auxiliar_busca)
livros_bp.route('/buscarLivrosTitulo/<string:nomeLivro>/<int:indiceInicial>', methods=['GET'])(buscar_por_titulo)
livros_bp.route('/buscarLivrosAutor/<string:nomeAutor>/<int:indiceInicial>', methods=['GET'])(buscar_por_autor)

livros_bp.route('/buscarLivrosGenero/<string:genero>/<int:indiceInicial>', methods= ['GET'])(buscar_por_genero)
livros_bp.route('/paginalivro/<id>')(buscar_livro_id)
