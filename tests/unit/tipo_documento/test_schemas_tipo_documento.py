from app.schemas.tipo_documento_sch import TipoDocumentoBase, TipoDocumentoCreate, TipoDocumentoUpdate, TipoDocumentoView
from datetime import datetime

def test_tipo_documento_base():
    tipo = TipoDocumentoBase(nombre="DNI", acronimo="DNI", descripcion="Documento Nacional de Identidad")
    assert tipo.nombre == "DNI"

def test_tipo_documento_create_inherits_base():
    tipo = TipoDocumentoCreate(nombre="DNI", acronimo="DNI", descripcion="Documento Nacional de Identidad")
    assert isinstance(tipo, TipoDocumentoBase)

def test_tipo_documento_update_partial():
    tipo = TipoDocumentoUpdate(nombre="CC")
    assert tipo.nombre == "CC"

def test_tipo_documento_view_fields():
    now = datetime.now()
    tipo = TipoDocumentoView(id=1, nombre="DNI", acronimo="DNI", descripcion="Documento Nacional de Identidad", creado_en=now, actualizado_en=now)
    assert tipo.id == 1
