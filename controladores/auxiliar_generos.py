from bs4 import BeautifulSoup
import pandas as pd
import time
import requests, urllib.request, json, re


dicionarioGeneros = {
    'Urban Fantasy'      : 'Fantasia Urbana',
    'Fiction Dystopian'  : 'Ficção Distópica',
    'Action & Adventure' : 'Ação e Aventura',
    'Epic' : 'Épico',
    'Space Opera' : 'Ópera Espacial',
    'Science Fiction': 'Ficção Cientíca',
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
    'Bibles': 'Bíblia',
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

def buscar_genero_webscrapper(id,categorias):
  headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
  }
  
  url = f"https://www.google.com.br/books/edition/%7B%7D/{id}?hl=en"
  
  response = requests.get(url, headers = headers) 
  
  soup = BeautifulSoup(response.content, 'html.parser')
  
  retornos = soup.find_all(class_="fl")
  
  lista = []
  
  for retorno in retornos:
    lista.append(str(retorno))
  
  for i in range(len(lista)):
    lista[i] = remove_html_tags(lista[i])
  
  listaGenerosWebScrapper = ' '.join(str(e) for e in lista)
  listaCategoriasAPI = ' '.join(str(e) for e in categorias)

  stringGeneros = listaGenerosWebScrapper + ' ' + listaCategoriasAPI
  
  return stringGeneros


def remove_html_tags(texto):
  padrao_html = re.compile('<.*?>')
  texto_limpo = re.sub(padrao_html, '', texto)
  return texto_limpo