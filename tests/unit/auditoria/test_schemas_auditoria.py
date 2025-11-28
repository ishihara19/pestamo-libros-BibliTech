from app.schemas.auditoria_sch import AuditoriaView
from datetime import datetime

def test_auditoria_view_fields():
    now = datetime.now()
    aud = AuditoriaView(
        id=1,
        tabla="usuario",
        operacion="INSERT",
        usuario_db="postgres",
        usuario_app="admin",
        ip="127.0.0.1",
        host="localhost",
        operacion_app="alta",
        fecha_operacion=now,
        datos_anteriores={},
        datos_nuevos={"nombre": "Juan"}
    )
    assert aud.tabla == "usuario"
    assert aud.datos_nuevos["nombre"] == "Juan"
