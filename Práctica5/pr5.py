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

URL = 'https://books.toscrape.com/'


# APARTADO 1 #
def explora_categoria(url):
    """ A partir de la URL de la página principal de una categoría, devuelve el nombre
        de la categoría y el número de libros """
    ...


def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    ...


# APARTADO 2 #
def url_categoria(nombre):
    """ Devuelve la URL de la página principal de una categoría a partir de su nombre (ignorar
        espacios al principio y final y también diferencias en mayúsculas/minúsculas) """
    ...


def todas_las_paginas(url):
    """ Sigue la paginación recopilando todas las URL *absolutas* atravesadas """
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
    ...

