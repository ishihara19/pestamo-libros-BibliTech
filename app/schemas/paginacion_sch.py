from typing import Generic, TypeVar
from pydantic import BaseModel, Field

# TypeVar para hacer la respuesta genérica
T = TypeVar('T')


class PaginationParams(BaseModel):
    """Parámetros de paginación para queries"""
    page: int = Field(default=1, ge=1, description="Número de página (inicia en 1)")
    page_size: int = Field(default=10, ge=1, le=100, description="Cantidad de items por página")
    
    @property
    def offset(self) -> int:
        """Calcula el offset para la query SQL"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Retorna el límite para la query SQL"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica"""
    items: list[T]
    total: int = Field(description="Total de items en la base de datos")
    page: int = Field(description="Página actual")
    page_size: int = Field(description="Tamaño de página")
    total_pages: int = Field(description="Total de páginas disponibles")
    has_next: bool = Field(description="Indica si hay una página siguiente")
    has_prev: bool = Field(description="Indica si hay una página anterior")
    
    @classmethod
    def create(cls, items: list[T], total: int, params: PaginationParams):
        """Método helper para crear una respuesta paginada"""
        total_pages = (total + params.page_size - 1) // params.page_size  # ceil division
        
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1
        )