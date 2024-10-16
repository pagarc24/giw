
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

import xml.sax

import html
from xml.etree import ElementTree

#from geopy.geocoders import Nominatim
#from geopy import distance

class NombresRestaurantesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.nombres = []
        self.current_name = ""
        self.in_name_tag = False

    def startElement(self, tag, attributes):
        if tag == "name":
            self.in_name_tag = True
            self.current_name = ""

    def endElement(self, tag):
        if tag == "name" and self.in_name_tag:
            nombre = html.unescape(self.current_name.strip())
            self.nombres.append(nombre)
            self.in_name_tag = False

    def characters(self, content):
        if self.in_name_tag:
            self.current_name += content

class SubcategoriasRestaurantesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.cjto_subcategorias = set()
        
        self.in_categoria_tag = False
        self.categoria_name = ""

        self.in_subcategoria_tag = False
        self.subcategoria_name = ""

        self.start_reading_categoria = False
        self.start_reading_subcategoria = False

    def startElement(self, tag, att):
        if tag == "item":
            if self.in_subcategoria_tag and att.get("name") == "SubCategoria":
                self.start_reading_subcategoria = True
            elif self.in_categoria_tag and att.get("name") == "Categoria":
                self.start_reading_categoria = True
        elif tag == "subcategoria":
            self.subcategoria_name = ""
            self.in_subcategoria_tag = True

            self.categoria_name = html.unescape(self.categoria_name.strip())
        elif tag == "categoria":
            self.categoria_name = ""
            self.in_categoria_tag = True

    def endElement(self, tag):
            if tag == "item":
                if self.in_subcategoria_tag:
                    self.start_reading_subcategoria = False
                elif self.in_categoria_tag:
                    self.start_reading_categoria = False
            elif tag == "subcategoria" and self.in_subcategoria_tag:
                self.subcategoria_name = html.unescape(self.subcategoria_name.strip())
                
                elem = self.categoria_name + " > " + self.subcategoria_name
                self.cjto_subcategorias.add(elem)

                self.in_subcategoria_tag = False
                self.subcategoria_name = ""
            elif tag == "categoria" and self.in_categoria_tag:
                self.in_categoria_tag = False
                self.categoria_name = ""

    def characters(self, content):
        if self.in_subcategoria_tag and self.start_reading_subcategoria:
            self.subcategoria_name += content
        elif self.in_categoria_tag and self.start_reading_categoria:
            self.categoria_name += content
        

def nombres_restaurantes(filename):
    """Devuelve una lista ordenada alfabéticamente con los nombres de todos los restaurantes"""
    parser = xml.sax.make_parser()
    handler = NombresRestaurantesHandler()
    parser.setContentHandler(handler)

    with open(filename, 'r', encoding='utf-8') as file:
        parser.parse(file)

    return sorted(handler.nombres)

def subcategorias(filename):
    """Esta función devuelve un conjunto de todas las subcategorías que existen en el fichero de restaurantes"""
    parser = xml.sax.make_parser()
    handler = SubcategoriasRestaurantesHandler()
    parser.setContentHandler(handler)

    with open(filename, 'r', encoding='utf-8') as file:
        parser.parse(file)

    return handler.cjto_subcategorias


def info_restaurante(filename, name):
    """devuelve un diccionario Python con la información básica del restaurante"""
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
    """Devuelve una lista de parejas (distancia, nombre_restaurante)
    con aquellos restaurantes que están como mucho a nkilómetros de distancia del lugar indicado"""
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

archivo = "restaurantes_v1_es.xml"
cjto_subcategorias = subcategorias(archivo)
print(cjto_subcategorias)