"""
Asignatura: GIW
Práctica 4
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

import sqlite3
import csv
from datetime import datetime

def crear_bd(db_name):
    # Conectamos o creamos la bd
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Crea la tabla datos_generales
    cur.execute('''
        CREATE TABLE IF NOT EXISTS datos_generales (
            ticker TEXT PRIMARY KEY,
            nombre TEXT,
            indice TEXT,
            pais TEXT
        )
    ''')

    # Crea la tabla semanales_IBEX35
    cur.execute('''
        CREATE TABLE IF NOT EXISTS semanales_IBEX35 (
            ticker TEXT,
            fecha TEXT,
            precio REAL,
            PRIMARY KEY (ticker, fecha),
            FOREIGN KEY (ticker) REFERENCES datos_generales(ticker)
        )
    ''')

    # Guarda los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def cargar_bd(db_name, tab_datos, tab_ibex35):
    # Conectamos a la bd
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Carga desde los CSV
    with open(tab_datos, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')  
        for row in reader:
            cur.execute('''
                INSERT OR IGNORE INTO datos_generales (ticker, nombre, indice, pais)
                VALUES (?, ?, ?, ?)
            ''', (row['ticker'], row['nombre'], row['indice'], row['pais']))

    with open(tab_ibex35, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')  
        for row in reader:
            # Convertir la fecha al formato correcto (ISO-8601)
            fecha_procesada = datetime.strptime(row['fecha'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
            cur.execute('''
                INSERT OR IGNORE INTO semanales_IBEX35 (ticker, fecha, precio)
                VALUES (?, ?, ?)
            ''', (row['ticker'], fecha_procesada, row['precio']))

    # Guardamos los datos y cerramos la conexión
    conn.commit()
    conn.close()



def consulta1(db_filename, indice):
    ...


def consulta2(db_filename):
    ...


def consulta3(db_filename, limite):
    # Conectamos a la bd
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    #Consulta
    cur.execute('''
    SELECT datosGen.ticker, datosGen.nombre, AVG(semanales.precio) AS promedio, 
           MAX(semanales.precio) - MIN(semanales.precio) AS diferencia
    FROM semanales_IBEX35 semanales
    JOIN datos_generales datosGen ON semanales.ticker = datosGen.ticker
    GROUP BY datosGen.ticker, datosGen.nombre
    HAVING promedio > ?
    ORDER BY promedio DESC
    ''', (limite,))


    res = cur.fetchall()
    conn.close()
    return res


def consulta4(db_filename, ticker):
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    query = f'SELECT fecha, precio FROM semanales_IBEX35 WHERE ticker = "{ticker}" ORDER BY fecha DESC'
    cur.execute(query)

    lista_valores_semanales = []
    for (fecha, precio) in cur.fetchall():
        lista_valores_semanales.append((ticker, fecha.split()[0], precio))

    con.close()
    return lista_valores_semanales

BD = 'bolsa.db'
crear_bd(BD)
datos_generales = 'Tabla1.csv'
datos_semanales = 'Tabla2.csv'
cargar_bd(BD, datos_generales, datos_semanales)
ticker = 'ACS'
solucion4 = consulta4(BD, ticker)
print(solucion4)