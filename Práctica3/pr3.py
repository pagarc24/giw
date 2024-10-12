
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

from geopy.geocoders import Nominatim
from geopy import distance




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

    geolocator = Nominatim(user_agent="GIW_pr3")
    location = geolocator.geocode(lugar)


    if location is None:
        raise ValueError("La dirección no se ha podido encontrar")
    
    latitud_dir=location.latitude
    longitud_dir=location.longitude
    
    arb = ElementTree.parse(filename)
    restaurantes = arb.findall("service")
    resultados = []
    
    for restaurante in restaurantes:
        nombre_elem = restaurante.find("basicData/name")
        nombre = html.unescape(nombre_elem.text.strip()) if nombre_elem is not None else None
        
        latitud_elem = restaurante.find("geoData/latitude")
        longitud_elem = restaurante.find("geoData/longitude")
        
        if nombre and latitud_elem is not None and longitud_elem is not None:
            try:
                latitud_rest = float(latitud_elem.text)
                longitud_rest = float(longitud_elem.text)
            except ValueError:
                continue

            dist = distance.distance((latitud_dir, longitud_dir), (latitud_rest, longitud_rest)).km

            if dist <= n:
                resultados.append((dist, nombre))
    
    resultados.sort(key=lambda x: x[0])
    
    return resultados


