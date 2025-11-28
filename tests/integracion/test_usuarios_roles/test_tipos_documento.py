import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_post_tipos_documento(admin_auth_headers):
    """POST /api/v1/tipos-documento - Crear un nuevo tipo de documento"""
    data = {
        "nombre": "TEST_DOC",
        "acronimo": "TD",
        "descripcion": "Tipo de documento de prueba."
    }
    resp = requests.post(f"{API_URL}/tipos-documento", json=data, headers=admin_auth_headers)
    # Puede ser 201 (creado), 409 (ya existe) o 422 (validación)
    # Esperado: 201 (creado), 409 (duplicado) o 422 (validación)
    assert resp.status_code in (201, 409, 422), f"Status: {resp.status_code}, Body: {resp.text}"

def test_get_tipos_documento(admin_auth_headers):
    """GET /api/v1/tipos-documento - Listar todos los tipos de documento"""
    resp = requests.get(f"{API_URL}/tipos-documento", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_tipos_documento_id(admin_auth_headers):
    """GET /api/v1/tipos-documento/{id} - Obtener tipo de documento por ID"""
    resp = requests.get(f"{API_URL}/tipos-documento", headers=admin_auth_headers)
    assert resp.status_code == 200
    tipos = resp.json()
    if tipos:
        tipo_id = tipos[0]["id"]
        resp_id = requests.get(f"{API_URL}/tipos-documento/{tipo_id}", headers=admin_auth_headers)
        assert resp_id.status_code == 200
        assert resp_id.json()["id"] == tipo_id

def test_put_tipos_documento_id(admin_auth_headers):
    """PUT /api/v1/tipos-documento/{id} - Actualizar un tipo de documento"""
    resp = requests.get(f"{API_URL}/tipos-documento", headers=admin_auth_headers)
    assert resp.status_code == 200
    tipos = resp.json()
    if tipos:
        tipo_id = tipos[0]["id"]
        data = {"nombre": "DOC_EDITADO", "acronimo": "DE"}
        resp_put = requests.put(f"{API_URL}/tipos-documento/{tipo_id}", json=data, headers=admin_auth_headers)
        assert resp_put.status_code in (200, 422)

def test_delete_tipos_documento_id(admin_auth_headers):
    """DELETE /api/v1/tipos-documento/{id} - Eliminar un tipo de documento"""
    # Creamos un tipo de documento para eliminarlo
    data = {"nombre": "DOC_ELIMINAR", "acronimo": "DE"}
    resp_create = requests.post(f"{API_URL}/tipos-documento", json=data, headers=admin_auth_headers)
    if resp_create.status_code == 201:
        tipo_id = resp_create.json()["id"]
        resp_del = requests.delete(f"{API_URL}/tipos-documento/{tipo_id}", headers=admin_auth_headers)
        assert resp_del.status_code in (200, 204)
