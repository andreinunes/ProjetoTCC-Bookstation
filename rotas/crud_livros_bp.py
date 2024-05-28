from flask import Blueprint
from controladores.crud_livros_controlador import adicionar_livro, remover_livro,remover_livro_favoritos, adicionar_nota_livro

crud_livros_bp = Blueprint('crud_livros_bp', __name__,template_folder='templates')

crud_livros_bp.route('/adicionarLivroEmLista/<string:idLivro>/<string:tipoLista>', methods=['GET','POST'])(adicionar_livro)

crud_livros_bp.route('/removerLivroDaLista/<string:idLivro>', methods=['GET','POST'])(remover_livro)

crud_livros_bp.route('/removerLivroFavoritos/<string:idLivro>', methods=['GET','POST'])(remover_livro_favoritos)

crud_livros_bp.route('/adicionarNotaEmLivro/<string:livro_id>/<string:nota_livro>', methods=['GET','POST'])(adicionar_nota_livro)

