import urllib.request, json, re
from datetime import datetime
from urllib.parse import quote

def remove_html_tags(texto):
  padrao_html = re.compile('<.*?>')
  texto_limpo = re.sub(padrao_html, '', texto)
  return texto_limpo

def formatar_palavra_busca(palavraBusca):
  palavraBusca = re.sub(r"[^\w\s]", '', palavraBusca)
  palavraBusca = re.sub(r"\s+", '+', palavraBusca)
  palavraBusca = urllib.parse.quote(palavraBusca)

  return palavraBusca

def realizar_request_api(url):
  jsondata = json.loads(urllib.request.urlopen(url).read())
  return jsondata


def verificar_ISBNs(dicionario):
  ISBN10 = ""
  ISBN13 = ""
  for item in dicionario:
      if item['ISBN'] == 'ISBN_10':
        ISBN10 = item['Identificador']
      if item['ISBN'] == 'ISBN_13':
        ISBN13 = item['Identificador']

  return {'ISBN10': ISBN10, 'ISBN13': ISBN13}


def converter_data(data):

  try:
    data_obj = datetime.strptime(data, '%Y-%m-%d')
  
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
  
    mes = meses[data_obj.month]
    
    data_formatada = f'{mes} {data_obj.day}, {data_obj.year}'
    return data_formatada
  except ValueError:
    return data


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


def getDicionarioGeneros():
  
  dicionarioGeneros = {
      'Adventure' : 'Aventura',
      'Action' : 'Ação',
      'Short Story': 'Conto',
      'Horror': 'Terror',  
      'Crime': 'Policial',
      'Mystery': 'Mistério',
      'Detective': 'Detetive',
      'Thriller': "Suspense",
      'Politics': 'Política',
      'Urban Fantasy'      : 'Fantasia Urbana',
      'Fiction Dystopian'  : 'Ficção Distópica',
      'Action & Adventure' : 'Ação e Aventura',
      'Epic' : 'Épico',
      'Space Opera' : 'Ópera Espacial',
      'Science Fiction': 'Ficção Cientifíca',
      'Fantasy': 'Fantasia',
      'Fiction': 'Ficção',
      'Drama': 'Drama',
      'Romance': 'Romance',
      'Philosophy': 'Filosofia',
      'Architecture': 'Arquitetura',
      'Art': 'Arte',
      'Performing Arts': 'Artes Perfomáticas',
      'Language Arts & Disciplines': 'Artes e Disciplinas da Linguagem',
      'Crafts Hobbies': 'Artesanato e passatempos',
      'Autobiography': 'Autobiografia',
      'Antiques & Collectibles': 'Antiguidades e Colecionáveis',
      'Self-Help': 'Auto-Ajuda',
      'Study Aids': 'Auxílios de Estudo',
      'Bibles': 'Biblia',
      'Biography': 'Biografia',
      'House & Home': 'Casa',
      'Cooking': 'Cozinha',
      'Computers': 'Computadores',
      'Body, Mind & Spirit': 'Corpo, mente e espírito',
      'Science': 'Ciência',
      'Political Science': 'Ciência Política',
      'Social Science': 'Ciência Social',
      'Literary Collections': 'Coleções Literárias',
      'Literary Criticism': 'Criticismo Literário',
      'Design': 'Design',
      'Law': 'Direito',
      'Business & Economics': 'Economia e Negócios',
      'Education': 'Educação',
      'Foreign Language Study': 'Estudo de Língua Estrangeira',
      'Sports & Recreation': 'Esportes e Recreações',
      'Photography': 'Fotografia',
      'Family & Relationships': 'Família e Relacionamento',
      'Juvenile Fiction': 'Ficção Juvenil',
      'Young Adult Fiction': 'Ficção Jovem Adulta',
      'History': 'História',
      'Humor': 'Humor',
      'Games & Activities': 'Jogos e Atividades',
      'Gardening': 'Jardinagem',
      'Mathematics': 'Matemática',
      'Medical': 'Medicina',
      'Music': 'Música',
      'Nature': 'Natureza',
      'Juvenile Nonfiction': 'Não-Ficção Juvenil',
      'Young Adult Nonfiction': 'Não-Ficção Jovem Adulta',
      'Pets': 'Pets',
      'Poetry': 'Poesia',
      'Psychology': 'Psicologia',
      'Religion': 'Religião',
      'Health & Fitness': 'Saúde e Bem-Estar',
      'Technology & Engineering': 'Tecnologia e Engenharia',
      'Transportation': 'Transporte',
      'Travel': 'Viagem',
      'True Crime': 'True Crime'
  }
  return dicionarioGeneros

def get_dados_livro(busca,retorno_api):
  if busca in retorno_api:
    return retorno_api[busca]
  else:
    return ''