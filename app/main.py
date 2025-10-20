from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from datetime import datetime
from zoneinfo import ZoneInfo

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Servidor iniciando...")
    
    tz = os.getenv("TZ_INFO", "UTC")
    print(f"Configurando zona horaria a: {tz}")

   
    yield
    print("Servidor cerrando...")

app = FastAPI(lifespan=lifespan,title="API BibliTech", description="API RESTful para la gestión de prestamo de libros", version="0.0.1")


@app.get("/")
async def root():
    tz_name = os.getenv("TZ_INFO", "UTC")  # Ej: "America/Bogota"
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = ZoneInfo("UTC")
    now_utc = datetime.now()
    now_tz = datetime.now(tz)
    return {"message": "Bienvenido a la API BibliTech",
            "now_utc":now_utc,
            "now_tz":now_tz}