from app.models.prestamo import Prestamo
from datetime import datetime, date

def test_prestamo_model_fields():
    prestamo = Prestamo(
        usuario_id=1,
        ejemplar_id=2,
        fecha_solicitud=datetime(2023, 1, 1, 10, 0, 0),
        fecha_prevista_devolucion=date(2023, 1, 8)
    )
    assert prestamo.usuario_id == 1
    assert prestamo.ejemplar_id == 2
    assert prestamo.fecha_prevista_devolucion == date(2023, 1, 8)
