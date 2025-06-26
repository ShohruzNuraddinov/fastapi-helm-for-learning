from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.utils.redis import init_redis_pool, close_redis_pool
from app.utils.db import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    This function is called when the application starts and stops.
    """
    await init_db()
    await init_redis_pool()
    yield
    await close_db()
    await close_redis_pool()
