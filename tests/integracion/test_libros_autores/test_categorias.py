import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_post_categorias(admin_auth_headers):
    """POST /api/v1/categorias - Crear una nueva categoría"""
    data = {"nombre": "CATEGORIA_TEST"}
    resp = requests.post(f"{API_URL}/categorias", json=data, headers=admin_auth_headers)
    # Puede ser 201 (creado) o 409 (ya existe)
    # Esperado: 201 (creado) o 409 (conflicto por duplicado)
    assert resp.status_code in (201, 409), f"Status: {resp.status_code}, Body: {resp.text}"

def test_get_categorias(admin_auth_headers):
    """GET /api/v1/categorias - Listar todas las categorías"""
    resp = requests.get(f"{API_URL}/categorias", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_categorias_id(admin_auth_headers):
    """GET /api/v1/categorias/{id} - Obtener categoría por ID"""
    resp = requests.get(f"{API_URL}/categorias", headers=admin_auth_headers)
    assert resp.status_code == 200
    cats = resp.json()
    if cats:
        cat_id = cats[0]["id"]
        resp_id = requests.get(f"{API_URL}/categorias/{cat_id}", headers=admin_auth_headers)
        assert resp_id.status_code == 200
        assert resp_id.json()["id"] == cat_id

def test_put_categorias_id(admin_auth_headers):
    """PUT /api/v1/categorias/{id} - Actualizar una categoría"""
    resp = requests.get(f"{API_URL}/categorias", headers=admin_auth_headers)
    assert resp.status_code == 200
    cats = resp.json()
    if cats:
        cat_id = cats[0]["id"]
        data = {"nombre": "CATEGORIA_EDITADA"}
        resp_put = requests.put(f"{API_URL}/categorias/{cat_id}", json=data, headers=admin_auth_headers)
        # Esperado: 200 (ok) o 422 (validación)
        assert resp_put.status_code in (200, 422), f"Status: {resp_put.status_code}, Body: {resp_put.text}"

def test_delete_categorias_id(admin_auth_headers):
    """DELETE /api/v1/categorias/{id} - Eliminar una categoría"""
    # Creamos una categoría para eliminarla
    data = {"nombre": "CATEGORIA_ELIMINAR"}
    resp_create = requests.post(f"{API_URL}/categorias", json=data, headers=admin_auth_headers)
    if resp_create.status_code == 201:
        cat_id = resp_create.json()["id"]
        resp_del = requests.delete(f"{API_URL}/categorias/{cat_id}", headers=admin_auth_headers)
        assert resp_del.status_code in (200, 204)
