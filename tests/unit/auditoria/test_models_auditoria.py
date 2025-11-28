from app.models.auditoria import Auditoria
from datetime import datetime

def test_auditoria_model_fields():
    aud = Auditoria(
        tabla="usuario",
        operacion="INSERT",
        usuario_db="postgres",
        usuario_app="admin",
        ip="127.0.0.1",
        host="localhost",
        operacion_app="alta",
        fecha_operacion=datetime.now(),
        datos_anteriores={},
        datos_nuevos={"nombre": "Juan"}
    )
    assert aud.tabla == "usuario"
    assert aud.datos_nuevos["nombre"] == "Juan"
