"""
Asignatura: GIW
Práctica 1
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
    """Devuelve si la matriz es simética o no"""
    # Nota: es simétrica si es igual a su traspuesta
    if es_cuadrada(matriz):
        len_matriz = len(matriz)
        for i in range(len_matriz):
            for j in range(len_matriz):
                if matriz[i][j]!=matriz[j][i]:
                    return False
        return True
    return False

def multiplica_escalar(matriz, k):
    """Devuelve la matriz resultado de multiplicar una matriz por un número k"""
    dim = dimension(matriz)

    if dim is None:
        return None

    resultado = [[j * k for j in i] for i in matriz]

    return resultado

def suma(matriz1, matriz2):
    """Devuelve la matriz resultado de sumar la matriz1 y la matriz2"""
    dim1 = dimension(matriz1)
    dim2 = dimension(matriz2)

    if dim1 is None or dim2 is None or dim1 != dim2:
        return None

    resultado = [[l + matriz1[i][k] for k,l in enumerate(j)] for i, j in enumerate(matriz2)]

    return resultado

# Ejercicio 2
def validar(grafo):
    """Comprueba si el grafo es válido"""
    # Primera etapa: nodos contiene una lista no vacía de etiquetas de nodos.
    is_graph = ("nodos" in grafo) and ("aristas" in grafo)

    # Segunda etapa: nodos contiene una lista no vacía de etiquetas de nodos.
    if is_graph:
        is_graph = len(grafo["nodos"]) != 0

    # Tercera etapa: nodos no tiene nodos repetidos.
    if is_graph:
        # Obtenemos los elementos únicos con un set que posteriormente casteamos al tipo list
        list_aux = list(set(grafo['nodos']))
        is_graph = len(grafo["nodos"]) == len(list_aux)

    # Cuarta etapa: Los nodos origen que aparecen en aristas son nodos definidos en nodos.
    if is_graph:
        list_aux = list(set(grafo['aristas'])) # Obtenemos las claves de aristas de manera única
        is_graph = grafo["nodos"] == list_aux

    # Quinta etapa: Los nodos destino que aparecen en aristas son nodos definidos en nodos.
    if is_graph:
        list_aux = []
        for lista in grafo["aristas"].values():
            list_aux.append(e for e in lista)

        list_aux = list(set(list_aux))

    return is_graph

def grado_entrada(grafo, nodo):
    """Devuelve el grado de entrada para un nodo dado"""
    grade = -1

    if validar(grafo) and (nodo in grafo["nodos"]):
        grade = 0
        for lista in grafo["aristas"]:
            grade = grade + 1 if nodo in lista else grade

    return grade

def distancia(grafo, nodo):
    """Devuelve un diccionario con la distancia de un nodo dado al resto de nodos del grafo"""
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
