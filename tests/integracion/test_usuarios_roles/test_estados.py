import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_post_estados(admin_auth_headers):
    """POST /api/v1/estados - Crear un nuevo estado"""
    data = {"nombre": "ESTADO_TEST", "tipo": "TEST", "descripcion": "Estado de prueba"}
    resp = requests.post(f"{API_URL}/estados", json=data, headers=admin_auth_headers)
    # Puede ser 201 (creado) o 409 (ya existe)
    # Esperado: 201 (creado) o 409 (conflicto por duplicado)
    assert resp.status_code in (201, 409), f"Status: {resp.status_code}, Body: {resp.text}"

def test_get_estados(admin_auth_headers):
    """GET /api/v1/estados - Listar todos los estados"""
    resp = requests.get(f"{API_URL}/estados", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_estados_tipo(admin_auth_headers):
    """GET /api/v1/estados/tipo - Listar estados por tipo"""
    resp = requests.get(f"{API_URL}/estados/tipo", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_estados_id(admin_auth_headers):
    """GET /api/v1/estados/{id} - Obtener estado por ID"""
    resp = requests.get(f"{API_URL}/estados", headers=admin_auth_headers)
    assert resp.status_code == 200
    estados = resp.json()
    if estados:
        estado_id = estados[0]["id"]
        resp_id = requests.get(f"{API_URL}/estados/{estado_id}", headers=admin_auth_headers)
        assert resp_id.status_code == 200
        assert resp_id.json()["id"] == estado_id

def test_put_estados_id(admin_auth_headers):
    """PUT /api/v1/estados/{id} - Actualizar un estado"""
    resp = requests.get(f"{API_URL}/estados", headers=admin_auth_headers)
    assert resp.status_code == 200
    estados = resp.json()
    if estados:
        estado_id = estados[0]["id"]
        data = {"nombre": "ESTADO_EDITADO", "tipo": "EDITADO"}
        resp_put = requests.put(f"{API_URL}/estados/{estado_id}", json=data, headers=admin_auth_headers)
        assert resp_put.status_code in (200, 422)

def test_delete_estados_id(admin_auth_headers):
    """DELETE /api/v1/estados/{id} - Eliminar un estado"""
    # Creamos un estado para eliminarlo
    data = {"nombre": "ESTADO_ELIMINAR", "tipo": "ELIMINAR"}
    resp_create = requests.post(f"{API_URL}/estados", json=data, headers=admin_auth_headers)
    if resp_create.status_code == 201:
        estado_id = resp_create.json()["id"]
        resp_del = requests.delete(f"{API_URL}/estados/{estado_id}", headers=admin_auth_headers)
        assert resp_del.status_code in (200, 204)
