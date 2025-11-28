import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_post_roles(admin_auth_headers):
    """POST /api/v1/roles - Crear un nuevo rol"""
    data = {
        "nombre": "TEST_ROLE",
        "acronimo": "TR",
        "descripcion": "Rol de prueba para test."
    }
    resp = requests.post(f"{API_URL}/roles", json=data, headers=admin_auth_headers)
    # Puede ser 201 (creado), 409 (ya existe) o 422 (validación)
    # Esperado: 201 (creado), 409 (duplicado) o 422 (validación)
    assert resp.status_code in (201, 409, 422), f"Status: {resp.status_code}, Body: {resp.text}"

def test_get_roles(admin_auth_headers):
    """GET /api/v1/roles - Listar todos los roles"""
    resp = requests.get(f"{API_URL}/roles", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_roles_id(admin_auth_headers):
    """GET /api/v1/roles/{id} - Obtener rol por ID"""
    # Primero obtenemos un rol existente
    resp = requests.get(f"{API_URL}/roles", headers=admin_auth_headers)
    assert resp.status_code == 200
    roles = resp.json()
    if roles:
        rol_id = roles[0]["id"]
        resp_id = requests.get(f"{API_URL}/roles/{rol_id}", headers=admin_auth_headers)
        assert resp_id.status_code == 200
        assert resp_id.json()["id"] == rol_id

def test_put_roles_id(admin_auth_headers):
    """PUT /api/v1/roles/{id} - Actualizar un rol"""
    # Obtenemos un rol existente
    resp = requests.get(f"{API_URL}/roles", headers=admin_auth_headers)
    assert resp.status_code == 200
    roles = resp.json()
    if roles:
        rol_id = roles[0]["id"]
        data = {"nombre": "ROL_EDITADO"}
        resp_put = requests.put(f"{API_URL}/roles/{rol_id}", json=data, headers=admin_auth_headers)
        assert resp_put.status_code in (200, 422)

def test_delete_roles_id(admin_auth_headers):
    """DELETE /api/v1/roles/{id} - Eliminar un rol"""
    # Creamos un rol para eliminarlo
    data = {"nombre": "ROL_ELIMINAR"}
    resp_create = requests.post(f"{API_URL}/roles", json=data, headers=admin_auth_headers)
    if resp_create.status_code == 201:
        rol_id = resp_create.json()["id"]
        resp_del = requests.delete(f"{API_URL}/roles/{rol_id}", headers=admin_auth_headers)
        assert resp_del.status_code in (200, 204)
