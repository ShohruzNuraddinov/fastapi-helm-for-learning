from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
# from sqlmodel import SQLModel

from config.settings import DATABASE_URL_ASYNC

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True, pool_pre_ping=True)


async def init_db():
    """
    Initialize the database connection.
    This function is called when the application starts.
    """
    # Code to run when the application starts
    async with engine.begin() as conn:
        pass


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session


async def close_db():
    """
    Close the database connection.
    This function is called when the application stops.
    """
    await engine.dispose()