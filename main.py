from fastapi import FastAPI

from app.utils.lifespan import lifespan
from app.routers import router as api_router

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")
