from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from datetime import datetime
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
    tz = os.getenv("TZ_INFO", "UTC")
    now_utc = datetime.now()
    now_tz = datetime.now(tz)
    return {"message": "Bienvenido a la API BibliTech",
            "now_utc":now_utc,
            "now_tz":now_tz}