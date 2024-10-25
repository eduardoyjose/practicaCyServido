import requests  # Importa la biblioteca requests para hacer peticiones HTTP

def obtener_usuarios():
    # Realiza una petición GET al servidor
    response = requests.get('http://localhost:5000/usuarios')  
    if response.status_code == 200:  # Si la respuesta es exitosa (código 200)
        usuarios = response.json()  # Convierte el cuerpo de la respuesta JSON a un objeto de Python (lista de diccionarios)
        print("Usuarios encontrados:")
        for usuario in usuarios:  # Itera sobre la lista de usuarios y muestra sus datos
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios")  # Muestra un mensaje de error si la solicitud falla

if __name__ == '__main__':
    obtener_usuarios()  # Ejecuta la función al iniciar el script

# Actualizamos el código del cliente para soportar las nuevas funcionalidades (POST, búsqueda por ID, DELETE y autenticación)


import requests
from requests.auth import HTTPBasicAuth

# Credenciales de autenticación básica
AUTH = HTTPBasicAuth('admin', 'secret')

def obtener_usuarios():
    # Realiza una petición GET al servidor para obtener todos los usuarios
    response = requests.get('http://localhost:5000/usuarios', auth=AUTH)
    if response.status_code == 200:
        usuarios = response.json()
        print("Usuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios")

def buscar_usuario_por_id(usuario_id):
    # Realiza una petición GET para obtener un usuario por su ID
    response = requests.get(f'http://localhost:5000/usuarios/{usuario_id}', auth=AUTH)
    if response.status_code == 200:
        usuario = response.json()
        print(f"Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    elif response.status_code == 404:
        print(f"Usuario con ID {usuario_id} no encontrado")
    else:
        print("Error al buscar usuario")

def crear_usuario(nombre):
    # Realiza una petición POST para crear un nuevo usuario
    usuario_data = {"nombre": nombre}
    response = requests.post('http://localhost:5000/usuarios', json=usuario_data, auth=AUTH)
    if response.status_code == 201:
        usuario = response.json()
        print(f"Usuario creado: ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al crear usuario:", response.json().get('description'))

def eliminar_usuario(usuario_id):
    # Realiza una petición DELETE para eliminar un usuario por su ID
    response = requests.delete(f'http://localhost:5000/usuarios/{usuario_id}', auth=AUTH)
    if response.status_code == 200:
        print("Usuario eliminado con éxito")
    elif response.status_code == 404:
        print(f"Usuario con ID {usuario_id} no encontrado")
    else:
        print("Error al eliminar usuario")

if __name__ == '__main__':
    print("1. Obtener usuarios")
    obtener_usuarios()
    
    print("\n2. Buscar usuario por ID (ID: 1)")
    buscar_usuario_por_id(1)

    print("\n3. Crear un nuevo usuario (Nombre: 'Carlos')")
    crear_usuario("Carlos")
    
    print("\n4. Eliminar usuario por ID (ID: 1)")
    eliminar_usuario(1)
