from app.models.ejemplar import Ejemplar
from datetime import date

def test_ejemplar_model_fields():
    ej = Ejemplar(codigo_interno="A1", libro_id=1, estado_id=1, fecha_adquisicion=date(2020,1,1))
    assert ej.codigo_interno == "A1"
    assert ej.libro_id == 1
    assert ej.estado_id == 1
    assert ej.fecha_adquisicion == date(2020,1,1)
