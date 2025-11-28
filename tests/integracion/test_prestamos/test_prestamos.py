import requests

API_URL = "http://127.0.0.1:8000/api/v1"

def test_listar_prestamos(bibliotecario_auth_headers):
    resp = requests.get(f"{API_URL}/prestamos", headers=bibliotecario_auth_headers)
    # Esperado: 200 (ok)
    assert resp.status_code == 200, f"Status: {resp.status_code}, Body: {resp.text}"
    assert isinstance(resp.json(), list)

# Los siguientes tests requieren datos específicos y pueden necesitar mocks o datos de ejemplo válidos
def test_post_prestamos():
    """POST /api/v1/prestamos - Crear un nuevo préstamo (requiere datos válidos)"""
    pass

def test_post_prestamos_no_ejemplares():
    """POST /api/v1/prestamos - No hay ejemplares disponibles para el libro solicitado (requiere setup especial)"""
    pass

def test_get_prestamos(bibliotecario_auth_headers):
    """GET /api/v1/prestamos - Listar todos los préstamos (bibliotecario)"""
    resp = requests.get(f"{API_URL}/prestamos", headers=bibliotecario_auth_headers)
    # Esperado: 200 (ok)
    assert resp.status_code == 200, f"Status: {resp.status_code}, Body: {resp.text}"
    assert isinstance(resp.json(), list)

def test_get_prestamos_lector(lector_auth_headers):
    """GET /api/v1/prestamos/lector - Listar préstamos del lector actual"""
    resp = requests.get(f"{API_URL}/prestamos/lector", headers=lector_auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_post_prestamos_confirmar_entrega():
    """POST /api/v1/prestamos/confirmar-entrega - Confirmar la entrega de un préstamo (requiere datos válidos)"""
    pass

def test_post_prestamos_confirmar_entrega_no_reservado():
    """POST /api/v1/prestamos/confirmar-entrega - No existe un préstamo reservado para este usuario y ejemplar (requiere setup especial)"""
    pass

def test_post_prestamos_confirmar_devolucion():
    """POST /api/v1/prestamos/{codigo_interno}/confirmar-devolucion - Registrar la devolución de un préstamo (requiere datos válidos)"""
    pass

def test_post_prestamos_confirmar_devolucion_no_activo():
    """POST /api/v1/prestamos/{codigo_interno}/confirmar-devolucion - No existe un préstamo activo para este ejemplar (requiere setup especial)"""
    pass
