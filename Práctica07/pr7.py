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

from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError

app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###

# almacenar asignaturas e id asignaturas
asignaturas = {}
current_id = 0 # pylint: disable=C0103

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
    "required": ["nombre", "numero_alumnos", "horario"],
    "additionalProperties": False
}

# Post; añade una asignatura nueva
@app.route('/asignaturas', methods=['POST'])
def add_asignatura():
    """Método para añadir una asignatura nueva"""

    global current_id # pylint: disable=C0103, W0603
    # Desactivamos la regla C0103
    # ya que la regla del UPPER_CASE es para constantes y current_id no es una constante.
    # Desactivamos también la relga W0603
    # ya que necesitamos global para modificar la variable current_id.
    data = request.get_json()

    # Validar estructura de la asignatura usando JSON Schema
    try:
        validate(instance=data, schema=asignatura_schema)
    except ValidationError as validation_error:
        return jsonify({"error": f"Formato incorrecto: {validation_error.message}"}), 400

    # Asignar ID único y agregar la asignatura
    asignatura_id = current_id
    asignaturas[asignatura_id] = {
        "id": asignatura_id,
        "nombre": data["nombre"],
        "numero_alumnos": data["numero_alumnos"],
        "horario": data["horario"]
    }
    current_id += 1
    return jsonify({"id": asignatura_id}), 201

# DELETE; elimina todas las asignaturas
@app.route('/asignaturas', methods=['DELETE'])
def delete_asignaturas():
    """Método para eliminar todas las asignaturas"""
    asignaturas.clear()
    return '', 204

# GET; devuelve la lista de URLs de todas las asignaturas
@app.route('/asignaturas', methods=['GET'])
def get_asignaturas():
    """
    Método para obtener la lista de URLs de todas las asignaturas
    con un número de alumnos mayor o igual al indicado en el parámetro alumnos_gte.
    También puede darse un resultado paginado
    """
    # Generar URLs para cada asignatura en la lista
    min_alumnos = request.args.get('alumnos_gte', default=0, type=int)
    per_page = request.args.get('per_page', default=None, type=int)
    page = request.args.get('page', default=None, type=int)

    if per_page is not None and page is not None:
        if per_page <= 0 or page <= 0:
            return '', 400
        start = (page - 1) * per_page
        end = start + per_page if start + per_page < len(asignaturas) else len(asignaturas)

        asignaturas_urls = [f"/asignaturas/{aid}"
                            for aid in asignaturas.keys()
                            if asignaturas[aid]["numero_alumnos"] >= min_alumnos][start:end]
        code = 200 if len(asignaturas_urls) == len(asignaturas) else 206

        return jsonify({"asignaturas": asignaturas_urls}), code
    elif per_page is None and page is None:
        asignaturas_urls = [f"/asignaturas/{aid}"
                            for aid in asignaturas.keys()
                            if asignaturas[aid]["numero_alumnos"] >= min_alumnos]
        code = 200 if len(asignaturas_urls) == len(asignaturas) else 206

        return jsonify({"asignaturas": asignaturas_urls}), code
    else:
        return '', 400

# GET, DELETE, PUT, PATCH asignatura específica
@app.route('/asignaturas/<int:id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def asignatura(id):
    """Método para obtener, eliminar, modificar o actualizar una asignatura específica"""
    if request.method == 'GET':
        if id in asignaturas:
            return jsonify(asignaturas[id]), 200
        else:
            return '', 404

    elif request.method == 'DELETE':
        if id in asignaturas:
            del asignaturas[id]
            return '', 204
        else:
            return '', 404

    elif request.method == 'PUT':
        data = request.get_json()
        if id not in asignaturas:
            return '', 404

        try:
            validate(instance=data, schema=asignatura_schema)
        except ValidationError as validation_error:
            return jsonify({"error": f"Formato incorrecto: {validation_error.message}"}), 400

        asignaturas[id] = {
            "id": id,
            "nombre": data["nombre"],
            "numero_alumnos": data["numero_alumnos"],
            "horario": data["horario"]
        }
        return '', 200

    elif request.method == 'PATCH':
        if id not in asignaturas:
            return '', 404

        data = request.get_json()
        if len(data.keys()) != 1:
            return '', 400

        clave = list(data.keys())[0]
        if clave not in ["nombre", "numero_alumnos", "horario"]:
            return '', 400

        try:
            validate(instance={clave: data[clave]},
                    schema={"type": "object", "properties":
                    {clave: asignatura_schema["properties"][clave]}, "required": [clave]})
        except ValidationError as validation_error:
            return jsonify({"error": f"Formato incorrecto: {validation_error.message}"}), 400

        asignaturas[id][clave] = data[clave]
        return '', 200

# Ruta para obtener el horario de una asignatura
@app.route('/asignaturas/<int:id>/horario', methods=['GET'])
def get_horario_asignatura(id):
    # Verificamos si la asignatura existe
    if id not in asignaturas:
        return '', 404  # Asignatura no encontrada

    # Obtenemos y devolvemos el horario de la asignatura
    horario = asignaturas[id].get("horario", [])
    return jsonify({"horario": horario}), 200

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
