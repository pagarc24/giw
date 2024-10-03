
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

from xml.dom.minidom import parse
import xml.dom.minidom
import html


def nombres_restaurantes(filename):
    ...


def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    """Devuelve un diccionario con la información básica del restaurante"""
    arb = xml.dom.minidom.parse(filename)
    lista_servicios = arb.documentElement
    restaurantes = lista_servicios.getElementsByTagName("service")
    diccionario = {}

    for restaurante in restaurantes:
        nombre = restaurante.firstChild.childNodes[1].firstChild.data
        if nombre == name:
            diccionario['nombre'] = nombre
            if restaurante.firstChild.childNodes[6].firstChild:
                desc = restaurante.firstChild.childNodes[6].firstChild.data
                diccionario['descripcion'] = html.unescape(desc)
            else:
                diccionario['descripcion'] = None

            if restaurante.firstChild.childNodes[2].firstChild:
                email = restaurante.firstChild.childNodes[2].firstChild.data
                diccionario['email'] = html.unescape(email)
            else:
                diccionario['email'] = None

            if restaurante.firstChild.childNodes[7].firstChild:
                web = restaurante.firstChild.childNodes[7].firstChild.data
                diccionario['web'] = html.unescape(web)
            else:
                diccionario['web'] = None

            if restaurante.firstChild.childNodes[3].firstChild:
                phone = restaurante.firstChild.childNodes[3].firstChild.data
                diccionario['phone'] = html.unescape(phone)
            else:
                diccionario['phone'] = None

            if restaurante.childNodes[3].childNodes[4].firstChild:
                horario = restaurante.childNodes[3].childNodes[4].firstChild.data
                diccionario['horario'] = html.unescape(horario)
            else:
                diccionario['horario'] = None

    return diccionario

#print(info_restaurante("Práctica3\estaurantes_v1_es.xml", "Hasaku Nikkei"))

def busqueda_cercania(filename, lugar, n):
    ...
