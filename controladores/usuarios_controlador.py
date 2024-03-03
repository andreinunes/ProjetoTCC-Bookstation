import sys
import re
from flask import render_template, redirect, url_for, request, abort,flash, jsonify
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
      login_user(usuario)
      return redirect(url_for('indice'))



def checar_senha():
  senha_entrada = request.args.get('senhaUsuario', '')
  resultado = verificar_forca_senha(senha_entrada)
  return jsonify({"resultado": resultado})


def verificar_forca_senha(senha):
  tamanho_minimo = 8
  maiusculo_regex = re.compile(r'[A-Z]')
  minusculo_regex = re.compile(r'[a-z]')
  digito_regex = re.compile(r'\d')
  caracter_especial_regex = re.compile(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]')
  
  if len(senha) < tamanho_minimo:
      return "Senha Fraca: Senha deve conter no minimo {} caracteres".format(tamanho_minimo)
  
  if not maiusculo_regex.search(senha) or not minusculo_regex.search(senha):
      return "Senha Fraca: Senha deve conter no minimo uma letra maiuscula e uma minuscula"
  
  if not digito_regex.search(senha):
      return "Senha fraca: Senha deve conter no mínimo um digito"
  
  if not caracter_especial_regex.search(senha):
      return "Senha fraca: Senha deve conter pelo menos um caractere especial"
  
  return ""

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