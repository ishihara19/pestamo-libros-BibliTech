from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
import io
import uuid
import json

from ..schemas.libro_sch import LibroCreate, LibroView, LibroUpdate, LibroViewNormalized, LibroURLUpdate
from ..schemas.paginacion_sch import PaginationParams, PaginatedResponse
from ..services.libro_service import LibroService
from ..schemas.generic_sch import GenericMessage
from ..core.db.postgre import get_session
from ..dependencies.auth import obtener_usuario_actual_administrador, obtener_usuario_actual_activo
from ..models.usuario import Usuario
from ..core.config import settings
from ..core.s3_client import S3Client
from ..utils.utils import validate_image, convert_to_webp, validate_max_size_image

s3_client = S3Client(
    endpoint_url=settings.R2_ENDPOINT,
    access_key_id=settings.R2_ACCESS_KEY_ID,
    secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    bucket_name=settings.R2_BUCKET_NAME,
    domain=settings.R2_DOMINIO
)

libro_router = APIRouter(prefix="/libros", tags=["Libros"])

@libro_router.post("", response_model=LibroView, status_code=201)
async def crear_libro(
    libro: str = Form(..., description="Datos del libro en formato JSON"),
    db: AsyncSession = Depends(get_session),
    file: UploadFile = File(..., description="Imagen del libro en formato JPEG o PNG"),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """
    Ejemplo del campo **libro**:
    ```json
    {
      "titulo": "string",
      "descripcion": "string",
      "categoria_id": 0,
      "editorial": "string",
      "fecha_publicacion": "1935-12-30"
    }
    ```
    """
    # Convertir el string JSON a un objeto Pydantic
    try:
        data = json.loads(libro)
        libro_obj = LibroCreate(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar los datos del libro: {e}")

    # Validar y procesar la imagen subida
    imagen_file = await file.read()
    
    try:
        await validate_max_size_image(imagen_file, max_size_mb=settings.MAX_SIZE_MB_IMAGE_UPLOAD)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        await validate_image(imagen_file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Optimizar y subir la imagen a S3
    image_optimizada_bytes = await convert_to_webp(imagen_file)
    file_key = f"libros/{uuid.uuid4()}.webp"
    try:
        s3_client.upload_fileobj(io.BytesIO(image_optimizada_bytes), file_key, "image/webp")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen a S3: {e}")

    # Generar la URL de la imagen subida
    imagen_url = s3_client.generate_file_url(file_key)

    # Guardar en la base de datos
    return await LibroService.create_libro(libro_obj, db, imagen_url)

@libro_router.get("", response_model=list[LibroView] | list[LibroViewNormalized] | PaginatedResponse[LibroView] | PaginatedResponse[LibroViewNormalized])
async def listar_libros(
    db: AsyncSession = Depends(get_session),
    page: int | None = Query(None, ge=1, description="Número de página"),
    page_size: int | None = Query(None, ge=1, le=100, description="Items por página"),
    normalizado: bool = Query(False, description="Retornar libros en formato normalizado")
):
    """
    Listar todos los libros.
    Usa paginación si se proveen los parámetros page y page_size.
    El parámetro 'normalizado' indica si se debe retornar el formato normalizado.
    """
    pagination = None
    if page is not None and page_size is not None:
        pagination = PaginationParams(page=page, page_size=page_size)
    
    return await LibroService.listar_libros(db, pagination, normalizado)

@libro_router.get("/{id}", response_model=LibroView | LibroViewNormalized)
async def obtener_libro_por_id(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_activo: Usuario = Depends(obtener_usuario_actual_activo),
    normalizado: bool = Query(False, description="Retornar libro en formato normalizado")
):
    """Obtener un libro por su ID"""
    return await LibroService.obtener_libro_por_id(id, db, normalizado)

@libro_router.put("/{id}", response_model=LibroView)
async def actualizar_libro(
    id: int,
    libro: LibroUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar un libro por su ID"""
    return await LibroService.actualizar_libro(id, libro, db)

@libro_router.patch("/{id}/imagen", response_model=LibroURLUpdate)
async def actualizar_imagen_libro(
    id: int,    
    file: UploadFile = File(..., description="Nueva imagen del libro en formato JPEG o PNG"),
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Actualizar la imagen de un libro por su ID"""
    
    # Validar y procesar la nueva imagen subida
    imagen_file = await file.read()
    
    try:
        await validate_max_size_image(imagen_file, max_size_mb=settings.MAX_SIZE_MB_IMAGE_UPLOAD)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        await validate_image(imagen_file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    image_optimizada_bytes = await convert_to_webp(imagen_file)      

    file_key = f"libros/{uuid.uuid4()}.webp"
    
    try:
        s3_client.upload_fileobj(io.BytesIO(image_optimizada_bytes), file_key, "image/webp")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen a S3: {e}")
    
    imagen_url = s3_client.generate_file_url(file_key)
    return await LibroService.actualizar_imagen_libro(id, imagen_url, db)

@libro_router.delete("/{id}", response_model=GenericMessage)
async def eliminar_libro(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_admin: Usuario = Depends(obtener_usuario_actual_administrador)
):
    """Eliminar un libro por su ID"""
    return await LibroService.eliminar_libro(id, db)
