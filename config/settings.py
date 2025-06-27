import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database Configuration
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.environ.get("DATABASE_PORT", 5432))
DATABASE_NAME = os.environ.get("DATABASE_NAME", "postgres")
DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")

# Full URLs
DATABASE_URL_ASYNC = os.environ.get(
    "DATABASE_URL_ASYNC",
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# JWT configuration
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 30))
SECRET_KEY = os.environ.get("SECRET_KEY", "your-fallback-secret-key")
ALGORITHM = "HS256"

# Redis
REDIS_HOST = os.environ.get("REDIS_CUSTOM_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_CUSTOM_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_CUSTOM_DB", 0))