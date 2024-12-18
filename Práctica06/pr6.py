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

from datetime import datetime
import requests

def inserta_usuarios(datos, token):
    """Inserta todos los usuarios de la lista 
    y devuelve True si todos han sido insertados correctamente.
    No funciona con los emails del enunciado hemos probado con 
    eva_1@..., ana_1@... y pepe_1@... y si funcionan"""
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
        return None
    return res.status_code


def borra_usuario(email, token):
    """ Elimina el usuario cuyo email sea exactamente el pasado como parámetro.
    En caso de éxito en el borrado devuelve True. Si no existe tal usuario
    devolverá False """

    user_id = get_ident_email(email, token)

    if user_id is None:
        return False

    res = requests.delete(f'https://gorest.co.in/public/v2/users/{user_id}',
                        headers={'Authorization': f'Bearer {token}'},
                        timeout=10
                        )


    return res.status_code == 204

def inserta_todo(email, token, title, due_on, status='pending'):
    """ Inserta un nuevo ToDo para el usuario con email exactamente 
    igual al pasado. Si el ToDo ha sido insertado con éxito devolverá 
    True, en otro caso devolverá False """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return False

    todo_data = {
        'user_id': user_id,
        'title': title,
        'due_on': due_on,
        'status': status
    }
    res = requests.post('https://gorest.co.in/public/v2/todos',
                        headers={'Authorization': f'Bearer {token}'},
                        data=todo_data,
                        timeout=10
                       )

    return res.status_code == 201


def lista_todos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados 
    al usuario con el email pasado como parámetro """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return []

    res = requests.get(f'https://gorest.co.in/public/v2/users/{user_id}/todos',
                       headers={'Authorization': f'Bearer {token}'},
                       timeout=10
                      )

    if res.status_code == 200:
        return res.json()
    return []


def lista_todos_no_cumplidos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al 
    usuario con el email pasado como parámetro que están pendientes (status=pending) 
    y cuya fecha tope (due_on) es anterior a la fecha y hora actual 
    (ignorar segundos y microsegundos). """

    user_id = get_ident_email(email, token)
    if user_id is None:
        return []

    # Solicitud de los ToDos asociados al usuario
    res = requests.get(f'https://gorest.co.in/public/v2/users/{user_id}/todos',
                       headers={'Authorization': f'Bearer {token}'},
                       timeout=10
                      )

    if res.status_code != 200:
        return []

    todos = res.json()
    pending_todos = []
    current_time = datetime.now().replace(second=0, microsecond=0)

    for todo in todos:
        if todo['status'] == 'pending':
            due_date = datetime.strptime(todo['due_on'][:16], "%Y-%m-%dT%H:%M")

            if due_date < current_time:
                pending_todos.append(todo)

    return pending_todos
