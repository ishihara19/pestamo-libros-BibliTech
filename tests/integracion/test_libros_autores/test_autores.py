import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_post_autores(admin_auth_headers):
    """POST /api/v1/autores - Crear un nuevo autor"""
    data = {
        "nombre": "AUTOR_TEST",
        "apellido": "PRUEBA",
        "fecha_nacimiento": "1980-01-01",
        "nacionalidad": "Colombiana"
    }
    resp = requests.post(f"{API_URL}/autores", json=data, headers=admin_auth_headers)
    # Puede ser 201 (creado) o 409 (ya existe)
    assert resp.status_code in (201, 409)

def test_get_autores(admin_auth_headers):
    """GET /api/v1/autores - Listar todos los autores"""
    resp = requests.get(f"{API_URL}/autores", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_autores_id(admin_auth_headers):
    """GET /api/v1/autores/{id} - Obtener autor por ID"""
    resp = requests.get(f"{API_URL}/autores", headers=admin_auth_headers)
    assert resp.status_code == 200
    autores = resp.json()
    if autores:
        autor_id = autores[0]["id"]
        resp_id = requests.get(f"{API_URL}/autores/{autor_id}", headers=admin_auth_headers)
        assert resp_id.status_code == 200
        assert resp_id.json()["id"] == autor_id

def test_put_autores_id(admin_auth_headers):
    """PUT /api/v1/autores/{id} - Actualizar un autor"""
    resp = requests.get(f"{API_URL}/autores", headers=admin_auth_headers)
    assert resp.status_code == 200
    autores = resp.json()
    if autores:
        autor_id = autores[0]["id"]
        data = {"nombre": "AUTOR_EDITADO", "apellido": "EDITADO"}
        resp_put = requests.put(f"{API_URL}/autores/{autor_id}", json=data, headers=admin_auth_headers)
        assert resp_put.status_code in (200, 422)

def test_delete_autores_id(admin_auth_headers):
    """DELETE /api/v1/autores/{id} - Eliminar un autor"""
    # Creamos un autor para eliminarlo
    data = {"nombre": "AUTOR_ELIMINAR", "apellido": "ELIMINAR"}
    resp_create = requests.post(f"{API_URL}/autores", json=data, headers=admin_auth_headers)
    if resp_create.status_code == 201:
        autor_id = resp_create.json()["id"]
        resp_del = requests.delete(f"{API_URL}/autores/{autor_id}", headers=admin_auth_headers)
        assert resp_del.status_code in (200, 204)
