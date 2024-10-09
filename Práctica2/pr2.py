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
import json
from geopy.geocoders import Nominatim
from geopy import distance

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

    acc_dia = {}

    for accidente in datos:
        fecha = accidente['fecha']

        if fecha in acc_dia:
            acc_dia[fecha] += 1
        else:
            acc_dia[fecha] = 1

    max_acc = max(acc_dia.values())

    dias_max_acc = {(fecha, num_acc) for fecha, num_acc in acc_dia.items() if num_acc == max_acc}

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

    lista_acc = list(dic_accidentes.items())

    orden_loc = sorted(lista_acc, key=lambda lista_acc : lista_acc[0], reverse = True)
    resultado = sorted(orden_loc, key=lambda lista_acc : lista_acc[1], reverse = True)

    return resultado[:k]


#### Formato JSON

def leer_monumentos(ruta):
    """Devuelve una lista de monumentos, cada uno representado como un diccionario Python."""
    with open(ruta, 'r', encoding='utf8') as file:
        archivo_monumentos = json.load(file)

    lista_monumentos = []

    for elem in archivo_monumentos['@graph']:
        monumento = {}

        monumento['id'] = elem.get('id', "unknown")
        monumento['nombre'] = elem.get('title', "Sin título")

        address = elem['address']
        distrito = address.get('district', None)
        distrito = distrito.get('@id', "''") if distrito is not None else "''"
        monumento['distrito'] = distrito
        monumento['ciudad'] = address.get('locality', "unknown")
        monumento['ZIP'] = address.get('postal-code', "''")
        monumento['calle'] = address.get('street-address', '')

        desc = elem.get('organization', None)
        desc = desc.get('organization-desc', "''") if desc is not None else "''"
        monumento['desc'] = desc

        coord = elem.get('location', None)
        lat = coord.get('latitude', "No disponible") if coord is not None else "No disponible"
        long = coord.get('longitude', "No disponible") if coord is not None else "No disponible"
        monumento['coordenadas'] = (lat, long)

        lista_monumentos.append(monumento)

    return lista_monumentos


def codigos_postales(monumentos):
    """Devuelve una lista ordenada de parejas (codigo_postal, numero_de_monumentos)"""
    dic_cod = {}

    for monumento in monumentos:
        codigo = monumento['ZIP']
        dic_cod[codigo] = dic_cod[codigo] + 1 if codigo in dic_cod else 1

    lista_pareja = dic_cod.items()
    lista_pareja = sorted(lista_pareja, key=lambda x : x[1], reverse = True)
    return lista_pareja


def busqueda_palabras_clave(monumentos, palabras):
    """
    Devuelve un conjunto de parejas (título, distrito) 
    de los monumentos que contienen las palabras clave en su título o descripción
    """
    resultado = set()

    for monumento in monumentos:
        campos_a_evaluar = monumento['nombre'].lower() + ' ' + monumento['desc'].lower()

        if all(palabra.lower() in campos_a_evaluar for palabra in palabras):
            resultado.add((monumento['nombre'], monumento['distrito']))

    return resultado



def busqueda_distancia(monumentos, direccion, distancia):
    """
    Devuelve una lista de ternas (título, id, distancia en kilómetros) de los monumentos 
    que se encuentran a menos de la distancia indicada
    """
    geolocator = Nominatim(user_agent="GIW_pr2")
    location = geolocator.geocode(direccion)

    if location is None:
        raise ValueError("La dirección no se ha podido encontrar")

    latitud_dir=location.latitude
    longitud_dir=location.longitude
    resultado = []

    for monumento in monumentos:
        coordenadas=monumento.get('coordenadas', None)
        if coordenadas!= ("No disponible", "No disponible"):
            latitud_mon, longitud_mon = coordenadas
            try:
                latitud_mon = float(latitud_mon)
                longitud_mon = float(longitud_mon)
            except ValueError:
                continue

            dist = distance.distance((latitud_dir, longitud_dir), (latitud_mon, longitud_mon)).km

            if dist <= distancia:
                resultado.append((monumento['nombre'], monumento['id'], dist))

    resultado.sort(key=lambda x: x[2]) #Ordenamos por el tercer valor que es la distancia

    return resultado
