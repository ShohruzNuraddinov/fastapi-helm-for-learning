import redis.asyncio as redis
from contextlib import asynccontextmanager

from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

pool: redis.ConnectionPool = None


@asynccontextmanager
async def get_redis_client():
    """
    Get a Redis client.
    """
    global pool
    redis_client = redis.Redis.from_pool(pool)
    try:
        yield await redis_client
    finally:
        await redis_client.aclose()


async def init_redis_pool():
    """
    Initialize the Redis connection pool.
    This function is called when the application starts.
    """
    global pool
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    
async def close_redis_pool():
    """
    Close the Redis connection pool.
    This function is called when the application stops.
    """
    global pool
    if pool:
        await pool.disconnect()
        pool = None