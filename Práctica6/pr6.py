"""
Asignatura: GIW
Práctica 6
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

import requests

def inserta_usuarios(datos, token):
    """ Inserta todos los usuarios de la lista y devuelve True si todos han sido insertados correctamente """
    usuarios_insertados = 0
    for usuario in datos:
        res = requests.post('https://gorest.co.in/public/v2/users',
                    headers={'Authorization': f'Bearer {token}'},
                    data=usuario,
                    timeout=10
                    )
        if res.status_code == 201:
            usuarios_insertados += 1
    return usuarios_insertados


def get_ident_email(email, token):
    """ Devuelve el identificador del usuario cuyo email sea exactamente el pasado como parámetro.
        En caso de que ese usuario no exista devuelve None """
    res = requests.get('https://gorest.co.in/public/v2/users',
                 params={'email': email},
                 headers={'Authorization': f'Bearer {token}'},
                 timeout=10
                 )

    if res.status_code == 200:
        usuario = res.json()
        if usuario:
            id_usuario = usuario[0]['id']
            return id_usuario
        else:
            return None
    else:
        return res.status_code


def borra_usuario(email, token):
    """ Elimina el usuario cuyo email sea exactamente el pasado como parámetro. En caso de éxito en el
        borrado devuelve True. Si no existe tal usuario devolverá False """
    
    id = get_ident_email(email, token)

    if id is None:
        return False
    
    r = requests.delete(f'https://gorest.co.in/public/v2/users/{id}', headers={'Authorization': f'Bearer {token}'})

    return r.status_code == 204

def inserta_todo(email, token, title, due_on, status='pending'):
    """ Inserta un nuevo ToDo para el usuario con email exactamente igual al pasado. Si el ToDo ha sido insertado
        con éxito devolverá True, en otro caso devolverá False """
    ...


def lista_todos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el email pasado como
        parámetro """
    ...


def lista_todos_no_cumplidos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el email pasado como
        parámetro que están pendientes (status=pending) y cuya fecha tope (due_on) es anterior a la fecha
        y hora actual. Para comparar las fechas solo hay que tener en cuenta el dia, la hora y los minutos; es
        decir, ignorar los segundos, microsegundos y el uso horario """
    ...

with open('token_gorest.txt', 'r', encoding='utf8') as f:
    token = f.read().strip()

