"""
TODO: rellenar

Asignatura: GIW
Práctica 1
Grupo: XXXXXXX
Autores: XXXXXX

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""


# Ejercicio 1

def dimension(matriz):
    """Devuelve una tupla (filas, columnas) con el tamaño de la matriz"""
    num_fil = len(matriz)
    num_col = 0
    mal = False

    if num_fil != 0:
        num_col = len(matriz[0])
        i = 1
        while i < len(matriz) and not mal:
            if num_col != len(matriz[i]):
                mal = True
            else:
                i = i + 1

    if num_col == 0 or mal:
        return None

    result = (num_fil, num_col)
    return result

def es_cuadrada(matriz):
    """Devuelve si la matriz es cuadrada o no"""
    result = True
    dim = dimension(matriz)
    if dim is None or dim[0] != dim[1]:
        result = False

    return result


def es_simetrica(matriz):
    ...


def multiplica_escalar(matriz, k):
    ...


def suma(matriz1, matriz2):
    ...


# Ejercicio 2
def validar(grafo):
    # Primera etapa: nodos contiene una lista no vacía de etiquetas de nodos.
    isGraph = ("nodos" in grafo) and ("aristas" in grafo)

    # Segunda etapa: nodos contiene una lista no vacía de etiquetas de nodos.
    if isGraph:
        isGraph = len(grafo["nodos"]) != 0

    # Tercera etapa: nodos no tiene nodos repetidos.
    if isGraph:
        listAux = list({e for e in grafo["nodos"]}) # Obtenemos los elementos únicos con un set que posteriormente casteamos al tipo list
        isGraph = len(grafo["nodos"]) == len(listAux)

    # Cuarta etapa: Los nodos origen que aparecen en aristas son nodos definidos en nodos.
    if isGraph:
        listAux = list({e for e in grafo["aristas"]}) # Obtenemos las claves de aristas de manera única
        isGraph = grafo["nodos"] == listAux

    # Quinta etapa: Los nodos destino que aparecen en aristas son nodos definidos en nodos.
    if isGraph:
        listaAux = []
        for l in grafo["aristas"].values():
            listAux.append(e for e in l)

        listaAux = list(set(listaAux))

    return isGraph

"""
g = {"nodos": [1,2], "aristas": {1: [2], 2: [2]}}
print(validar(g))
"""

def grado_entrada(grafo, nodo):
    grade = -1

    if validar(grafo) and (nodo in grafo["nodos"]):
        grade = 0
        for l in grafo["aristas"]:
            grade = grade + 1 if nodo in l else grade

    return grade


def distancia(grafo, nodo):
    #Comporbamos que el grafo sea válido y que el nodo pertenezca a este
    if not validar(grafo) or nodo not in grafo["nodos"]:
        return None
    
    #Inicializamos el diccionario de distancias (Todos a -1 excepto el de inicio)
    distancias = {n: -1 for n in grafo["nodos"]}
    distancias[nodo] = 0
    
    #Cola para recorrer el grafo nodo por nodo
    cola = [nodo]
    
    while cola:
        actual = cola.pop(0) #Quita primer nodo de la cola
        for vecino in grafo["aristas"].get(actual, []): #Itera sobre los nodos vecinos
            if distancias[vecino] == -1: #Comprueba si lo ha visitado y opera en base a ello
                distancias[vecino] = distancias[actual] + 1 
                cola.append(vecino) 
    return distancias
