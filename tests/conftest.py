import pytest
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

USERS = {
    "admin": {
        "correo": "admin_test@example.com",
        "contrasena": "Admin123!"
    },
    "bibliotecario": {
        "correo": "bibliotecario_test@example.com",
        "contrasena": "Biblio123!"
    },
    "lector": {
        "correo": "lector_test@example.com",
        "contrasena": "Lector123!"
    }
}


def get_token(correo, contrasena):
    resp = requests.post(
        f"{API_URL}/auth/inicio-sesion",
        data={"username": correo, "password": contrasena},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.status_code == 200, f"Login failed for {correo}: {resp.text}"
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def admin_token():
    return get_token(USERS["admin"]["correo"], USERS["admin"]["contrasena"])

@pytest.fixture(scope="session")
def bibliotecario_token():
    return get_token(USERS["bibliotecario"]["correo"], USERS["bibliotecario"]["contrasena"])

@pytest.fixture(scope="session")
def lector_token():
    return get_token(USERS["lector"]["correo"], USERS["lector"]["contrasena"])

@pytest.fixture
def admin_auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
def bibliotecario_auth_headers(bibliotecario_token):
    return {"Authorization": f"Bearer {bibliotecario_token}"}

@pytest.fixture
def lector_auth_headers(lector_token):
    return {"Authorization": f"Bearer {lector_token}"}
