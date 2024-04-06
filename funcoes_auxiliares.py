import requests, urllib.request, json, re
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

def verificar_prioridade(dict_livro,textoBusca):
  titulo = dict_livro['titulo']
  subtitulo = dict_livro['subtitulo']
  descricao = dict_livro['descricao']
  
  if textoBusca.casefold() in titulo.casefold():
    return 0
  elif textoBusca.casefold() in subtitulo.casefold():
    return 0
  
  return 1

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
  except:
    return data
      
