from modelos.usuarios_modelo import Usuario
from controladores.usuarios_controlador import verificar_forca_senha
from modelos.livros_generos_modelo import Livro_Genero
from modelos.listas_livros_modelo import Lista_Livro
from modelos.usuarios_preferencias_modelo import Usuario_Preferencia
from modelos.busca_livro_modelo import Busca_Livro
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
  assert Livro_Genero.verificar_genero('Fantasy') == 'Fantasy'
  assert Livro_Genero.verificar_genero('Fantasia') == 'Fantasy'
  assert Livro_Genero.verificar_genero('Teste') == '0'

def test_getGeneroChave_valido():
  assert Livro_Genero.getGeneroChave('Fantasy') == 'Fantasia'
  assert Livro_Genero.getGeneroChave('Drama') == 'Drama'
  assert Livro_Genero.getGeneroChave('Action') == 'Ação'
  assert Livro_Genero.getGeneroChave('Biography') == 'Biografia'

def test_getGeneroChave_invalido():
  assert Livro_Genero.getGeneroChave('Fantasia') == ''
  assert Livro_Genero.getGeneroChave('') == ''
  assert Livro_Genero.getGeneroChave('Test') == ''


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
    resposta = Busca_Livro.buscar_livro_id(id = 'idinexistente')
    assert resposta[0] is None



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

def test_adicionar_livro_lista(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    with app.app_context():
      assert Lista_Livro.query.count() == 1
      assert Lista_Livro.query.first().livro_id == "_J4qAwAAQBAJ"


def test_adicionar_livro_lista_inexistente(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "XX"},
        follow_redirects=True
    )
    with app.app_context():
      assert Lista_Livro.query.count() == 0

    assert len(captured_templates) == 2

    template = captured_templates[1]

    assert template.name == "indice.html"
      
def test_adicionar_livro_repetido_lista(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaAdicaoRepetida = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LA"},
        follow_redirects=True
    )
    
    with app.app_context():
      assert Lista_Livro.query.count() == 1

    assert len(captured_templates) == 3

    template = captured_templates[2]

    assert template.name == "indice.html"


def test_adicionar_livro_lista_favoritos(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaAdicaoFavoritos = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "FAV"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "FAV"},
        follow_redirects=True
    )
    
    with app.app_context():
      assert Lista_Livro.query.count() == 2

def test_remover_livro_lista_favoritos(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaAdicaoFavoritos = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "FAV"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "FAV"},
        follow_redirects=True
    )
    respostaRemocaoFavoritos = client.post(
        url_for('crud_livros_bp.remover_livro_favoritos', idLivro = "_J4qAwAAQBAJ"),
        data={"idLivroExcluirFavorito": "_J4qAwAAQBAJ"},
        follow_redirects=True
    )

    with app.app_context():
      assert Lista_Livro.query.count() == 1
      assert Lista_Livro.query.first().livro_id == "_J4qAwAAQBAJ"


