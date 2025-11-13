from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from .core.config import settings
from .core.db.postgre import on_startup
from .routes.estado_routes import estado_router
from .routes.tipo_documento_routers import tipo_documento_router
from .routes.rol_routes import rol_router
from .routes.usuario_routes import usuario_router
from .routes.auth_routes import auth
from .routes.autor_routes import autor_router
from .routes.categoria_routes import categoria_router
from .routes.libro_routes import libro_router
from .routes.auditoria_router import auditoria_router
from .routes.ejemplar_routers import ejemplar_router
from .utils.utils import normalizar_nombre_propio


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Servidor iniciando...")
    await on_startup()

    yield
    print("Servidor cerrando...")


app = FastAPI(
    lifespan=lifespan,
    title="API BibliTech",
    description="API RESTful para la gestión de prestamo de libros",
    version="1.0.1",
)

app.include_router(estado_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(tipo_documento_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(rol_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(usuario_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(auth, prefix=settings.PREFIX_API_VERSION)
app.include_router(autor_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(categoria_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(libro_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(ejemplar_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(auditoria_router, prefix=settings.PREFIX_API_VERSION)

class rootResponse(BaseModel):
    message: str
    now_utc: datetime
    now_tz: datetime
    nombre: str
    nombre_normalizado: str


@app.get("/", response_model=rootResponse)
async def root(nombre: str = "USUARIO DE LAS CASAS"):
    nombre_normalizado = normalizar_nombre_propio(nombre)
    tz_info = settings.TZ_INFO
    try:
        tz = ZoneInfo(tz_info)
    except Exception:
        tz = ZoneInfo("UTC")
    now_utc = datetime.now()
    now_tz = datetime.now(tz)

    return rootResponse.model_validate(
        {
            "message": "Bienvenido a la API BibliTech tz_info: " + tz_info,
            "now_utc": now_utc,
            "now_tz": now_tz,
            "nombre": nombre,
            "nombre_normalizado": nombre_normalizado,
        }
    )
