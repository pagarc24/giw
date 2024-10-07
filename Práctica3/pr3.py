
"""
Asignatura: GIW
Práctica 3
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

import html
from xml.etree import ElementTree


def nombres_restaurantes(filename):
    ...


def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    """Devuelve un diccionario con la información básica del restaurante"""

    arb = ElementTree.parse(filename)
    restaurantes = arb.findall("service")
    diccionario = {}

    for restaurante in restaurantes:
        nombre = restaurante[0][1].text
        if nombre == name:
            diccionario['nombre'] = nombre
            diccionario['descripcion'] = html.unescape(restaurante[0][6].text)
            diccionario['email'] = restaurante[0][2].text
            diccionario['web'] = restaurante[0][7].text
            diccionario['phone'] = restaurante[0][3].text
            diccionario['horario'] = html.unescape(restaurante[3][4].text)

    if len(diccionario) == 0:
        return None

    return diccionario


def busqueda_cercania(filename, lugar, n):
    ...
