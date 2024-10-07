"""
Asignatura: GIW
Práctica 2
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

### Formato CSV
import csv
from pprint import pprint

def lee_fichero_accidentes(ruta):
    """Devuelve los datos del archivo en una lista de diccionarios"""

    with open(ruta, 'r', newline='', encoding='utf8') as fich:
        diccionario = csv.DictReader(fich, delimiter=';')
        lista = list(diccionario)

    return lista


def accidentes_por_distrito_tipo(datos):
    """Crea un diccionario por distrito y tipo de accidente indicando cuantos acccidentes hubo"""

    resultado = {}

    for accidente in datos:
        distrito = accidente['distrito']
        tipo_accidente = accidente['tipo_accidente']
        clave = (distrito, tipo_accidente)

        if clave in resultado:
            resultado[clave] += 1
        else:
            resultado[clave] = 1

    return resultado

def dias_mas_accidentes(datos):
    """Devuelve las fechas con más accidentes, devolviendo (día, numero accidentes)"""

    accidentes_al_dia = {}

    for accidente in datos:
        fecha = accidente['fecha']

        if fecha in accidentes_al_dia:
            accidentes_al_dia[fecha] += 1
        else:
            accidentes_al_dia[fecha] = 1

    max_acc = max(accidentes_al_dia.values())

    dias_max_acc = {(fecha, num_acc) for fecha, num_acc in accidentes_al_dia.items() if num_acc == max_acc}

    return dias_max_acc

def puntos_negros_distrito(datos, distrito, k):
    """Genera una lista con el top-k de localizaciones donde más accidentes se han producido"""

    dic_accidentes = {}

    for accidente in datos:
        if accidente['distrito'] == distrito:
            localizacion = accidente['localizacion']
            if localizacion in dic_accidentes:
                dic_accidentes[localizacion] += 1
            else:
                dic_accidentes[localizacion] = 1

    lista_accidentes = list(dic_accidentes.items())

    def criterio(elemento):
        return (-elemento[1], elemento[0])

    lista_accidentes.sort(key=criterio)

    return lista_accidentes[:k]



#### Formato JSON
import json
from geopy.geocoders import Nominatim 
from geopy import distance


def leer_monumentos(ruta):
    """Esta función acepta la ruta del fichero JSON y devuelve una lista de monumentos, cada uno representado como un diccionario Python."""
    with open(ruta, 'r', encoding='utf8') as file:
        archivo_monumentos = json.load(file)
    
    lista_monumentos = []

    for e in archivo_monumentos['@graph']:
        monumento = {}
        monumento['nombre'] = e.get('title', "Sin título")
        monumento['id'] = e.get('id', "unknown")

        address = e['address']
        monumento['ciudad'] = address.get('locality', "unknown")
        monumento['ZIP'] = address.get('postal-code', "unknown")

        monumento['URL'] = e.get('url', "Sin URL")

        coordenadas = e.get('location', None)
        latitud = coordenadas.get('latitude', "No disponible") if coordenadas != None else "No disponible"
        longitud = coordenadas.get('longitude', "No disponible") if coordenadas != None else "No disponible"
        monumento['coordenadas'] = (latitud, longitud)

        lista_monumentos.append(monumento)

    return lista_monumentos


def codigos_postales(monumentos):
    """Esta función recibe una lista de monumentos y devuelve una lista ordenada de parejas (codigo_postal, numero_de_monumentos)"""
    dict_codigosPostales = {}

    for e in monumentos:
        dict_codigosPostales[e['ZIP']] = dict_codigosPostales.get(e['ZIP'], 1) + 1

    lista_codigosPostales = []
    for codigoPostal in dict_codigosPostales:
        lista_codigosPostales.append((codigoPostal, dict_codigosPostales[codigoPostal]))

    lista_codigosPostales = sorted(lista_codigosPostales, key=lambda cantidad: cantidad[1], reverse=True)

    return lista_codigosPostales
    

def busqueda_palabras_clave(monumentos, palabras):
    """Esta función devuelve un conjunto de parejas (título, distrito) de aquellos monumentos que contienen las palabras clave en su título o en su descripción (campo 'organization-desc'). """
    resultado = set()

    for monumento in monumentos:
        titulo=monumento.get('nombre','').lower()
        descripcion=monumento.get('organization-desc','').lower()
        titulo_y_descripcion=titulo+''+descripcion

        if all(palabra.lower() in titulo_y_descripcion for palabra in palabras):
            mon=monumento['nombre']
            distrito=monumento.get('distrito',{}).get('@id','')
            resultado.add((mon,distrito))
    return resultado



def busqueda_distancia(monumentos, direccion, distancia):
    
    geolocator = Nominatim(user_agent="GIW_pr2")
    location = geolocator.geocode(direccion)

    if location is None:
        raise ValueError("La dirección no se ha podido encontrar")
    
    latitud_dir=location.latitude
    longitud_dir=location.longitude
    resultado= list()

    for monumento in monumentos:
        coordenadas=monumento.get('coordenadas', None)
        if coordenadas and coordenadas != ("No disponible", "No disponible"):
            latitud_monumento, longitud_monumento = coordenadas
            try:
                latitud_monumento = float(latitud_monumento)
                longitud_monumento = float(longitud_monumento)
            except ValueError:
                continue  
            
            dist = distance((latitud_dir, longitud_dir), (latitud_monumento, longitud_monumento)).km
            
            if dist <= distancia:
                resultado.append((monumento['nombre'], monumento['id'], dist))
    
    resultado.sort(key=lambda x: x[2]) #Ordenamos por el tercer valor que es la distancia
    
    return resultado


lista_monumentos = leer_monumentos('300356-0-monumentos-ciudad-madrid.json')
pprint(codigos_postales(lista_monumentos))