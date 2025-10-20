from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Servidor iniciando...")
   

   
    yield
    print("Servidor cerrando...")

app = FastAPI(lifespan=lifespan,title="API Biblioteca", description="API RESTful para la gestión de una biblioteca utilizando FastAPI y PostgreSQL", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL + SQLAlchemy ORM funcionando 🚀"}