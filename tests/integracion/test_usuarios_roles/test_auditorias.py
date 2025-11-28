import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_get_auditorias(admin_auth_headers):
    """GET /api/v1/auditorias - Listar registros de auditoría"""
    resp = requests.get(f"{API_URL}/auditorias", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_auditorias_id(admin_auth_headers):
    """GET /api/v1/auditorias/{id} - Obtener registro de auditoría por ID"""
    resp = requests.get(f"{API_URL}/auditorias", headers=admin_auth_headers)
    assert resp.status_code == 200
    auditorias = resp.json()
    if auditorias:
        aud_id = auditorias[0]["id"]
        resp_id = requests.get(f"{API_URL}/auditorias/{aud_id}", headers=admin_auth_headers)
        assert resp_id.status_code == 200
        assert resp_id.json()["id"] == aud_id
