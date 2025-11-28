import requests

def test_listar_usuarios(admin_auth_headers):
    resp = requests.get("http://127.0.0.1:8000/api/v1/usuarios", headers=admin_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
