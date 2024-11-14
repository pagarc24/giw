"""
Asignatura: GIW
Práctica 7
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

from flask import Flask, request, session, render_template, jsonify
app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###

# almacenar asignaturas e id asignaturas
asignaturas = {}
current_id = 0 


# Valida la estructura de la asignatura
def validar_asignatura(data):
    if 'nombre' not in data or not isinstance(data['nombre'], str):
        return False
    if 'numero_alumnos' not in data or not isinstance(data['numero_alumnos'], int):
        return False
    if 'horario' not in data or not isinstance(data['horario'], list):
        return False
    for entrada in data['horario']:
        if ('dia' not in entrada or not isinstance(entrada['dia'], str) or
                'hora_inicio' not in entrada or not isinstance(entrada['hora_inicio'], int) or
                'hora_final' not in entrada or not isinstance(entrada['hora_final'], int)):
            return False
    return True

# Post; añade una asignatura nueva
@app.route('/asignaturas', methods=['POST'])
def add_asignatura():
    global current_id
    data = request.get_json()

    # valida la estructura de la asignatura
    if not validar_asignatura(data):
        return jsonify({"error": "Formato incorrecto"}), 400

    # asigna id y agrega la asignatura
    asignatura_id = current_id
    asignaturas[asignatura_id] = {
        "id": asignatura_id,
        "nombre": data["nombre"],
        "numero_alumnos": data["numero_alumnos"],
        "horario": data["horario"]
    }
    current_id += 1
    
    # Devolver el ID de la nueva asignatura
    return jsonify({"id": asignatura_id}), 201

# DELETE; elimina todas las asignaturas
@app.route('/asignaturas', methods=['DELETE'])
def delete_asignaturas():
    asignaturas.clear()
    return '', 204

# GET; devuelve la lista de URLs de todas las asignaturas
@app.route('/asignaturas', methods=['GET'])
def get_asignaturas():
    # Generar URLs para cada asignatura en la lista
    asignaturas_urls = [f"/asignaturas/{aid}" for aid in asignaturas.keys()]
    return jsonify({"asignaturas": asignaturas_urls}), 200

### FIN DEL SERVICIO REST ###


if __name__ == '__main__':
    # Activa depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True

    # Imprescindible para usar sesiones
    app.config['SECRET_KEY'] = 'giw_clave_secreta'

    app.config['STATIC_FOLDER'] = 'static'
    app.config['TEMPLATES_FOLDER'] = 'templates'

    app.run()

