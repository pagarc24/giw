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
    
    max_accidentes = max(accidentes_al_dia.values())
    
    dias_max_accidentes = {(fecha, num_accidentes) for fecha, num_accidentes in accidentes_al_dia.items() if num_accidentes == max_accidentes}
    
    return dias_max_accidentes

def puntos_negros_distrito(datos, distrito, k):
    ...


#### Formato JSON
def leer_monumentos(ruta):
    ...

def codigos_postales(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, direccion, distancia):
    ...
