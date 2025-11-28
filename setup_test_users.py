import requests

API_URL = "http://127.0.0.1:8000/api/v1"

USERS = [
    {
        "correo": "admin_test@example.com",
        "nombre": "Admin",
        "apellido": "Test",
        "documento": "10000001",
        "tipo_documento_id": 1,  # Asume que 1 es un tipo válido
        "telefono": "3000000001",
        "direccion": "Calle 1 #1-01",
        "fecha_nacimiento": "1990-01-01",
        "contrasena": "Admin123!",
        "rol": "admin"
    },
    {
        "correo": "bibliotecario_test@example.com",
        "nombre": "Biblio",
        "apellido": "Test",
        "documento": "10000002",
        "tipo_documento_id": 1,
        "telefono": "3000000002",
        "direccion": "Calle 2 #2-02",
        "fecha_nacimiento": "1992-02-02",
        "contrasena": "Biblio123!",
        "rol": "bibliotecario"
    },
    {
        "correo": "lector_test@example.com",
        "nombre": "Lector",
        "apellido": "Test",
        "documento": "10000003",
        "tipo_documento_id": 1,
        "telefono": "3000000003",
        "direccion": "Calle 3 #3-03",
        "fecha_nacimiento": "2000-03-03",
        "contrasena": "Lector123!",
        "rol": "lector"
    }
]


# 1. Registrar usuarios
for user in USERS:
    print(f"Registrando usuario: {user['correo']}")
    user_data = user.copy()
    user_data.pop("rol")  # No enviar el campo rol al endpoint de registro
    resp = requests.post(f"{API_URL}/auth/registro", json=user_data)
    if resp.status_code == 201:
        print(f"Status: {resp.status_code}, Usuario creado exitosamente.")
    elif resp.status_code == 409:
        print(f"Status: {resp.status_code}, Usuario ya existe.")
    else:
        print(f"Status: {resp.status_code}, Respuesta: {resp.text}")

admin_user = USERS[0]
# 2. Iniciar sesión como admin para obtener token
resp = requests.post(
    f"{API_URL}/auth/inicio-sesion",
    data={
        "username": admin_user["correo"],
        "password": admin_user["contrasena"]
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # 3. Asignar roles a los usuarios (excepto admin)
    for user in USERS:
        if user["rol"] != "admin":
            print(f"Asignando rol {user['rol']} a {user['correo']}")
            # Busca el usuario por correo para obtener el id
            usuarios_resp = requests.get(f"{API_URL}/usuarios", headers=headers)
            try:
                usuarios = usuarios_resp.json()
            except Exception:
                print(f"Respuesta inesperada al consultar usuarios: {usuarios_resp.text}")
                usuarios = []
            # Mostrar la estructura para depuración
            print(f"Respuesta de usuarios: {usuarios}")
            if isinstance(usuarios, list):
                usuario = next((u for u in usuarios if u.get("correo") == user["correo"]), None)
            elif isinstance(usuarios, dict) and "results" in usuarios:
                usuario = next((u for u in usuarios["results"] if u.get("correo") == user["correo"]), None)
            else:
                usuario = None
            if usuario:
                user_id = usuario["id"]
                # Actualiza el rol usando el endpoint de admin
                resp_rol = requests.put(f"{API_URL}/usuarios/{user_id}/admin", headers=headers, json={"rol": user["rol"]})
                print(f"Status: {resp_rol.status_code}, Respuesta: {resp_rol.text}")
            else:
                print(f"No se encontró el usuario {user['correo']} para asignar rol.")
else:
    print("No se pudo iniciar sesión como admin_test para asignar roles.")
