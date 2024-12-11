"""
Asignatura: GIW
Práctica 10
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

import hashlib
import os
from flask import Flask, json, make_response, redirect, request, session
import requests
# Resto de importaciones


app = Flask(__name__)


# Credenciales
CLIENT_ID = ''
CLIENT_SECRET = ''

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'


@app.route('/login_google', methods=['GET'])
def login_google():

    token_antifalsificación = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['CSRF'] = token_antifalsificación

    respuesta_json = requests.get(DISCOVERY_DOC).json()
    authorization_endpoint = respuesta_json["authorization_endpoint"]

    url = (
        f"{authorization_endpoint}?client_id={CLIENT_ID}&response_type=code"
        f"&scope=openid%20email&redirect_uri={REDIRECT_URI}&state={token_antifalsificación}"
    )

    return redirect(url)

@app.route('/token', methods=['GET'])
def token():
    if request.args.get('state') != session.get('CSRF'):
        response = make_response(json.dumps('Token invalido'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.args.get("code")

    respuesta_json = requests.get(DISCOVERY_DOC).json()
    token_endpoint = respuesta_json["token_endpoint"]

    datos_token = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    respuesta_token = requests.post(token_endpoint, data=datos_token)
    token_respuesta_json = respuesta_token.json()
    id_token = token_respuesta_json['id_token']

    url_tokeninfo = f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
    respuesta_tokeninfo = requests.get(url_tokeninfo)

    if respuesta_tokeninfo.status_code == 200:
        usuario_info = respuesta_tokeninfo.json()
        email = usuario_info['email']
        return f"Bienvenido {email}"
    else:
        return "Error con tokeninfo", 400




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
