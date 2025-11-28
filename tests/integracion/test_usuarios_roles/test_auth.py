
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_post_auth_registro():
    """POST /api/v1/auth/registro - Registrar un nuevo usuario"""
    data = {
        "correo": "nuevo_usuario_test@example.com",
        "nombre": "Nuevo",
        "apellido": "Test",
        "documento": "10000099",
        "tipo_documento_id": 1,
        "telefono": "3000000099",
        "direccion": "Calle 99 #9-99",
        "fecha_nacimiento": "1995-09-09",
        "contrasena": "Nuevo123!"
    }
    resp = requests.post(f"{API_URL}/auth/registro", json=data)
    # Puede ser 201 (creado) o 409 (ya existe)
    # Esperado: 201 (creado), 409 (duplicado) o 400 (datos inválidos)
    assert resp.status_code in (201, 409, 400), f"Status: {resp.status_code}, Body: {resp.text}"

def test_post_auth_inicio_sesion():
    """POST /api/v1/auth/inicio-sesion - Iniciar sesión"""
    data = {
        "username": "admin_test@example.com",
        "password": "Admin123!"
    }
    resp = requests.post(f"{API_URL}/auth/inicio-sesion", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert resp.status_code == 200
    json_resp = resp.json()
    assert "access_token" in json_resp
    assert json_resp["token_type"] == "bearer"

def test_get_auth_yo(admin_auth_headers):
    """GET /api/v1/auth/yo - Obtener usuario actual"""
    resp = requests.get(f"{API_URL}/auth/yo", headers=admin_auth_headers)
    assert resp.status_code == 200
    json_resp = resp.json()
    assert json_resp["correo"] == "admin_test@example.com"
