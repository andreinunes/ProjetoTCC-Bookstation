from flask import redirect, url_for, request,flash
from flask_login import current_user
from modelos.usuarios_listas_modelo import Usuario_Lista

def adicionar_livro(idLivro,tipoLista):
  if not current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    if request.method == 'GET':
      return redirect(url_for('indice'))
    elif request.method == 'POST':
      idLivro = request.form['idLivro']
      tipoLista = request.form['tipoLista']
      retornoAdicaoLivro = Usuario_Lista.adicionar_livro_lista(current_user.id,tipoLista,idLivro)
      if retornoAdicaoLivro == 0:
        
        flash("Livro adicionado com sucesso")
        return  redirect(url_for('livros_bp.buscar_livro_id',id = idLivro))

      elif retornoAdicaoLivro == 1:

        flash('Livro já na lista')
        return  redirect(url_for('indice'))


def remover_livro(idLivro):
  if not current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    if request.method == 'GET':
      return redirect(url_for('indice'))
    elif request.method == 'POST':
      idLivro = request.form['idLivroExcluir']
      retornoRemocaoLivro = Usuario_Lista.remover_livro_lista(current_user.id,idLivro)
      if retornoRemocaoLivro == 0:

        flash("Livro removido com sucesso")
        return  redirect(url_for('livros_bp.buscar_livro_id',id = idLivro))

      elif retornoRemocaoLivro == 1:

        flash('Não foi possível remover o livro')
        return  redirect(url_for('livros_bp.buscar_livro_id',id = idLivro))

def remover_livro_favoritos(idLivro):
  if not current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    if request.method == 'GET':
      return redirect(url_for('indice'))
    elif request.method == 'POST':
      idLivro = request.form['idLivroExcluirFavorito']
      retornoRemocaoLivro = Usuario_Lista.remover_livro_lista_favorito(current_user.id,idLivro)
      if retornoRemocaoLivro == 0:

        flash("Livro removido com sucesso")
        return  redirect(url_for('livros_bp.buscar_livro_id',id = idLivro))

      elif retornoRemocaoLivro == 1:

        flash('Não foi possível remover o livro')
        return  redirect(url_for('livros_bp.buscar_livro_id',id = idLivro))