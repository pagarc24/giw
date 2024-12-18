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
import os
# Obtener la ruta absoluta del directorio en el que se encuentra pr4.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas de los archivos CSV
DATOS_GENERALES = os.path.join(BASE_DIR, 'Tabla1.csv')
DATOS_SEMANALES = os.path.join(BASE_DIR, 'Tabla2.csv')

def crear_bd(db_name):
    """Crea la base de datos con las tablas necesarias"""
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
    """Carga los datos de los CSV en la base de datos"""
    # Conectamos a la bd
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Carga desde los CSV
    with open(tab_datos, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            cur.execute('''
                INSERT OR IGNORE INTO datos_generales (ticker, nombre, indice, pais)
                VALUES (?, ?, ?, ?)
            ''', (row['ticker'], row['nombre'], row['indice'], row['pais']))

    with open(tab_ibex35, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Convertir la fecha al formato correcto (ISO-8601)
            fecha_procesada = datetime.strptime(row['fecha'], '%d/%m/%Y %H:%M') \
                .strftime('%Y-%m-%d %H:%M')
            cur.execute('''
                INSERT OR IGNORE INTO semanales_IBEX35 (ticker, fecha, precio)
                VALUES (?, ?, ?)
            ''', (row['ticker'], fecha_procesada, row['precio']))

    # Guardamos los datos y cerramos la conexión
    conn.commit()
    conn.close()

def consulta1(db_filename, indice):
    """Devuelve una lista de tuplas (ticker, nombre) de todas las acciones
       que componen el índice pasado como parámetro"""
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ticker, nombre FROM datos_generales
        WHERE indice = ?
        ORDER BY ticker ASC
    ''', (indice,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def consulta2(db_filename):
    """Devuelve una lista de tuplas (ticker, nombre, precio máximo) de las distintas
       acciones del IBEX35 según los datos históricos"""
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT dg.ticker, dg.nombre, MAX(se.precio)
        FROM datos_generales dg
        JOIN semanales_IBEX35 se ON dg.ticker = se.ticker
        WHERE dg.indice = 'IBEX 35'
        GROUP BY dg.ticker, dg.nombre
        ORDER BY dg.nombre ASC
    ''')

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def consulta3(db_filename, limite):
    """Devuelve una lista con los datos generales de las empresas cuyo precio promedio
       sea superior al límite dado"""
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

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

def consulta4(db_filename, query_ticker):
    """Devuelve una lista con los valores semanales del IBEX35 para el ticker dado"""
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    query = f'SELECT fecha, precio FROM semanales_IBEX35 WHERE ticker = "{query_ticker}" ' \
            f'ORDER BY fecha DESC'
    cur.execute(query)

    lista_valores_semanales = [
        (query_ticker, fecha.split()[0], precio) for fecha, precio in cur.fetchall()
    ]

    con.close()
    return lista_valores_semanales

BD = 'bolsa.db'
crear_bd(BD)
cargar_bd(BD, DATOS_GENERALES, DATOS_SEMANALES)
TICKER = 'ACS'
solucion4 = consulta4(BD, TICKER)
print(solucion4)
