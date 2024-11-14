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
from jsonschema import validate, ValidationError

app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###

# almacenar asignaturas e id asignaturas
asignaturas = {}
current_id = 0 

# Esquema JSON para validar las asignaturas
asignatura_schema = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string"},
        "numero_alumnos": {"type": "integer"},
        "horario": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "dia": {"type": "string"},
                    "hora_inicio": {"type": "integer"},
                    "hora_final": {"type": "integer"}
                },
                "required": ["dia", "hora_inicio", "hora_final"]
            }
        }
    },
    "required": ["nombre", "numero_alumnos", "horario"]
}


# Post; añade una asignatura nueva
@app.route('/asignaturas', methods=['POST'])
def add_asignatura():
    global current_id
    data = request.get_json()

    # Validar estructura de la asignatura usando JSON Schema
    try:
        validate(instance=data, schema=asignatura_schema)
    except ValidationError as e:
        return jsonify({"error": f"Formato incorrecto: {e.message}"}), 400

    # Asignar ID único y agregar la asignatura
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

