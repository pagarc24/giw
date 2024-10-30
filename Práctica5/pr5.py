"""
Asignatura: GIW
Práctica 5
Grupo: 07
Autores:    NICOLÁS JUAN FAJARDO CARRASCO
            PABLO GARCÍA FERNÁNDEZ
            MANUEL LOURO MENESES
            ROBERTO MORENO GUILLÉN

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from word2number import w2n

# URL de la página principal
URL = 'https://books.toscrape.com/'

# APARTADO 1
def explora_categoria(url):
    """ A partir de la URL de la página principal de una categoría, devuelve el nombre
        de la categoría y el número de libros """
    ...


def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    ...


# APARTADO 2
def url_categoria(nombre):
    """ Devuelve la URL de la página principal de una categoría a partir de su nombre (ignorar
        espacios al principio y final y también diferencias en mayúsculas/minúsculas) """
    
    #Convierte el nombre a minúsculas y elimina los espacios al principio y final
    nombre = nombre.lstrip().rstrip().lower()

    # Obtiene el HTML de la página principal y lo parsea
    html = requests.get(URL, timeout=10).text
    soup = BeautifulSoup(html, 'html.parser')

    # Obtiene la lista de categorías
    categorias = soup.find('ul', class_='nav nav-list').find_all('li')

    # Busca la categoría con el nombre dado y devuelve su URL en caso de encontrarla
    for categoria in categorias:
        if nombre == categoria.text.strip().rstrip().lower():
            return urljoin(URL, categoria.find('a')['href'])
    return None

def todas_las_paginas(url):
    """ Sigue la paginación recopilando todas las URL absolutas atravesadas """
    paginas = [url]
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, 'html.parser')
    boton_next = soup.find('li', class_='next')

    while boton_next is not None:
        next_url = boton_next.find('a')['href']
        url = urljoin(url, next_url)
        paginas.append(url)

        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        boton_next = soup.find('li', class_='next')

    return paginas

def libros_categoria(nombre):
    """ Dado el nombre de una categoría, devuelve un conjunto de tuplas 
    (titulo, precio, valoracion), donde el precio será un número real y la 
    valoración un número natural """

    url = url_categoria(nombre)
    if url is None:
        return set()
    
    libros = set()
    paginas = todas_las_paginas(url)

    for pagina in paginas:
        response = requests.get(pagina, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrae la información de cada libro
        libros_pagina = soup.select(".product_pod")
        for libro in libros_pagina:
            titulo = libro.h3.a["title"]
            precio = float(libro.select_one(".price_color").text[1:])
            valoracion = w2n.word_to_num(libro.p["class"][1])
            libros.add((titulo, precio, valoracion))
    
    return libros