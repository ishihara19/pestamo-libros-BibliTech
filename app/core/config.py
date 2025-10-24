import os
import dotenv
from zoneinfo import ZoneInfo

dotenv.load_dotenv()

class Settings:
    # CORS
    ALLOW_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "https://bv2x6hss-8000.use2.devtunnels.ms/",
    ]
    TZ_INFO = os.getenv("TZ_INFO", "UTC")

    PREFIX_API_VERSION = os.getenv("PREFIX_API_VERSION", "/api/v")
    # DATABASE PostgreSQL
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_URL = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES", 10))
    
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    ROL_ADMIN = int(os.getenv("ROL_ADMIN", 2))
    ESTADO_ACTIVO = int(os.getenv("ESTADO_ACTIVO", 1))


settings = Settings()