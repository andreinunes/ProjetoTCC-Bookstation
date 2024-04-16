from modelos.usuarios_modelo import Usuario
from controladores.usuarios_controlador import verificar_forca_senha
from controladores.generos_controlador import getGeneroChave,verificar_genero
from flask import url_for
from funcoes_auxiliares import remove_html_tags, formatar_palavra_busca,converter_data

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

def test_login_credenciais_invalidas(client, app,captured_templates):
  resposta = client.post(
      url_for('usuarios_bp.login'),
      data={'email': 'exemplo@invalido.com', 'senha': 'senhaerrada'},
      follow_redirects=True
  )
  assert 'Login' in resposta.data.decode('utf-8')
  assert len(captured_templates) == 1
  template = captured_templates[0]
  assert template.name == "login_usuario.html"

def test_logout(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    resposta = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    resposta = client.get(
        url_for('usuarios_bp.logout'),
        follow_redirects=True
    )
    assert b'Cadastre-se' in resposta.data

    template = captured_templates[1]

    assert template.name == "indice.html"

def test_verificar_forca_senha():
  
  assert verificar_forca_senha('teste') == 'Senha Fraca: Senha deve conter no minimo 8 caracteres'
  assert verificar_forca_senha('teste123') == 'Senha Fraca: Senha deve conter no minimo uma letra maiuscula e uma minuscula'
  assert verificar_forca_senha('TESTE123') == 'Senha Fraca: Senha deve conter no minimo uma letra maiuscula e uma minuscula'
  assert verificar_forca_senha('Testeteste') == 'Senha fraca: Senha deve conter no mínimo um digito'
  assert verificar_forca_senha('Testeteste123') == 'Senha fraca: Senha deve conter pelo menos um caractere especial'
  assert verificar_forca_senha('Testeteste123%') == ''

def test_remove_tag_html():
  assert remove_html_tags('<h1>Teste</h1>') == 'Teste'
  assert remove_html_tags('<h1>Teste</h1><p>Teste</p>') == 'TesteTeste'
  assert remove_html_tags('<h1>Teste</h1><p>Teste</p><p>Teste</p>') == 'TesteTesteTeste'
  assert remove_html_tags('Teste') == 'Teste'

def test_formatar_palavra_busca():
  assert formatar_palavra_busca('Palavra Separada') == 'Palavra%2BSeparada'
  assert formatar_palavra_busca('Testão') == 'Test%C3%A3o'

def test_converter_data():
  assert converter_data('2020-01-01') == 'Janeiro 1, 2020'
  assert converter_data('2020') == '2020'
  assert converter_data('') == ''
  assert converter_data('01-01-2020') == '01-01-2020'

def test_verificar_genero():
  assert verificar_genero('Fantasy') == 'Fantasy'
  assert verificar_genero('Fantasia') == 'Fantasy'
  assert verificar_genero('Teste') == '0'

def test_getGeneroChave_valido():
  assert getGeneroChave('Fantasy') == 'Fantasia'
  assert getGeneroChave('Drama') == 'Drama'
  assert getGeneroChave('Action') == 'Ação'
  assert getGeneroChave('Biography') == 'Biografia'

def test_getGeneroChave_invalido():
  assert getGeneroChave('Fantasia') == ''
  assert getGeneroChave('') == ''
  assert getGeneroChave('Test') == ''


def test_busca_livro_titulo(client,captured_templates):
  resposta = client.get("/livros/buscarLivrosTitulo/Teste/0")

  assert b'Resultado da busca: Teste' in resposta.data

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "busca_livros.html"

def test_busca_livro_titulo_inexistente(client,captured_templates):
  resposta = client.get("/livros/buscarLivrosTitulo/testetituloquenaoexiste/0")

  assert 'Não há resultados' in resposta.data.decode('utf-8')

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "busca_livros.html"

def test_busca_livro_autor(client,captured_templates):
  resposta = client.get("/livros/buscarLivrosAutor/Sanderson/0")

  assert b'Resultado da busca: Sanderson' in resposta.data

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "busca_livros.html"

def test_busca_livro_autor_inexistente(client,captured_templates):
  resposta = client.get("/livros/buscarLivrosAutor/testeautorquenaoexiste/0")

  assert 'Não há resultados' in resposta.data.decode('utf-8')

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "busca_livros.html"

def test_buscar_livro_id(client,captured_templates):
  resposta = client.get("livros/paginalivro/_J4qAwAAQBAJ")

  assert 'Genêros' in resposta.data.decode('utf-8')

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "pagina_livro.html"

def test_buscar_livro_id_inexistente(client,captured_templates):
  resposta = client.get("livros/paginalivro/idinexistente")

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "indice.html"



def test_busca_livro_genero(client,captured_templates):
  resposta = client.get("livros/buscarLivrosGenero/Fantasia/")

  assert b'Fantasia' in resposta.data

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "busca_livros.html"

def test_busca_livro_genero_inexistente(client,captured_templates):
  resposta = client.get("/livros/buscarLivrosGenero/Teste/")

  assert 'Não há resultados' in resposta.data.decode('utf-8')

  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "busca_livros.html"
  
  
  
  
      
