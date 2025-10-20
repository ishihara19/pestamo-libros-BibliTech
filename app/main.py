from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Servidor iniciando...")
   

   
    yield
    print("Servidor cerrando...")

app = FastAPI(lifespan=lifespan,title="API BibliTech", description="API RESTful para la gestión de prestamo de libros", version="0.0.1")


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API BibliTech"}