from modelos.usuarios_modelo import Usuario
from flask import url_for

def test_app_eh_criado(app):
  assert app.name == 'app'

def test_config_esta_carregada(config):
  assert config["DEBUG"] is True

def test_pagina_404(client):
  resposta = client.get("/pagina_nao_existe")
  assert '<h1 class="display-1 fw-bold">404</h1>' in resposta.data.decode('utf-8')

def test_cadastro(client,app):
  resposta = client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with app.app_context():
      assert Usuario.query.count() == 1
      assert Usuario.query.first().email == "teste@teste.com"


def test_login(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})
  
  with client:
    resposta = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    assert b'TesteMan' in resposta.data
    
    assert len(captured_templates) == 1

    template = captured_templates[0]

    assert template.name == "indice.html"

def test_login_invalid_credentials(client, app,captured_templates):
  resposta = client.post(
      url_for('usuarios_bp.login'),
      data={'email': 'invalid@example.com', 'senha': 'wrongpassword'},
      follow_redirects=True
  )
  assert 'Login' in resposta.data.decode('utf-8')
  assert len(captured_templates) == 1
  template = captured_templates[0]
  assert template.name == "login_usuario.html"
  
      
