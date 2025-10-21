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

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Servidor iniciando...")
    await on_startup()

    yield
    print("Servidor cerrando...")

app = FastAPI(lifespan=lifespan,title="API BibliTech", description="API RESTful para la gestión de prestamo de libros", version="0.0.1")
app.include_router(estado_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(tipo_documento_router, prefix=settings.PREFIX_API_VERSION)
app.include_router(rol_router, prefix=settings.PREFIX_API_VERSION)

class rootResponse(BaseModel):
    message: str
    now_utc: datetime
    now_tz: datetime

@app.get("/", response_model=rootResponse)
async def root():
    tz_info = settings.TZ_INFO
    try:
        tz = ZoneInfo(tz_info)
    except Exception:
        tz = ZoneInfo("UTC")
    now_utc = datetime.now()
    now_tz = datetime.now(tz)
    
    return rootResponse.model_validate({
        "message": "Bienvenido a la API BibliTech tz_info: "+tz_info,
        "now_utc":now_utc,
        "now_tz":now_tz})