def test_remover_livro_lista(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaRemocao = client.post(
        url_for('crud_livros_bp.remover_livro', idLivro = "_J4qAwAAQBAJ"),
        data={"idLivroExcluir": "_J4qAwAAQBAJ"},
        follow_redirects=True
    )

    with app.app_context():
      assert Lista_Livro.query.count() == 0

    assert len(captured_templates) == 3

    template = captured_templates[2]

    assert template.name == "pagina_livro.html"

def test_adicionar_nota_livro(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaAdicaoNota = client.post(
        url_for('crud_livros_bp.adicionar_nota_livro', livro_id = "_J4qAwAAQBAJ", nota_livro = 1),
        data={"livro_id_nota": "_J4qAwAAQBAJ", "nota_livro": 1},
        follow_redirects=True
    )
    
    with app.app_context():
      assert Lista_Livro.query.count() == 1
      assert Lista_Livro.query.first().livro_id == "_J4qAwAAQBAJ"
      assert Lista_Livro.query.first().nota_livro == 1
    
    client.post(
        url_for('crud_livros_bp.adicionar_nota_livro', livro_id = "_J4qAwAAQBAJ", nota_livro = 5),
        data={"livro_id_nota": "_J4qAwAAQBAJ", "nota_livro": 5},
        follow_redirects=True
    )

    with app.app_context():
      assert Lista_Livro.query.count() == 1
      assert Lista_Livro.query.first().livro_id == "_J4qAwAAQBAJ"
      assert Lista_Livro.query.first().nota_livro == 5


def test_adicionar_nota_livro_valores_invalidos(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaAdicaoNota = client.post(
        url_for('crud_livros_bp.adicionar_nota_livro', livro_id = "_J4qAwAAQBAJ", nota_livro = -1),
        data={"livro_id_nota": "_J4qAwAAQBAJ", "nota_livro": -1},
        follow_redirects=True
    )

    with app.app_context():
      assert Lista_Livro.query.count() == 1
      assert Lista_Livro.query.first().livro_id == "_J4qAwAAQBAJ"
      assert Lista_Livro.query.first().nota_livro == 0

    client.post(
        url_for('crud_livros_bp.adicionar_nota_livro', livro_id = "_J4qAwAAQBAJ", nota_livro = 6),
        data={"livro_id_nota": "_J4qAwAAQBAJ", "nota_livro": 6},
        follow_redirects=True
    )

    with app.app_context():
      assert Lista_Livro.query.count() == 1
      assert Lista_Livro.query.first().livro_id == "_J4qAwAAQBAJ"
      assert Lista_Livro.query.first().nota_livro == 5
    

def test_adicionar_livro_lista_get_invalido(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.get(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    with app.app_context():
      assert Lista_Livro.query.count() == 0

def test_adicionar_livro_lista_sem_login(client,app,captured_templates):
  
  with client:
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    with app.app_context():
      assert Lista_Livro.query.count() == 0

def test_remover_livro_lista_get_invalido(client,app,captured_templates):
  client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

  with client:
    respostaLogin = client.post(
        url_for('usuarios_bp.login'),
        data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
        follow_redirects=True
    )
    respostaAdicao = client.post(
        url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
        data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
        follow_redirects=True
    )
    respostaRemocao = client.get(
        url_for('crud_livros_bp.remover_livro', idLivro = "_J4qAwAAQBAJ"),
        data={"idLivroExcluir": "_J4qAwAAQBAJ"},
        follow_redirects=True
    )

    with app.app_context():
      assert Lista_Livro.query.count() == 1

def test_remover_livro_lista_sem_login(client,app,captured_templates):
  
  respostaRemocao = client.post(
      url_for('crud_livros_bp.remover_livro', idLivro = "_J4qAwAAQBAJ"),
      data={"idLivroExcluir": "_J4qAwAAQBAJ"},
      follow_redirects=True
  )
  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "indice.html"


def test_remover_livro_lista_favorito_get_invalido(client,app,captured_templates):
      client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

      with client:
        respostaLogin = client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        respostaAdicao = client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
            follow_redirects=True
        )
        respostaAdicaoFavoritos = client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "FAV"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "FAV"},
            follow_redirects=True
        )
        respostaRemocaoFavoritos = client.get(
            url_for('crud_livros_bp.remover_livro_favoritos', idLivro = "_J4qAwAAQBAJ"),
            data={"idLivroExcluirFavorito": "_J4qAwAAQBAJ"},
            follow_redirects=True
        )

        with app.app_context():
          assert Lista_Livro.query.count() == 2

def test_remover_livro_lista_sem_login(client,app,captured_templates):

  respostaRemocaoFavoritos = client.post(
    url_for('crud_livros_bp.remover_livro_favoritos', idLivro = "_J4qAwAAQBAJ"),
    data={"idLivroExcluirFavorito": "_J4qAwAAQBAJ"},
    follow_redirects=True
  )
  assert len(captured_templates) == 1

  template = captured_templates[0]

  assert template.name == "indice.html"


def test_busca_lista_usuario_livroslidos(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "LL"),
            follow_redirects=True
        )

        assert len(captured_templates) == 3

        template = captured_templates[2]

        assert template.name == "pagina_usuario.html"

        assert 'LIVROS LIDOS' in resposta.data.decode('utf-8')

def test_busca_lista_usuario_lendomomento(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LM"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LM"},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "LM"),
            follow_redirects=True
        )

        assert len(captured_templates) == 3

        template = captured_templates[2]

        assert template.name == "pagina_usuario.html"

        assert 'LENDO NO MOMENTO' in resposta.data.decode('utf-8')


