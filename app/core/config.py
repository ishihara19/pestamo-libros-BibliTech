import os
import dotenv
from zoneinfo import ZoneInfo

dotenv.load_dotenv()


# Application settings
class Settings:

    # CORS
    ALLOW_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "https://bv2x6hss-8000.use2.devtunnels.ms/",
    ]

    # Timezone
    TZ_INFO = os.getenv("TZ_INFO", "UTC")

    # API
    PREFIX_API_VERSION = os.getenv("PREFIX_API_VERSION", "/api/v")

    # DATABASE PostgreSQL
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # Email settings
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    # Application specific settings
    ROL_ADMIN = int(os.getenv("ROL_ADMIN", 2))
    ROL_BIBLIOTECARIO = int(os.getenv("ROL_BIBLIOTECARIO", 3))
    ESTADO_ACTIVO = int(os.getenv("ESTADO_ACTIVO", 1))
    ESTADO_INACTIVO = int(os.getenv("ESTADO_INACTIVO", 2))
    DOCUMENTO_MAYOR_EDAD_ID = int(os.getenv("DOCUMENTO_MAYOR_EDAD_ID", 1))
    DOCUMENTO_MENOR_EDAD_ID = int(os.getenv("DOCUMENTO_MENOR_EDAD_ID", 2))
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES", 10)
    )
    EDAD_MINIMA_USUARIO = int(os.getenv("EDAD_MINIMA_USUARIO", 9))
    
    R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
    R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
    R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
    R2_ENDPOINT =f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    R2_DOMINIO = os.getenv("R2_DOMINIO")


settings = Settings()
