
from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Simulamos una base de datos de usuarios
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "María"}
    ]
}

# Simulamos credenciales de autenticación básica
usuarios_validos = {
    "admin": "secret"
}

@auth.verify_password
def verificar_password(usuario, contrasena):
    if usuario in usuarios_validos and usuarios_validos[usuario] == contrasena:
        return usuario

# Ruta para obtener todos los usuarios (protegida con autenticación)
@app.route('/usuarios', methods=['GET'])
@auth.login_required
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])

# Ruta para obtener un usuario por su ID
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
@auth.login_required
def obtener_usuario(usuario_id):
    usuario = next((u for u in base_datos['usuarios'] if u['id'] == usuario_id), None)
    if usuario is None:
        abort(404, description="Usuario no encontrado")
    return jsonify(usuario)

# Ruta para crear un nuevo usuario con validación de datos
@app.route('/usuarios', methods=['POST'])
@auth.login_required
def crear_usuario():
    nuevo_usuario = request.json
    if not nuevo_usuario or 'nombre' not in nuevo_usuario or not nuevo_usuario['nombre']:
        abort(400, description="Datos inválidos, el nombre es requerido")
    
    nuevo_id = max([u['id'] for u in base_datos['usuarios']]) + 1 if base_datos['usuarios'] else 1
    nuevo_usuario['id'] = nuevo_id
    base_datos['usuarios'].append(nuevo_usuario)
    return jsonify(nuevo_usuario), 201

# Ruta para eliminar un usuario por su ID
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@auth.login_required
def eliminar_usuario(usuario_id):
    usuario = next((u for u in base_datos['usuarios'] if u['id'] == usuario_id), None)
    if usuario is None:
        abort(404, description="Usuario no encontrado")
    
    base_datos['usuarios'].remove(usuario)
    return jsonify({"mensaje": "Usuario eliminado con éxito"})

if __name__ == '__main__':
    app.run(port=5000)