def test_busca_lista_usuario_leiturasfuturas(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LF"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LF"},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "LF"),
            follow_redirects=True
        )

        assert len(captured_templates) == 3

        template = captured_templates[2]

        assert template.name == "pagina_usuario.html"

        assert 'LEITURAS FUTURAS' in resposta.data.decode('utf-8')


def test_busca_lista_usuario_livrosabandonados(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LA"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LA"},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "LA"),
            follow_redirects=True
        )

        assert len(captured_templates) == 3

        template = captured_templates[2]

        assert template.name == "pagina_usuario.html"

        assert 'LIVROS ABANDONADOS' in resposta.data.decode('utf-8')


def test_busca_lista_usuario_favoritos(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "LL"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "LL"},
            follow_redirects=True
        )
        client.post(
            url_for('crud_livros_bp.adicionar_livro', idLivro = "_J4qAwAAQBAJ", tipoLista = "FAV"),
            data={"idLivro": "_J4qAwAAQBAJ", "tipoLista": "FAV"},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "FAV"),
            follow_redirects=True
        )

        assert len(captured_templates) == 4

        template = captured_templates[3]

        assert template.name == "pagina_usuario.html"

        assert 'FAVORITOS' in resposta.data.decode('utf-8')

def test_busca_lista_usuario_vazia(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "LA"),
            follow_redirects=True
        )

        assert len(captured_templates) == 2

        template = captured_templates[1]

        assert template.name == "pagina_usuario.html"

        assert 'Não há livros na lista' in resposta.data.decode('utf-8')


def test_busca_lista_usuario_inexistente(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        resposta = client.get(
            url_for('usuarios_bp.buscar_lista_usuario', tipoLista = "XX"),
            follow_redirects=True
        )

        assert len(captured_templates) == 2

        template = captured_templates[1]

        assert template.name == "pagina_usuario.html"

        assert 'Não há livros na lista' in resposta.data.decode('utf-8')


def test_pagina_usuario(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})

    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        resposta = client.get(url_for('usuarios_bp.pagina_usuario'),
                  follow_redirects=True)

        assert len(captured_templates) == 2

        template = captured_templates[1]

        assert template.name == "pagina_usuario.html"

        assert '<div class="quadradoPaginaUsuario">Lidos<br> 0</div>' in resposta.data.decode('utf-8')


def test_atualizar_preferencias_usuario(client,app,captured_templates):
    client.post("/usuarios/cadastrar", data={"nomeUsuario": "TesteMan", "emailUsuario": "teste@teste.com", "senhaUsuario": "Teste123%", "confirmacaoSenhaUsuario": "Teste123%"})
    with client:
        client.post(
            url_for('usuarios_bp.login'),
            data={'email': 'teste@teste.com', 'senha': 'Teste123%'},
            follow_redirects=True
        )
        resposta = client.post(url_for('usuarios_bp.atualizar_preferencias_usuario'),
                  data={"stringPreferencias": "Arquitetura#Arte#Conto"},
                  follow_redirects=True)

        assert len(captured_templates) == 2

        template = captured_templates[1]

        with app.app_context():
         retornoConsulta1 = Usuario_Preferencia.query.filter_by( usuario_id=1,nome_genero="Arquitetura").first()
        retornoConsulta2 = Usuario_Preferencia.query.filter_by( usuario_id=1,nome_genero="Arte").first()
        retornoConsulta3 = Usuario_Preferencia.query.filter_by( usuario_id=1,nome_genero="Conto").first()
        retornoConsulta4 = Usuario_Preferencia.query.filter_by( usuario_id=1,nome_genero="Fantasia").first()

        assert retornoConsulta1.estado_preferencia == 'A'
        assert retornoConsulta2.estado_preferencia == 'A'
        assert retornoConsulta3.estado_preferencia == 'A'
        assert retornoConsulta4.estado_preferencia == 'I'

        assert template.name == "pagina_usuario.html"
        
        
        

  
      

    
  
  
  
  
  
      
