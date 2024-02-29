import sys
from flask import render_template, redirect, url_for, request, abort,flash
from modelos.usuarios_modelo import Usuario
from flask_sqlalchemy import SQLAlchemy
from database import db

def cadastrar():
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

    
    usuario = Usuario(nome, email, senha)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('indice'))
    