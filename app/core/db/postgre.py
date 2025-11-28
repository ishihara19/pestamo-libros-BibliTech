from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from ..config import settings
from typing import AsyncGenerator, Optional

# --- Engine con pool_pre_ping para reconectar automáticamente ---
engine = create_async_engine(
    settings.POSTGRES_URL, echo=False, pool_pre_ping=True, future=True
)

# --- Sessionmaker ---
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# --- Base para modelos ---
Base = declarative_base()


# --- Crear tablas al iniciar la app ---
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tablas creadas/verificadas en PostgreSQL")


# --- Dependency para FastAPI ---
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def _set_guc(db: AsyncSession, name: str, value: Optional[str]):
    """
    Establece una GUC (variable de configuración) de PostgreSQL de forma parametrizada y segura.

    Utiliza la función set_config(nombre, valor, is_local) de PostgreSQL en lugar de
    ejecutar una sentencia SET con concatenación de valores. Esto evita errores de sintaxis
    cuando se intentan usar parámetros en posiciones donde PostgreSQL no los acepta
    (p. ej. en SET) y previene riesgos de SQL injection.

    Parámetros
    - db: AsyncSession o Connection de SQLAlchemy sobre la cual ejecutar la consulta.
    - name: nombre completo de la GUC (por ejemplo: "app.usuario_app").
    - value: valor a asignar. Si es None se convierte a cadena vacía para evitar pasar NULL.

    Comportamiento
    - El tercer argumento de set_config es 'true', lo que equivale a SET LOCAL: el valor
      solo es visible dentro de la transacción actual.
    - No es necesaria una función de escape manual (como safe()), porque bindparams
      maneja el escape del valor enviado al servidor.
    """
    await db.execute(
        text("SELECT set_config(:name, :value, true)").bindparams(name=name, value=value or "")
    )

async def set_app_context(
    db: AsyncSession,
    usuario_app: Optional[str],
    ip: Optional[str],
    host: Optional[str],
    operacion: Optional[str],
):
    """
    Asigna valores de contexto específicos de la aplicación en la sesión/transaction actual.

    Uso recomendado:
    - Llamar a esta función al inicio de una transacción (p. ej. dentro de un servicio)
      antes de ejecutar otras consultas que deban acceder a estas variables mediante
      current_setting('app.x') en triggers, funciones o logs de auditoría.

    Ejemplo de variables usadas:
    - app.usuario_app : correo o identificador del usuario que realiza la operación.
    - app.ip          : dirección IP del cliente.
    - app.host        : nombre del host desde donde se ejecuta la petición.
    - app.operation   : nombre lógico de la operación (ej. "actualizar_perfil_usuario").

    Notas de seguridad:
    - Al usar set_config con parámetros vinculados evitamos inyección SQL, por lo que no
      es necesario escapar manualmente comillas simples.
    - Los valores se convierten a cadena vacía si son None; si prefieres permitir NULL,
      adapta bindparams para enviar None en lugar de "".
    """
    await _set_guc(db, "app.usuario_app", usuario_app)
    await _set_guc(db, "app.ip", ip)
    await _set_guc(db, "app.host", host)
    await _set_guc(db, "app.operation", operacion)

async def clear_app_context(db: AsyncSession):
    """
    Restablece (RESET) las GUCs de contexto de la aplicación a su estado por defecto.

    Observaciones:
    - RESET no admite parámetros para el nombre de la variable; aquí utilizamos nombres
      literales confiables (constantes internas de la aplicación).
    - RESET afecta la sesión/transaction según el scope de la variable; si usaste set_config(..., true)
      la variable ya era local a la transacción y al finalizar la transacción dejará de existir.
    """
    await db.execute(text('RESET "app.usuario_app"'))
    await db.execute(text('RESET "app.ip"'))
    await db.execute(text('RESET "app.host"'))
    await db.execute(text('RESET "app.operation"'))