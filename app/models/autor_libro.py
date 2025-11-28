from sqlalchemy import Table, Column, BigInteger, ForeignKey
from ..core.db.postgre import Base


autor_libro = Table(
    "autor_libro",
    Base.metadata,
    Column("autor_id", BigInteger, ForeignKey("autor.id"), nullable=False),
    Column("libro_id", BigInteger, ForeignKey("libro.id"), nullable=False),
)
