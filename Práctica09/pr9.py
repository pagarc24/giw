"""
Asignatura: GIW
Práctica 9
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
import base64
from flask import Flask, request, render_template_string
from mongoengine import connect, Document, StringField, EmailField
from argon2 import PasswordHasher
import pyotp
import qrcode
# Resto de importaciones


app = Flask(__name__)
connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
# ** No es necesario modificarla **
class User(Document):
    """
    Clase que representa un usuario en nuestra base de datos
    """
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


##############
# APARTADO 1 #
##############

#
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#
# Utilizamos el algoritmo Argon2, que es un algoritmo de ralentizado (para mayor seguridad),
# para hacer el hash de la contraseña del usuario. Este algoritmo crea la sal automáticamente
# en el proceso de hashing, por lo que no hace falta crear la sal aparte ni guardarla en la base
# de datos, lo que hace a este algoritmo más seguro. En nuestra base de datos solo guardamos el
# hash resultante para evitar almacenar la contraseña en texto plano.

@app.route('/signup', methods=['POST'])
def signup():
    """
    Función que realiza un registro en nuestra aplicación
    """
    nickname = request.form['nickname']
    full_name = request.form['full_name']
    country = request.form['country']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    if password != password2:
        return "Las contraseñas no coinciden"

    if User.objects(user_id = nickname):
        return "El usuario ya existe"

    pass_hash = PasswordHasher().hash(password)
    usuario = User(user_id=nickname, full_name=full_name,
        country=country, email=email, passwd=pass_hash)
    usuario.save()
    return f"Bienvenido usuario {full_name}"

@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Función que cambia la contraseña de un usuario de nuestro sistema
    """
    nickname = request.form['nickname']
    old_password = request.form['old_password']
    new_password = request.form['new_password']

    usuario = User.objects(user_id=nickname).first()
    if not usuario:
        return "Usuario no encontrado"

    try:
        PasswordHasher().verify(usuario.passwd, old_password)
    except Exception:
        return "Contraseña incorrecta"

    usuario.passwd = PasswordHasher().hash(new_password)
    usuario.save()
    return "Contraseña cambiada con éxito"

@app.route('/login', methods=['POST'])
def login():
    """
    Función que realiza un login en nuestra aplicación
    """
    nickname = request.form['nickname']
    password = request.form['password']

    usuario = User.objects(user_id=nickname).first()

    if not usuario:
        return "Usuario o contraseña incorrectos"

    try:
        PasswordHasher().verify(usuario.passwd, password)
    except Exception:
        return "Usuario o contraseña incorrectos"

    return f"Bienvenido {usuario.full_name}"

##############
# APARTADO 2 #
##############

#
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#

# Generamos un secreto aleatorio en Base32 utilizando  pyotp.random_base32().
# Almacenamos el secreto junto con la información del usuario en la base de datos.
# Utilizamos pyotp.utils.build_uri para construir la URL de reegistro
# a partir del secreto, usuario y emisor.
# Y por último generamos el código QR a partir de la URL utilizando la biblioteca qrcode
# y lo incrustamos en la página HTML.

@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    """
    Función que realiza un registro con TOTP en nuestra aplicación
    """
    nickname = request.form['nickname']
    full_name = request.form['full_name']
    country = request.form['country']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    if password != password2:
        return "Las contraseñas no coinciden"

    if User.objects(user_id = nickname):
        return "El usuario ya existe"

    pass_hash = PasswordHasher().hash(password)

    secreto = pyotp.random_base32()

    usuario = User(user_id=nickname, full_name=full_name,
        country=country, email=email, passwd=pass_hash, totp_secret=secreto)
    usuario.save()

    url = pyotp.utils.build_uri(secreto, nickname)

    qr_code = qrcode.QRCode(version=1,box_size=10,border=5)
    qr_code.add_data(url)
    qr_code.make(fit=True)
    imagen = qr_code.make_image(fill='black', back_color='white')
    imagen.save("codigo_qr.png")

    with open("codigo_qr.png", "rb") as file:
        qr_imagen = base64.b64encode(file.read()).decode()

    html = f"""
    <html>
    <head>
        <title>Registro completado</title>
    </head>
    <body>
        <h1>Registro completado</h1>
        <p>Nombre de usuario: {full_name}</p>
        <p>Secreto TOTP: {secreto}</p>
        <p>Código QR:</p>
        <img src="data:image/png;base64,{qr_imagen}">
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/login_totp', methods=['POST'])
def login_totp():
    """
    Función que realiza un login con TOTP en nuestra aplicación
    """
    nickname = request.form['nickname']
    password = request.form['password']
    codigo_totp = request.form['totp']

    usuario = User.objects(user_id=nickname).first()
    if not usuario:
        return "Usuario o contraseña incorrectos"

    try:
        PasswordHasher().verify(usuario.passwd, password)
    except Exception:
        return "Usuario o contraseña incorrectos"

    totp = pyotp.TOTP(usuario.totp_secret)
    if not totp.verify(codigo_totp):
        return "Usuario o contraseña incorrectos"

    return f"Bienvenido {usuario.full_name}"


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
