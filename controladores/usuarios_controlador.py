from flask import render_template, redirect, url_for, request,flash,jsonify
from flask_login import logout_user, current_user
from modelos.usuarios_modelo import Usuario
from modelos.formularios_modelo import LoginForm
from modelos.usuarios_listas_modelo import Usuario_Lista
from modelos.usuarios_preferencias_modelo import Usuario_Preferencia
from funcoes_auxiliares import verificar_forca_senha

def cadastrar():
  if current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    if request.method == 'GET':
      return render_template('cadastrar_usuario.html')
    elif request.method == 'POST':
      nome = request.form['nomeUsuario']
      email = request.form['emailUsuario']
      senha = request.form['senhaUsuario']
      csenha = request.form['confirmacaoSenhaUsuario']
  
      if senha != csenha:
        flash('Senhas incompativeis')
        return redirect(url_for('usuarios_bp.cadastrar'))

      if Usuario.busca_usuario(email) :  
          flash('Email já existe')
          return redirect(url_for('usuarios_bp.cadastrar'))

      if Usuario.cadastrar_usuario(nome, email, senha):
        return redirect(url_for('indice'))

def checar_senha():
  senha_entrada = request.args.get('senhaUsuario', '')
  resultado = verificar_forca_senha(senha_entrada)
  return jsonify({"resultado": resultado})

def login():
  if current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    form = LoginForm()
    if form.validate_on_submit():
      usuario = Usuario.login_usuario(form)
      if usuario != '0':
        flash("Logado com sucesso")
        return redirect(url_for('indice'))
      else:
        flash("Usuário ou senha inválidos")
    return render_template('login_usuario.html', form_login=form)

def logout():
  logout_user()
  flash("Deslogado com sucesso")
  return redirect(url_for('indice'))


def pagina_usuario():
  if not current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    quantidade_livros = Usuario_Lista.quantidade_livro_lista(current_user.id)
    stringPreferencias = Usuario_Preferencia.get_preferencias_usuario(current_user.id)
    return render_template('pagina_usuario.html', usuario=current_user,quantidade_livros=quantidade_livros, stringPreferencias = stringPreferencias)

def buscar_lista_usuario(tipoLista):
  if not current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    lista_livros = []
    descricaoLista = ""
    if tipoLista == 'LL':
      descricaoLista = "LIVROS LIDOS"
    elif tipoLista == 'LF':
      descricaoLista = "LEITURAS FUTURAS"
    elif tipoLista == 'LM':
      descricaoLista = "LENDO NO MOMENTO"
    elif tipoLista == 'LA':
      descricaoLista = "LIVROS ABANDONADOS"
    elif tipoLista == 'FAV':
      descricaoLista = "FAVORITOS"
    elif tipoLista == 'REC':
      descricaoLista = "RECOMENDAÇÃO!"
    elif tipoLista == 'RECPREF':
      descricaoLista = "RECOMENDAÇÃO!!"
    stringPreferencias = Usuario_Preferencia.get_preferencias_usuario(current_user.id)
    lista_livros = Usuario_Lista.get_lista_livros(current_user.id,tipoLista, stringPreferencias)
    quantidadeRetorno = 0
    if lista_livros is None:
      quantidadeRetorno = 0
    else:
      quantidadeRetorno = len(lista_livros)
      
    return render_template('pagina_usuario.html', usuario=current_user ,listaLivros = lista_livros, quantidadeRetorno = quantidadeRetorno, descricaoLista = descricaoLista,stringPreferencias = stringPreferencias)


def atualizar_preferencias_usuario():
  if not current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    if request.method == 'GET':
      return redirect(url_for('indice'))
    elif request.method == 'POST':
      stringPreferencias = request.form['stringPreferencias']
      retornoAtualizaoPreferencias = Usuario_Preferencia.atualizar_preferencias_usuario(current_user.id,stringPreferencias)
      return redirect(url_for('usuarios_bp.pagina_usuario'))


      
      