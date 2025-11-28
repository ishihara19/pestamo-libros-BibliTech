from app.schemas.prestamo_sch import HacerPrestamo
from datetime import datetime

def test_hacer_prestamo_valid():
    prestamo = HacerPrestamo(
        libro_id=1,
        fecha_solicitud=datetime(2023, 1, 1, 10, 0, 0),
        dias_prestamo=7
    )
    assert prestamo.libro_id == 1
    assert prestamo.dias_prestamo == 7
