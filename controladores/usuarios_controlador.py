import sys
from flask import render_template, redirect, url_for, request, abort,flash
from flask_login import login_user, logout_user, current_user, login_required
from modelos.usuarios_modelo import Usuario
from modelos.formularios_modelo import LoginForm
from flask_sqlalchemy import SQLAlchemy
from database import db
from passlib.hash import pbkdf2_sha256

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

      buscar_usuario = Usuario.query.filter_by(email=email).first()  

      if buscar_usuario:  
          flash('Email já existe')
          return redirect(url_for('usuarios_bp.cadastrar'))
  
      usuario = Usuario(nome, email, senha)
      db.session.add(usuario)
      db.session.commit()
      return redirect(url_for('indice'))

def verificar_senha(senha):
  """
  Verifica a "força" da senha
  Senha forte:
      8 caracteres ou mais 
      1 digito ou mais
      1 simbolo ou mais
      1 letra maiuscula ou mais
      1 letra minuscula ou mais
  """

  # calculating the length
  length_error = len(password) < 8
  
  # searching for digits
  digit_error = re.search(r"\d", password) is None
  
  # searching for uppercase
  uppercase_error = re.search(r"[A-Z]", password) is None
  
  # searching for lowercase
  lowercase_error = re.search(r"[a-z]", password) is None
  
  # searching for symbols
  symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
  
  # overall result
  password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
  
  return {
      'password_ok' : password_ok,
      'length_error' : length_error,
      'digit_error' : digit_error,
      'uppercase_error' : uppercase_error,
      'lowercase_error' : lowercase_error,
      'symbol_error' : symbol_error,
  }

def login():
  if current_user.is_authenticated:
    return redirect(url_for('indice'))
  else:
    form = LoginForm()
    if form.validate_on_submit():
      usuario = Usuario.query.filter_by(email=form.email.data).first()
      if usuario and pbkdf2_sha256.verify(form.senha.data, usuario.senha):
        login_user(usuario)
        flash("Logado com sucesso")
        return redirect(url_for('indice'))
      else:
        flash("Usuário ou senha inválidos")
    
    return render_template('login_usuario.html', form_login=form)

def logout():
  logout_user()
  flash("Deslogado com sucesso")
  return redirect(url_for('indice'))